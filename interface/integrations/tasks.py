from clickhouse_driver import connect
from clickhouse_driver.dbapi.extras import DictCursor
from integrations.models import ClickHouseLogger
from integrations.models import ClickHouseCaptureException
from integrations.models import SimplePrintCatch
from simple_print import catch 
from settings import CLICKHOUSE_HOST
from settings import CLICKHOUSE_PORT
from settings import CLICKHOUSE_USER
from settings import CLICKHOUSE_PASSWORD
from settings import SIMPLE_PRINT_AMQP_URI


def get_clickhouse_logger_records():
    # python run.py integrations.tasks "get_clickhouse_logger_records()"
    # docker run -it python run.py integrations.tasks "get_clickhouse_logger_records()"

    query = f"""
        SELECT (*) FROM django_clickhouse_logger.logger
    """

    data = []   
    clickhouse_connect = connect(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, user=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD)

    with clickhouse_connect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    for row in data:
        record, created = ClickHouseLogger.objects.get_or_create(exc_hash=row["exc_hash"])
        for field in ClickHouseLogger._meta.fields:
            field_name = field.name
            if field_name in row and row[field_name]:         
                setattr(record, field_name, row[field_name]) 
        if created:
            record.save()
        else:
            record.errors_count += 1
            record.save()   
            print(f"record saved id={record.id}")    

    query = f"""
        TRUNCATE TABLE IF EXISTS django_clickhouse_logger.logger
    """

    with clickhouse_connect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(query)



def get_clickhouse_captured_exceptions():
    # python run.py integrations.tasks "get_clickhouse_captured_exceptions()"
    # docker run -it python run.py integrations.tasks "get_clickhouse_captured_exceptions()"

    query = f"""
        SELECT (*) FROM django_clickhouse_logger.capture_exception
    """

    data = []   
    clickhouse_connect = connect(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, user=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD)
    with clickhouse_connect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    for row in data:
        record, created = ClickHouseCaptureException.objects.get_or_create(exc_hash=row["exc_hash"])
        for field in ClickHouseCaptureException._meta.fields:
            field_name = field.name
            if field_name in row and row[field_name]:         
                setattr(record, field_name, row[field_name]) 
        if created:
            record.save()
        else:
            record.errors_count += 1
            record.save() 
            print(f"record saved id={record.id}")   

    query = f"""
        TRUNCATE TABLE IF EXISTS django_clickhouse_logger.capture_exception
    """

    with clickhouse_connect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(query)


def catch_simple_print_messages():
    # python run.py integrations.tasks "catch_simple_print_messages()"
    # docker run -it python run.py integrations.tasks "catch_simple_print_messages()"

    for message in catch(count=100, uri=SIMPLE_PRINT_AMQP_URI):
        catched = SimplePrintCatch()
        catched.message = message["msg"]
        catched.tag = message["tag"]
        catched.uuid = message["uuid"]
        catched.filename = message["filename"]
        catched.function_name = message["function_name"]
        catched.lineno = message["lineno"]
        catched.save() 
        print(f"record saved id={catched.id}")    

