import Clouds_Coder as cc


def test_parse_tool_arguments_basic():
    assert cc.parse_tool_arguments({"x": 1}) == {"x": 1}
    assert cc.parse_tool_arguments('{"x": 1}') == {"x": 1}
    assert cc.parse_tool_arguments("not-json") == {}


def test_normalize_work_text_status_cleanup():
    assert cc.normalize_work_text("[x] Implement feature - in_progress", "in_progress") == "Implement feature"
    assert cc.normalize_work_text("pending: Fix bug") == "Fix bug"


def test_user_id_from_ip_mapping_is_not_merged():
    assert cc.user_id_from_ip("127.0.0.1") != cc.user_id_from_ip("192.168.1.6")
    assert cc.user_id_from_ip("::ffff:127.0.0.1") == cc.user_id_from_ip("127.0.0.1")
