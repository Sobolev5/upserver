import asyncio
from messager import Messager


async def every_minute():
    messager = Messager()
    await messager.run()


if __name__ == "__main__":  
    asyncio.run(every_minute())