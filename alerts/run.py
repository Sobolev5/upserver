import asyncio
from messager import Messager


async def run_messager():
    messager = Messager()
    await messager.run()


if __name__ == "__main__":
    asyncio.run(run_messager())
