from settings import AMQP_URI
from throw_catch import throw
from messager import Messager


async def test_messager(define_test_scope):
    # pytest tests/tests.py::test_messager -rP
    # for _ in range(5):
    #     throw(payload={"test": "test"}, uri=AMQP_URI, routing_key="alerts", ttl=0) 
    messager = Messager()
    await messager.run()


            


