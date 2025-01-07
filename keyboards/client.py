from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo

from database.db import DataBase
from other.languages import languages


class ClientKeyboard:

    @staticmethod
    async def start_keyboard(lang: str, user_id: int):
        #dt = WebAppInfo(url="https://rasenganero.github.io/sitewin.github.io/")
        
        
        ikb = InlineKeyboardBuilder()
        ikb.button(text=languages[lang]["instruction"], callback_data="instruction")
        ikb.button(text=languages[lang]["register"], callback_data="register")
        ikb.button(text=languages[lang]["choose_lang"], callback_data="get_lang")

        check_user = await DataBase.check_register(user_id) # Если пользователь уже зарегистрирован, то показываему ему кнопку "Получить сигнал"
        if check_user == 1:
            ikb.button(text=languages[lang]["get_signal"],web_app=WebAppInfo(url="https://rasenganero.github.io/sitewin.github.io/")) 
        ikb.adjust(1)
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
        new_ref_url = await DataBase.get_ref()
        ikb.button(text=languages[lang]["register_action"], url=new_ref_url)
        ikb.button(text=languages[lang]["back"], callback_data="back")
        ikb.adjust(1)
        return ikb.as_markup()

    @staticmethod
    async def dep_keyboard(callback: types.CallbackQuery, lang: str):
        ikb = InlineKeyboardBuilder()
        new_ref_url = await DataBase.get_ref()
        ikb.button(text=languages[lang]["dep_action"], url=new_ref_url)
        ikb.button(text=languages[lang]["back"], callback_data="back")
        ikb.adjust(1)
        return ikb.as_markup()

    @staticmethod
    async def back_keyboard(lang: str):
        ikb = InlineKeyboardBuilder()
        ikb.button(text=languages[lang]["back"], callback_data="back")
        return ikb.as_markup()


