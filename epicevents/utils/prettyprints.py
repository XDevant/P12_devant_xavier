from pathlib import Path


BASE_DIR = str(Path(__file__).resolve().parent.parent)


class Colors:
    OK = '\033[0;32m'
    KO = '\033[6;31m'
    END = '\033[0m'
    HEADER = '\033[4;33m'
    METHOD = '\033[1;33m'
    URL = '\033[4;34m'
    UPDATED = '\033[0;33m'

    @staticmethod
    def get(code, string):
        return getattr(Colors, code) + string + Colors.END


class PRR:
    BASE_URL = "http://127.0.0.1:8000/"
    key_mismatch = 0
    value_mismatch = 0
    updated = 0

    @staticmethod
    def colorize(string, check):
        if check:
            string = Colors.get('OK', string)
        else:
            string = Colors.get('KO', string)
        return string

    @staticmethod
    def format(key, value):
        if ("date" in key or "payment_due" in key) and value != "None":
            if "T" in value:
                value = value.split('T')[0]
            else:
                value = value.split(' ')[0]
        if "contact" in key:
            value = value.split(':')[-1]
        if key and len(key) > 20:
            key = key[:18] + '...'
        if value and len(value) > 25:
            value = value[:23] + '...'
        return key, value

    @staticmethod
    def prettify_key_value(key, value, offset, checks=(None, None)):
        len_key = len(key)
        len_value = len(value)
        if key:
            if checks[0] is not None:
                key = PRR.colorize(key, checks[0])
            if checks[1] is not None:
                value = PRR.colorize(value, checks[1])
            result = (23 - offset) * ' ' + key + (offset - len_key) * ' '
            result += ' : ' + value + (23 - len_value) * ' '
        else:
            result = 49 * ' '
        return result

    @staticmethod
    def get_longest_key(list_of_key_values):
        longest = 0
        for key_value in list_of_key_values:
            longest = max(longest, len(key_value[0]))
        return longest

    @staticmethod
    def get_headers(method, display_expected, sum_events=0):
        headers = 17 * ' '
        expect = 'Expected Result'
        if method == 'PUT':
            headers += '  '
            expect = 'Target Item'
        if method in ['POST', 'PUT']:
            headers += Colors.HEADER + 'Request  Body' + Colors.END + 35 * ' '
        headers += Colors.HEADER + 'Response Data' + Colors.END + 35 * ' '
        if display_expected or sum_events != 0:
            headers += Colors.HEADER + expect + Colors.END
        return headers

    @staticmethod
    def get_errors(k_mismatch, v_mismatch, updated=0):
        string_1 = f"{k_mismatch} key error{'s' if k_mismatch > 1 else ''}. "
        total = PRR.colorize(string_1, k_mismatch == 0)
        string_2 = f"{v_mismatch} value error{'s' if v_mismatch > 1 else ''}."
        total += PRR.colorize(string_2, v_mismatch == 0)
        string_3 = f"{updated} value{'s' if updated > 1 else ''} updated."
        if updated > 0:
            string_3 += Colors.get('UPDATED', string_3)
            total += string_3
        return total

    @staticmethod
    def get_title(method, url, logs=None):
        title = 'Request:  ' + Colors.get('METHOD', method) + '   '
        title += Colors.get('URL', PRR.BASE_URL + url)
        title += ' ' * (100 - len(method) - len(PRR.BASE_URL + url))
        if logs:
            email = PRR.colorize("email", False) + '=' + logs["email"]
            password = PRR.colorize("password", False) + '=' + logs["password"]
            title += f'login: {email} {password}'
        else:
            logs += PRR.colorize('login required', False)
        return title

    @staticmethod
    def save_report(report_rows, action, model='', app='crm', mode='a'):
        if model:
            model += '\\'
        file = BASE_DIR + f'\\doc\\{app}\\{model}{action}.txt'
        with open(file, mode, encoding='cp1252') as f:
            for row in report_rows:
                print(row, file=f)

    @staticmethod
    def print_doc(action, model='', app='crm'):
        if model:
            model += '\\'
        file = BASE_DIR + f'\\doc\\{app}\\{model}{action}.txt'
        with open(file, 'r', encoding='cp1252') as f:
            for row in f:
                print(row, end='')


class Report:
    """A little helper to format the kwargs passed to the PRR subclass
    kwargs: url(string), logs(dict), method(string), request_body(dict),
                 expected(dict), response_body(dict), display_expected(bool),
                 display_errors(bool), mapping(tuple of ints)
    """
    def __init__(self, url="", logs=None, action="",
                 request_body=None,
                 expected=None,
                 response_body=None,
                 display_expected=False,
                 display_errors=False,
                 mapping=()):
        self.url = url
        if logs is None:
            logs = {}
        self.logs = logs
        self.action = action
        if self.action.lower() in ['list', 'detail', 'search']:
            self.method = 'GET'
        elif self.action.lower() == 'add':
            self.method = 'POST'
        elif self.action.lower() == 'change':
            self.method = 'PUT'
        else:
            self.method = action
        if request_body is None:
            request_body = {}
        self.request_body = request_body
        if expected is None:
            expected = {}
        self.expected = expected
        if response_body is None:
            response_body = {}
        self.response_body = response_body
        self.display_expected = display_expected
        self.display_errors = display_errors
        self.mapping = mapping


class PrettifyReport(PRR):

    def __init__(self, report):
        """
        Agr : report (Report object)
        The init is the workhorse of the system.
        It builds a list of key, value tuples for each column of data we
        want to display from the passed dicts.
        It also formats the values and keys before any check,
        turning DateTimes into Dates.
        Finally, the init calls get_pretty rows and other helpers
        to build every line of the report."""
        self.url = report.url
        self.logs = report.logs
        self.action = report.action
        self.method = report.method

        items = report.request_body.items()
        self.request_body = [self.format(k, str(v)) for k, v in items]

        if isinstance(report.expected, list):
            self.expected_response = [
                [self.format(k, str(v)) for k, v in data.items()]
                for data in report.expected]
        else:
            self.expected_response = [
                [self.format(k, str(v)) for k, v in report.expected.items()]]
        if self.expected_response:
            self.initial_data = self.expected_response[0]
        else:
            self.initial_data = self.expected_response

        if isinstance(report.response_body, list):
            self.response_body = [
                [self.format(k, str(v)) for k, v in data.items()]
                for data in report.response_body]
        else:
            items = report.response_body.items()
            self.response_body = [
                [self.format(k, str(v)) for k, v in items]]
        if self.response_body:
            self.longest_key = self.get_longest_key(
                self.request_body + self.response_body[0])
        else:
            self.longest_key = self.get_longest_key(self.request_body)
        self.display_expected = False
        if len(self.initial_data) > 0 and report.display_expected:
            self.display_expected = True
        self.display_errors = report.display_errors
        self.mapping = sorted(list(report.mapping), reverse=True)
        self.title = self.get_title(self.method,
                                    self.url,
                                    self.logs)
        self.result = self.get_pretty_rows()
        sum_events = self.key_mismatch + self.value_mismatch + self.updated
        self.headers = self.get_headers(self.method,
                                        self.display_expected,
                                        sum_events=sum_events)
        self.errors = self.get_errors(self.key_mismatch,
                                      self.value_mismatch,
                                      self.updated)
        self.report = [self.title]
        self.report += [65 * ' ' + 10 * '-', self.headers] + self.result
        if self.display_errors:
            self.report.append(self.errors + '\n')

    def get_pretty_rows(self):
        if self.method == 'POST':
            return self.get_pretty_post_rows()
        if self.method == 'PUT':
            return self.get_pretty_put_rows()
        if self.method == 'GET':
            return self.get_pretty_get_rows()
        return []

    def print(self):
        for row in self.report:
            print(row)

    def save(self, model='', app='crm', mode='a'):
        super().save_report(self.report, self.action, model, app, mode)

    def get_pretty_post_rows(self):
        """
        Builds each row with 2 (resp. 3) key_value pairs according to
        display_expected option.
        Checks each key and each value with expected result if provided.
        Failed checks are colored in red, successful ones in green.
        Returns the list of colored and justified rows.
        """
        result = []
        if self.response_body:
            self.response_body = self.response_body[0]
        self.expected_response = self.initial_data
        for index in self.mapping:
            if index < len(self.request_body):
                req = self.request_body
                self.request_body = req[:index] + [("", "")] + req[index:]

        while len(self.request_body) < max(len(self.expected_response),
                                           len(self.response_body)):
            self.request_body += [("", "")]
        while len(self.response_body) < len(self.expected_response):
            self.response_body += [("", "")]

        if len(self.expected_response) > 0:
            raw_table = zip(self.request_body,
                            self.expected_response,
                            self.response_body)
            for body_row, expected_row, response_row in raw_table:
                row = self.prettify_key_value(*body_row, self.longest_key)

                checks = (expected_row[0] == response_row[0],
                          expected_row[1] == response_row[1])
                row += self.prettify_key_value(*response_row,
                                               self.longest_key,
                                               checks)
                if not checks[0] or not checks[1]:
                    if not checks[0]:
                        self.key_mismatch += 1
                    if not checks[1]:
                        self.value_mismatch += 1
                    row += self.prettify_key_value(*expected_row,
                                                   self.longest_key,
                                                   checks)
                elif self.display_expected:
                    row += self.prettify_key_value(*expected_row,
                                                   self.longest_key,
                                                   checks)
                result.append(row)
        else:
            for body_row, response_row in zip(self.request_body,
                                              self.response_body):
                row = self.prettify_key_value(*body_row, self.longest_key)
                row += self.prettify_key_value(*response_row,
                                               self.longest_key)
                result.append(row)
        result.append(65 * ' ' + 10 * '-')
        return result

    def get_pretty_put_rows(self):
        """
        Builds each row with 2 (resp. 3) key_value pairs according to
        display_expected option as cells.
        Checks each key and each value with expected result if provided.
        Failed checks are colored in red, successful ones in green.
        Returns the list of colored and justified rows.
        """
        result = []
        request = dict(self.request_body)
        initial = dict()
        if self.initial_data:
            initial = dict(self.initial_data)
        if self.response_body:
            response = dict(self.response_body[0])
        else:
            response = dict()
        if len(self.initial_data) == 0:
            initial = response
        else:
            for key, value in response.items():
                row = ''
                if key in request.keys() and key in initial.keys():
                    check = request[key] == response[key]
                    updated = check and initial[key] != response[key]
                    row += self.prettify_key_value(key,
                                                   request[key],
                                                   self.longest_key,
                                                   (True, check))
                    row += self.prettify_key_value(key,
                                                   value,
                                                   self.longest_key,
                                                   (True, check))
                    if self.display_expected or updated or not check:
                        expected = self.prettify_key_value(key,
                                                           initial[key],
                                                           self.longest_key)
                        if updated:
                            expected = Colors.get('UPDATED', expected)
                            self.updated += 1
                        row += expected
                    if not check:
                        self.value_mismatch += 1
                    request.pop(key, None)
                    initial.pop(key, None)
                elif key in initial.keys():
                    row += ' ' * 49
                    check = initial[key] == value or key == "date_updated"
                    row += self.prettify_key_value(key,
                                                   value,
                                                   self.longest_key,
                                                   (True, check))
                    if self.display_expected:
                        row += self.prettify_key_value(key,
                                                       initial[key],
                                                       self.longest_key,
                                                       (True, check))
                    if not check:
                        self.value_mismatch += 1
                    initial.pop(key, None)
                elif key in request.keys():
                    check = request[key] == value
                    row += self.prettify_key_value(key,
                                                   request[key],
                                                   self.longest_key,
                                                   (False, check))
                    if not check:
                        self.value_mismatch += 1
                    initial.pop(key, None)
                    self.key_mismatch += 1
                    request.pop(key, None)
                else:
                    row += ' ' * 98
                    row += self.prettify_key_value(key,
                                                   value,
                                                   self.longest_key)
                result.append(row)
        for key, value in initial.items():
            row = ''
            if key in request.keys():
                check = request[key] == value
                row += self.prettify_key_value(key,
                                               request[key],
                                               self.longest_key,
                                               (True, check))
                if self.display_expected or not check:
                    row += self.prettify_key_value(key,
                                                   value,
                                                   self.longest_key,
                                                   (True, check))
                if not check:
                    self.value_mismatch += 1
                request.pop(key, None)
            else:
                row += ' ' * 49
                row += self.prettify_key_value(key,
                                               value,
                                               self.longest_key,
                                               (False, None))
                self.key_mismatch += 1
            result.append(row)

        for key, value in request.items():
            result.append(self.prettify_key_value(key,
                                                  value,
                                                  self.longest_key,
                                                  (False, False)))
        result.append(65 * ' ' + 10 * '-')
        return result

    def get_pretty_get_rows(self):
        result = []
        if not self.expected_response[0]:
            for resp in self.response_body:
                for key, value in resp:
                    result.append(self.prettify_key_value(key,
                                                          value,
                                                          self.longest_key))
                result.append("\n")
            result.append(65 * ' ' + 10 * '-')
            return result

        expects = [dict(exp) for exp in self.expected_response]
        responses = [dict(resp) for resp in self.response_body]
        for resp, expect in zip(responses, expects):
            for key, value in resp.items():
                check_1 = key in expect.keys()
                check_2 = check_1 and expect[key] == value
                row = self.prettify_key_value(key,
                                              value,
                                              self.longest_key,
                                              (check_1, check_2))
                if check_1 and (self.display_expected or not check_2):
                    row += self.prettify_key_value(key,
                                                   expect[key],
                                                   self.longest_key,
                                                   (True, check_2))
                if not check_1:
                    self.key_mismatch += 1
                if not check_2:
                    self.value_mismatch += 1
                result.append(row)
            result.append(65 * ' ' + 10 * '-')
        return result


if __name__ == "__main__":
    _request = {'status': 2,
                'contact_email': 'bi@bi.co',
                'attendees': 15,
                'event_date': '2022-08-17',
                'notes': 'bla'}
    _expected = {'id': '3',
                 'client_id': '1',
                 'status': 'True',
                 'contact_email': 'Bi Bo couriel:bi@bi.co',
                 'attendees': '15',
                 'event_date': '2022-08-17T00:00:00Z',
                 'notes': 'bla',
                 'date_created': '2022-09-29T15:55:46.37Z'}
    _response = {'id': '3',
                 'client_id': '1',
                 'status': 'True',
                 'contact_email': 'Bi Bi couriel:bi@bi.co',
                 'attendees': '15',
                 'event_date': '2022-08-17T00:00:00Z',
                 'notes': 'bla',
                 'date_created': '2022-09-29T15:55:46.38Z'}
    update = {
               'contact_email': 'bi@bi.co',
               'attendees': 15,
               'event_date': '2022-08-17',
               'notes': 'blabla'
    }
    _logs = {"email": "de@de.co", "password": "xxxx"}

    report_1 = PrettifyReport(Report(url="/events/",
                                         logs=_logs,
                                         action='add',
                                         request_body=_request,
                                         response_body=_response,
                                         expected=_expected,
                                         mapping=[0, 0]))
    report_1.print()
    report_1 = PrettifyReport(Report(url="/events/",
                                     display_expected=True,
                                     logs=_logs,
                                     action='add',
                                     request_body=_request,
                                     response_body=_response,
                                     expected=_expected,
                                     mapping=[0, 0]))
    report_1.print()
    _response["notes"] = "blabla"
    report_1 = PrettifyReport(Report(url="/events/3/",
                                     display_expected=True,
                                     display_errors=True,
                                     action='change',
                                     logs=_logs,
                                     request_body=update,
                                     response_body=_response,
                                     expected=_expected))
    report_1.print()
    report_1 = PrettifyReport(Report(url="/events/3/",
                                     action='change',
                                     logs=_logs,
                                     request_body=update,
                                     response_body=_response,
                                     expected=_expected))
    report_1.print()
    report_1 = PrettifyReport(Report(url="/events/",
                                     display_expected=True,
                                     display_errors=True,
                                     action='list',
                                     logs=_logs,
                                     response_body=[_response, _response],
                                     expected=[_expected, _expected]))
    report_1.print()
    report_1 = PrettifyReport(Report(url="/events/",
                                     action='list',
                                     logs=_logs,
                                     response_body=[_response, _response],
                                     expected=[_expected, _expected]
                                     ))
    report_1.print()
    # PRR.save_report(report_5.report, "change", model="event")
    # PRR.print_doc("change", model="event")
