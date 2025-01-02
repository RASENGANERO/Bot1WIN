from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db import DataBase
from other.languages import languages


class ClientKeyboard:

    @staticmethod
    async def start_keyboard(lang: str):
        ikb = InlineKeyboardBuilder()
        ikb.button(text=languages[lang]["instruction"], callback_data="instruction"),
        ikb.button(text=languages[lang]["register"], callback_data="register"),
        ikb.button(text=languages[lang]["choose_lang"], callback_data="get_lang")
        return ikb.as_markup()

    @staticmethod
    async def languages_board(data: str):
        ikb = InlineKeyboardBuilder()
        ikb.button(text="🇷🇺 Русский", callback_data=f"{data}|ru")
        ikb.button(text="🇬🇧 English", callback_data=f"{data}|en")
        ikb.adjust(2)
        return ikb.as_markup()

    @staticmethod
    async def menu_keyboard(user_info: list, lang: str):
        print(user_info)
        ikb = InlineKeyboardBuilder()
        ikb.button(text=languages[lang]["register"], callback_data="register")
        ikb.button(text=languages[lang]["instruction"], callback_data="instruction")
        ikb.button(text=languages[lang]["choose_lang"], callback_data="get_lang")


        if user_info[3] != "dep":
            ikb.button(text=languages[lang]["get_signal"], callback_data="register")
        else:
            ikb.button(text=languages[lang]["get_signal"], web_app=types.WebAppInfo(url="https://entyludik.github.io/entymain/"))

        ikb.adjust(2, 1, 1)
        return ikb.as_markup()

    @staticmethod
    async def register_keyboard(callback: types.CallbackQuery, lang: str):
        ikb = InlineKeyboardBuilder()
        user_id = callback.from_user.id
        new_ref_url = f"{(await DataBase.get_ref())}&sub1={user_id}"
        ikb.button(text=languages[lang]["register_action"], url=new_ref_url)
        ikb.button(text=languages[lang]["back"], callback_data="back")
        ikb.adjust(1)
        return ikb.as_markup()

    @staticmethod
    async def dep_keyboard(callback: types.CallbackQuery, lang: str):
        ikb = InlineKeyboardBuilder()
        user_id = callback.from_user.id
        new_ref_url = f"{(await DataBase.get_ref())}&sub1={user_id}"
        ikb.button(text=languages[lang]["dep_action"], url=new_ref_url)
        ikb.button(text=languages[lang]["back"], callback_data="back")
        ikb.adjust(1)
        return ikb.as_markup()

    @staticmethod
    async def back_keyboard(lang: str):
        ikb = InlineKeyboardBuilder()
        ikb.button(text=languages[lang]["back"], callback_data="back")
        return ikb.as_markup()

    @staticmethod
    async def get_signal_keyboard(lang: str):
        ikb = InlineKeyboardBuilder()
        ikb.button(text=languages[lang]["get_signal"], web_app=types.WebAppInfo(url="https://entyludik.github.io/entymain/"))
        ikb.button(text=languages[lang]["back"], callback_data="back")
        ikb.adjust(1)
        return ikb.as_markup()
