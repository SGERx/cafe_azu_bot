import functools
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


def search_places_in_restaurants(num_people: str, date: str):
    """Функция осуществляет поиск вариантов возможной рассадки во всех ресторанах.
    Ожадается список ресторанов и номера столиков для сохранения во временном хранилище.
    """
    if int(num_people) < 9:
        return True
    else:
        return False


def print_state_key(key):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(message, state: FSMContext, *args, **kwargs):
            data = await state.get_data()
            print(f"Текущий ключ состояния {data.get(key, None)}")
            return await func(message, state, *args, **kwargs)

        return wrapper

    return decorator


def print_state_key_callback_query(key):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(
            callback: CallbackQuery,
            callback_data: dict,
            state: FSMContext,
            *args,
            **kwargs,
        ):
            data = await state.get_data()
            print(f"Текущий ключ состояния {data.get(key, None)}")
            return await func(callback, callback_data, state, *args, **kwargs)

        return wrapper

    return decorator
