import datetime
import math
import threading
import traceback
import pika
import io
import time
import os
import sys
import psutil
import pprint
from loguru import logger
from functools import wraps
from croniter import croniter
from throw_catch import catch
from settings import AMQP_URI
from settings import DEBUG
from log_collector import models
from simple_print import sprint
from django.db import connection
from django.db import reset_queries


def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def format_exception(ei) -> str:
    sio = io.StringIO()
    tb = ei[2]
    traceback.print_exception(ei[0], ei[1], tb, None, sio)
    s = sio.getvalue()
    sio.close()
    if s[-1:] == "\n":
        s = s[:-1]
    return s


def format_memory(memory_before, memory_after):
    def convert_memory_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        x = int(math.floor(math.log(size_bytes, 1024)))
        y = math.pow(1024, x)
        z = round(size_bytes / y, 2)
        return f"{z} {size_name[x]}"

    memory_difference = memory_after - memory_before
    task_memory = ""
    task_memory += f"Memory before: {convert_memory_size(memory_before)}\n"
    task_memory += f"Memory after: {convert_memory_size(memory_after)}\n"
    task_memory += f"Memory difference: {convert_memory_size(memory_difference)}\n"
    return task_memory


def task_decorator(cron_time):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*a, **kw):

            task_name = fn.__name__
            datetime_now = datetime.datetime.now()
            current_thread = threading.current_thread()
            logger.opt(colors=True).info(
                f"Task {task_name} start in thread [ <green>{current_thread}</green> ]"
            )

            if models.TaskScheduler.objects.filter(
                task_name=task_name,
                task_active=True).count() > 0:
                if DEBUG:
                    logger.opt(colors=True).info(f"Tasks.{task_name} [ <red>ALREADY WORKED</red> ]")

                return None

            if DEBUG:
                logger.opt(colors=True).info(f"Tasks.{task_name} [ <green>START</green> ]")

            time_start = time.process_time()
            task_stdout = f"{task_name} start {datetime_now}\n"
            task_error_tb = None
            task_memory_before = ""
            task_memory_after = ""
            task_query_count = 0
            reset_queries()

            t = models.TaskScheduler()
            t.task_name = task_name
            t.task_active = True
            t.task_completed = False
            t.task_stdout = task_stdout
            t.task_cron_time = cron_time
            t.save()

            stdout_backup = sys.stdout
            res = None

            try:
                sys.stdout = io.StringIO()
                task_memory_before = get_process_memory()
                res = fn(*a, **kw)
                task_memory_after = get_process_memory()
                task_query_count = len(connection.queries)
                try:
                    task_stdout += sys.stdout.getvalue()
                except AttributeError:
                    pass
            except Exception:
                ei = sys.exc_info()
                task_error_tb = format_exception(ei)
                t.task_completed = False
                t.task_active = False
                t.save()

                if DEBUG:
                    logger.opt(colors=True).info(f"Tasks.{task_name} [ <red>FAIL</red> ]")
                    pprint.pprint(task_error_tb)
                return None
            
            finally:
                sys.stdout.close()
                sys.stdout = stdout_backup

            if DEBUG:
                logger.opt(colors=True).info(f"Tasks.{task_name} [ <green>FINISH</green> ]")

            task_time = time.process_time() - time_start
            task_time = f"{round(task_time, 4)}"

            try:
                task_memory = format_memory(task_memory_before, task_memory_after)
            except:
                task_memory = ""

            task_stdout += f"\n{task_name} finish {datetime_now}\n"
            t.task_active = False     
            t.task_completed = True
            t.task_time = task_time
            t.task_stdout = task_stdout
            t.task_error_tb = task_error_tb
            t.task_memory = task_memory
            t.task_query_count = task_query_count
            t.save()
            return res

        wrapper.cron_time = cron_time
        return wrapper
    return decorator


class Tasks:

    @task_decorator("0 0 1 1 *")
    def task_test():
        # python run.py log_collector.tasks "run_every_minute(force_task='task_test')"
        time.sleep(10)
        print("test task")

    @task_decorator("* * * * *")
    def task_any_logger():
        # python run.py log_collector.tasks "run_every_minute(force_task='task_any_logger')"

        messages = catch(uri=AMQP_URI, queue="any_logger", count=1)    
        messages_count = 0
        for row in messages:
            if DEBUG:
                sprint(row, c="green", i=8)
            models.AnyLogger.save_record(row=row)
            messages_count += 1     
        return messages_count   
    

    @task_decorator("* * * * *")
    def task_django_logger():
        # python run.py log_collector.tasks "run_every_minute(force_task='task_django_logger')"

        messages = catch(uri=AMQP_URI, queue="django_logger", count=1)    
        messages_count = 0
        for row in messages:
            if DEBUG:
                sprint(row, c="green")            
            models.DjangoLogger.save_record(row=row)
            messages_count += 1
        return messages_count

    @task_decorator("* * * * *")
    def task_django_exception():
        # python run.py log_collector.tasks "run_every_minute(force_task='task_django_exception')"

        messages = catch(uri=AMQP_URI, queue="django_exception", count=1)    
        messages_count = 0                     
        for row in messages:
            if DEBUG:
                sprint(row, c="green")         
            models.DjangoException.save_record(row=row)
            messages_count += 1        
        return messages_count    


    @task_decorator("* * * * *")
    def task_nginx_logger():
        # python run.py log_collector.tasks "run_every_minute(force_task='task_nginx_logger')"

        connection = pika.BlockingConnection(pika.URLParameters(AMQP_URI))
        channel = connection.channel()
        queue = channel.queue_declare(queue="nginx_log_collector", durable=False)  

        messages_count = 0
        for _ in range(queue.method.message_count):

            method_frame, header_frame, f_binary = channel.basic_get(
                queue="nginx_log_collector", 
                auto_ack=True
            )

            if DEBUG:
                sprint(
                    f"Tasks.catch_nginx_logger() method_frame={method_frame}", 
                    c="green", 
                    i=4
                ) 

            if method_frame:
                models.NginxLogger.save_records(f_binary)
                messages_count += 1        
        return messages_count   


def run_every_minute(force_task=None):
    # python run.py tasks.tasks "run_every_minute()"

    datetime_now = datetime.datetime.now()
    if DEBUG:
        sprint(f'tasks.tasks "run_every_minute() force_task={force_task}', c="yellow")
    for fn_name, fn in filter(lambda x: x[0].startswith("task"), Tasks.__dict__.items()):
        if force_task:
            if fn_name == force_task:
                thread = threading.Thread(target=fn)
                thread.start()
        else:
            if hasattr(fn, "cron_time") and fn.cron_time:
                if croniter.match(fn.cron_time, datetime_now):
                    thread = threading.Thread(target=fn)
                    thread.start()



def show_all_environ():
    # python run.py log_collector.tasks "show_all_environ()"
    import os
    for name, value in os.environ.items():
        print("{0}: {1}".format(name, value))
