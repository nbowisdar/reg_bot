from datetime import datetime
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from setup import admins_id


class IsAdmin(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        if data["event_from_user"].id in admins_id:
            return await handler(event, data)
        print('forbidden')
