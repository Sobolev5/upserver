from settings import AMQP_URI
from throw_catch import throw
from messager import Messager


def test_messager(capsys):
    # pytest tests/tests.py::test_messager -s -v 
    
    throw(payload={"test": "test"}, uri=AMQP_URI, routing_key="alerts", ttl=0) 
    Messager.run()
    captured = capsys.readouterr()
    assert "OK" in captured.out

            


