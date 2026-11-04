"""Portable workspace execution without granting a host shell or Python runtime.

The fallback interprets a deliberately bounded Python AST and simple file
commands. Values exposed to interpreted code are primitives or explicit capability
objects. No user code is passed to exec/eval, importlib or a host subprocess.
Unsupported operations produce a recoverable tool result, never a fake success.
"""

from __future__ import annotations

import ast
import base64
import collections
import csv
import fnmatch
import io
import json
import math
import operator
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath, PureWindowsPath

from .context import PORTABLE_MODULE_CAPABILITIES, json_text, utf8_bytes, utf8_text, subprocess_environment

MAX_FILE = 1_000_000
MAX_ITEMS = 100_000
MAX_STEPS = 100_000


class UnsupportedCommand(ValueError):
    pass


class _RegexPattern:
    def __init__(self, values):
        self.values = values


class _RegexMatch:
    def __init__(self, values):
        self.values = values

    def group_index(self, key):
        if isinstance(key, str):
            key = self.values['groupindex'][key]
        if not isinstance(key, int) or key < 0 or key >= len(self.values['groups']):
            raise IndexError('no such group')
        return key

    def __getitem__(self, key):
        return self.values['groups'][self.group_index(key)]


_REGEX_WORKER = r'''
import base64,json,re,sys

def decode(value):
    if isinstance(value,dict) and set(value)=={'bytes'}:
        return base64.b64decode(value['bytes'])
    if isinstance(value,list):
        return [decode(x) for x in value]
    if isinstance(value,dict):
        return {k:decode(v) for k,v in value.items()}
    return value

def encode(value):
    if isinstance(value,bytes): return {'bytes':base64.b64encode(value).decode('ascii')}
    if isinstance(value,re.Pattern): return {'pattern':encode(value.pattern),'flags':value.flags,'groups_count':value.groups,'groupindex':dict(value.groupindex),'kind':'pattern'}
    if isinstance(value,re.Match):
        return {'kind':'match','groups':encode([value.group(i) for i in range(value.re.groups+1)]),
                'spans':encode([value.span(i) for i in range(value.re.groups+1)]),'groupindex':dict(value.re.groupindex),
                'pattern':encode(value.re.pattern),'flags':value.re.flags,'string':encode(value.string),
                'pos':value.pos,'endpos':value.endpos,'lastindex':value.lastindex,'lastgroup':value.lastgroup}
    if isinstance(value,tuple): return {'tuple':[encode(x) for x in value]}
    if isinstance(value,list): return [encode(x) for x in value]
    if isinstance(value,dict): return {k:encode(v) for k,v in value.items()}
    return value
try:
    packet=decode(json.load(sys.stdin))
    operation=packet['operation']
    allowed={'search','match','fullmatch','findall','finditer','sub','subn','split','escape','compile','expand'}
    if operation not in allowed: raise ValueError('Unsupported regular expression operation')
    if 'match' in packet:
        match=packet['match']
        target=re.compile(match['pattern'],match['flags']).match(match['string'],match['spans'][0][0],match['endpos'])
        result=target.expand(*packet['args'],**packet['kwargs'])
    elif 'pattern' in packet:
        target=re.compile(packet['pattern'],packet.get('flags',0))
        result=getattr(target,operation)(*packet['args'],**packet['kwargs'])
    else:
        result=getattr(re,operation)(*packet['args'],**packet['kwargs'])
    if operation=='finditer':
        items=[]
        for item in result:
            if len(items)>=100000: raise ValueError('Too many regular expression matches')
            items.append(item)
        result=items
    answer={'result':encode(result)}
    output=json.dumps(answer,ensure_ascii=True)
    if len(output)>8000000: raise ValueError('Regular expression result too large')
    sys.stdout.write(output)
except Exception as error:
    sys.stdout.write(json.dumps({'error':str(error),'type':type(error).__name__}))
'''


def _regex_encode(value):
    if isinstance(value, bytes):
        return {'bytes': base64.b64encode(value).decode('ascii')}
    if isinstance(value, (list, tuple)):
        return [_regex_encode(item) for item in value]
    if isinstance(value, dict):
        return {key: _regex_encode(item) for key, item in value.items()}
    return value


def _regex_decode(value):
    if isinstance(value, dict):
        if set(value) == {'bytes'}:
            return base64.b64decode(value['bytes'])
        if set(value) == {'tuple'}:
            return tuple(_regex_decode(item) for item in value['tuple'])
        result = {key: _regex_decode(item) for key, item in value.items()}
        if result.get('kind') == 'pattern':
            return _RegexPattern(result)
        if result.get('kind') == 'match':
            return _RegexMatch(result)
        return result
    if isinstance(value, list):
        return [_regex_decode(item) for item in value]
    return value


class _Return(Exception):
    def __init__(self, value):
        self.value = value


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


class _Exit(Exception):
    def __init__(self, code):
        self.code = int(code or 0)


class _Module:
    def __init__(self, values):
        self.values = values


class _Function:
    def __init__(self, node, env, defaults, kwdefaults=None):
        self.node, self.env, self.defaults = node, env, defaults
        self.kwdefaults = dict(kwdefaults or {})


class _Path:
    def __init__(self, fs, name):
        self.fs, self.name = fs, fs.relative(name)

    def __str__(self):
        return "/workspace" + ("/" + self.name if self.name != "." else "")

    def __truediv__(self, name):
        return _Path(self.fs, "/workspace/" + str(PurePosixPath(self.name) / str(name)))


class _File:
    def __init__(self, fs, name, mode="r", encoding="utf-8", **kwargs):
        if mode not in {"r", "w", "a", "rb", "wb", "ab", "rt", "wt", "at"}:
            raise UnsupportedCommand(
                "Only workspace text/binary read, write and append are supported"
            )
        if encoding.lower().replace("_", "-") not in {"utf-8", "utf8", "ascii"}:
            raise UnsupportedCommand("Use UTF-8 for portable workspace files")
        self.fs, self.name, self.mode = fs, _Path(fs, name), mode
        self.writable = mode[0] in "wa"
        self.closed = False
        raw = b"" if mode[0] == "w" else fs.read(self.name)
        self.buffer = (
            io.BytesIO(raw) if "b" in mode else io.StringIO(raw.decode(encoding))
        )
        if mode[0] == "a":
            self.buffer.seek(0, 2)

    def __iter__(self):
        return iter(self.buffer.getvalue().splitlines(keepends=True))

    def write(self, value):
        if not self.writable:
            raise OSError("File is read-only")
        if len(value) + self.buffer.tell() > MAX_FILE:
            raise UnsupportedCommand("Workspace file size limit exceeded")
        return self.buffer.write(value)

    def close(self):
        if self.closed:
            return
        if self.writable:
            value = self.buffer.getvalue()
            self.fs.write(
                self.name, value if isinstance(value, bytes) else utf8_bytes(value)
            )
        self.writable = False
        self.buffer.close()
        self.closed = True


class WorkspaceFiles:
    """Bounded writes are staged; no unsupported program leaves partial writes."""

    def __init__(self, root, cwd=None):
        self.root = Path(root).resolve()
        self.cwd = Path(cwd or self.root).resolve()
        if not self.cwd.is_relative_to(self.root):
            raise UnsupportedCommand("Working directory escapes workspace")
        self.prefix = self.cwd.relative_to(self.root).as_posix()
        self.writes, self.deleted, self.directories = {}, set(), set()

    def relative(self, name):
        raw = (
            "/workspace/" + name.name if isinstance(name, _Path) else str(name)
        ).replace("\\", "/")
        if (
            "\x00" in raw
            or PureWindowsPath(raw).drive
            or PureWindowsPath(raw).is_absolute()
        ):
            raise UnsupportedCommand(
                "Absolute and drive paths are outside the portable workspace"
            )
        if raw.startswith("/workspace/") or raw == "/workspace":
            raw = raw[len("/workspace") :].lstrip("/")
        elif raw.startswith("/"):
            host = Path(raw)
            if not host.is_relative_to(self.root):
                raise UnsupportedCommand("Absolute path escapes workspace")
            raw = host.relative_to(self.root).as_posix()
        else:
            raw = str(PurePosixPath(self.prefix) / raw)
        parts = PurePosixPath(raw).parts
        if ".." in parts or any(":" in part for part in parts):
            raise UnsupportedCommand("Parent traversal is outside workspace")
        reserved = {
            "con",
            "prn",
            "aux",
            "nul",
            "clock$",
            *[f"com{i}" for i in range(1, 10)],
            *[f"lpt{i}" for i in range(1, 10)],
        }
        if any(
            part.endswith((".", " "))
            or any(ord(char) < 32 or char in '<>:"|?*' for char in part)
            or part.split(".")[0].casefold() in reserved
            for part in parts
        ):
            raise UnsupportedCommand(
                "Filename is not portable across Windows/macOS/Linux"
            )
        relative = PurePosixPath(*parts).as_posix()
        target = self.root / relative
        current = self.root
        for part in parts:
            current = current / part
            if current.is_symlink():
                raise UnsupportedCommand(
                    "Symlinks are unavailable in the portable backend"
                )
        if not target.resolve().is_relative_to(self.root):
            raise UnsupportedCommand("Path escapes workspace")
        if target.is_file() and target.stat().st_nlink > 1:
            raise UnsupportedCommand(
                "Hard links are unavailable in the portable backend"
            )
        return relative

    def read(self, name):
        name = self.relative(name)
        if name in self.deleted:
            raise FileNotFoundError(name)
        if name in self.writes:
            return self.writes[name]
        target = self.root / name
        if not target.is_file():
            raise FileNotFoundError(name)
        if target.stat().st_size > MAX_FILE:
            raise UnsupportedCommand("Workspace file exceeds size limit: " + name)
        return target.read_bytes()

    def mutable(self, name):
        if any(
            part.casefold() in {".git", ".application_skills", ".clouds_coder"}
            for part in PurePosixPath(name).parts
        ):
            raise UnsupportedCommand("Protected workspace metadata is read-only")

    def write(self, name, value):
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError("Binary file writes require bytes")
        name, value = self.relative(name), bytes(value)
        self.mutable(name)
        if (
            len(value) > MAX_FILE
            or sum(map(len, self.writes.values())) + len(value) > 8 * MAX_FILE
        ):
            raise UnsupportedCommand("Workspace write quota exceeded")
        self.writes[name] = value
        self.deleted.discard(name)

    def exists(self, name):
        name = self.relative(name)
        return name not in self.deleted and (
            name in self.writes
            or name in self.directories
            or (self.root / name).exists()
        )

    def files(self):
        found = set(self.writes)
        # Walk explicitly so symlinked directories are never traversed.
        for current, dirs, files in os.walk(self.root, followlinks=False):
            dirs[:] = [d for d in dirs if not (Path(current) / d).is_symlink()]
            for name in files:
                target = Path(current) / name
                if not target.is_symlink():
                    found.add(target.relative_to(self.root).as_posix())
                if len(found) > 2000:
                    raise UnsupportedCommand(
                        "Workspace listing limit exceeded; use a narrower file tool"
                    )
        return sorted(found - self.deleted)

    def commit(self):
        for name in set(self.directories) | set(self.writes) | self.deleted:
            self.relative("/workspace/" + name)
            self.mutable(name)
        changed = []
        for name in sorted(self.directories):
            target = self.root / self.relative("/workspace/" + name)
            target.mkdir(parents=True, exist_ok=True)
        for name, value in self.writes.items():
            target = self.root / self.relative("/workspace/" + name)
            target.parent.mkdir(parents=True, exist_ok=True)
            # Atomic replacement avoids modifying an existing hard-linked inode.
            import tempfile

            descriptor, temporary = tempfile.mkstemp(
                prefix=".portable-", dir=target.parent
            )
            try:
                with os.fdopen(descriptor, "wb") as handle:
                    handle.write(value)
                os.replace(temporary, target)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
            changed.append(name)
        for name in self.deleted:
            target = self.root / self.relative("/workspace/" + name)
            if target.is_file():
                target.unlink()
                changed.append(name)
        return changed


class PythonWorkspace:
    """Small AST interpreter; only explicitly exposed capabilities are callable."""

    def __init__(self, fs, checkpoint, timeout):
        self.fs, self.checkpoint, self.deadline = (
            fs,
            checkpoint,
            time.monotonic() + max(0.01, timeout),
        )
        self.steps, self.depth, self.output = 0, 0, []
        self.allowed = set()
        self.modules = {}
        self.opened = []
        self.builtins = {
            name: self.allow(value)
            for name, value in {
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
                "len": len,
                "chr": chr,
                "ord": ord,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "enumerate": enumerate,
                "zip": zip,
                "all": all,
                "any": any,
                "isinstance": isinstance,
                "reversed": reversed,
                "ValueError": ValueError,
                "TypeError": TypeError,
                "KeyError": KeyError,
                "AssertionError": AssertionError,
                "NotImplementedError": NotImplementedError,
                "FileNotFoundError": FileNotFoundError,
                "range": self.range,
                "sorted": self.sorted,
                "print": self.print,
                "open": self.open,
            }.items()
        }

    def allow(self, value):
        if callable(value):
            self.allowed.add(value)
        return value

    def tick(self):
        self.steps += 1
        if self.steps > MAX_STEPS or time.monotonic() > self.deadline:
            raise TimeoutError("Portable command step/time limit exceeded")
        if self.steps % 100 == 0:
            self.checkpoint()

    def data_size(self, value, limit=MAX_FILE):
        total = 0
        pending = [(value, 0)]
        visited = 0
        while pending:
            current, depth = pending.pop()
            visited += 1
            if visited > MAX_ITEMS or depth > 50:
                raise UnsupportedCommand("Portable data graph limit exceeded")
            if isinstance(current, (str, bytes)):
                total += len(current) + 2
            elif isinstance(current, dict):
                pending.extend(
                    (child, depth + 1) for pair in current.items() for child in pair
                )
            elif isinstance(current, (list, tuple, set)):
                pending.extend((child, depth + 1) for child in current)
            elif isinstance(current, range):
                total += len(current) * 8
            else:
                total += 16
            if total > limit:
                raise UnsupportedCommand("Portable data size limit exceeded")
        return total

    def bound(self, value):
        if isinstance(value, (str, bytes)) and len(value) > MAX_FILE:
            raise UnsupportedCommand("Portable value size limit exceeded")
        if (
            isinstance(value, (list, tuple, dict, set, range))
            and len(value) > MAX_ITEMS
        ):
            raise UnsupportedCommand("Portable collection size limit exceeded")
        if isinstance(value, int) and value.bit_length() > 20000:
            raise UnsupportedCommand("Portable integer size limit exceeded")
        self.data_size(value)
        return value

    def range(self, *args):
        return self.bound(range(*args))

    def sorted(self, values, *, key=None, reverse=False):
        values = self.bound(list(values))
        return sorted(
            values,
            key=(lambda value: self.invoke(key, [value], {})) if key else None,
            reverse=reverse,
        )

    def print(self, *values, sep=" ", end="\n", file=None, **kwargs):
        if (
            sum(self.data_size(value, 16000) for value in values)
            + len(sep) * len(values)
            + len(end)
            > 16000
        ):
            raise UnsupportedCommand("Portable output limit exceeded")
        text = sep.join(map(str, values)) + end
        if file is not None:
            file.write(text)
        else:
            if sum(map(len, self.output)) + len(text) > 16000:
                raise UnsupportedCommand("Portable output limit exceeded")
            self.output.append(text)

    def open(self, name, mode="r", **kwargs):
        if len(self.opened) >= 128:
            raise UnsupportedCommand("Portable file-handle limit exceeded")
        handle = _File(self.fs, name, mode, **kwargs)
        self.opened.append(handle)
        return handle

    def dumps(self, value, **kwargs):
        self.bound(value)
        indent = kwargs.get("indent")
        if indent is not None and (
            isinstance(indent, int)
            and not 0 <= indent <= 16
            or isinstance(indent, str)
            and len(indent) > 16
        ):
            raise UnsupportedCommand("Portable JSON indentation limit exceeded")
        separators = kwargs.get("separators")
        if separators and any(len(str(part)) > 16 for part in separators):
            raise UnsupportedCommand("Portable JSON separator limit exceeded")
        return self.bound(
            json_text(
                value,
                **{key: item for key, item in kwargs.items() if key != "ensure_ascii"},
            )
        )

    def regex(self, operation, *args, _pattern=None, _match=None, **kwargs):
        self.tick()
        if args and isinstance(args[0], _RegexPattern) and _pattern is None:
            if operation == 'compile':
                return args[0]
            _pattern, args = args[0], args[1:]
        # Replacement functions execute only inside this AST interpreter.
        replacement_index = 0 if _pattern is not None else 1
        if operation in {'sub', 'subn'} and len(args) > replacement_index and isinstance(args[replacement_index], _Function):
            pattern = _pattern.values['pattern'] if _pattern is not None else args[0]
            flags = _pattern.values['flags'] if _pattern is not None else kwargs.get('flags', args[4] if len(args) > 4 else 0)
            replacement, text = args[replacement_index:replacement_index+2]
            count = kwargs.get('count', args[replacement_index+2] if len(args) > replacement_index+2 else 0)
            matches = self.regex('finditer', pattern, text, flags=flags)
            output, start, used = [], 0, 0
            for match in matches:
                if count and used >= count:
                    break
                left, right = match.values['spans'][0]
                output.extend([text[start:left], self.invoke(replacement, [match], {})])
                self.bound(output)
                start, used = right, used + 1
            output.append(text[start:])
            value = self.bound((b'' if isinstance(text, bytes) else '').join(output))
            return (value, used) if operation == 'subn' else value
        packet = {'operation': operation, 'args': args, 'kwargs': kwargs}
        if _match is not None:
            packet['match'] = _match.values
        if _pattern is not None:
            packet.update(pattern=_pattern.values['pattern'], flags=_pattern.values['flags'])
        data = json_text(_regex_encode(packet))
        if len(data) > 2 * MAX_FILE:
            raise UnsupportedCommand('Regular expression input exceeds portable data limits')
        remaining = min(2.0, self.deadline - time.monotonic())
        if remaining <= 0:
            raise TimeoutError('Portable regular expression deadline exceeded')
        try:
            response = subprocess.run([sys.executable, '-I', '-S', '-c', _REGEX_WORKER], input=data,
                text=True, encoding='utf-8', errors='backslashreplace', capture_output=True,
                timeout=remaining, cwd=self.fs.root, env=subprocess_environment())
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError('Portable regular expression exceeded its time budget') from exc
        self.checkpoint()
        if response.returncode or not response.stdout:
            raise UnsupportedCommand('Regular expression worker unavailable')
        result = json.loads(response.stdout)
        if 'error' in result:
            raise ValueError(result['error'])
        return self.bound(_regex_decode(result['result']))

    def module(self, name):
        if name in self.modules:
            return self.modules[name]
        if name == "json":
            values = {
                "loads": json.loads,
                "dumps": self.dumps,
                "load": lambda handle: json.loads(handle.buffer.getvalue()),
                "dump": lambda obj, handle, **kw: handle.write(self.dumps(obj, **kw)),
            }
        elif name == "re":
            values = {}
            for member in PORTABLE_MODULE_CAPABILITIES['re']:
                if member == 'error':
                    values[member] = ValueError
                elif member.isupper():
                    values[member] = int(getattr(re, member, 0))
                else:
                    values[member] = lambda *args, _operation=member, **kwargs: self.regex(_operation, *args, **kwargs)
        elif name == "pathlib":
            values = {
                "Path": lambda *parts: _Path(
                    self.fs, str(PurePosixPath(*map(str, parts)))
                )
            }
        elif name == "math":
            values = {
                key: getattr(math, key)
                for key in (
                    "ceil",
                    "floor",
                    "sqrt",
                    "isfinite",
                    "isclose",
                    "fsum",
                    "pi",
                    "e",
                )
            }
        elif name == "collections":
            values = {
                "Counter": collections.Counter,
                "defaultdict": lambda *_args: collections.defaultdict(int),
            }
        elif name == "csv":
            values = {
                "reader": lambda handle, **kw: list(csv.reader(handle, **kw)),
                "DictReader": lambda handle, **kw: list(csv.DictReader(handle, **kw)),
            }
        elif name == "os.path":
            values = {
                "join": lambda *p: str(PurePosixPath(*map(str, p))),
                "basename": lambda p: PurePosixPath(str(p)).name,
                "exists": self.fs.exists,
                "isfile": lambda p: self.fs.relative(p) in self.fs.files(),
            }
        elif name == "os":
            values = {
                "path": self.module("os.path"),
                "getcwd": lambda: (
                    "/workspace"
                    + ("/" + self.fs.prefix if self.fs.prefix != "." else "")
                ),
            }
        elif name == "sys":
            values = {
                "exit": lambda code=0: (_ for _ in ()).throw(_Exit(code)),
                "argv": ["workspace.py"],
            }
        elif name == "importlib.util":

            def spec(_name, filename):
                self.fs.relative(filename)
                return _Module(
                    {
                        "filename": str(filename),
                        "loader": _Module({"exec_module": self.allow(load)}),
                    }
                )

            def load(target):
                filename = target.values["filename"]
                env = {"__name__": "workspace_module"}
                self.run(self.fs.read(filename).decode("utf-8"), env)
                target.values.update(env)

            values = {
                "spec_from_file_location": spec,
                "module_from_spec": lambda spec: _Module(dict(spec.values)),
            }
        elif name == "importlib":
            values = {"util": self.module("importlib.util")}
        else:
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name):
                raise UnsupportedCommand(
                    "Unsupported import; use a workspace module or json/pathlib/math/csv"
                )
            filename = name + ".py"
            try:
                source = self.fs.read(filename).decode("utf-8")
            except OSError as exc:
                raise UnsupportedCommand(
                    "Module is not a supplied workspace file: " + name
                ) from exc
            module = _Module({"__name__": name})
            self.modules[name] = module
            self.run(source, module.values)
            return module
        module = _Module({key: self.allow(value) for key, value in values.items()})
        self.modules[name] = module
        return module

    @staticmethod
    def encoding(value):
        if str(value).lower().replace("_", "-") not in {"utf-8", "utf8", "ascii"}:
            raise UnsupportedCommand("Portable files support UTF-8 and ASCII")
        return value

    def attribute(self, obj, name):
        if name.startswith("_"):
            raise UnsupportedCommand(
                "Private attributes and reflection are unavailable"
            )
        if isinstance(obj, _Module):
            if name not in obj.values:
                raise UnsupportedCommand("Module capability unavailable: " + name)
            return obj.values[name]
        if isinstance(obj, _RegexPattern):
            if name in {'pattern', 'flags'}:
                return obj.values[name]
            if name == 'groups':
                return obj.values['groups_count']
            if name == 'groupindex':
                return dict(obj.values['groupindex'])
            if name in {'search', 'match', 'fullmatch', 'findall', 'finditer', 'sub', 'subn', 'split'}:
                return self.allow(lambda *args, **kwargs: self.regex(name, *args, _pattern=obj, **kwargs))
            raise UnsupportedCommand('Regular expression pattern capability unavailable: ' + name)
        if isinstance(obj, _RegexMatch):
            if name in {'string', 'pos', 'endpos', 'lastindex', 'lastgroup'}:
                return obj.values[name]
            if name == 'regs':
                return tuple(obj.values['spans'])
            if name == 're':
                return _RegexPattern({'pattern': obj.values['pattern'], 'flags': obj.values['flags'],
                    'groups_count': len(obj.values['groups'])-1, 'groupindex': obj.values['groupindex']})
            if name == 'group':
                return self.allow(lambda *keys: obj[keys[0] if keys else 0] if len(keys) <= 1 else tuple(obj[key] for key in keys))
            if name == 'groups':
                return self.allow(lambda default=None: tuple(default if value is None else value for value in obj.values['groups'][1:]))
            if name == 'groupdict':
                return self.allow(lambda default=None: {key: default if obj[key] is None else obj[key] for key in obj.values['groupindex']})
            if name == 'expand':
                return self.allow(lambda template: self.regex('expand', template, _match=obj))
            if name in {'span', 'start', 'end'}:
                def location(key=0):
                    pair = obj.values['spans'][obj.group_index(key)]
                    return pair if name == 'span' else pair[0 if name == 'start' else 1]
                return self.allow(location)
            raise UnsupportedCommand('Regular expression match capability unavailable: ' + name)
        if isinstance(obj, _Path):
            fs, p = obj.fs, obj.name
            attrs = {
                "name": PurePosixPath(p).name,
                "suffix": PurePosixPath(p).suffix,
                "stem": PurePosixPath(p).stem,
                "parent": _Path(fs, "/workspace/" + str(PurePosixPath(p).parent)),
                "read_text": lambda encoding="utf-8": fs.read(obj).decode(
                    self.encoding(encoding)
                ),
                "read_bytes": lambda: fs.read(obj),
                "write_text": lambda text, encoding="utf-8": (
                    fs.write(obj, utf8_text(text).encode(self.encoding(encoding)))
                    or len(text)
                ),
                "write_bytes": lambda raw: fs.write(obj, raw) or len(raw),
                "exists": lambda: fs.exists(obj),
                "is_file": lambda: p in fs.files(),
                "as_posix": lambda: p,
                "mkdir": lambda **kw: fs.directories.add(p),
                "unlink": lambda **kw: fs.deleted.add(p),
                "glob": lambda pattern: [
                    _Path(fs, "/workspace/" + f)
                    for f in fs.files()
                    if fnmatch.fnmatch(f, str(PurePosixPath(p) / pattern))
                ],
            }
            if name not in attrs:
                raise UnsupportedCommand("Path capability unavailable: " + name)
            return self.allow(attrs[name])
        if isinstance(obj, _File):
            if name == "write":
                return self.allow(obj.write)
            if name == "close":
                return self.allow(obj.close)
            if name in {"read", "readline", "readlines", "seek", "tell", "flush"}:
                return self.allow(getattr(obj.buffer, name))
        methods = {
            str: {
                "strip",
                "lstrip",
                "rstrip",
                "split",
                "rsplit",
                "splitlines",
                "join",
                "replace",
                "startswith",
                "endswith",
                "lower",
                "upper",
                "casefold",
                "isdigit",
                "isalpha",
                "isalnum",
                "find",
                "count",
                "removeprefix",
                "removesuffix",
            },
            bytes: {"decode", "split", "strip"},
            list: {
                "append",
                "extend",
                "insert",
                "pop",
                "remove",
                "count",
                "index",
                "copy",
                "reverse",
                "clear",
            },
            dict: {
                "get",
                "items",
                "keys",
                "values",
                "update",
                "setdefault",
                "pop",
                "copy",
            },
            set: {
                "add",
                "discard",
                "union",
                "intersection",
                "difference",
                "issubset",
                "update",
            },
            tuple: {"count", "index"},
        }
        for kind, names in methods.items():
            if isinstance(obj, kind) and name in names:
                return self.allow(getattr(obj, name))
        raise UnsupportedCommand("Attribute capability unavailable: " + name)

    def invoke(self, function, args, kwargs):
        self.tick()
        if isinstance(function, _Function):
            node = function.node
            parameters = node.args
            names = [item.arg for item in parameters.posonlyargs + parameters.args]
            local = (
                dict(zip(names[-len(function.defaults) :], function.defaults))
                if function.defaults
                else {}
            )
            local.update(function.kwdefaults)
            local.update(zip(names, args))
            known = names + [item.arg for item in parameters.kwonlyargs]
            positional = set(names[: len(args)])
            positional_only = {item.arg for item in parameters.posonlyargs}
            for key, value in kwargs.items():
                if key in positional or key in positional_only:
                    raise TypeError("Duplicate or positional-only argument: " + key)
                if key not in known and not parameters.kwarg:
                    raise TypeError("Unexpected keyword argument: " + key)
                if key in known:
                    local[key] = value
            if parameters.vararg:
                local[parameters.vararg.arg] = tuple(args[len(names) :])
            if len(args) > len(names) and not parameters.vararg:
                raise TypeError("Too many arguments")
            if parameters.kwarg:
                local[parameters.kwarg.arg] = {
                    k: v for k, v in kwargs.items() if k not in known
                }
            if any(key not in local for key in known):
                raise TypeError("Missing function argument")
            if self.depth >= 50:
                raise UnsupportedCommand("Portable call depth exceeded")
            self.depth += 1
            env = collections.ChainMap(local, function.env)
            try:
                if isinstance(node, ast.Lambda):
                    return self.value(node.body, env)
                self.statements(node.body, env)
            except _Return as result:
                return result.value
            finally:
                self.depth -= 1
            return None
        try:
            allowed = function in self.allowed
        except TypeError:
            allowed = False
        if not allowed:
            raise UnsupportedCommand("Callable is outside the portable capability set")
        for value in args:
            self.bound(value)
        owner = getattr(function, "__self__", None)
        name = getattr(function, "__name__", "")
        if isinstance(owner, str) and name == "replace" and len(args) > 1:
            occurrences = owner.count(args[0])
            if len(owner) + occurrences * len(args[1]) > MAX_FILE:
                raise UnsupportedCommand("Portable string expansion limit exceeded")
        if isinstance(owner, str) and name == "join" and args:
            args[0] = self.bound(list(args[0]))
            if (
                sum(len(item) for item in args[0]) + len(owner) * len(args[0])
                > MAX_FILE
            ):
                raise UnsupportedCommand("Portable join size limit exceeded")
        result = self.bound(function(*args, **kwargs))
        self.bound(owner)
        return result

    def value(self, node, env):
        self.tick()
        if node is None:
            return None
        if isinstance(node, ast.Constant):
            return self.bound(node.value)
        if isinstance(node, ast.Name):
            if node.id.startswith("__") and node.id != "__name__":
                raise UnsupportedCommand("Private runtime names unavailable")
            if node.id in env:
                return env[node.id]
            if node.id in self.builtins:
                return self.builtins[node.id]
            raise NameError(node.id)
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            values = []
            for child in node.elts:
                if isinstance(child, ast.Starred):
                    values.extend(self.value(child.value, env))
                else:
                    values.append(self.value(child, env))
            return self.bound(
                tuple(values)
                if isinstance(node, ast.Tuple)
                else set(values)
                if isinstance(node, ast.Set)
                else values
            )
        if isinstance(node, ast.Dict):
            result = {}
            for key, value in zip(node.keys, node.values):
                if key is None:
                    result.update(self.value(value, env))
                else:
                    result[self.value(key, env)] = self.value(value, env)
            return self.bound(result)
        if isinstance(node, ast.Attribute):
            return self.attribute(self.value(node.value, env), node.attr)
        if isinstance(node, ast.Subscript):
            return self.value(node.value, env)[self.value(node.slice, env)]
        if isinstance(node, ast.Slice):
            return slice(
                self.value(node.lower, env),
                self.value(node.upper, env),
                self.value(node.step, env),
            )
        if isinstance(node, ast.Call):
            args = []
            for child in node.args:
                if isinstance(child, ast.Starred):
                    args.extend(self.value(child.value, env))
                else:
                    args.append(self.value(child, env))
            kwargs = {}
            for item in node.keywords:
                if item.arg is None:
                    kwargs.update(self.value(item.value, env))
                else:
                    kwargs[item.arg] = self.value(item.value, env)
            return self.invoke(self.value(node.func, env), args, kwargs)
        if isinstance(node, ast.BinOp):
            left, right = self.value(node.left, env), self.value(node.right, env)
            if isinstance(node.op, ast.Mult):
                seq, count = (left, right) if isinstance(right, int) else (right, left)
                if (
                    isinstance(seq, (str, bytes, list, tuple))
                    and isinstance(count, int)
                    and len(seq) * max(0, count) > MAX_FILE
                ):
                    raise UnsupportedCommand("Portable allocation limit exceeded")
            if isinstance(node.op, ast.Pow) and (
                not isinstance(right, (int, float))
                or abs(right) > 1000
                or isinstance(left, int)
                and left.bit_length() * abs(right) > 20000
            ):
                raise UnsupportedCommand("Portable exponent limit exceeded")
            if (
                isinstance(node.op, ast.Mod)
                and isinstance(left, str)
                and (len(left) > 16000 or left.count("%") > 256)
            ):
                raise UnsupportedCommand("Portable format size limit exceeded")
            if (
                isinstance(node.op, ast.Mod)
                and isinstance(left, str)
                and re.search(r"%[^%]*\d{5,}|%[^%]*\*", left)
            ):
                raise UnsupportedCommand("Portable format width exceeded")
            operations = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.FloorDiv: operator.floordiv,
                ast.Mod: operator.mod,
                ast.Pow: operator.pow,
                ast.BitOr: operator.or_,
            }
            if type(node.op) not in operations:
                raise UnsupportedCommand("Unsupported arithmetic operation")
            return self.bound(operations[type(node.op)](left, right))
        if isinstance(node, ast.UnaryOp):
            return {
                ast.Not: operator.not_,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
            }[type(node.op)](self.value(node.operand, env))
        if isinstance(node, ast.BoolOp):
            result = None
            for child in node.values:
                result = self.value(child, env)
                if (
                    isinstance(node.op, ast.And)
                    and not result
                    or isinstance(node.op, ast.Or)
                    and result
                ):
                    return result
            return result
        if isinstance(node, ast.Compare):
            left = self.value(node.left, env)
            operations = {
                ast.Eq: operator.eq,
                ast.NotEq: operator.ne,
                ast.Lt: operator.lt,
                ast.LtE: operator.le,
                ast.Gt: operator.gt,
                ast.GtE: operator.ge,
                ast.In: lambda a, b: a in b,
                ast.NotIn: lambda a, b: a not in b,
                ast.Is: operator.is_,
                ast.IsNot: operator.is_not,
            }
            for op, child in zip(node.ops, node.comparators):
                right = self.value(child, env)
                if not operations[type(op)](left, right):
                    return False
                left = right
            return True
        if isinstance(node, ast.IfExp):
            return self.value(
                node.body if self.value(node.test, env) else node.orelse, env
            )
        if isinstance(node, ast.Lambda):
            return _Function(
                node,
                env,
                [self.value(v, env) for v in node.args.defaults],
                {
                    item.arg: self.value(value, env)
                    for item, value in zip(node.args.kwonlyargs, node.args.kw_defaults)
                    if value is not None
                },
            )
        if isinstance(
            node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
        ):
            values = []
            local = collections.ChainMap({}, env)

            def visit(index):
                if index == len(node.generators):
                    values.append(
                        (self.value(node.key, local), self.value(node.value, local))
                        if isinstance(node, ast.DictComp)
                        else self.value(node.elt, local)
                    )
                    self.bound(values)
                    return
                gen = node.generators[index]
                for item in self.value(gen.iter, local):
                    self.tick()
                    self.assign(gen.target, item, local)
                    if all(self.value(test, local) for test in gen.ifs):
                        visit(index + 1)

            visit(0)
            return (
                dict(values)
                if isinstance(node, ast.DictComp)
                else set(values)
                if isinstance(node, ast.SetComp)
                else values
            )
        if isinstance(node, ast.JoinedStr):
            pieces = []
            for child in node.values:
                if isinstance(child, ast.FormattedValue):
                    value = self.value(child.value, env)
                    if not isinstance(value, (str, int, float, bool, type(None))):
                        value = str(value)
                    if child.conversion == 114:
                        value = repr(value)
                    spec = (
                        self.value(child.format_spec, env) if child.format_spec else ""
                    )
                    if len(spec) > 64 or re.search(r"\d{5,}", spec):
                        raise UnsupportedCommand("Portable format width exceeded")
                    pieces.append(format(value, spec))
                else:
                    pieces.append(str(child.value))
                if sum(map(len, pieces)) > MAX_FILE:
                    raise UnsupportedCommand("Portable formatted string limit exceeded")
            return self.bound("".join(pieces))
        raise UnsupportedCommand(
            "Python expression unsupported: " + type(node).__name__
        )

    def assign(self, target, value, env):
        self.bound(value)
        if isinstance(target, ast.Name):
            if target.id.startswith("__"):
                raise UnsupportedCommand("Private runtime names unavailable")
            env[target.id] = value
        elif isinstance(target, (ast.Tuple, ast.List)):
            values = list(value)
            if len(values) != len(target.elts):
                raise ValueError("Unpacking length mismatch")
            for child, item in zip(target.elts, values):
                self.assign(child, item, env)
        elif isinstance(target, ast.Subscript):
            obj = self.value(target.value, env)
            if not isinstance(obj, (dict, list)):
                raise UnsupportedCommand("Only data containers can be assigned")
            obj[self.value(target.slice, env)] = value
            self.bound(obj)
        else:
            raise UnsupportedCommand("Assignment target unsupported")

    def statements(self, nodes, env):
        for node in nodes:
            self.tick()
            if isinstance(node, ast.Expr):
                self.value(node.value, env)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                value = self.value(node.value, env)
                for target in (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                ):
                    self.assign(target, value, env)
            elif isinstance(node, ast.AugAssign):
                expression = ast.BinOp(left=node.target, op=node.op, right=node.value)
                self.assign(node.target, self.value(expression, env), env)
            elif isinstance(node, ast.FunctionDef):
                if node.decorator_list:
                    raise UnsupportedCommand("Function decorators unavailable")
                env[node.name] = _Function(
                    node,
                    env,
                    [self.value(v, env) for v in node.args.defaults],
                    {
                        item.arg: self.value(value, env)
                        for item, value in zip(
                            node.args.kwonlyargs, node.args.kw_defaults
                        )
                        if value is not None
                    },
                )
            elif isinstance(node, ast.Return):
                raise _Return(self.value(node.value, env))
            elif isinstance(node, ast.If):
                self.statements(
                    node.body if self.value(node.test, env) else node.orelse, env
                )
            elif isinstance(node, (ast.For, ast.While)):
                iterator = (
                    iter(self.value(node.iter, env))
                    if isinstance(node, ast.For)
                    else None
                )
                broken = False
                while True:
                    self.tick()
                    if iterator is not None:
                        try:
                            item = next(iterator)
                        except StopIteration:
                            break
                        self.assign(node.target, item, env)
                    elif not self.value(node.test, env):
                        break
                    try:
                        self.statements(node.body, env)
                    except _Continue:
                        continue
                    except _Break:
                        broken = True
                        break
                if not broken:
                    self.statements(node.orelse, env)
            elif isinstance(node, ast.Break):
                raise _Break()
            elif isinstance(node, ast.Continue):
                raise _Continue()
            elif isinstance(node, ast.Assert):
                if not self.value(node.test, env):
                    raise AssertionError(
                        self.value(node.msg, env) if node.msg else "assertion failed"
                    )
            elif isinstance(node, ast.Raise):
                error = self.value(node.exc, env)
                if not isinstance(error, Exception):
                    raise UnsupportedCommand(
                        "Only explicit data exceptions can be raised"
                    )
                raise error
            elif isinstance(node, ast.Import):
                for item in node.names:
                    env[item.asname or item.name.split(".")[0]] = self.module(
                        item.name if item.asname else item.name.split(".")[0]
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    raise UnsupportedCommand("Relative package imports unavailable")
                module = self.module(node.module)
                for item in node.names:
                    env[item.asname or item.name] = self.attribute(module, item.name)
            elif isinstance(node, ast.With):
                handles = []
                try:
                    for item in node.items:
                        handle = self.value(item.context_expr, env)
                        if not isinstance(handle, _File):
                            raise UnsupportedCommand(
                                "Only workspace files support with"
                            )
                        handles.append(handle)
                        if item.optional_vars:
                            self.assign(item.optional_vars, handle, env)
                    self.statements(node.body, env)
                finally:
                    for handle in handles:
                        handle.close()
            elif isinstance(node, ast.Try):
                try:
                    self.statements(node.body, env)
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AssertionError,
                    FileNotFoundError,
                ) as error:
                    # Capability denials cannot be caught and suppressed by code.
                    if isinstance(error, UnsupportedCommand):
                        raise
                    handler = next(
                        (
                            h
                            for h in node.handlers
                            if h.type and isinstance(error, self.value(h.type, env))
                        ),
                        None,
                    )
                    if handler is None:
                        raise
                    if handler.name:
                        env[handler.name] = error
                    self.statements(handler.body, env)
                else:
                    self.statements(node.orelse, env)
                finally:
                    self.statements(node.finalbody, env)
            elif isinstance(node, ast.Pass):
                pass
            else:
                raise UnsupportedCommand(
                    "Python statement unsupported: " + type(node).__name__
                )

    def run(self, source, env=None):
        tree = ast.parse(utf8_text(source))
        if sum(1 for _ in ast.walk(tree)) > 20000:
            raise UnsupportedCommand("Python AST size limit exceeded")
        self.statements(tree.body, env if env is not None else {"__name__": "__main__"})


def parse_portable_command(command):
    """Parse only; no shell expansion, pipelines or arbitrary executables."""
    source = str(command)
    if len(source) > MAX_FILE:
        raise UnsupportedCommand("Command size limit exceeded")
    heredoc = re.fullmatch(
        r"\s*(python(?:3(?:\.\d+)?)?|py)(?:\s+-)?\s+<<\s*[\'\"]?(\w+)[\'\"]?\s*\n(.*?)\n\2\s*",
        source,
        re.S,
    )
    if heredoc:
        return [(["python3", "-c", heredoc[3]], None, None)]
    lexer = shlex.shlex(source, posix=True, punctuation_chars=";&|<>")
    lexer.whitespace_split = True
    lexer.commenters = "#"
    tokens = list(lexer)
    if tokens and tokens[-1] in {"&&", "||"}:
        raise UnsupportedCommand("Trailing conditional shell operator")
    groups = []
    current = []
    redirect = None
    for token in tokens + [";"]:
        if token in {";", "&&", "||"}:
            if not current and token in {"&&", "||"}:
                raise UnsupportedCommand("Missing command around shell operator")
            if current:
                groups.append((current, redirect, token))
                current = []
                redirect = None
        elif token in {"|", "&", "<", "<<", "<<<"}:
            raise UnsupportedCommand(
                "Pipelines/background/stdin redirection unavailable; use Python file operations"
            )
        else:
            current.append(token)
    parsed = []
    supported = {
        "python",
        "python3",
        "py",
        "pwd",
        "echo",
        "printf",
        "cat",
        "ls",
        "dir",
        "head",
        "tail",
        "wc",
        "mkdir",
        "touch",
        "cp",
        "mv",
        "rm",
        "true",
        "false",
        "exit",
        "test",
    }
    for args, _, connector in groups:
        if any(t in args for t in (">", ">>")):
            index = next(i for i, t in enumerate(args) if t in {">", ">>"})
            if index != len(args) - 2:
                raise UnsupportedCommand("Only one final file redirection is supported")
            redirect = (args[-1], args[index])
            args = args[:index]
        else:
            redirect = None
        if not args or args[0] not in supported:
            raise UnsupportedCommand(
                "Unsupported portable command; use list_files/read_file/write_file or python3 -c with json/pathlib"
            )
        if args[0] in {"python", "python3", "py"}:
            if "-c" in args:
                index = args.index("-c")
                if index + 1 >= len(args):
                    raise UnsupportedCommand("Python -c requires source")
                ast.parse(utf8_text(args[index + 1]))
            elif len(args) < 2:
                raise UnsupportedCommand("Python requires a workspace script or -c")
        parsed.append((args, redirect, connector))
    if not parsed:
        raise UnsupportedCommand("Empty portable command")
    return parsed


def run_portable_command(
    root, command, *, cwd=None, timeout=15, checkpoint=lambda: None
):
    start = time.monotonic()
    fs = WorkspaceFiles(root, cwd)
    vm = PythonWorkspace(fs, checkpoint, timeout)
    result = {
        "backend": "portable_workspace",
        "exit_code": 0,
        "output": "",
        "changed_files": [],
        "recoverable": False,
    }
    try:
        groups = parse_portable_command(command)
        previous = None
        for args, redirect, connector in groups:
            if (
                previous == "&&"
                and result["exit_code"] != 0
                or previous == "||"
                and result["exit_code"] == 0
            ):
                previous = connector
                continue
            checkpoint()
            vm.tick()
            before = len(vm.output)
            code = 0
            name, params = args[0], args[1:]
            try:
                if name in {"python", "python3", "py"}:
                    if "-c" in params:
                        vm.run(params[params.index("-c") + 1])
                    elif params[:2] == ["-m", "py_compile"]:
                        if len(params) < 3:
                            raise UnsupportedCommand(
                                "py_compile requires workspace filenames"
                            )
                        for filename in params[2:]:
                            ast.parse(utf8_text(fs.read(filename).decode("utf-8")))
                    else:
                        vm.run(
                            fs.read(
                                next(p for p in params if not p.startswith("-"))
                            ).decode("utf-8")
                        )
                    for handle in vm.opened:
                        handle.close()
                elif name == "pwd":
                    vm.print(
                        "/workspace" + ("/" + fs.prefix if fs.prefix != "." else "")
                    )
                elif name == "echo":
                    vm.print(
                        " ".join(params[1:] if params[:1] == ["-n"] else params),
                        end="" if params[:1] == ["-n"] else "\n",
                    )
                elif name == "printf":
                    if not params:
                        raise UnsupportedCommand("printf requires a format")
                    pattern = params[0].replace("\\n", "\n").replace("\\t", "\t")
                    if (
                        len(pattern) > 16000
                        or pattern.count("%") > 256
                        or re.search(r"%[^%]*\d{5,}", pattern)
                    ):
                        raise UnsupportedCommand("Portable format width exceeded")
                    vm.print(
                        (pattern % tuple(params[1:])) if len(params) > 1 else pattern,
                        end="",
                    )
                elif name in {"cat", "head", "tail", "wc"}:
                    count = 10
                    if params[:1] == ["-n"]:
                        count = int(params[1])
                        params = params[2:]
                    chunks = []
                    total = 0
                    for filename in params:
                        if filename.startswith("-"):
                            continue
                        checkpoint()
                        chunk = fs.read(filename).decode("utf-8")
                        total += len(chunk)
                        if total > MAX_FILE:
                            raise UnsupportedCommand(
                                "Portable command input limit exceeded"
                            )
                        chunks.append(chunk)
                    data = "".join(chunks)
                    if name == "head":
                        data = "".join(data.splitlines(True)[:count])
                    elif name == "tail":
                        data = "".join(data.splitlines(True)[-count:])
                    elif name == "wc":
                        data = str(len(data.splitlines())) + "\n"
                    vm.print(data, end="")
                elif name in {"ls", "dir"}:
                    vm.print("\n".join(fs.files()))
                elif name == "mkdir":
                    for p in params:
                        if not p.startswith("-"):
                            fs.directories.add(fs.relative(p))
                elif name == "touch":
                    for p in params:
                        if not fs.exists(p):
                            fs.write(p, b"")
                elif name in {"cp", "mv"}:
                    if len(params) != 2:
                        raise UnsupportedCommand(
                            "cp/mv requires source and destination files"
                        )
                    fs.write(params[1], fs.read(params[0]))
                    if name == "mv":
                        fs.deleted.add(fs.relative(params[0]))
                elif name == "rm":
                    for p in params:
                        if p.startswith("-"):
                            raise UnsupportedCommand(
                                "Recursive deletion unavailable; remove explicit files"
                            )
                        fs.deleted.add(fs.relative(p))
                elif name == "test":
                    if len(params) != 2 or params[0] not in {"-f", "-e"}:
                        raise UnsupportedCommand("Use test -f/-e PATH")
                    code = 0 if fs.exists(params[1]) else 1
                elif name in {"false", "exit"}:
                    code = 1 if name == "false" else int(params[0]) if params else 0
            except _Exit as done:
                code = done.code
            if redirect:
                text = "".join(vm.output[before:])
                del vm.output[before:]
                fs.write(
                    redirect[0],
                    (
                        fs.read(redirect[0])
                        if redirect[1] == ">>" and fs.exists(redirect[0])
                        else b""
                    )
                    + utf8_bytes(text),
                )
            result["exit_code"] = code
            previous = connector
        checkpoint()
        result["changed_files"] = fs.commit()
    except UnsupportedCommand as error:
        result.update(
            exit_code=126,
            recoverable=True,
            error_code="portable_operation_unavailable",
            output=str(error)
            + "; continue with workspace file tools or supported Python data operations.",
        )
    except (_Return, _Break, _Continue):
        result.update(
            exit_code=126,
            recoverable=True,
            error_code="portable_operation_unavailable",
            output="Control flow used outside a function or loop",
        )
    except Exception as error:
        if getattr(error, "code", None):
            raise
        result.update(
            exit_code=1, output=type(error).__name__ + ": " + utf8_text(error)
        )
    result["output"] = utf8_text("".join(vm.output) + result["output"])[:16000]
    result["duration_ms"] = round((time.monotonic() - start) * 1000)
    return result
