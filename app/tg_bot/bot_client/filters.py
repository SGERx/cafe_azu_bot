from datetime import datetime
import re
from typing import Optional
from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsValidFillNumPeople(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.isdigit() and 1 <= int(message.text) <= 20


class IsValidFillName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return re.match(r"^[а-яА-Яa-zA-Z ]+$", message.text)


class IsValidFillFhone(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return re.match(
            r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message.text
        )


def is_valid_date(
    date: datetime, begin: Optional[datetime] = None, end: Optional[datetime] = None
) -> bool:
    current_datetime = datetime.now()
    if end and begin:
        if begin <= date <= end:
            return True
    elif end:
        if current_datetime <= date <= end:
            return True

    elif begin:
        if begin <= date:
            return True

    else:
        return date >= current_datetime


if __name__ == "__main__":
    print(re.match(r"^[а-яА-Яa-zA-Z ]+$", "Людвиг ван Бетховен"))
