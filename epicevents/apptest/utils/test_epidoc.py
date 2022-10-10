import io
import sys
import pytest
from epicdoc import Doc
import epicdoc


class MockResponse:

    @staticmethod
    def print_doc(action, model, app):
        return action, model, app


class TestDoc:
    def test_doc_init_no_arg(self):
        doc = Doc([])
        assert doc.selected_models == doc.models
        assert doc.selected_actions == doc.actions
        assert doc.selected_apps == doc.apps

    @pytest.mark.parametrize("arg", ["client", "crm client", "add client", "add client"])
    def test_doc_init_model(self, arg):
        doc = Doc(arg.split(' '))
        assert list(set(doc.selected_models)) == ["clients"]
        assert list(set(doc.selected_apps)) == ["crm"]

    @pytest.mark.parametrize("arg", ["add", "crm add", "add client", "crm add client"])
    def test_doc_init_action(self, arg):
        doc = Doc(arg.split(' '))
        assert list(set(doc.selected_actions)) == ["add"]

    def test_doc_help(self):
        doc = Doc(["help", "add"])
        assert doc.is_help
        assert list(set(doc.selected_actions)) == ["add"]

    def test_print_calls_simple(self, mocker):
        mocker.patch('epicdoc.PRR', return_value=MockResponse())
        doc = Doc(["clients", "add"])
        output = io.StringIO()
        sys.stdout = output
        doc.print()
        sys.stdout = sys.__stdout__
        epicdoc.PRR.print_doc.assert_called_once_with("add", "clients", "crm")
        assert "CRM" in output.getvalue()
        assert "CLIENTS\x1b[0m:  Clients have contracts" in output.getvalue()
        assert "ADD\x1b[0m: Only members of the sales gr" in output.getvalue()
        print(output.getvalue())

    def test_print_calls_multiple_crm(self, mocker):
        mocker.patch('epicdoc.PRR', return_value=MockResponse())
        new_doc = Doc("crm events".split(' '))
        assert new_doc.selected_actions == Doc.actions
        output = io.StringIO()
        sys.stdout = output
        new_doc.print()
        sys.stdout = sys.__stdout__
        assert "CRM" in output.getvalue()
        assert "EVENTS\x1b[0m:  Events are" in output.getvalue()
        assert "ADD\x1b[0m: Only members of the sales gr" in output.getvalue()
        assert "CHANGE\x1b[0m: Only admins and" in output.getvalue()
        assert "DELETE\x1b[0m: Only super" in output.getvalue()
        assert "DETAIL\x1b[0m: Only admins," in output.getvalue()
        assert "LIST\x1b[0m: Except admin" in output.getvalue()
        assert "SEARCH\x1b[0m: Same as" in output.getvalue()
        assert "SALES\x1b[0m:" not in output.getvalue()
        print(output.getvalue())

    def test_print_calls_multiple_auth(self, mocker):
        mocker.patch('epicdoc.PRR', return_value=MockResponse())
        new_doc = Doc("user".split(' '))
        assert new_doc.selected_actions == Doc.actions
        output = io.StringIO()
        sys.stdout = output
        new_doc.print()
        sys.stdout = sys.__stdout__
        assert "AUTHENTICATION" in output.getvalue()
        assert "USERS\x1b[0m:  Users can only b" in output.getvalue()
        assert "DELETE\x1b[0m: Items in the crm" in output.getvalue()
        assert "SALES\x1b[0m:" not in output.getvalue()
        print(output.getvalue())
