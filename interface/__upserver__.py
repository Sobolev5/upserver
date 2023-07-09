from throw_catch import throw
from settings import AMQP_URI
from settings import DEBUG
from simple_print import sprint


def any_throw(payload, ttl=1800, routing_key="any_logger") -> None:
    """ttl 0 without deletion time"""
    throw(payload=payload, uri=AMQP_URI, routing_key=routing_key, ttl=ttl) 