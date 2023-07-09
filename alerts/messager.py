import aiohttp
import pprint
import asyncio
import time
import json
from simple_print import sprint
from throw_catch import catch
from settings import DEBUG
from settings import TEST
from settings import AMQP_URI
from settings import TELEGRAM_BOT_TOKEN
from settings import TELEGRAM_CHAT_IDS


class Messager:

    def __init__(self, data={}):
        self.data = data

    async def run(self):

        batch_size = 10
        if DEBUG or TEST:
            sprint(f"Messager.run 👽 AMQP_URI={AMQP_URI}", c="cyan")   
            batch_size = 5    

        for catched_message in catch(queue="alerts", uri=AMQP_URI, count=batch_size):
            payload = catched_message["payload"]
            if DEBUG or TEST:
                sprint(f"Messager.run 👽 catched_payload={payload}", c="green")    

            payload = json.dumps(payload, indent=2)[:4000]
            pprint.pprint(payload)
            try:
                await self.send_telegram_alert(payload)
            except:
                continue
            time.sleep(1)
            

    async def send_telegram_alert(self, payload):

        if DEBUG or TEST:
            sprint(f"Messager.send_telegram_alert 👽 {payload} BOT_TOKEN={TELEGRAM_BOT_TOKEN} TELEGRAM_CHAT_IDS={TELEGRAM_CHAT_IDS}", c="yellow")        

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        for chat_id in TELEGRAM_CHAT_IDS:
            
            attempts = 5
            params = {
                "chat_id": chat_id,
                "text": payload,
            }

            while attempts >= 0:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as resp:
                        if resp.status == 200:
                            return
                        elif resp.status == 429:
                            attempts -= 1
                            await asyncio.sleep(1)
                            continue
                        else:
                            raise RuntimeError(f"Bad HTTP response: {resp}")


