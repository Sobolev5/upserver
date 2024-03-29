from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def health(request):
    return PlainTextResponse("200 OK")


class AmqpHttpServer(Starlette):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


app = AmqpHttpServer(
    routes=[
        Route("/", health),
    ],
)
