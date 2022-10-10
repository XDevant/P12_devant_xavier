import io
import sys
import pytest
from utils.prettyprints import PRR, Colors, BASE_DIR


class TestColors:
    def test_colors(self):
        assert Colors.END == "\x1b[0m"

    def test_colors_get(self):
        string = Colors.get('OK', 'bla')
        print(f"\nChecking if {string} is green.    ", end='')
        assert string == Colors.OK + 'bla' + Colors.END


class TestPRR:
    def test_colorize(self):
        string = PRR.colorize("bla", True)
        print(f"\nChecking if {string} is green.    ", end='')
        assert len(string.split('\033[0;32m')) == 2
        string = PRR.colorize("bla", False)
        print(f"Checking if {string} is red.    ", end='')
        assert len(string.split('\033[6;31m')) == 2

    def test_format(self):
        date = "date_abcdefghijklmnopqrstuvwxyz"
        key, value = PRR.format(date, "1211-11-01 23:13")
        assert value == "1211-11-01" and len(key) == 21
        key, value = PRR.format("contact_email", "dbd: dd@f.c")
        assert value == "dd@f.c"

    def test_prettify_key_value(self):
        pretty = PRR.prettify_key_value("key", "value", 10, (None, None))
        assert pretty == 13 * ' ' + "key" + 7 * ' ' + ' : ' + "value" + 18 * ' '
        pretty = PRR.prettify_key_value("key", "value", 10, (True, False))
        print(f"\nChecking if key is green and value red:{pretty}", end='')
        assert len(pretty.split('\033[6;31m')) == 2
        assert len(pretty.split('\033[0;32m')) == 2

    def test_get_longest_key(self):
        keys = [("key", "value"), ("very_long_key", "13"), ("key", "value")]
        assert PRR.get_longest_key(keys) == len("very_long_key")

    def test_get_title(self):
        title = PRR.get_title("GET", "api", {"email": "a@a.c"})
        url = PRR.BASE_URL + "api"
        assert Colors.METHOD + "GET" in title and Colors.URL + url in title
        assert 'login required' in title
        title = PRR.get_title("GET", "api", {"email": "a@a.c",
                                             "password": "mdp"})
        print(f"Checking title holds method, url and logs:\n{title} ", end='')
        assert 'login required' not in title and "a@a.c" in title

    @pytest.mark.parametrize("method, check, columns", [("GET", True, 2),
                                                        ("GET", False, 1),
                                                        ("POST", False, 2),
                                                        ("PUT", False, 2),
                                                        ("POST", True, 3),
                                                        ("PUT", True, 3)])
    def test_get_headers(self, method, check, columns):
        headers = PRR.get_headers(method, check)
        assert len(headers.split(Colors.HEADER)) == columns + 1
        print(f"\nChecking if headers contains {columns} headers    ", end='')
        if method in ["POST", "PUT"]:
            assert 'Request' in headers
        else:
            assert 'Request' not in headers
        if check:
            if method == "PUT":
                assert 'Target' in headers
            else:
                assert 'Expected' in headers
        else:
            assert 'Expected' not in headers

    def test_get_errors(self):
        errors = PRR.get_errors(0, 0)
        assert "0 key error." in errors
        assert "0 value error." in errors
        assert "updated" not in errors

        errors = PRR.get_errors(0, 2, 1)
        assert "0 key error." in errors
        assert "2 value errors." in errors
        assert "updated" in errors
        print(f"\nChecking if {errors} is Green Red Yellow. ", end='')
        assert len(errors.split(Colors.OK)) == 2
        assert len(errors.split(Colors.KO)) == 2
        assert len(errors.split(Colors.UPDATED)) == 2

    def test_print_save_report(self):
        PRR.save_report(["bla"], "test", model="", app="test", mode='w')
        output = io.StringIO()
        sys.stdout = output
        PRR.print_doc("test", model="", app="test")
        sys.stdout = sys.__stdout__
        out = output.getvalue()
        print(f"\nSaving 'bla' as report and loading file, find: {out}",
              end='')
        assert "bla\n" == out
