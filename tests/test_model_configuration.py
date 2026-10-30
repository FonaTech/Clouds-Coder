import json
import unittest
import threading
import time
from unittest import mock

import Clouds_Coder as cc


class ModelConfigurationTests(unittest.TestCase):
    def setUp(self):
        with cc._PROVIDER_MODEL_CACHE_LOCK:
            cc._PROVIDER_MODEL_CACHE.clear()

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
        self.assertEqual(
            cc.model_reasoning_style("openai_compat", "o3-mini", {}),
            "none",
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

    def test_ollama_probe_inspects_all_models_by_default(self):
        tags = [f"model-{index}" for index in range(10)]

        class _Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return json.dumps(self.payload).encode("utf-8")

        def fake_urlopen(request, **_kwargs):
            if request.full_url.endswith("/api/tags"):
                return _Response({"models": [{"name": name} for name in tags]})
            model = json.loads(request.data.decode("utf-8"))["name"]
            return _Response({"capabilities": ["thinking"] if model == tags[-1] else ["completion"]})

        with mock.patch.object(cc, "urlopen", side_effect=fake_urlopen):
            records = cc.probe_ollama_model_records("http://ollama.test")

        self.assertEqual(len(records), len(tags))
        self.assertEqual(records[-1]["capabilities"].get("reasoning_supported"), True)

    def test_probed_directory_merges_models_and_capabilities(self):
        profile = {"id": "provider", "model": "", "models": ["configured"]}
        changed = cc.merge_probed_models_into_profile(
            profile,
            [
                {"id": "configured", "capabilities": {"reasoning_supported": True, "reasoning_style": "openai"}},
                {"id": "discovered", "capabilities": {"reasoning_supported": False}},
            ],
        )

        self.assertTrue(changed)
        self.assertEqual(profile["models"], ["configured", "discovered"])
        self.assertEqual(profile["model"], "configured")
        self.assertEqual(profile["model_settings"]["configured"]["reasoning_style"], "openai")
        self.assertFalse(profile["model_settings"]["discovered"]["reasoning_supported"])

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

    def test_anthropic_probe_uses_native_headers_and_imports_all_pages(self):
        requests = []

        class _Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return json.dumps(self.payload).encode("utf-8")

        def fake_urlopen(request, **_kwargs):
            requests.append(request)
            if "after_id=" in request.full_url:
                return _Response(
                    {"data": [{"id": "claude-page-2"}], "has_more": False}
                )
            return _Response(
                {
                    "data": [{"id": "claude-page-1"}],
                    "has_more": True,
                    "last_id": "claude-page-1",
                }
            )

        profile = {
            "provider": "anthropic",
            "base_url": "https://api.anthropic.test",
            "api_key": "secret-key",
        }
        with mock.patch.object(cc, "urlopen", side_effect=fake_urlopen):
            records = cc.probe_provider_models(profile, force_refresh=True)

        self.assertEqual(
            [record["id"] for record in records],
            ["claude-page-1", "claude-page-2"],
        )
        self.assertEqual(len(requests), 2)
        self.assertTrue(requests[0].full_url.endswith("/v1/models?limit=1000"))
        headers = {key.lower(): value for key, value in requests[0].header_items()}
        self.assertEqual(headers["x-api-key"], "secret-key")
        self.assertEqual(headers["anthropic-version"], "2023-06-01")
        self.assertNotIn("authorization", headers)

    def test_multiple_provider_probe_imports_each_complete_directory(self):
        profiles = [
            {"id": "first", "provider": "openai_compat", "models": []},
            {"id": "second", "provider": "custom_http", "models": []},
        ]

        def fake_probe(profile, **_kwargs):
            prefix = profile["id"]
            return [{"id": f"{prefix}-{index}", "capabilities": {}} for index in range(3)]

        with mock.patch.object(cc, "probe_provider_models", side_effect=fake_probe):
            changed = cc.probe_and_merge_model_profiles(profiles)

        self.assertTrue(changed)
        self.assertEqual(profiles[0]["models"], ["first-0", "first-1", "first-2"])
        self.assertEqual(profiles[1]["models"], ["second-0", "second-1", "second-2"])

    def test_structured_custom_provider_preserves_name_title_and_url(self):
        parsed = cc.parse_llm_config_profiles(
            {
                "profiles": [
                    {
                        "provider": "AcmeGateway",
                        "name": "Acme Coding",
                        "title": "Private Models",
                        "url": "https://acme.test/v1",
                        "models": ["acme-a", "acme-b"],
                    }
                ]
            },
            "http://127.0.0.1:11434",
            "llama3",
        )

        profile = parsed["profiles"][0]
        self.assertEqual(profile["provider"], "custom_http")
        self.assertEqual(profile["display_name"], "Acme Coding")
        self.assertEqual(profile["title"], "Private Models")
        self.assertEqual(profile["base_url"], "https://acme.test/v1")
        self.assertEqual(profile["models"], ["acme-a", "acme-b"])

    def test_runtime_selection_keeps_probed_reasoning_per_model(self):
        session = object.__new__(cc.SessionState)
        session.model_profiles = {
            "vendor": {
                "id": "vendor",
                "provider": "openai_compat",
                "model": "plain",
                "models": ["plain", "reasoner"],
                "base_url": "https://provider.test/v1",
            }
        }
        session.active_profile_id = "vendor"
        session.failed_selections = []
        session.auto_task_level_ceiling = "expert"
        session._profile_is_runnable = lambda _profile: True
        session._apply_active_profile = lambda: None
        session._ensure_active_profile_capabilities = lambda force_probe=False: {}
        session._persist = lambda: None
        session._emit = lambda *_args, **_kwargs: None
        session.model_catalog = lambda: {}

        records = [
            {
                "id": "reasoner",
                "capabilities": {
                    "reasoning_supported": True,
                    "reasoning_style": "openai",
                },
            }
        ]
        with mock.patch.object(cc, "probe_provider_models", return_value=records):
            cc.SessionState.set_runtime_selection(
                session,
                "vendor::reasoner",
                settings={"effort": "high", "response_stream": True},
            )

        profile = session.model_profiles["vendor"]
        self.assertNotIn("reasoning_supported", profile)
        self.assertNotIn("reasoning_style", profile)
        self.assertEqual(
            profile["model_settings"]["reasoner"],
            {
                "effort": "high",
                "response_stream": True,
                "reasoning_supported": True,
                "reasoning_style": "openai",
            },
        )

    def test_main_webui_model_management_is_wired_to_real_controls(self):
        self.assertIn('id="menuPopup" class="menu-popup is-hidden"', cc.INDEX_HTML)
        self.assertIn('id="modelManageBtn"', cc.INDEX_HTML)
        self.assertNotIn('id="applyModelBtn"', cc.INDEX_HTML)
        self.assertNotIn('id="llmConfigBtn"', cc.INDEX_HTML)
        self.assertNotIn('id="modelSettingsBtn"', cc.INDEX_HTML)
        self.assertIn("select.onchange=()=>applyModel()", cc.APP_JS)
        self.assertIn("showModelManager(manageBtn)", cc.APP_JS)
        self.assertIn("showModelSettings(anchor,option)", cc.APP_JS)
        self.assertIn("openLlmConfigModal()", cc.APP_JS)
        self.assertIn(".menu-popup.agent-model-menu", cc.APP_CSS)

    def test_model_popup_reopens_after_global_close_and_controls_align(self):
        self.assertIn("menu.classList.remove('is-hidden')", cc.APP_JS)
        self.assertIn("popup.style.display='block'", cc.APP_JS)
        self.assertIn("window.addEventListener('pageshow',bindWebModelManager)", cc.APP_JS)
        self.assertIn(".model-picker button{box-sizing:border-box", cc.APP_CSS)
        self.assertIn("height:44px;min-width:44px;min-height:44px", cc.APP_CSS)


if __name__ == "__main__":
    unittest.main()
