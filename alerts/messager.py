import aiohttp
import asyncio
import json
from throw_catch import catch
from settings import AMQP_URI
from settings import TELEGRAM_BOT_TOKEN
from settings import TELEGRAM_CHAT_IDS


class Messager:
    def __init__(
        self,
        data: dict = {},
    ) -> None:
        self.data = data

    async def run(self) -> None:
        for catched_message in catch(
            queue="alerts",
            uri=AMQP_URI,
            count=10,
        ):
            payload = catched_message["payload"]
            payload = json.dumps(
                payload,
                indent=2,
            )[:4000]
            await self.send_telegram_alert(payload)

    async def send_telegram_alert(self, payload) -> None:
        for chat_id in TELEGRAM_CHAT_IDS:
            attempts = 5
            params = {
                "chat_id": chat_id,
                "text": payload,
            }

            while attempts >= 0:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                        params=params,
                    ) as resp:
                        if resp.status == 200:
                            return
                        elif resp.status == 429:
                            attempts -= 1
                            await asyncio.sleep(1)
                            continue
                        else:
                            raise RuntimeError(f"Bad HTTP response: {resp=}")
