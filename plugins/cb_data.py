import os
import sys
import asyncio
from bot import Bot
from presets import Presets
from pyrogram import Client, filters
from plugins.chat_config import start_bot, help_me
from plugins.clone import clone_medias
from init import (source_message_id, dest_message_id, source_chat, destination_chat, clone_status)
from pyrogram.types import CallbackQuery, ForceReply

# --------------------------- Source Button Action ------------------------------ #
@Client.on_callback_query(filters.regex(r'^source_btn$'))
async def source_chat_config(client: Bot, cb: CallbackQuery):
    usr = int(cb.from_user.id)
    await cb.message.delete()
    source = await client.send_message(
        chat_id=cb.message.chat.id,
        text=Presets.ASK_SOURCE,
        parse_mode='html',
        reply_markup=ForceReply(True)
    )
    source_message_id[usr] = int(source.message_id)
    await asyncio.sleep(30)
    await source.delete()
    return


# --------------------------- Destination Button Action ------------------------- #
@Client.on_callback_query(filters.regex(r'^dest_btn$'))
async def dest_chat_config(client: Bot, cb: CallbackQuery):
    usr = int(cb.from_user.id)
    await cb.message.delete()
    dest = await client.send_message(
        chat_id=cb.message.chat.id,
        text=Presets.ASK_DESTINATION,
        parse_mode='html',
        reply_markup=ForceReply(True)
    )
    dest_message_id[usr] = int(dest.message_id)
    await asyncio.sleep(30)
    await dest.delete()
    return


# ---------------------------- Chat View Button Action -------------------------- #
@Client.on_callback_query(filters.regex(r'^view_btn$'))
async def view_config(client: Bot, cb: CallbackQuery):
    usr = int(cb.from_user.id)
    if usr in source_chat and destination_chat:
        await cb.message.delete()
        await client.send_message(
            chat_id=cb.message.chat.id,
            text=Presets.VIEW_CONF.format(source_chat[usr], destination_chat[usr]),
            parse_mode='html'
        )
        await asyncio.sleep(2)
        await start_bot(client, cb.message)
    else:
        await cb.answer(text=Presets.NOT_CONFIGURED, show_alert=True)


# --------------------------- Delete configuration Button Action --------------- #
@Client.on_callback_query(filters.regex(r'^del_cfg_btn$'))
async def del_config(client: Bot, cb: CallbackQuery):
    usr = int(cb.from_user.id)
    if usr in source_chat and destination_chat:
        source_chat.pop(usr)
        destination_chat.pop(usr)
        await cb.answer(text=Presets.CLEAR_CONFIG, show_alert=True)
    else:
        await cb.answer(Presets.NOT_CONFIGURED, show_alert=True)


# --------------------------- Clone Button Action ----------------------------- #
@Client.on_callback_query(filters.regex(r'^clone_btn$'))
async def clone_button(client: Bot, cb: CallbackQuery):
    usr = int(cb.from_user.id)
    if usr in source_chat and destination_chat:
        await cb.message.delete()
        await clone_medias(client, cb.message)
    else:
        await cb.answer(Presets.NOT_CONFIGURED_CLONE, show_alert=True)


# --------------------------- Help Button Action ----------------------------- #
@Client.on_callback_query(filters.regex(r'^help_btn$'))
async def help_txt(client: Bot, cb: CallbackQuery):
    await cb.message.delete()
    await help_me(client, cb.message)


# --------------------------- Stop Button Action ----------------------------- #
@Client.on_callback_query(filters.regex(r'^stop_clone$'))
async def stop_process(client: Bot, cb: CallbackQuery):
    usr = int(cb.from_user.id)
    await cb.message.delete()
    clone_status.pop(usr)


# ----------------------------- Close Button Action --------------------------- #
@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close_button_data(client: Bot, cb: CallbackQuery):
    await cb.answer()
    await cb.message.delete()


# ------------------------------ Home Button Action --------------------------- #
@Client.on_callback_query(filters.regex(r'^home_btn$'))
async def main_menu(client: Bot, cb: CallbackQuery):
    await cb.message.delete()
    await start_bot(client, cb.message)
