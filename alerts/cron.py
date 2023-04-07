import aiocron
from messager import Messager


@aiocron.crontab("* * * * *", start=False)
async def every_minute():
    messager = Messager()
    await messager.run()