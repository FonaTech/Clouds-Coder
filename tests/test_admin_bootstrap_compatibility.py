"""Real Chromium regressions; emulate older Edge without structuredClone."""

import json
import os
import re
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import Clouds_Coder as cc
from liquid_kernel import normalize_evolution_config

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None


@unittest.skipUnless(
    sync_playwright, "Playwright unavailable in this Python environment"
)
class AdminBootstrapCompatibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        requested = os.environ.get("EVOLUTION_BROWSER_EXECUTABLE")
        mac_chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if not requested and not os.path.isfile(mac_chrome):
            with sync_playwright() as probe:
                if not os.path.isfile(probe.chromium.executable_path):
                    raise unittest.SkipTest("Chromium binary unavailable; CI installs it explicitly")
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def do_GET(self):
                if self.path.split("?")[0].endswith(".js"):
                    content, kind = cc.ADMIN_JS, "application/javascript"
                else:
                    content, kind = cls.html, "text/html"
                body = content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", kind + "; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        cls.html = cc.ADMIN_INDEX_HTML
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.playwright = sync_playwright().start()
        executable = os.environ.get("EVOLUTION_BROWSER_EXECUTABLE")
        if not executable and os.path.isfile(
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ):
            executable = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        cls.browser = cls.playwright.chromium.launch(
            headless=True, executable_path=executable
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def page(self, missing=None, offline=False, hanging=False):
        page = self.browser.new_page()
        self.addCleanup(page.close)
        self.__class__.html = cc.ADMIN_INDEX_HTML
        if missing:
            self.__class__.html = self.html.replace(
                'id="' + missing + '"', 'id="removed-' + missing + '"'
            )
        page.add_init_script(
            "globalThis.structuredClone=undefined;localStorage.clear();sessionStorage.clear();"
        )
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        def route(request):
            endpoint = request.request.url.split("?", 1)[0]
            if endpoint.endswith("/api/admin/language"):
                request.fulfill(json={"language": "zh-CN"})
            elif endpoint.endswith("/api/admin/auth/status"):
                if offline:
                    request.abort("internetdisconnected")
                else:
                    request.fulfill(
                        json={
                            "setup_required": False,
                            "password_login_enabled": True,
                            "token_login_enabled": True,
                        }
                    )
            else:
                request.fulfill(json={})

        page.route("**/api/admin/**", route)
        if hanging:
            page.add_init_script(
                """const originalFetch=window.fetch.bind(window);window.fetch=(url,opt)=>String(url).includes('/api/admin/auth/')?new Promise(()=>{}):originalFetch(url,opt);const originalTimeout=window.setTimeout;window.setTimeout=(callback,delay,...args)=>originalTimeout(callback,delay===15000?20:delay,...args);"""
            )
        page.goto("http://127.0.0.1:" + str(self.server.server_port) + "/admin")
        return page, errors

    def test_real_login_bootstrap_and_config_edit_without_structured_clone(self):
        page, errors = self.page()
        page.wait_for_function("!E('passwordLoginForm').classList.contains('hidden')")
        cfg = normalize_evolution_config({"mode": "Thinking"})
        page.evaluate(
            "(cfg)=>{A.evolution={config:cfg};fillEvolutionForm(cfg);evolutionControls()}",
            cfg,
        )
        result = page.evaluate(
            """()=>{const clone=cloneAdminConfig(A.evolutionDraft);clone.task_benchmark.max_tasks=99;return{fields:EVOLUTION_FIELDS.map(field=>[field,!!E('evolution'+field)]),isolated:A.evolutionDraft.task_benchmark.max_tasks!==99,passwordHandler:typeof E('passwordLoginForm').onsubmit,cloneMissing:typeof structuredClone}}"""
        )
        self.assertTrue(all(exists for _, exists in result["fields"]), result)
        self.assertTrue(result["isolated"])
        self.assertEqual(result["passwordHandler"], "function")
        self.assertEqual(result["cloneMissing"], "undefined")
        page.evaluate(
            "E('evolutionTaskTokens').value='1234';E('evolutionTaskTokens').dispatchEvent(new Event('input',{bubbles:true}))"
        )
        self.assertTrue(page.evaluate("A.evolutionDirty"))
        self.assertFalse(errors, errors)

    def test_missing_optional_evolution_field_does_not_block_auth(self):
        page, errors = self.page(missing="evolutionTimezone")
        page.wait_for_function("!E('passwordLoginForm').classList.contains('hidden')")
        self.assertEqual(
            page.evaluate("typeof E('tokenLoginForm').onsubmit"), "function"
        )
        self.assertFalse(errors, errors)

    def test_no_change_is_not_a_new_candidate_and_model_prose_is_not_partially_translated(self):
        page, errors = self.page()
        page.wait_for_function("!E('passwordLoginForm').classList.contains('hidden')")
        reason = 'Changes to context, prompting, recovery, or tool routing would be speculative.'
        score = {'hard': 98, 'soft': 90, 'mixed': 91.6}
        detail = {'run_id': 'no-change-view', 'status': 'no_change', 'result': {'evaluations': [
            {'decision': 'no_change', 'incumbent': score, 'candidate': {**score, 'same_version': True}, 'reason': reason}]}}
        page.evaluate('(detail)=>renderEvolutionRunDetail(detail)', detail)
        text = page.locator('#evolutionDetail').inner_text()
        self.assertIn(reason, text)
        self.assertNotIn('con文本', text)
        self.assertIn('同一内核（未修改）', text)
        self.assertNotIn('候选 1', text)
        self.assertFalse(errors, errors)

    def test_rejected_real_candidate_displays_version_and_actual_scores(self):
        page, errors = self.page()
        page.wait_for_function("!E('passwordLoginForm').classList.contains('hidden')")
        detail = {'status': 'rejected', 'score_summary': {'evaluations': [
            {'candidate_index': 1, 'candidate_version': 'kernel-0002-retained-example', 'decision': 'reject',
             'incumbent': {'hard': 98, 'soft': 90, 'mixed': 91.6},
             'candidate': {'hard': 85, 'soft': 80, 'mixed': 80.5}, 'reason': 'Independent paired confirmation failed'}]}}
        page.evaluate('detail=>renderEvolutionRunDetail(detail)', detail)
        content = page.locator('#evolutionDetail').inner_text()
        self.assertIn('kernel-0002-retained-example', content)
        self.assertIn('85.0', content)
        self.assertIn('98.0', content)
        self.assertNotIn('同一内核', content)
        self.assertFalse(errors, errors)

    def test_unrelated_binding_failure_cannot_remove_login_handlers(self):
        page, errors = self.page(missing="refreshMetricsBtn")
        page.wait_for_function("!E('passwordLoginForm').classList.contains('hidden')")
        self.assertEqual(
            page.evaluate("typeof E('passwordLoginForm').onsubmit"), "function"
        )
        self.assertFalse(errors, errors)

    def test_offline_auth_has_actionable_retry_instead_of_waiting_forever(self):
        page, errors = self.page(offline=True)
        page.wait_for_function("!E('retryAuthBtn').classList.contains('hidden')")
        self.assertIn("不可用", page.locator("#authTitle").inner_text())
        self.assertFalse(errors, errors)

    def test_auth_service_never_responds_is_bounded(self):
        page, errors = self.page(hanging=True)
        page.wait_for_function("!E('retryAuthBtn').classList.contains('hidden')")
        self.assertIn("不可用", page.locator("#authTitle").inner_text())
        self.assertFalse(errors, errors)


class AdminFieldContract(unittest.TestCase):
    def test_editable_fields_exist_in_markup(self):
        match = re.search(r"const EVOLUTION_FIELDS=(\[[^;]*\]);", cc.ADMIN_JS)
        fields = json.loads(match[1].replace("'", '"'))
        for field in fields:
            self.assertIn('id="evolution' + field + '"', cc.ADMIN_INDEX_HTML)
        self.assertNotIn("ControlReserve", fields)
        self.assertIn("PatchLines", fields)
        self.assertIn("DeploymentPolicy", fields)
