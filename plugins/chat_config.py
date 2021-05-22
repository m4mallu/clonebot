# ----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
import asyncio
from bot import Bot
from presets import Presets
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from init import source_chat, destination_chat, source_message_id, dest_message_id, help_message_id


# ----------------------------- Start Message command function --------------------------- #
@Bot.on_message(filters.private & filters.command('start'))
async def start_bot(client: Bot, message: Message):
    usr = int(message.chat.id)
    try:
        help_message_id.pop(usr)
    except Exception:
        pass
    await message.reply_text(
        text=Presets.WELCOME_TEXT,
        parse_mode='html',
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⏳   SOURCE", callback_data="source_btn"),
                 InlineKeyboardButton(text="🎯   DESTINATION", callback_data="dest_btn")],
                [InlineKeyboardButton(text="💡   VIEW CONFIG", callback_data="view_btn"),
                 InlineKeyboardButton(text="🚫   DEL CONFIG", callback_data="del_cfg_btn")],
                [InlineKeyboardButton(text="🌀 CLONE 🌀", callback_data="clone_btn")],
                [InlineKeyboardButton(text="❓   HELP", callback_data="help_btn"),
                 InlineKeyboardButton(text="❌   CLOSE", callback_data="close_btn")]
            ]
        )
    )


# -------------------------- Chat Id Input All-In-One function ---------------------------- #

# This fn code is a little bit complex as its logic. But optimized..
# When a replay is coming to the bot from ForceReply either from Source button or Destination button,
# this function will 'try:' to identify the message id which is replied. # All-In-One Input Function.

# When the replay is to wards the source:
# code will check..
#     1. The replay value is a perfect chat id or not !
#     2. The replay value is already in destination chat config (To avoid self spamming).
#     3. Whether the string user is a member in the source chat id given.
#     4. If any error in the above 3 states, bot will give the appropriate message nd leaves to Home.
#
# For any of the exceptions to the above: (Replay towards destination)
# code will check..
#     1. The replay value is a perfect chat id or not !
#     2. The replay value is already in source chat config (To avoid self spamming).
#     3. The string user status(As admin) and "Posting Privileges" in destination chat id given.
#     4. If any error in the above 3 states, bot will give the appropriate message nd leaves to Home.
#
# If all states found okay, bot will add both chat ids to the dict, later, can proceed to clone function.

@Client.on_message(filters.private & filters.text & filters.reply)
async def chat_reply(client: Bot, message: Message):
    usr = int(message.from_user.id)
    user_bot_me = await client.USER.get_me()
    try:
        if message.reply_to_message.message_id == source_message_id[usr]:
            if str(message.text).startswith('-100') and message.text[1:].isdigit():
                bot_msg = await message.reply_text(text=Presets.WAIT_MSG)
                await asyncio.sleep(1)
                try:
                    if destination_chat[usr] == message.text:
                        await message.delete()
                        await client.delete_messages(message.chat.id, source_message_id[usr])
                        await bot_msg.edit(Presets.CHAT_DUPLICATED_MSG)
                        await asyncio.sleep(5)
                        await bot_msg.delete()
                        await start_bot(client, message)
                        return
                except Exception:
                    pass
                try:
                    await client.USER.get_chat_member(chat_id=int(message.text), user_id=int(user_bot_me.id))
                except Exception:
                    await message.delete()
                    await bot_msg.edit(Presets.IN_CORRECT_PERMISSIONS_MESSAGE_SOURCE)
                    await client.delete_messages(message.chat.id, source_message_id[usr])
                    source_message_id.pop(usr)
                    await asyncio.sleep(5)
                    await bot_msg.delete()
                    await start_bot(client, message)
                    return
                await client.delete_messages(message.chat.id, source_message_id[usr])
                source_chat[usr] = message.text
                await message.delete()
                source_message_id.pop(usr)
                await bot_msg.edit(Presets.SOURCE_CONFIRM.format(source_chat[usr]))
                await asyncio.sleep(2)
                await start_bot(client, message)
                return
            else:
                await client.delete_messages(message.chat.id, source_message_id[usr])
                warn = await message.reply_text(Presets.INVALID_CHAT_ID)
                await message.delete()
                source_message_id.pop(usr)
                await asyncio.sleep(3)
                await warn.delete()
                await start_bot(client, message)
                return
    except Exception:
        if message.reply_to_message.message_id == dest_message_id[usr]:
            if str(message.text).startswith('-100') and message.text[1:].isdigit():
                bot_msg = await message.reply_text(text=Presets.WAIT_MSG)
                await asyncio.sleep(1)
                try:
                    if source_chat[usr] == message.text:
                        await message.delete()
                        await client.delete_messages(message.chat.id, dest_message_id[usr])
                        await bot_msg.edit(Presets.CHAT_DUPLICATED_MSG)
                        await asyncio.sleep(5)
                        await bot_msg.delete()
                        await start_bot(client, message)
                        return
                except Exception:
                    pass
                try:
                    member_status = await client.USER.get_chat_member(
                        chat_id=int(message.text),
                        user_id=int(user_bot_me.id)
                    )
                except Exception:
                    await client.delete_messages(message.chat.id, dest_message_id[usr])
                    await bot_msg.edit(text=Presets.IN_CORRECT_PERMISSIONS_MESSAGE_DEST_ADMIN)
                    await message.delete()
                    dest_message_id.pop(usr)
                    await asyncio.sleep(5)
                    await bot_msg.delete()
                    await start_bot(client, message)
                    return
                if member_status.can_post_messages == bool(1):
                    destination_chat[usr] = message.text
                    await client.delete_messages(message.chat.id, dest_message_id[usr])
                    await bot_msg.edit(Presets.DESTINATION_CONFIRM.format(destination_chat[usr]))
                    await message.delete()
                    dest_message_id.pop(usr)
                    await asyncio.sleep(2)
                    await start_bot(client, message)
                    return
                else:
                    await client.delete_messages(message.chat.id, dest_message_id[usr])
                    await bot_msg.edit(text=Presets.IN_CORRECT_PERMISSIONS_MESSAGE_DEST_POSTING)
                    await message.delete()
                    dest_message_id.pop(usr)
                    await asyncio.sleep(5)
                    await bot_msg.delete()
                    await start_bot(client, message)
                    return
        else:
            await client.delete_messages(message.chat.id, dest_message_id[usr])
            warn = await message.reply_text(Presets.INVALID_CHAT_ID)
            await message.delete()
            dest_message_id.pop(usr)
            await asyncio.sleep(3)
            await warn.delete()
            await start_bot(client, message)
            return


# ----------------------------- Help Function (How to use Bot) --------------------------- #
async def help_me(client: Bot, message: Message):
    usr = int(message.chat.id)
    msg_help = await message.reply_text(
        text=Presets.HELP_TEXT.format(message.from_user.first_name),
        parse_mode='html',
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="🏠 HOME 🏠️", callback_data="home_btn")]
            ]
        )
    )
    help_message_id[usr] = msg_help.message_id
    await asyncio.sleep(30)
    try:
        if help_message_id[usr] == msg_help.message_id:
            await msg_help.delete()
            await start_bot(client, message)
    except Exception:
        pass
