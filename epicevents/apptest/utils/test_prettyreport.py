from utils.prettyprints import Report


class TestReport:
    def test_init(self):
        report = Report(url="/client/", action="list",
                        response_body={"key": "value"})
        assert report.logs == {}
        assert report.url == "/client/"
        assert report.response_body == [[("key", "value")]]
        assert report.request_body is None
        assert report.expected is None
        assert not report.display_expected
        assert not report.display_errors
        assert report.mapping == []
        assert report.method == "GET"
        assert Report(action="biz").method == "BIZ"
        assert Report(action="change").method == "PUT"
        assert Report(action="add").method == "POST"
        assert Report(action="detail").method == "GET"
        assert Report(action="search").method == "GET"


class TestPrettifyReports:
    def test_init_and_rows(self):
        report = {"url": "/client/",
                  "action": "list",
                  "response_body": {"key": "value"}}
        pretty = Report(**report)
        assert pretty.longest_key == 3
        assert 'login required' in pretty.title
        assert pretty.sum_events == 0
        assert len(pretty.result) == 2
        assert "key : value" in pretty.result[0]
        report["response_body"]["key_2"] = "value_2"
        pretty = Report(**report)
        assert pretty.response_body == [[("key", "value"),
                                         ("key_2", "value_2")]]
        assert len(pretty.result) == 3
        assert "key   : value" in pretty.result[0]
        assert "key_2 : value_2" in pretty.result[1]

        value_3 = "2222-11-11 00:00:00.001Z"
        report["response_body"]["key_date"] = value_3
        pretty = Report(**report)
        assert pretty.response_body == [[("key", "value"),
                                         ("key_2", "value_2"),
                                         ("key_date", "2222-11-11 00:00")]]
        assert "key_date : 2222-11-11 00:00" in pretty.result[2]
        assert "key_date : 2222-11-11 00:00:" not in pretty.result[2]
        print("\nChecking format and justification(single):")
        for row in pretty.result:
            if row != "\n":
                print(row)
        pretty = Report(action="list",
                        response_body=[{"key": "value"}, {"key": "value"}])
        assert pretty.response_body == [[("key", "value")],
                                        [("key", "value")]]
        print("\nChecking format and justification(list):")
        for row in pretty.result:
            if row != "\n":
                print(row)

    def test_report_factory(self):
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

        report = Report(url="/events/",
                        logs=_logs,
                        action='add',
                        request_body=_request,
                        response_body=_response,
                        expected=_expected,
                        mapping=[0, 0])
        report.print()
        assert report.sum_events == 0
        report = Report(url="/events/",
                        display_expected=True,
                        logs=_logs,
                        action='add',
                        request_body=_request,
                        response_body=_response,
                        expected=_expected,
                        mapping=[0, 0])
        report.print()
        assert report.sum_events == 0
        _response["notes"] = "blabla"
        report = Report(url="/events/3/",
                        display_expected=True,
                        display_errors=True,
                        action='change',
                        logs=_logs,
                        request_body=update,
                        response_body=_response,
                        expected=_expected)
        report.print()
        assert report.updated == 1 and report.sum_events == 1
        report = Report(url="/events/3/",
                        action='change',
                        logs=_logs,
                        request_body=update,
                        response_body=_response,
                        expected=_expected)
        report.print()
        assert report.sum_events == 1
        report = Report(url="/events/",
                        display_expected=True,
                        display_errors=True,
                        action='list',
                        response_body=[_response, _response],
                        expected=[_expected, _expected])
        report.print()
        assert report.value_errors == 2
        _expected["notes"] = "blabla"
        report = Report(url="/events/",
                        action='list',
                        response_body=[_response, _response],
                        expected=[_expected, _expected])
        report.print()
        assert report.value_errors == 0
