from throw_catch import throw

AMQP_URI = f"amqp://admin:admin@127.0.0.1:5672/vhost"


def any_throw(payload, tag="throw", ttl=180) -> None:
    # ttl 0 without deletion time
    throw(payload=payload, tag=tag, uri=COLLECTOR_AMQP_URI, routing_key="any_logger", ttl=ttl) 


if __name__ == "__main__":
    any_throw()