import asyncio

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from cron import every_minute

from settings import DEBUG


async def health(request):
    return PlainTextResponse("200 OK")


class AmqpHttpServer(Starlette):
    def __init__(self, *args, **kwargs):
        every_minute.start()
        super().__init__(*args, **kwargs)


app = AmqpHttpServer(
    debug=DEBUG,
    routes=[
        Route("/", health),
    ],
)