import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import Redis, RedisStorage

from config import load_data
from handlers.admin_handlers import router as admin_router
from handlers.user_handlers import router as user_router


async def main() -> None:
    config = load_data()
    
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)
    
    bot: Bot = Bot(token=config.bot_token)
    dp: Dispatcher = Dispatcher(storage=storage)
    
    dp.include_router(router=user_router)
    dp.include_router(router=admin_router)

    await bot.delete_webhook()
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())


