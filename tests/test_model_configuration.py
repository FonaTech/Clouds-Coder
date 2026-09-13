import threading
import time
import unittest
from unittest import mock

import Clouds_Coder as cc


class ModelConfigurationTests(unittest.TestCase):
    def test_model_probe_extracts_reasoning_capabilities(self):
        records = cc.extract_openai_compat_model_records(
            {
                "data": [
                    {"id": "reasoner", "supported_parameters": ["reasoning_effort"]},
                    {"id": "plain", "capabilities": ["vision"]},
                ]
            }
        )

        self.assertEqual([row["id"] for row in records], ["reasoner", "plain"])
        self.assertEqual(
            records[0]["capabilities"],
            {"reasoning_supported": True, "reasoning_style": "openai"},
        )
        self.assertEqual(records[1]["capabilities"], {})

    def test_reasoning_metadata_overrides_name_fallback(self):
        self.assertEqual(
            cc.model_reasoning_style(
                "openai_compat", "o3-mini", {"reasoning_supported": False}
            ),
            "none",
        )
        self.assertEqual(
            cc.model_reasoning_style(
                "openai_compat", "plain-model", {"reasoning_supported": True}
            ),
            "openai",
        )

    def test_ollama_capabilities_are_read_from_show_metadata(self):
        self.assertEqual(
            cc.extract_ollama_model_capabilities(
                {"capabilities": ["completion", "thinking", "tools", "vision"]}
            ),
            {
                "reasoning_supported": True,
                "reasoning_style": "ollama",
                "vision": True,
                "tools": True,
            },
        )
        self.assertEqual(
            cc.extract_ollama_model_capabilities({"capabilities": ["completion"]}),
            {},
        )

    def test_cold_provider_probe_returns_before_network_finishes(self):
        released = threading.Event()
        extracted = threading.Event()
        base_url = f"https://probe-{cc.uuid.uuid4().hex}.example/v1"
        profile = {
            "provider": "openai_compat",
            "base_url": base_url,
            "api_key": "test-key",
        }

        class _Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return b'{"data":[{"id":"background-model"}]}'

        original_extract = cc.extract_openai_compat_model_records

        def extract(payload):
            result = original_extract(payload)
            extracted.set()
            return result

        def slow_urlopen(*_args, **_kwargs):
            released.wait(1.0)
            return _Response()

        started = time.monotonic()
        with mock.patch.object(cc, "urlopen", side_effect=slow_urlopen):
            with mock.patch.object(cc, "extract_openai_compat_model_records", side_effect=extract):
                self.assertEqual(cc.probe_provider_models(profile, background=True), [])
                self.assertLess(time.monotonic() - started, 0.25)
                released.set()
                self.assertTrue(extracted.wait(1.0))
                records = cc.probe_provider_models(profile)

        self.assertEqual([row["id"] for row in records], ["background-model"])

    def test_provider_model_directory_is_preserved_and_selects_first_auto_model(self):
        parsed = cc.parse_llm_config_profiles(
            {
                "provider": "vllm",
                "vllm_url": "http://localhost:8000/v1",
                "vllm_models": ["coder-a", "coder-b"],
            },
            "http://127.0.0.1:11434",
            "llama3",
        )

        profile = parsed["profiles"][0]
        self.assertEqual(profile["model"], "coder-a")
        self.assertEqual(profile["models"], ["coder-a", "coder-b"])

    def test_model_reasoning_capabilities_survive_config_round_trip(self):
        parsed = cc.parse_llm_config_profiles(
            {
                "provider": "custom_http",
                "custom_url": "https://example.test/v1/chat/completions",
                "custom_models": ["plain", "reasoner"],
                "model_reasoning_capabilities": {
                    "reasoner": {
                        "reasoning_supported": True,
                        "reasoning_style": "openai",
                    }
                },
            },
            "http://127.0.0.1:11434",
            "llama3",
        )

        profile = parsed["profiles"][0]
        self.assertEqual(profile["model"], "plain")
        self.assertEqual(profile["models"], ["plain", "reasoner"])
        self.assertEqual(
            profile["model_settings"]["reasoner"],
            {"reasoning_supported": True, "reasoning_style": "openai"},
        )


if __name__ == "__main__":
    unittest.main()
