import importlib.util
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
STORE_CLASSES = (
    "CollaborationStore",
    "AgentWebSearchEngine",
    "AdminAuthStore",
    "IDEAuthStore",
    "UserMemoryStore",
    "SkillsStudioStore",
    "TelemetryStore",
)


class SQLiteLifecycleChecks:
    @classmethod
    def setUpClass(cls):
        if not (ROOT / cls.filename).is_file():
            raise unittest.SkipTest("Optional historical source snapshot is not distributed")
        name = "_sqlite_lifecycle_" + cls.__name__
        spec = importlib.util.spec_from_file_location(name, ROOT / cls.filename)
        cls.module = importlib.util.module_from_spec(spec)
        sys.modules[name] = cls.module
        cls.addClassCleanup(sys.modules.pop, name, None)
        spec.loader.exec_module(cls.module)

    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="cc-sqlite-test-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def store(self, class_name):
        # Exercise each real connection factory without unrelated startup work.
        store_class = getattr(self.module, class_name)
        store = store_class.__new__(store_class)
        store.path = store.db_path = self.root / (class_name + ".sqlite")
        store._initialized = False
        return store

    def assert_closed(self, conn):
        with self.assertRaises(sqlite3.ProgrammingError):
            conn.execute("SELECT 1")

    def test_every_store_commits_and_closes(self):
        for name in STORE_CLASSES:
            with self.subTest(store=name):
                store = self.store(name)
                conn = store._connect()
                self.addCleanup(conn.close)
                with conn:
                    conn.execute("CREATE TABLE items(value INTEGER)")
                    conn.execute("INSERT INTO items VALUES(42)")
                self.assert_closed(conn)
                with store._connect() as reader:
                    self.assertEqual(reader.execute("SELECT value FROM items").fetchone()[0], 42)

    def test_every_store_rolls_back_and_closes_on_error(self):
        for name in STORE_CLASSES:
            with self.subTest(store=name):
                store = self.store(name)
                conn = store._connect()
                self.addCleanup(conn.close)
                conn.execute("CREATE TABLE items(value INTEGER)")
                with self.assertRaisesRegex(RuntimeError, "abort transaction"), conn:
                    conn.execute("BEGIN IMMEDIATE")
                    conn.execute("INSERT INTO items VALUES(42)")
                    raise RuntimeError("abort transaction")
                self.assert_closed(conn)
                with store._connect() as reader:
                    self.assertEqual(reader.execute("SELECT COUNT(*) FROM items").fetchone()[0], 0)

    def test_failed_connection_setup_closes_handle(self):
        real_connect = sqlite3.connect
        opened = []

        class FailingPragmaConnection(sqlite3.Connection):
            def execute(self, sql, *args, **kwargs):
                if sql.startswith("PRAGMA"):
                    raise sqlite3.OperationalError("injected setup failure")
                return super().execute(sql, *args, **kwargs)

        def connect(*args, **kwargs):
            kwargs["factory"] = FailingPragmaConnection
            conn = real_connect(*args, **kwargs)
            opened.append(conn)
            self.addCleanup(conn.close)
            return conn

        for name in STORE_CLASSES:
            if name in {"AgentWebSearchEngine", "UserMemoryStore"}:
                continue  # These factories have no PRAGMA setup.
            with self.subTest(store=name):
                with mock.patch.object(self.module.sqlite3, "connect", side_effect=connect):
                    with self.assertRaisesRegex(sqlite3.OperationalError, "injected setup failure"):
                        self.store(name)._connect()
                self.assert_closed(opened[-1])

    def test_failed_commit_still_closes_and_rolls_back(self):
        store = self.store("CollaborationStore")
        conn = store._connect()
        self.addCleanup(conn.close)
        conn.executescript(
            "CREATE TABLE parents(id INTEGER PRIMARY KEY);"
            "CREATE TABLE children(parent_id INTEGER REFERENCES parents(id) "
            "DEFERRABLE INITIALLY DEFERRED);"
        )
        with self.assertRaises(sqlite3.IntegrityError), conn:
            conn.execute("BEGIN")
            conn.execute("INSERT INTO children VALUES(42)")
        self.assert_closed(conn)
        with store._connect() as reader:
            self.assertEqual(reader.execute("SELECT COUNT(*) FROM children").fetchone()[0], 0)

    def test_local_kernel_registry_closes_connections(self):
        plane = self.module.LiquidKernelControlPlane(self.root / "kernel")
        with plane.registry._connect() as conn:
            self.assertEqual(conn.execute("SELECT 1").fetchone()[0], 1)
        self.assert_closed(conn)

    def test_released_embedded_kernel_closes_without_main_adapter(self):
        package = self.root / "released_kernel"
        self.module._ensure_embedded_liquid_kernel_package(package)
        name = "_released_kernel_" + type(self).__name__
        spec = importlib.util.spec_from_file_location(name, package / "__init__.py", submodule_search_locations=[str(package)])
        released = importlib.util.module_from_spec(spec)
        sys.modules[name] = released
        def unload():
            for key in list(sys.modules):
                if key == name or key.startswith(name + "."):
                    sys.modules.pop(key, None)
        self.addCleanup(unload)
        spec.loader.exec_module(released)
        control = sys.modules[name + ".control"]
        registry = control.LiquidKernelRegistry(self.root / "released_state")
        with registry._connect() as conn:
            conn.execute("CREATE TABLE closure_probe(value INTEGER)")
            conn.execute("INSERT INTO closure_probe VALUES(42)")
        self.assert_closed(conn)
        with registry._connect() as reader:
            self.assertEqual(reader.execute("SELECT value FROM closure_probe").fetchone()[0], 42)
        with self.assertRaisesRegex(RuntimeError, "abort"), registry._connect() as conn:
            conn.execute("INSERT INTO closure_probe VALUES(99)")
            raise RuntimeError("abort")
        self.assert_closed(conn)
        with registry._connect() as reader:
            self.assertEqual(reader.execute("SELECT COUNT(*) FROM closure_probe").fetchone()[0], 1)

    def test_legacy_local_package_adapter_is_idempotent_and_preserves_transactions(self):
        class LegacyRegistry:
            def _connect(inner_self):
                return sqlite3.connect(self.root / "legacy.sqlite")

        self.module._ensure_liquid_kernel_sqlite_lifecycle(LegacyRegistry)
        adapted = LegacyRegistry._connect
        self.module._ensure_liquid_kernel_sqlite_lifecycle(LegacyRegistry)
        self.assertIs(LegacyRegistry._connect, adapted)
        registry = LegacyRegistry()
        with registry._connect() as conn:
            conn.execute("CREATE TABLE items(value INTEGER)")
            conn.execute("INSERT INTO items VALUES(42)")
        self.assert_closed(conn)
        with self.assertRaisesRegex(RuntimeError, "abort"), registry._connect() as conn:
            conn.execute("INSERT INTO items VALUES(99)")
            raise RuntimeError("abort")
        self.assert_closed(conn)
        with registry._connect() as conn:
            self.assertEqual(conn.execute("SELECT value FROM items").fetchall(), [(42,)])

    def test_diagnostics_report_missing_path_without_creating_database(self):
        path = self.root / "missing" / "database.sqlite"
        with self.assertRaises(sqlite3.OperationalError) as caught:
            self.module._connect_sqlite(str(path), timeout=1)
        details = self.module.sqlite_failure_diagnostics(caught.exception)
        self.assertEqual(details["cause"], "storage_path_unavailable")
        self.assertEqual(details["operation"], "connect")
        self.assertEqual(details["database"], str(path))
        self.assertFalse(path.exists())

    def test_diagnostics_record_failed_pragma(self):
        path = self.root / "pragma.sqlite"
        with self.assertRaises(sqlite3.OperationalError) as caught:
            self.module._connect_sqlite(str(path), timeout=1, pragmas=("PRAGMA !invalid",))
        details = self.module.sqlite_failure_diagnostics(caught.exception)
        self.assertEqual(details["operation"], "PRAGMA !invalid")
        self.assertEqual(details["database"], str(path))
        self.assertEqual(details["cause"], "undetermined")

    def test_watcher_logs_diagnostics_without_exposing_paths_in_health(self):
        store = self.store("CollaborationStore")
        store.db_path = self.root / "missing" / "db.sqlite"
        app = type("App", (), {"collaboration": store})()
        logs = []
        stop = mock.Mock()
        stop.wait.side_effect = [False, True]
        self.module.collaboration_file_watcher_loop(app, stop, log=logs.append)
        self.assertTrue(any("storage diagnostics:" in line for line in logs))
        self.assertTrue(any("storage_path_unavailable" in line for line in logs))
        health = self.module.collaboration_watcher_health(app)
        self.assertEqual(health["status"], "degraded")
        self.assertNotIn(str(self.root), repr(health))

    @unittest.skipIf(sys.platform == "win32", "requires POSIX file descriptor limits")
    def test_watcher_stays_available_without_garbage_collection(self):
        # Keep the reduced FD limit and GC changes isolated from the test runner.
        script = r'''
import gc
import importlib.util
import os
from pathlib import Path
import resource
import socket
import sys
import tempfile

spec = importlib.util.spec_from_file_location("cc_fd_check", sys.argv[1])
cc = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cc
spec.loader.exec_module(cc)
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    store = cc.CollaborationStore(root / "collaboration.sqlite", root / "Codes", root / "state")
    kernel = cc.LiquidKernelControlPlane(root / "kernel")
    gc.collect()
    gc.disable()
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (min(256, soft), hard))
    try:
        for _ in range(1000):
            # The evolution scheduler queries even in Off mode while idle.
            kernel.registry.list_runs(limit=1)
            if _ % 10 == 0:
                kernel.dashboard()
            store.scan_external_writes()
            assert store.storage_health()["available"]
            with socket.socket():
                pass
        # Diagnose real process-wide exhaustion, not only a mocked SQLite error.
        held = []
        try:
            while True:
                held.append(os.open(os.devnull, os.O_RDONLY))
        except OSError:
            pass
        try:
            try:
                store.scan_external_writes()
            except cc.sqlite3.OperationalError as exc:
                diagnostic = cc.sqlite_failure_diagnostics(exc, store.db_path)
                assert diagnostic["cause"] == "file_descriptor_exhaustion", diagnostic
                assert diagnostic["fd_limit_soft"] <= 256, diagnostic
            else:
                raise AssertionError("expected exhausted descriptor limit")
        finally:
            for descriptor in held:
                os.close(descriptor)
    finally:
        resource.setrlimit(resource.RLIMIT_NOFILE, (soft, hard))
        gc.enable()
        gc.collect()
'''
        result = subprocess.run(
            [sys.executable, "-c", script, str(ROOT / self.filename)],
            cwd=ROOT, capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class CurrentSQLiteLifecycleTests(SQLiteLifecycleChecks, unittest.TestCase):
    filename = "Clouds_Coder.py"


class Version5204SQLiteLifecycleTests(SQLiteLifecycleChecks, unittest.TestCase):
    filename = "Clouds_Coder_5.20_4.py"


if __name__ == "__main__":
    unittest.main()
