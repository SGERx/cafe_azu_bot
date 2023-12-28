from typing import Optional, Union

from aiogram.filters.callback_data import CallbackData


class CalendarCallbackFactory(CallbackData, prefix="simple_calendar"):
    act: str
    year: int
    month: int
    day: int


class DishCallbackFactory(CallbackData, prefix="dinner_set"):
    act: Optional[str] = "None"
    payment: Optional[bool] = False
    resume: Optional[bool] = False
    price: Optional[float] = 0
    count: Optional[int] = 0
    id: Optional[int] = 0

    def set_attr(self, name: str, value: Union[str, int, bool]):
        setattr(self, name, value)
        return self

    # def set_count(self, count: int):
    #     setattr(self, "count", count)
    #     return self

    # def set_payment(self, value: bool):
    #     setattr(self, "payment", value)
    #     return self

    # def set_resume(self, value: bool):
    #     setattr(self, "resume", value)
    #     return self
