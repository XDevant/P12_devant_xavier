

class Colors:
    OK = '\033[0;32m'
    KO = '\033[6;31m'
    END = '\033[0m'
    HEADER = '\033[4;33m'
    METHOD = '\033[1;33m'
    URL = '\033[4;34m'

    @staticmethod
    def get(code, string):
        return getattr(Colors, code) + string + Colors.END


class PRR:
    BASE_URL = "http://127.0.0.1:8000/"
    key_mismatch = 0
    value_mismatch = 0

    @staticmethod
    def colorize(string, check):
        if check:
            string = Colors.get('OK', string)
        else:
            string = Colors.get('KO', string)
        return string

    @staticmethod
    def format(key, value):
        if "date" in key:
            value = value.split('T')[0]
            if value[-1] != 'Z':
                value += 'Z'
        if "_email" in key:
            value = value.split(':')[-1]
        if key and len(key) > 20:
            key = key[:18] + '...'
        if value and len(value) > 25:
            key = key[:23] + '...'
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
            pretty = (23 - offset) * ' ' + key + (offset - len_key) * ' ' + ' : '
            pretty += value + (23 - len_value) * ' '
        else:
            pretty = 49 * ' '
        return pretty

    @staticmethod
    def get_longest_key(list_of_key_values):
        longest = 0
        for key_value in list_of_key_values:
            longest = max(longest, len(key_value[0]))
        return longest

    @staticmethod
    def get_headers(method, display_expected):
        headers = 17 * ' '
        expect = 'Expected Result'
        if method == 'PUT':
            expect = 'Target Item'
        if method in ['POST', 'PUT']:
            headers += Colors.HEADER + 'Request  Body' + Colors.END + 35 * ' '
        if display_expected:
            headers += Colors.HEADER + expect + Colors.END + 35 * ' '
        headers += Colors.HEADER + 'Response Data' + Colors.END
        return headers

    @staticmethod
    def get_errors(k_mismatch, v_mismatch):
        string_1 = f"{k_mismatch} key error{'s' if k_mismatch > 1 else ''}. "
        total = PRR.colorize(string_1, k_mismatch == 0)
        string_2 = f"{v_mismatch} value error{'s' if v_mismatch > 1 else ''}."
        total += PRR.colorize(string_2, v_mismatch == 0)
        return total

    @staticmethod
    def get_title(method, request_url, request_logs=''):
        title = '\nRequest:  ' + Colors.get('METHOD', method) + '    '
        title += Colors.get('URL', PRR.BASE_URL + request_url) + '      '
        if request_logs:
            title += 'logs: ' + str(request_logs)
        return title + '\n'


class PrettifyPostReport(PRR):
    """The init is the workhorse of the system. It builds a list of key, value tuples
    for each column of data we want to display from the passed dicts.
    It also format the values and keys before any check, turning DateTimes into Dates.
    Finally the init calls get_pretty rows and other helpers to build every line of
    the repport.
    Args:
        request_dict: holds 3 keys: "url" is a string, "logs" a dict with the user logs
                and body, the data of the POST request.
        response_body: dict, raw response.body
    Kwargs:
        expected_response: dict expected to match the previous one, if not provided no check
                           will occur.
        mapping: a list of indexes where we want to insert a blank in the request column
                needs to be the index of the existing key so if you want the first column
                to start on line 3 mapping=[0,0]
        display_expected: bool if true the expected results will be in the middle column.
                          if false only request and response data are listed.
    """
    method = 'POST'

    def __init__(self,
                 request_dict,
                 response_body,
                 expected_response=None,
                 mapping=None,
                 display_expected=True
                 ):
        items = request_dict["body"].items()
        self.request_body = [PRR.format(key, str(val)) for key, val in items]
        self.request_url = request_dict["url"]
        self.request_logs = request_dict["logs"]
        self.expected_response = []
        if expected_response is not None:
            items = expected_response.items()
            self.expected_response = [PRR.format(k, str(v)) for k, v in items]
        items = response_body.items()
        self.response_body = [PRR.format(k, str(v)) for k, v in items]
        self.longest_key = PRR.get_longest_key(
            self.request_body + self.expected_response + self.response_body)
        if mapping is not None:
            self.mapping = sorted(mapping, reverse=True)
            for i in self.mapping:
                new = self.request_body
                self.request_body = new[:i] + [("", "")] + new[i:]
        while len(self.request_body) < max(len(self.expected_response),
                                           len(self.response_body)):
            self.request_body += [("", "")]
        while len(self.response_body) < len(self.expected_response):
            self.response_body += [("", "")]
        self.display_expected = False
        if len(self.expected_response) > 0 and display_expected:
            self.display_expected = True
        self.title = PRR.get_title(self.method,
                                   self.request_url,
                                   self.request_logs)
        self.headers = PRR.get_headers(self.method, self.display_expected)
        self.result = self.get_pretty_rows()
        self.errors = PRR.get_errors(self.key_mismatch, self.value_mismatch)

    def pretty_print(self):
        print(self.title)
        print(self.headers)
        for row in self.result:
            print(row)
        if len(self.expected_response) > 0:
            print(self.errors)

    def get_pretty_rows(self):
        """
        Builds each row with 2 (resp. 3) key_value pairs according to display_expected option
        Checks each key and each value with expected result if provided.
        Failed checks are colored in red, successfull ones in green.
        Returns the list of colored and justified rows.
        """
        result = []
        if len(self.expected_response) > 0:
            for body_row, expected_row, response_row in zip(self.request_body,
                                                            self.expected_response,
                                                            self.response_body):
                checks = (expected_row[0] == response_row[0],
                          expected_row[1] == response_row[1])

                row = PRR.prettify_key_value(*body_row, self.longest_key)
                if not checks[0] or not checks[1]:
                    if not checks[0]:
                        self.key_mismatch += 1
                    if not checks[1]:
                        self.value_mismatch += 1
                    if self.display_expected:
                        expect = PRR.prettify_key_value(*expected_row,
                                                        self.longest_key)
                        row += PRR.colorize(expect, False)
                elif self.display_expected:
                    row += PRR.prettify_key_value(*expected_row,
                                                  self.longest_key)
                else:
                    row += ''
                row += PRR.prettify_key_value(*response_row,
                                              self.longest_key,
                                              checks)
                result.append(row)
        else:
            for body_row, response_row in zip(self.request_body,
                                              self.response_body):
                row = PRR.prettify_key_value(*body_row, self.longest_key)
                row += PRR.prettify_key_value(*response_row,
                                              self.longest_key)
                result.append(row)
        return result


class PrettifyPutReport(PRR):
    """The init is the workhorse of the system. It builds a list of key, value tuples
    for each column of data we want to display from the passed dicts.
    It also format the values and keys before any check, turning DateTimes into Dates.
    Finally the init calls get_pretty rows and other helpers to build every line of
    the repport.
    Args:
        request_dict: holds 3 keys: "url" is a string, "logs" a dict with the user logs
                and 'body', the data of the POST request.
        response_body: dict, raw response.body
    Kwargs:
        expected_response: dict expected to match the previous one, if not provided, checks
                           will only occur against key values in request.
        mapping: a list of indexes where we want to insert a blank in the request column
                needs to be the index of the existing key so if you want the first column
                to start on line 3 mapping=[0,0]
        display_expected: bool if true the expected results will be in the middle column.
                          if false only request and response data are listed.
    """
    method = 'PUT'

    def __init__(self,
                 request_dict,
                 response_body,
                 expected_response=None,
                 display_expected=True
                 ):
        items = request_dict["body"].items()
        self.request_body = [PRR.format(key, str(val)) for key, val in items]
        self.request_url = request_dict["url"]
        self.request_logs = request_dict["logs"]
        self.expected_response = []
        if expected_response is not None:
            items = expected_response.items()
            self.expected_response = [PRR.format(k, str(v)) for k, v in items]
        items = response_body.items()
        self.response_body = [PRR.format(k, str(v)) for k, v in items]
        self.longest_key = PRR.get_longest_key(
            self.request_body + self.expected_response + self.response_body)
        self.display_expected = False
        if len(self.expected_response) > 0 and display_expected:
            self.display_expected = True
        self.title = PRR.get_title(self.method,
                                   self.request_url,
                                   self.request_logs)
        self.headers = PRR.get_headers(self.method, self.display_expected)
        self.result = self.get_pretty_rows()
        self.errors = PRR.get_errors(self.key_mismatch, self.value_mismatch)

    def pretty_print(self):
        print(self.title)
        print(self.headers)
        for row in self.result:
            print(row)
        print(self.errors)

    def get_pretty_rows(self):
        """
        Builds each row with 2 (resp. 3) key_value pairs according to display_expected option
        Checks each key and each value with expected result if provided.
        Failed checks are colored in red, successfull ones in green.
        Returns the list of colored and justified rows.
        """
        result = []
        data = dict(self.request_body)
        expect = dict(self.expected_response)
        body = dict(self.response_body)
        if len(self.expected_response) == 0:
            expect = body
        else:
            for key, value in body.items():
                row = ''
                if key in data.keys() and key in expect.keys():
                    check = data[key] == expect[key]
                    row += PRR.prettify_key_value(key,
                                                  data[key],
                                                  self.longest_key,
                                                  (True, check))
                    row += PRR.prettify_key_value(key,
                                                  expect[key],
                                                  self.longest_key,
                                                  (True, None))
                    row += PRR.prettify_key_value(key,
                                                  value,
                                                  self.longest_key,
                                                  (True, check))
                    if not check:
                        self.value_mismatch += 1
                    data.pop(key, None)
                    expect.pop(key, None)
                elif key in expect.keys():
                    row += ' ' * 49
                    check = expect[key] == value
                    row += PRR.prettify_key_value(key,
                                                  expect[key],
                                                  self.longest_key,
                                                  (True, check))
                    row += PRR.prettify_key_value(key,
                                                  value,
                                                  self.longest_key,
                                                  (True, check))
                    if not check:
                        self.value_mismatch += 1
                    expect.pop(key, None)
                elif key in data.keys():
                    check = data[key] == value
                    row += PRR.prettify_key_value(key,
                                                  data[key],
                                                  self.longest_key,
                                                  (False, check))
                    if not check:
                        self.value_mismatch += 1
                    expect.pop(key, None)
                    self.key_mismatch += 1
                    data.pop(key, None)
                else:
                    row += ' ' * 98
                    row += PRR.prettify_key_value(key,
                                                  value,
                                                  self.longest_key)
                result.append(row)
        for key, value in expect.items():
            row = ''
            if key in data.keys():
                check = data[key] == value
                row += PRR.prettify_key_value(key,
                                              data[key],
                                              self.longest_key,
                                              (True, check))
                row += PRR.prettify_key_value(key,
                                              value,
                                              self.longest_key,
                                              (True, check))
                if not check:
                    self.value_mismatch += 1
                data.pop(key, None)
            else:
                row += ' ' * 49
                row += PRR.prettify_key_value(key,
                                              value,
                                              self.longest_key)
                if len(self.expected_response) != 0:
                    self.key_mismatch += 1
            result.append(row)

        for key, value in data.items():
            result.append(PRR.prettify_key_value(key,
                                                 value,
                                                 self.longest_key,
                                                 (False, False)))
        return result


if __name__ == "__main__":
    request = {'status': 2,
               'contact_email': 'bi@bi.co',
               'attendees': 15,
               'event_date': '2022-08-17',
               'notes': 'bla'}
    expected = {'id': 3,
                'client_id': '1',
                'status': 'True',
                'contact_email': 'Bi Bo couriel:bi@bi.co',
                'attendees': 15, 'event_date': '2022-08-17T00:00:00Z',
                'notes': 'bla',
                'date_created': '2022-09-29T15:55:46.37Z'}
    response = {'id': 3,
                'client_id': '1',
                'status': 'True',
                'contact_email': 'Bi Bi couriel:bi@bi.co',
                'attendees': 15,
                'event_date': '2022-08-17T00:00:00Z',
                'notes': 'bla',
                'date_created': '2022-09-29T15:55:46.38Z'}
    update = {
               'contact_email': 'bi@bi.co',
               'attendees': 15,
               'event_date': '2022-08-17',
               'notes': 'bla'
    }
    request_dic = {"url": "/event/",
                   "logs": {"username": "de@de.co", "password": "xxxx"},
                   "body": request}
    update_dic = {"url": "/event/",
                  "logs": {"username": "de@de.co", "password": "xxxx"},
                  "body": update}
    report = PrettifyPostReport(request_dic, response, expected, [0, 0])
    report.pretty_print()
    report_2 = PrettifyPostReport(request_dic, expected)
    report_2.pretty_print()
    report_3 = PrettifyPostReport(request_dic, response, expected, [0, 0], display_expected=False)
    report_3.pretty_print()
    report_4 = PrettifyPutReport(update_dic, response)
    report_4.pretty_print()
    report_4 = PrettifyPutReport(update_dic, response, expected)
    report_4.pretty_print()