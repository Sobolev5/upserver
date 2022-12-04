python manage.py migrate
python manage.py shell --command="from django_clickhouse_logger.db import *; create_logger_table(); create_capture_exception_table();" 
python run.py initial_database "prepare()"