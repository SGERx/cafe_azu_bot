# flake8: noqa

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


# todo убрать лишние состояния
class FSMReservation(StatesGroup):
    fill_name = State()  # todo ввод текста
    fill_phone = State()  # todo ввод сообщением, валидация
    fill_date = State()  # todo инлайн клавиатура, ввод даты
    fill_num_people = State()  # todo ввод сообщением, валидация
    fill_restaurant = State()  # todo инлайн клавиатура
    fill_dinner_sets = State()  # todo попробовать инлайн выбор(названия, нумерация)
    fill_description_sets = State()
    fill_count_sets = State()
    payment = State()
    pre_checkout = State()
    successful_payment = State()
    approval = State()


async def add_curr_state(
    context: FSMContext,
    lexicon_key: str,
    markup: str = None,
    param_kb: dict = None,
) -> None:
    curr_state = await context.get_state()
    data = await context.get_data()
    state_stack = data.get("state_stack", [])
    step = dict(
        prev_state=curr_state, lexicon_key=lexicon_key, markup=markup, param_kb=param_kb
    )
    state_stack.append(step)
    await context.update_data(state_stack=state_stack)


async def get_prev_state(context: FSMContext) -> State or None:
    data = await context.get_data()
    state_stack = data.get("state_stack", [])
    if state_stack:
        state_stack.pop()
        return state_stack.pop()
    return None
