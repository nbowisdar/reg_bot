from datetime import datetime
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from setup import admin_id


# Это будет inner-мидлварь на сообщения
class IsAdmin(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        #if not _is_weekend():
        x = data["event_from_user"]
        if data["event_from_user"].id == admin_id:
            return await handler(event, data)
        print('forbidden')
        # В противном случае просто вернётся None
        # и обработка прекратится