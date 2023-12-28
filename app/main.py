import asyncio
import sys

from app.tg_bot.bot_client.client_bot_main import main_bot_client
from app.tg_bot.bot_admin.admin_bot_main import main_bot_admin
sys.path.insert(0, "/home/llirik_05/Dev/cafe_azu_bot_3")


async def main():
    await asyncio.gather(main_bot_admin(), main_bot_client())
    # await main_bot_client()


if __name__ == "__main__":
    asyncio.run(main())
