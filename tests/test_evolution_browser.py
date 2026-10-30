"""Browser behavior against the real Admin API and local HTTP model service."""
import os
import unittest
from urllib.parse import urlparse

import test_evolution_integration as integration

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None


def browser_executable(pw):
    selected = os.environ.get("EVOLUTION_BROWSER_EXECUTABLE")
    if selected:
        return selected
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.isfile(chrome):
        return chrome
    if not os.path.isfile(pw.chromium.executable_path):
        raise unittest.SkipTest("Chromium binary unavailable; CI installs it explicitly")
    return None


@unittest.skipUnless(sync_playwright, 'Playwright unavailable in this Python environment')
class EvolutionBrowserTests(unittest.TestCase):
    def test_editor_polling_save_run_conflict_and_errors(self):
        fixture = integration.EvolutionHTTPTests()
        fixture.setUp()
        try:
            fixture.model_server.mode = 'no_change'
            fixture.app.global_profiles['disabled-profile'] = {**fixture.app.global_profiles['gen'], 'enabled': False}
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True, executable_path=browser_executable(pw))
                page = browser.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                # Only unrelated initial admin requests are stubbed. Evolution
                # and its model calls go through both actual HTTP servers.
                def route(request):
                    path = urlparse(request.request.url).path
                    if path.startswith('/api/admin/evolution'):
                        request.continue_()
                    elif path == '/api/admin/auth/status':
                        request.fulfill(json={'setup_required': False, 'password_login_enabled': True, 'token_login_enabled': True})
                    elif path == '/api/admin/language':
                        request.fulfill(json={'language': 'zh-CN'})
                    else:
                        request.fulfill(json={})
                page.route('**/api/**', route)
                page.goto('http://127.0.0.1:' + str(fixture.server.server_port) + '/admin')
                page.wait_for_function("typeof A !== 'undefined'")
                page.evaluate("A.token='test-admin';setAuthenticated(true);switchView('evolution')")
                page.wait_for_function("A.evolutionModels && A.evolutionDraft")
                self.assertEqual(page.locator('#evolutionGeneratorProfile').evaluate('(el)=>el.tagName'), 'SELECT')
                self.assertIn('未登录 IDE', page.locator('#evolutionModelSources').inner_text())
                self.assertTrue(page.locator('#runEvolutionBtn').is_disabled())
                options = page.evaluate('A.evolutionModels.options')
                # select_option() can set a disabled option programmatically;
                # also check native DOM state and keyboard type-ahead selection.
                for index, option in enumerate(options):
                    element = page.locator(f'#evolutionGeneratorProfile option[value="{index}"]')
                    self.assertEqual(element.evaluate('(el)=>el.disabled'), not option['available'])
                    self.assertIn(option['model'], element.text_content())
                    if option['available']:
                        self.assertIsNone(element.get_attribute('disabled'))
                    else:
                        self.assertIn('已停用', element.text_content())
                page.focus('#evolutionGeneratorProfile')
                # Type-ahead works with native selects in headless macOS;
                # OS popup menus cannot be navigated there with arrow keys.
                page.keyboard.press('[')
                page.keyboard.press('Tab')
                self.assertTrue(options[int(page.input_value('#evolutionGeneratorProfile'))]['available'])
                self.assertTrue(page.evaluate('A.evolutionDirty'))
                gen = next(str(i) for i, o in enumerate(options) if o['ref']['profile_id'] == 'gen' and o['model'] == 'selected-model')
                judge = next(str(i) for i, o in enumerate(options) if o['ref']['profile_id'] == 'judge' and o['model'] == 'selected-model')
                page.select_option('#evolutionMode', 'Thinking')
                self.assertEqual(page.input_value('#evolutionTaskCount'), '4')
                self.assertEqual(page.input_value('#evolutionTaskRounds'), '200')
                self.assertEqual(page.locator('#evolutionTaskBenchmarks').count(), 0)
                page.fill('#evolutionTaskCount', '2')
                self.assertTrue(page.locator('#evolutionTaskRounds').evaluate('(el) => el.readOnly'))
                page.select_option('#evolutionGeneratorProfile', gen)
                page.select_option('#evolutionJudgeProfile', judge)
                page.fill('#evolutionTimezone', 'UTC')
                page.fill('#evolutionHistoryDepth', '0')
                page.fill('#evolutionStartDate', '2026-09-01')
                page.fill('#evolutionUserScope', 'test-owner')
                self.assertIn('未保存', page.locator('#evolutionRevision').inner_text())
                page.evaluate('loadEvolution()')
                self.assertEqual(page.input_value('#evolutionMode'), 'Thinking')
                self.assertEqual(page.input_value('#evolutionGeneratorProfile'), gen)
                self.assertEqual(page.input_value('#evolutionTimezone'), 'UTC')
                self.assertEqual(page.input_value('#evolutionHistoryDepth'), '0')
                self.assertEqual(page.input_value('#evolutionStartDate'), '2026-09-01')
                self.assertEqual(page.input_value('#evolutionUserScope'), 'test-owner')
                self.assertEqual(page.input_value('#evolutionTaskCount'), '2')
                self.assertEqual(page.input_value('#evolutionTaskRounds'), '200')
                # This existing interaction fixture serves the contract-only
                # backend; task-driven real HTTP rollouts have a separate test.
                self.assertTrue(page.locator('#runEvolutionBtn').is_disabled())
                page.click('#saveEvolutionBtn')
                page.wait_for_function('!A.evolutionBusy && !A.evolutionDirty')
                saved = fixture.app.liquid_kernel.config()['task_benchmark']
                self.assertTrue(saved['enabled'])
                self.assertEqual((saved['max_tasks'], saved['max_rounds']), (2, 200))
                self.assertFalse(page.locator('#runEvolutionBtn').is_disabled())
                # Hold the request response so a second click is observable.
                fixture.model_server.release.clear()
                page.evaluate('Promise.all([runEvolution(),runEvolution()])')
                self.assertEqual(fixture.app.liquid_kernel.registry.list_runs()['total'], 1)
                self.assertTrue(page.locator('#runEvolutionBtn').is_disabled())
                fixture.model_server.release.set()
                page.wait_for_function("A.evolution?.runs?.runs?.[0]?.status === 'no_change'", timeout=20000)
                page.fill('#evolutionSessionScope', 'unsaved-session')
                base = fixture.app.liquid_kernel.config()
                fixture.app.liquid_kernel.save_config({'timezone': 'Asia/Shanghai'}, base['revision'])
                page.evaluate('loadEvolution()')
                self.assertEqual(page.input_value('#evolutionSessionScope'), 'unsaved-session')
                self.assertIn('配置已被其他页面修改', page.locator('#evolutionPolicyNote').inner_text())
                self.assertTrue(page.locator('#saveEvolutionBtn').is_disabled())
                page.once('dialog', lambda dialog: dialog.accept())
                page.click('#reloadEvolutionConfigBtn')
                page.wait_for_function('!A.evolutionDirty && A.evolutionDraft.revision === A.evolution.config.revision')
                fixture.app.global_profiles['gen']['api_key'] = 'changed-key'
                page.click('#runEvolutionBtn')
                page.wait_for_function("A.evolutionError.includes('configuration changed')")
                self.assertIn('configuration changed', page.locator('#evolutionPolicyNote').inner_text())
                self.assertEqual(errors, [])
                browser.close()
        finally:
            fixture.tearDown()

    def test_toolbar_and_long_model_names_fit_desktop_and_mobile(self):
        fixture = integration.EvolutionHTTPTests()
        fixture.setUp()
        try:
            long_model = 'vendor/' + 'long-context-reasoning-model-' * 8
            fixture.app.global_profiles['long-profile'] = {
                **fixture.app.global_profiles['gen'], 'model': long_model, 'models': [long_model]}
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True, executable_path=browser_executable(pw))
                page = browser.new_page(viewport={'width': 1440, 'height': 1100})
                def route(request):
                    path = urlparse(request.request.url).path
                    if path.startswith('/api/admin/evolution'):
                        request.continue_()
                    elif path == '/api/admin/auth/status':
                        request.fulfill(json={'setup_required': False, 'password_login_enabled': True, 'token_login_enabled': True})
                    elif path == '/api/admin/language':
                        request.fulfill(json={'language': 'zh-CN'})
                    else:
                        request.fulfill(json={})
                page.route('**/api/**', route)
                page.goto('http://127.0.0.1:' + str(fixture.server.server_port) + '/admin')
                page.wait_for_function("typeof A !== 'undefined'")
                page.evaluate("A.token='test-admin';setAuthenticated(true);switchView('evolution')")
                page.wait_for_function('A.evolutionModels && A.evolutionDraft')
                options = page.evaluate('A.evolutionModels.options')
                value = next(str(i) for i, row in enumerate(options) if row['model'] == long_model)
                page.select_option('#evolutionGeneratorProfile', value)
                page.fill('#evolutionTimezone', 'UTC')
                for language in ('zh-CN', 'en'):
                    page.evaluate('(language)=>applyAdminLanguage(language)', language)
                    self.assertIn('Global models' if language == 'en' else '全局模型',
                                  page.locator('#evolutionModelSources').inner_text())
                    self.assertEqual(page.input_value('#evolutionTimezone'), 'UTC')
                    self.assertTrue(page.evaluate('A.evolutionDirty'))
                    for width in (1440, 1280, 1024, 768, 390, 320):
                        with self.subTest(language=language, width=width):
                            page.set_viewport_size({'width': width, 'height': 1100})
                            geometry = page.evaluate("""() => {
                                const rect = el => el.getBoundingClientRect().toJSON();
                                return {viewport:innerWidth,pageWidth:document.documentElement.scrollWidth,
                                    card:rect(document.querySelector('.evolution-settings')),
                                    primary:[...document.querySelectorAll('.evolution-actions button')].map(rect),
                                    secondary:[...document.querySelectorAll('.evolution-secondary-actions button')].map(rect),
                                    controls:[...document.querySelectorAll('.evolution-form-grid input,.evolution-form-grid select')].map(rect),
                                    nav:[...document.querySelectorAll('.admin-nav .nav-tab')].map(rect),
                                    checkbox:rect(E('evolutionEventTriggers')),
                                    switch:rect(E('evolutionEventTriggers').parentElement)};
                            }""")
                            self.assertLessEqual(geometry['pageWidth'], width + 1)
                            self.assertLess(max(tab['height'] for tab in geometry['nav']), 50)
                            card = geometry['card']
                            for box in geometry['primary'] + geometry['secondary'] + geometry['controls']:
                                self.assertGreaterEqual(box['left'], card['left'])
                                self.assertLessEqual(box['right'], card['right'] + 1)
                            primary, secondary = geometry['primary'], geometry['secondary']
                            self.assertAlmostEqual(primary[0]['top'], primary[1]['top'], delta=1)
                            self.assertAlmostEqual(primary[0]['height'], primary[1]['height'], delta=1)
                            self.assertAlmostEqual(primary[0]['width'], primary[1]['width'], delta=1)
                            if width > 480:
                                self.assertAlmostEqual(primary[0]['top'], primary[2]['top'], delta=1)
                            else:
                                self.assertGreaterEqual(primary[2]['top'] - primary[0]['bottom'], 7)
                            self.assertGreaterEqual(secondary[0]['top'] - max(row['bottom'] for row in primary), 9)
                            self.assertAlmostEqual(secondary[0]['top'], secondary[1]['top'], delta=1)
                            self.assertAlmostEqual(geometry['checkbox']['left'], geometry['switch']['left'], delta=1)
                            self.assertEqual(page.input_value('#evolutionGeneratorProfile'), value)
                            self.assertIn(long_model, page.locator('#evolutionGeneratorProfile').get_attribute('title'))
                screenshot_dir = os.environ.get('EVOLUTION_SCREENSHOT_DIR')
                if screenshot_dir:
                    from pathlib import Path
                    folder = Path(screenshot_dir)
                    folder.mkdir(parents=True, exist_ok=True)
                    page.evaluate("applyAdminLanguage('zh-CN')")
                    for width in (1280, 390):
                        page.set_viewport_size({'width': width, 'height': 1100})
                        page.screenshot(path=str(folder / f'evolution-{width}.png'), full_page=True)
                browser.close()
        finally:
            fixture.tearDown()


if __name__ == '__main__':
    unittest.main()
