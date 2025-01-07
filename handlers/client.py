import asyncio
import datetime
from random import uniform, randint
#from main import bot, appFlask

from aiogram import F, Router, types, Bot
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from pprint import pprint

from database.db import DataBase
from keyboards.client import ClientKeyboard
from other.languages import languages
class DummyUser:
    def __init__(self, user_id):
        self.id = user_id
class DummyCallback:
    def __init__(self, user_id):
        self.from_user = DummyUser(user_id)

router = Router()

class RegisterState(StatesGroup):
    input_id = State()

class GetSignalStates(StatesGroup):
    chosing_mines = State()


class ChangeReferral(StatesGroup):
    input_ref = State()

@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.delete()
    lang = await DataBase.get_lang(message.chat.id)
    if lang is None:
        await get_language(message, True)
        return
    else:
        await message.answer(languages[lang]["welcome"].format(first_name=message.from_user.first_name),
                         reply_markup=await ClientKeyboard.start_keyboard(lang, message.chat.id), parse_mode="HTML")





@router.callback_query(F.data.startswith("sel_lang"))
async def select_language(callback: CallbackQuery):
    data = callback.data.split("|")
    await DataBase.register_lang(callback.from_user.id, data[2])
    await start_command(message=callback.message)


@router.callback_query(F.data.startswith("resel_lang"))
async def select_language(callback: CallbackQuery):
    data = callback.data.split("|")
    await DataBase.update_lang(int(data[1]), data[2])
    await start_command(message=callback.message)


@router.callback_query(F.data == "get_lang")
async def get_language(query: Message, first: bool = False):
    q = query
    if isinstance(query, CallbackQuery):
        query = query.message
    try:
        await query.delete()
    except:
        pass

    if first:
        prefix = f"sel_lang|{query.from_user.id}"
    else:
        prefix = f"resel_lang|{q.from_user.id}"
    await query.answer("Select language",
                       reply_markup=await ClientKeyboard.languages_board(prefix))


@router.callback_query(F.data.in_(["back", "check"]))
async def menu_output(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    user_info = await DataBase.get_user_info(callback.from_user.id)
    lang = await DataBase.get_lang(callback.from_user.id)
    text = languages[lang]["register_info"]
    if lang == "ru":
        photo = types.FSInputFile("hello.jpg")
    else:
        photo = types.FSInputFile("hel.jpg")  
    await callback.message.answer_photo(photo, caption=languages[lang]["welcome_message"],
                                        parse_mode="HTML",
                                        reply_markup=await ClientKeyboard.menu_keyboard(user_info, lang))
    await callback.answer()





@router.callback_query(F.data == "register")
async def register_handler(callback: types.CallbackQuery, state: FSMContext):
    lang = await DataBase.get_lang(callback.from_user.id)
    text = languages[lang]["register_info"]
    try:
        await callback.message.delete()
    except:
        pass

    photo = types.FSInputFile("reger.png")
    await callback.message.answer_photo(
             photo=photo,
             caption=text,
             parse_mode="HTML",
             reply_markup=await ClientKeyboard.register_keyboard(callback, lang)
         )
    await state.set_state(RegisterState.input_id)

@router.message(RegisterState.input_id)
async def mailing_state(message: types.Message, state: FSMContext, bot: Bot):
    lang = await DataBase.get_lang(message.chat.id)
    if str(message.text).isnumeric()==True:
        text_capt = ''
        acc_id = message.text
        checked = await DataBase.check_register(message.chat.id)
        if checked == 0:
            await DataBase.register(message.chat.id,acc_id)
            text_capt = languages[lang]["success_registration"]
        else:
            text_capt = languages[lang]["check_register"]
        
        photo = types.FSInputFile("dep.png")
        dummy_callback = DummyCallback(message.chat.id)
        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=text_capt,
            parse_mode="HTML",
            reply_markup=await ClientKeyboard.dep_keyboard(dummy_callback, lang)
        )
    else:
        await message.answer(languages["ru"]["welcome"].format(first_name=message.from_user.first_name),
                         reply_markup=await ClientKeyboard.start_keyboard(lang), parse_mode="HTML")

    
    await state.clear()


@router.callback_query(F.data == "instruction")
async def instruction_handler(callback: types.CallbackQuery):
    new_ref_url = await DataBase.get_ref()
    lang = await DataBase.get_lang(callback.from_user.id)
    text = languages[lang]["instruction_info"].format(ref_url=new_ref_url)

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(text, reply_markup=await ClientKeyboard.back_keyboard(lang),
                                  parse_mode="HTML")






def deposit_required(func):
    async def wrapper(event, *args, **kwargs):
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return
            
        deposit_status = await DataBase.get_deposit_status(user_id)
        if deposit_status != 'dep':
            lang = await DataBase.get_lang(user_id)
            await event.answer(
                languages[lang]["deposit_required"],
                show_alert=True
            )
            return
        
        return await func(event, *args, **kwargs)
    return wrapper




@router.callback_query(F.data == "change_ref")
async def change_referral_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    lang = await DataBase.get_lang(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(languages[lang]["enter_new_ref"])
    await state.set_state(ChangeReferral.input_ref)


@router.message(ChangeReferral.input_ref)
async def change_referral_message_state(message: types.Message, state: FSMContext):
    lang = await DataBase.get_lang(message.from_user.id)
    await message.answer(languages[lang]["ref_changed"])
    await DataBase.edit_ref(message.text)
    await state.clear()
