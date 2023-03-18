import datetime
import io
import logging
import traceback
import shortuuid
import hashlib
import logging
from django.core.handlers.wsgi import WSGIRequest
from throw_catch import throw

AMQP_URI = f"amqp://admin:admin@127.0.0.1:5672/vhost"
DJANGO_LOGGER_REQUEST_EXTRA = "session"

def format_exception(ei) -> str:
    sio = io.StringIO()
    tb = ei[2]
    traceback.print_exception(ei[0], ei[1], tb, None, sio)
    s = sio.getvalue()
    sio.close()
    if s[-1:] == "\n":
        s = s[:-1]
    return s


def process_record(record: logging.LogRecord = "") -> None:

    request = record.request
    exc_info = getattr(record, "exc_info", "")

    if exc_info:
        exc_info = format_exception(exc_info)   

    payload = {}
    payload["uuid"] = shortuuid.uuid()
    payload["asctime"] = datetime.datetime.now()
    payload["exc_info"] = exc_info 
    payload["exc_hash"] = hashlib.md5(exc_info.encode()).hexdigest()
    payload["user"] = str(request.user)
    payload["user_id"] = request.user.id
    payload["request_extra"] = str(getattr(request, DJANGO_LOGGER_REQUEST_EXTRA, ""))
    payload["site"] = f"{request.get_host()}:{request.get_port()}"
    payload["scheme"] = str(request.scheme) 
    payload["body"] = str(request.body) 
    payload["path"] = str(request.path) 
    payload["method"] = str(request.method)  
    payload["GET"] = str(request.GET)  
    payload["POST"] = str(request.POST)  
    payload["headers"] = str(request.headers) 
    payload["args"] = str(request.resolver_match.args)
    payload["kwargs"] = str(request.resolver_match.kwargs)  
    payload["pathname"] = str(getattr(record, "pathname", ""))
    payload["funcName"] = str(getattr(record, "funcName", ""))
    payload["lineno"] = getattr(record, "lineno", 0)
    payload["message"] = record.getMessage() 
    payload["exc_text"] = str(getattr(record, "exc_text", ""))   
    payload["created"] = getattr(record, "lineno", 0)
    payload["filename"] = str(getattr(record, "filename", ""))  
    payload["levelname"] = str(getattr(record, "levelname", ""))  
    payload["levelno"] = str(getattr(record, "levelno", ""))  
    payload["module"] = str(getattr(record, "module", ""))  
    payload["msecs"] = getattr(record, "msecs", 0)  
    payload["msg"] = str(getattr(record, "msg", ""))  
    payload["name"] = str(getattr(record, "name", ""))  
    payload["process"] = str(getattr(record, "process", ""))  
    payload["processName"] = str(getattr(record, "processName", ""))  
    payload["relativeCreated"] = str(getattr(record, "relativeCreated", ""))  
    payload["stack_info"] = str(getattr(record, "stack_info", ""))  
    payload["thread"] = str(getattr(record, "thread", ""))  
    payload["threadName"] = str(getattr(record, "threadName", ""))  
    
    throw(payload=payload, uri=AMQP_URI, routing_key="django_logger") 


def capture_exception(error: BaseException, message: str = "") -> None:

    exc_info = traceback.format_exception(error)
    exc_info = "\n".join(exc_info)
    
    payload = {}
    payload["uuid"] = shortuuid.uuid()
    payload["asctime"] = datetime.datetime.now()
    payload["exc_info"] = exc_info 
    payload["exc_hash"] = hashlib.md5(exc_info.encode()).hexdigest()
    payload["message"] = message

    throw(payload=payload, uri=AMQP_URI, routing_key="django_exception") 


class LoggerHandler(logging.StreamHandler):

    def emit(self, record) -> None:
        if isinstance(record, logging.LogRecord) and getattr(record, "request", False) and isinstance(record.request, WSGIRequest):
            try:
                process_record(record)
            except Exception as e:
                logging.exception(f"{e}")