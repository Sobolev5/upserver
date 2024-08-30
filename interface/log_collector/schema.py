from log_collector.models import AnyLogger, DjangoLogger, DjangoException
from ninja import ModelSchema


class AnyLoggerSchema(ModelSchema):
    class Config:
        model = AnyLogger
        model_exclude = ["id", "assigned_to", "creation_date"]


class DjangoLoggerSchema(ModelSchema):
    class Config:
        model = DjangoLogger
        model_exclude = ["id", "assigned_to", "status", "errors_count", "creation_date"]


class DjangoExceptionSchema(ModelSchema):
    class Config:
        model = DjangoException
        model_exclude = ["id", "assigned_to", "status", "errors_count", "creation_date"]
