import pytest
from epicdoc import Doc


class TestDoc:
    def test_doc_init_no_arg(self):
        doc = Doc([])
        assert doc.selected_models == doc.models
        assert doc.selected_actions == doc.actions
        assert doc.selected_apps == doc.apps

    @pytest.mark.parametrize("model", ["client", "crm client", "add client", "add client"])
    def test_doc_init_model(self, model):
        doc = Doc([model])
        assert doc.selected_models == ["clients"]
        assert doc.selected_apps == ["crm"]

    @pytest.mark.parametrize("action", ["add", "crm add", "add client", "crm add client"])
    def test_doc_init_action(self, action):
        doc = Doc([action])
        assert doc.selected_actions == ["add"]

    def test_doc_help(self):
        doc = Doc(["help", "add"])
        assert doc.is_help
        assert list(set(doc.selected_actions)) == ["add"]

    def test_print_calls(self, mocker):
        mocker.patch('utils.prettyprints.PRR.save_report', return_value=True)
        doc = Doc(["client", "add"])



