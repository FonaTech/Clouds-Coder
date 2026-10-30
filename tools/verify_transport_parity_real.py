"""Compare real ordinary/structured transports using the same public task-design request.

No user sessions are read or sent. Each HTTP attempt is bounded and retries are
explicitly disabled so an unavailable service cannot hide behind backoff.
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import Clouds_Coder as cc  # noqa: E402
from liquid_kernel.agentic import build_task_bank, normalize_task_design  # noqa: E402
from liquid_kernel.control import normalize_evolution_config  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--profiles", default="openrouter,siliconflow")
    parser.add_argument("--timeout", type=float, default=45)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    profiles = {
        p["id"]: p
        for p in cc.parse_llm_config_profiles(
            json.loads(args.config.read_text()), "http://127.0.0.1:11434", ""
        )["profiles"]
    }
    config = normalize_evolution_config({"mode": "Tuning"})
    requests = [
        "Implement a Python Todo list that updates existing stable IDs in place and discards tool-envelope metadata.",
        "Implement file-evidence memory with exact historical recall and invalidation of cached current facts after file changes.",
    ]
    experience = {
        "history_by_version": {
            "public": {
                "records": [
                    {
                        "user_id": "public",
                        "session_id": "public-" + str(i),
                        "title": "Public harness regression task",
                        "messages": [
                            {"role": "user", "content": goal},
                            {
                                "role": "user",
                                "content": "After round 3, change the output from a text report to result.json and verify the revised requirements using actual Python checks.",
                            },
                        ],
                    }
                    for i, goal in enumerate(requests)
                ]
            }
        }
    }
    captured = {}

    class Captured(Exception):
        pass

    def capture(system, prompt):
        captured.update(system=system, prompt=prompt)
        raise Captured()

    try:
        build_task_bank(experience, config, capture, 27)
    except Captured:
        pass
    system, prompt = (
        captured["system"],
        json.dumps(captured["prompt"], ensure_ascii=False),
    )

    def verify(target):
        pid, mode = target
        profile = profiles[pid]
        client = cc.OllamaClient(profile.get("base_url", ""), profile["model"])
        client.apply_profile(profile)
        endpoint = urlparse(client.endpoint or client.base_url)
        client.structured_json_output = mode != "ordinary_stream"
        client.structured_thinking_disabled = mode != "ordinary_stream" and bool(
            (endpoint.hostname or "").endswith((".volces.com", ".volcengine.com"))
            and endpoint.path.startswith(("/api/plan/", "/api/v3"))
        )
        row = {
            "profile": pid,
            "model": client.model,
            "mode": mode,
            "stream": mode != "evolution_nonstream",
            "json_mode": client.structured_json_output,
            "request_chars": len(system + prompt),
            "output_limit": 4096,
            "private_history_sent": False,
            "http_retries": 0,
        }
        start = time.monotonic()
        chunks = []

        def delta(text):
            chunks.append((time.monotonic() - start, len(str(text))))

        try:
            response = client.chat(
                [{"role": "user", "content": prompt}],
                system=system,
                tools=None,
                max_tokens=4096,
                temperature=0.1,
                think=False,
                effort="off",
                response_stream=row["stream"],
                on_content_delta=delta,
                request_timeout=args.timeout,
                auxiliary=True,
                label="transport_parity",
            )
            raw = response.get("raw") or {}
            choices = raw.get("choices") or [{}]
            row.update(
                content_chars=len(response.get("content", "")),
                thinking_chars=len(response.get("thinking", "")),
                first_chunk_seconds=round(chunks[0][0], 2) if chunks else None,
                finish_reason=choices[0].get("finish_reason", raw.get("done_reason")),
                usage=client._usage_tokens(response),
            )
            value = cc.standard_model_json_object(response.get("content", ""))
            row["json_root_keys"] = list(value)[:20]
            normalize_task_design(value, config["task_benchmark"])
            row["passed"] = True
        except Exception as exc:
            reason = str(exc)
            for secret in [
                profile.get("api_key", ""),
                *profile.get("headers", {}).values(),
            ]:
                if isinstance(secret, str) and len(secret) > 4:
                    reason = reason.replace(secret, "[redacted]")
            row.update(
                passed=False,
                error_type=type(exc).__name__,
                http_status=getattr(exc, "status", 0),
                reason=reason[:400],
            )
        row["seconds"] = round(time.monotonic() - start, 2)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        return row

    targets = [
        (p, m)
        for p in args.profiles.split(",")
        if p in profiles
        for m in ("evolution_nonstream", "ordinary_stream", "structured_stream")
    ]
    with ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(verify, targets))
    args.report.write_text(
        json.dumps(
            {"source": "declared public executable task design", "rows": rows},
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
