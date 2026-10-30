import json
import subprocess
import types
import unittest

import Clouds_Coder as cc


class AdminLanguagePayloadTests(unittest.TestCase):
    def test_admin_language_uses_shared_webui_user_preference(self):
        manager = types.SimpleNamespace(user_language="ja")
        payload = cc.admin_language_payload(manager)
        self.assertEqual(payload["language"], "ja")
        self.assertEqual(payload["default_language"], "ja")
        self.assertEqual(payload["source"], "webui_user_preference")
        self.assertTrue(payload["sync_with_webui"])
        self.assertEqual(
            [row["code"] for row in payload["supported_languages"]],
            ["zh-CN", "zh-TW", "ja", "en"],
        )

    def test_admin_language_falls_back_without_loading_sessions(self):
        class Manager:
            user_language = "unsupported"

            @property
            def sessions(self):
                raise AssertionError("language lookup must not inspect sessions")

        payload = cc.admin_language_payload(Manager())
        self.assertEqual(payload["language"], cc.DEFAULT_UI_LANGUAGE)


class AdminI18nAssetTests(unittest.TestCase):
    def test_score_comparison_renders_historical_zero_without_invented_reviews(self):
        renderer = cc.ADMIN_JS.split('function renderEvolutionRunDetail(detail){', 1)[1].split('\nconst EVOLUTION_PIPELINE=', 1)[0]
        script = r'''
const A={},elements={};
function node(tag,attrs={},text=''){return {tag,text,children:[],classList:{remove(){}},appendChild(x){this.children.push(x)},append(...xs){this.children.push(...xs)},replaceChildren(){this.children=[]}}}
function E(id){return elements[id]??=node('div')}
function renderEvolutionProgress(){}
function evolutionText(x){return x}
function evolutionReason(x){return x}
function renderEvolutionRunDetail(detail){
''' + renderer + r'''
renderEvolutionRunDetail({run_id:'old-rejection',result:{evaluations:[{code:'patch_too_large'}]},score_summary:{
  incumbent:{hard:0},evaluations:[{candidate_index:1,code:'patch_too_large',incumbent:{hard:0},
  candidate:{mixed:0,score_status:'validation_failed',task_execution_measured:false}}]}});
const panel=E('evolutionDetail').children.find(n=>n.children.some(c=>c.tag==='table'));
const table=panel.children.find(n=>n.tag==='table');
console.log(JSON.stringify({rows:table.children.map(n=>n.children.map(c=>c.text)),notices:panel.children.filter(c=>c.tag==='p').map(c=>c.text)}));
'''
        completed = subprocess.run(['node', '-e', script], check=True, capture_output=True, text=True)
        rendered = json.loads(completed.stdout)
        self.assertEqual(rendered['rows'][1], ['Baseline', '0.0', 'Not scored', 'Not scored'])
        self.assertEqual(rendered['rows'][2], ['Candidate', 'Not scored', 'Not scored', '0.0'])
        self.assertTrue(any('were not performed' in notice for notice in rendered['notices']))

    def test_new_quota_deployment_and_score_labels_have_all_translations(self):
        prefix = cc.ADMIN_JS.split('const ADMIN_TEXT_SOURCE', 1)[0]
        labels = ['Unlimited', 'Score comparison', 'Not scored', 'Scoring baseline', '部署方式', '单任务 Token 配额（0=不限）', '补丁修改行数上限（0=不限）']
        script = "global.sessionStorage={getItem:()=>''};global.document={getElementById:()=>null};\n" + prefix
        script += '\nconsole.log(JSON.stringify(' + json.dumps(labels, ensure_ascii=False) + '.map(s=>[s,...["zh-CN","zh-TW","ja","en"].map(l=>adminTranslate(s,l))])));'
        completed = subprocess.run(['node', '-e', script], check=True, capture_output=True, text=True)
        for row in json.loads(completed.stdout):
            self.assertTrue(all(row))
            self.assertNotEqual(row[3], row[0], row)

    def test_admin_page_has_language_controls_in_shell_and_login(self):
        self.assertIn('id="adminLanguageSelect"', cc.ADMIN_INDEX_HTML)
        self.assertIn('id="adminLoginLanguageSelect"', cc.ADMIN_INDEX_HTML)
        for language in ("zh-CN", "zh-TW", "ja", "en"):
            self.assertGreaterEqual(
                cc.ADMIN_INDEX_HTML.count(f'value="{language}"'), 2
            )

    def test_admin_i18n_covers_static_dynamic_and_config_content(self):
        required = (
            "ADMIN_I18N_ROWS",
            "ADMIN_CONFIG_I18N_ROWS",
            "ADMIN_DYNAMIC_I18N_ROWS",
            "MutationObserver",
            "applyAdminI18n",
            "translateAdminTextNode",
            "translateAdminAttributes",
            "loadAdminLanguage",
            "saveAdminLanguage",
            "'/api/admin/language'",
            "Synced with WebUI language",
            "WebUI のユーザー言語と同期",
            "與 WebUI 使用者語言同步",
        )
        for marker in required:
            self.assertIn(marker, cc.ADMIN_JS)
        for mode in ("Off", "Tuning", "Thinking", "Aggressive"):
            self.assertIn(f'<option value="{mode}">{mode}</option>', cc.ADMIN_INDEX_HTML)

    def test_admin_translation_runtime_switches_representative_text(self):
        prefix = cc.ADMIN_JS.split("const ADMIN_TEXT_SOURCE", 1)[0]
        script = "global.sessionStorage={getItem:()=>''};global.document={getElementById:()=>null};\n" + prefix + "\n" + "console.log(JSON.stringify({" + \
            "en:[adminTranslate('运行统计','en'),adminTranslate('Bind host','en'),adminTranslate('紧急中止','en')]," + \
            "ja:[adminTranslate('运行统计','ja'),adminTranslate('Bind host','ja'),adminTranslate('紧急中止','ja')]," + \
            "tw:[adminTranslate('运行统计','zh-TW'),adminTranslate('Bind host','zh-TW'),adminTranslate('紧急中止','zh-TW')]" + \
            "}));"
        completed = subprocess.run(
            ["node", "-e", script],
            check=True,
            capture_output=True,
            text=True,
        )
        translated = json.loads(completed.stdout)
        self.assertEqual(translated["en"], ["Metrics", "Bind host", "Emergency abort"])
        self.assertEqual(translated["ja"], ["稼働統計", "バインドホスト", "緊急中止"])
        self.assertEqual(translated["tw"], ["執行統計", "繫結主機", "緊急中止"])

    def test_admin_language_routes_are_lightweight_and_bidirectional(self):
        source = open(cc.__file__, encoding="utf-8").read()
        self.assertGreaterEqual(source.count('if path == "/api/admin/language":'), 2)
        self.assertIn("admin_language_payload(self._session_mgr())", source)
        self.assertIn("self._session_mgr().set_user_language(language)", source)


if __name__ == "__main__":
    unittest.main()
