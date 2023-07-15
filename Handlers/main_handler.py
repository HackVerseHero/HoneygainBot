from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from States.states import FSMUser
from Keyboards.main_kb import main_board
import Keyboards.main_kb
from Messages.bot_messages import Messages
from create_bot import bot, USER_ID
from honeygain import hg


async def start_handler(message: types.Message, state: FSMContext):
    state = await state.get_state()
    if (message.text != '/start') and (state is None):
        first_name = message.from_user.first_name
        await message.answer(await Messages.starting_message(first_name=first_name))
    elif message.text == '/start':
        await message.answer(Messages.hello_message, reply_markup=main_board)
        await FSMUser.menu.set()
    else:
        first_name = message.from_user.first_name
        await message.answer(await Messages.unrecognised_command_message(first_name=first_name))


async def status_handler(message):
    await bot.send_message(chat_id=USER_ID, text=message)


async def open_honeypot(message: types.Message):
    await message.answer(text=Messages.honeypot_opening)
    open_status = await hg.open_honeypot()
    if open_status:
        await hg.reset_timers()


async def get_honeypot_status(message: types.Message):
    await message.answer(text=Messages.getting_honeypot_status)
    await hg.get_honeypot_status()


async def get_statistics(message: types.Message):
    await message.answer(text=Messages.getting_statistics)
    await hg.get_statistics()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(open_honeypot, Text(equals=Keyboards.main_kb.open_honeypot_button.text),
                                state=FSMUser.menu)
    dp.register_message_handler(get_honeypot_status, Text(equals=Keyboards.main_kb.get_status_button.text),
                                state=FSMUser.menu)
    dp.register_message_handler(get_statistics, Text(equals=Keyboards.main_kb.get_statistics_button.text),
                                state=FSMUser.menu)
