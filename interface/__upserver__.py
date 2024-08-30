from throw_catch import throw
from settings import AMQP_URI


def any_throw(
    payload: dict,
    ttl=1800,
    routing_key="any_logger",
) -> None:
    """Throw any data to syscollector

    Args:
        payload (_type_): _description_
        ttl (int, optional): _description_. Defaults to 1800.
        routing_key (str, optional): _description_. Defaults to "any_logger".
    """
    throw(payload=payload, uri=AMQP_URI, routing_key=routing_key, ttl=ttl)
