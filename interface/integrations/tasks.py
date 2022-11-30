from clickhouse_driver import connect
from clickhouse_driver.dbapi.extras import DictCursor
from integrations.models import ClickHouseLogger
from integrations.models import ClickHouseCaptureException
from integrations.models import SimplePrintCatch


def fill_clickhouse_logger():
    query = f"""
        SELECT (*) FROM django_clickhouse_logger.logger
    """
    data = []   
    with connect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    exc_hashes = ClickHouseLogger.object.values_list("exc_hash", flat=True)
    for row in data:
        if row["exc_hash"] in exc_hashes:
            continue
        record = ClickHouseLogger()
        for field in ClickHouseLogger._meta.fields:
            if field in row and row["field"]:
                setattr(record, field) 
        try:
            record.save()          
        except:
            continue



def fill_clickhouse_capture_exception():
    query = f"""
        SELECT (*) FROM django_clickhouse_logger.capture_exception
    """
    data = []   
    with connect.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    exc_hashes = ClickHouseCaptureException.object.values_list("exc_hash", flat=True)
    for row in data:
        if row["exc_hash"] in exc_hashes:
            continue        
        record = ClickHouseCaptureException()
        for field in ClickHouseCaptureException._meta.fields:
            if field in row and row["field"]:
                setattr(record, field) 
        try:
            record.save()          
        except:
            continue


def simple_print_catch():
    # TODO make catch

