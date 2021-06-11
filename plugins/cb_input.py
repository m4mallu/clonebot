import asyncio
from bot import Bot
from library.sql import *
from presets import Presets
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, ForceReply


@Client.on_callback_query(filters.regex(r'^source_btn$'))
async def source_chat_config(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    await cb.answer(Presets.INFO_CHAT_TYPES, True)
    await cb.message.delete()
    msg = await client.send_message(cb.message.chat.id,
                                    Presets.ASK_SOURCE,
                                    parse_mode='html',
                                    reply_markup=ForceReply(True)
                                    )
    s_chat_msg_id = int(msg.message_id)
    await source_force_reply(id, s_chat_msg_id)
    await asyncio.sleep(30)
    await msg.delete()


@Client.on_callback_query(filters.regex(r'^target_btn$'))
async def dest_chat_config(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    await cb.answer(Presets.INFO_CHAT_TYPES, True)
    await cb.message.delete()
    msg = await client.send_message(cb.message.chat.id,
                                    Presets.ASK_DESTINATION,
                                    parse_mode='html',
                                    reply_markup=ForceReply(True)
                                    )
    d_chat_msg_id = int(msg.message_id)
    await target_force_reply(id, d_chat_msg_id)
    await asyncio.sleep(30)
    await msg.delete()


@Client.on_callback_query(filters.regex(r'^from_btn$'))
async def from_msg_config(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    ping = await query_msg(id)
    query = int(ping.s_chat)
    if query == bool(0):
        await cb.answer(Presets.CNF_SOURCE_FIRST, True)
        return
    await cb.answer(Presets.NOT_REQUIRED)
    await cb.message.delete()
    msg = await client.send_message(cb.message.chat.id,
                                    Presets.ASK_START_MSG_ID,
                                    parse_mode='html',
                                    reply_markup=ForceReply(True)
                                    )
    from_msg_id = int(msg.message_id)
    await from_msg_id_force_reply(id, from_msg_id)
    await asyncio.sleep(30)
    await msg.delete()


@Client.on_callback_query(filters.regex(r'^up_to_btn$'))
async def to_msg_config(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    ping = await query_msg(id)
    query = int(ping.s_chat)
    if query == bool(0):
        await cb.answer(Presets.CNF_SOURCE_FIRST, True)
        return
    await cb.answer(Presets.NOT_REQUIRED)
    await cb.message.delete()
    msg = await client.send_message(cb.message.chat.id,
                                    Presets.ASK_END_MSG_ID,
                                    parse_mode='html',
                                    reply_markup=ForceReply(True)
                                    )
    to_msg_id = int(msg.message_id)
    await to_msg_id_force_reply(id, to_msg_id)
    await asyncio.sleep(30)
    await msg.delete()
