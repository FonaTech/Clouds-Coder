"""Source-bound model references. Credentials stay in the existing profile store."""
from __future__ import annotations

import hashlib
import hmac
import json

from .control import LiquidKernelError, normalize_model_ref


class EvolutionModels:
    def __init__(self, profiles, records, settings, signing_key: bytes):
        self.profiles = profiles
        self.records = records
        self.settings = settings
        self.signing_key = signing_key

    def model_ids(self, profile):
        configured = profile.get("models", [])
        configured = configured if isinstance(configured, list) else []
        return sorted({str(item).strip() for item in [profile.get("model", ""), *configured,
                       *(row.get("id", "") for row in self.records(profile))] if str(item).strip()})

    def effective(self, profile, model):
        row = {**profile, **self.settings(profile, model), "model": model}
        # Directory/UI metadata and settings for other models do not affect this call.
        for key in ("id", "label", "title", "display_name", "source", "selection", "models", "model_settings"):
            row.pop(key, None)
        row["provider"] = str(row.get("provider") or "ollama")
        row["base_url"] = str(row.get("base_url") or "").rstrip("/")
        row["endpoint"] = str(row.get("endpoint") or "")
        row["api_key"] = str(row.get("api_key") or "")
        row["headers"] = row.get("headers") if isinstance(row.get("headers"), dict) else {}
        row["payload_template"] = str(row.get("payload_template") or "")
        return row

    def fingerprint(self, profile):
        raw = json.dumps(profile, sort_keys=True, ensure_ascii=False, default=str).encode()
        return hmac.new(self.signing_key, raw, hashlib.sha256).hexdigest()

    def resolve(self, reference=None, legacy=""):
        ref = normalize_model_ref(reference)
        if ref is None:
            profiles, active = self.profiles("global", "")
            pid, sep, model = str(legacy or "").partition("::")
            pid = pid or active
            profile = profiles.get(pid)
            if not profile:
                raise LiquidKernelError("model_profile_missing", "global model configuration no longer exists", 409)
            ref = normalize_model_ref({"source": "global", "owner": "", "profile_id": pid,
                                       "model": model if sep else profile.get("model", "")})
        profiles, _ = self.profiles(ref["source"], ref["owner"])
        profile = profiles.get(ref["profile_id"])
        if not isinstance(profile, dict):
            raise LiquidKernelError("model_profile_missing", "selected model configuration was deleted or is unavailable", 409)
        if profile.get("disabled") or profile.get("enabled") is False:
            raise LiquidKernelError("model_disabled", "selected model configuration is disabled", 409)
        if ref["model"] not in self.model_ids(profile):
            raise LiquidKernelError("model_missing", "selected model is no longer in its model directory", 409)
        effective = self.effective(profile, ref["model"])
        if not (effective.get("base_url") or effective.get("endpoint")):
            raise LiquidKernelError("model_address_missing", "selected model has no service address", 409)
        fingerprint = self.fingerprint(effective)
        if ref.get("fingerprint") and not hmac.compare_digest(ref["fingerprint"], fingerprint):
            raise LiquidKernelError("model_config_changed", "selected model configuration changed; refresh models and save again", 409)
        return {**ref, "fingerprint": fingerprint}, effective

    def validate_config(self, config, *, context=None, current=None):
        out = dict(config)
        for role in ("generator", "judge"):
            key = f"{role}_model_ref"
            ref = normalize_model_ref(out.get(key))
            if context is not None and ref and ref["source"] != "global":
                permitted = context.get(ref["source"], "") == ref["owner"]
                unchanged = ref == (current or {}).get(key)
                if not permitted and not unchanged:
                    raise LiquidKernelError("model_owner_forbidden", "sign in as the owner to select this private model", 403)
            # Off must remain available even if an existing model has disappeared.
            if config["mode"] == "Off" and ref == (current or {}).get(key) and out.get(f"{role}_profile", "") == (current or {}).get(f"{role}_profile", ""):
                continue
            resolved, _ = self.resolve(ref, out.get(f"{role}_profile", ""))
            if ref is not None:
                out[key] = resolved
        return out

    def bind_run(self, config):
        out = dict(config)
        for role in ("generator", "judge"):
            out[f"{role}_model_ref"], _ = self.resolve(config.get(f"{role}_model_ref"), config.get(f"{role}_profile", ""))
        return out

    def catalog(self, context, config):
        options, sources = [], []
        for source in ("global", "agent", "ide"):
            owner = "" if source == "global" else context.get(source, "")
            if source != "global" and not owner:
                sources.append({"source": source, "available": False, "reason": "Sign in to IDE to use this source." if source == "ide" else "Agent identity unavailable."})
                continue
            try:
                profiles, _ = self.profiles(source, owner)
            except LiquidKernelError as exc:
                sources.append({"source": source, "available": False, "reason": str(exc)})
                continue
            sources.append({"source": source, "available": True, "reason": ""})
            merged = {}
            for pid, profile in profiles.items():
                if not isinstance(profile, dict):
                    continue
                models = self.model_ids(profile)
                if not models:
                    options.append({"ref": None, "aliases": [], "sources": [source], "model": "",
                                    "label": f"[{source}] {pid}", "available": False, "reason": "No model configured."})
                for model in models:
                    ref = {"source": source, "owner": owner, "profile_id": pid, "model": model}
                    reason = ""
                    try:
                        ref, effective = self.resolve(ref)
                        signature = self.fingerprint(effective)
                    except LiquidKernelError as exc:
                        reason, signature = str(exc), f"{pid}:{model}"
                    if signature in merged:
                        merged[signature]["aliases"].append(ref)
                        continue
                    option = {"ref": ref, "aliases": [ref], "sources": [source], "model": model,
                              "label": f"[{source}] {model} · {pid}", "available": not reason, "reason": reason}
                    merged[signature] = option
                    options.append(option)
        resolved = {}
        for role in ("generator", "judge"):
            try:
                ref, _ = self.resolve(config.get(f"{role}_model_ref"), config.get(f"{role}_profile", ""))
                resolved[role] = {"ref": ref, "available": True, "reason": ""}
            except LiquidKernelError as exc:
                resolved[role] = {"ref": config.get(f"{role}_model_ref"), "available": False, "reason": str(exc)}
        return {"ok": True, "options": options, "sources": sources, "resolved": resolved}
