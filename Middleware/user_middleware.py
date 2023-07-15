import asyncio
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class UserMiddleware(BaseMiddleware):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.from_user.id != self.user_id:
            print(f'Unsupported user: {message.from_user.id}')
            raise asyncio.CancelledError()
