from typing import Any
from aiogram.filters import BaseFilter
from aiogram import types, Bot

from database.db import DataBase


class RegisteredFilter(BaseFilter):

    async def __call__(self, callback: types.CallbackQuery) -> Any:
        return not await DataBase.get_user(callback.from_user.id) is None
