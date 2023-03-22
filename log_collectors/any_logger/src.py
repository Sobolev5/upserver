from throw_catch import throw

AMQP_URI = f"amqp://admin:admin@127.0.0.1:5672/vhost"


def any_throw(payload) -> None:
    throw(payload=payload, uri=COLLECTOR_AMQP_URI, routing_key="any_logger", ttl=180) 

if __name__ == "__main__":
    any_throw()