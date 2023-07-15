import asyncio
from aiogram import executor
from create_bot import dp, USER_ID
from Handlers import main_handler
from honeygain import hg
from Middleware.user_middleware import UserMiddleware


dp.middleware.setup(UserMiddleware(user_id=USER_ID))
main_handler.register_handlers(dp)

dp.register_message_handler(main_handler.start_handler, state='*')


async def main():
    hg.handler = main_handler.status_handler
    await hg.start()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    executor.start_polling(dp, loop=loop, skip_updates=True)
    loop.run_forever()
