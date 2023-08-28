from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Dict, Any, Callable, Awaitable

def office_hours() -> bool:
    return datetime.now().weekday() in (0,1,2,3,4) and datetime.now().hour in ([i for i in (range(8,19))])


class OfficeHoursMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], #если любые события то TelegramObject вместо Message
        event: Message,  #если любые события то TelegramObject вместо Message
        data: Dict[str, Any]
    ) -> Any:
        if office_hours():
            return await handler(event,data)
        return event.answer('Время работы бота:\r\nПн-Пт с 8 до 18. Приходите в рабочие часы.')
