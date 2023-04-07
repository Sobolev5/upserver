from throw_catch import throw
from settings import AMQP_URI


def any_throw(payload, tag="throw", ttl=180) -> None:
    # ttl 0 without deletion time
    throw(payload=payload, tag=tag, uri=AMQP_URI, routing_key="any_logger", ttl=ttl) 