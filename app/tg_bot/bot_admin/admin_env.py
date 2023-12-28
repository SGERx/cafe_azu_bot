import os

from dotenv import load_dotenv

dotenv_path = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ), "..", "..", "..", ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
    if ADMIN_TOKEN is None:
        raise ValueError("ADMIN_TOKEN не найден в .env файле")
else:
    print("НЕ ЗАГРУЖЕН .ENV")
