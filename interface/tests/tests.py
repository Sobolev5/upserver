import pytest
import logging
from pathlib import Path
from log_collector.models import AnyLogger, DjangoLogger, \
                                 DjangoException, NginxLogger


@pytest.mark.django_db
def test_catch_any_logger():
    # pytest tests/tests.py::test_catch_any_logger -rP
    
    row = {'payload': {'hello': 'world'}, 
            'tag': 'throwed', 
            'routing_key': 'any_logger', 
            'ttl': 180, 
            'filename': 'main/views.py', 
            'function_name': 'profile', 
            'lineno': 119, 
            'send_datetime': '2023-03-16 07:00:00'
    }

    AnyLogger.save_record(row=row)

 
@pytest.mark.django_db
def test_django_logger():
    # pytest tests/tests.py::test_django_logger -rP

    row = {
        "payload":{
            "uuid":"MkDQs68KmPtBFhFESFzGSu",
            "asctime":"2023-03-16T06:55:46.280989",
            "exc_info":"Traceback (most recent call last):\n  File \"/test/env/lib/python3.10/site-packages/django/core/handlers/exception.py\", line 55, in inner\n    response = get_response(request)\n  File \"/test/env/lib/python3.10/site-packages/django/core/handlers/base.py\", line 197, in _get_response\n    response = wrapped_callback(request, *callback_args, **callback_kwargs)\n  File \"/test/apps/userprofiles/decorators.py\", line 158, in inner_decorator\n    return function(request, *args, **kwargs)\n  File \"/test/apps/main/views.py\", line 119, in profile\n    throw(payload=payload, uri=COLLECTOR_AMQP_URI, routing_key=\"any_logger\", ttl=ttl)\nNameError: name \\'payload\\' is not defined",
            "exc_hash":"3157411c4f4ef84636501424d4e23b0d",
            "user":"Sobolev Andrej",
            "user_id":315,
            "request_extra":"<user_sessions.backends.db.SessionStore object at 0x7fe2fd263220>",
            "site":"dev1:11001",
            "scheme":"http",
            "body":"b''",
            "path":"/profile/",
            "method":"GET",
            "GET":"<QueryDict: {'any_throw': ['']}>",
            "POST":"<QueryDict: {}>",
            "headers":"{\\'Content-Length\\': \\'\\', \\'Content-Type\\': \\'text/plain\\', \\'Host\\': \\'dev1\\', \\'X-Real-Ip\\': \\'95.179.122.214\\', \\'X-Forwarded-For\\': \\'95.179.122.214\\', \\'Connection\\': \\'close\\', \\'Cache-Control\\': \\'max-age=0\\', \\'Sec-Ch-Ua\\': \\'\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"\\', \\'Sec-Ch-Ua-Mobile\\': \\'?0\\', \\'Sec-Ch-Ua-Platform\\': \\'\"Windows\"\\', \\'Dnt\\': \\'1\\', \\'Upgrade-Insecure-Requests\\': \\'1\\', \\'User-Agent\\': \\'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36\\', \\'Accept\\': \\'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\\', \\'Sec-Fetch-Site\\': \\'none\\', \\'Sec-Fetch-Mode\\': \\'navigate\\', \\'Sec-Fetch-User\\': \\'?1\\', \\'Sec-Fetch-Dest\\': \\'document\\', \\'Accept-Encoding\\': \\'gzip, deflate, br\\', \\'Accept-Language\\': \\'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7\\', \\'Cookie\\': \\'unihotel_user_id=315; user_id=315; csrftoken=hHcvqpr22wTBcavkaP1xuMgrhxWrkF6vZlDc5Ww8MRLWjNzBKAJBA3P4hF4EULVG; dev1.sessionid=rz829vaq3qgyqbom19wj3oquic62o3k2\\'}",
            "args":"()",
            "kwargs":"{}",
            "pathname":"/test/env/lib/python3.10/site-packages/django/utils/log.py",
            "funcName":"log_response",
            "lineno":241,
            "message":"Internal Server Error: /profile/",
            "exc_text":"None",
            "created":241,
            "filename":"log.py",
            "levelname":"ERROR",
            "levelno":"40",
            "module":"log",
            "msecs":280.26747703552246,
            "msg":"%s: %s",
            "name":"django.request",
            "process":"3227155",
            "processName":"MainProcess",
            "relativeCreated":"89924.0288734436",
            "stack_info":"None",
            "thread":"140612883982080",
            "threadName":"Thread-1 (process_request_thread)"
        },
        "tag":"throwed",
        "routing_key":"django_logger",
        "ttl":180,
        "filename":"/test/__upserver_.py",
        "function_name":"process_record",
        "lineno":74,
        "send_datetime":"2023-03-16 06:55:46"
    }

    DjangoLogger.save_record(row=row)


@pytest.mark.django_db
def test_django_exception():
    # pytest tests/tests.py::test_django_exception -rP

    row = {
        "payload":{
            "uuid":"8yk5me3hHvjEneFx62WvsJ",
            "asctime":"2023-03-16T08:36:12.269142",
            "exc_info":"Traceback (most recent call last):\n\n  File \"/test/apps/main/views.py\", line 124, in profile\n    print(test_afdasfadfadsf)\n\nNameError: name \\'test_afdasfadfadsf\\' is not defined\n",
            "exc_hash":"c45319b1dd26e50a99fceb5f5bbec5da",
            "message":""
        },
        "tag":"throwed",
        "routing_key":"django_exception",
        "ttl":180,
        "filename":"/test/__upserver_.py",
        "function_name":"capture_exception",
        "lineno":89,
        "send_datetime":"2023-03-16 08:36:12"
    }

    DjangoException.save_record(row=row)


@pytest.mark.skip
@pytest.mark.django_db
def test_parse_nginx_logger(caplog):
    # pytest tests/tests.py::test_parse_nginx_logger -rP
    # TODO in progress

    NGINX_LOG_DIR = Path(__file__).resolve() + "nginx/"

    for f_name in ["access", "error"]:

        try:
            fp = open(f"{NGINX_LOG_DIR}{f_name}log", "rb")
            f_binary = fp.read()
            fp.close()
        except FileNotFoundError:
            print("Please check the path.")

        NginxLogger.save_records(f_binary)



