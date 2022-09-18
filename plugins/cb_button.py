# ----------------------------------- https://github.com/m4mallu/clonebot ---------------------------------------------#
import sys
from bot import Bot
from library.sql import *
from presets import Presets
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from plugins.clone import clone_medias
from pyrogram.types import CallbackQuery
from library.chat_support import del_user_cfg
from plugins.cb_input import update_type_buttons
from plugins.commands import reply_markup_home
from plugins.index_files import index_target_chat, purge_media

if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


@Client.on_callback_query(filters.regex(r'^start_btn$'))
async def start_settings(client: Bot, cb: CallbackQuery):
    user = await Bot.get_me(self=client.USER)
    id = int(cb.from_user.id)
    if id != int(user.id):
        await cb.answer(Presets.NOT_AUTH_TEXT, show_alert=True)
        return
    await add_user(id)
    await cb.answer()
    try:
        await cb.message.edit_text(Presets.WELCOME_TEXT,
                                   reply_markup=reply_markup_home,
                                   parse_mode=ParseMode.MARKDOWN
                                   )
    except Exception:
        pass


@Client.on_callback_query(filters.regex(r'^view_btn$'))
async def view_chat_config(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    query = await query_msg(id)
    a = str(query.s_chat)
    b = str(query.d_chat)
    c = str(query.from_id)
    d = str(query.to_id)
    e = bool(query.delayed_clone)
    f = bool(query.caption)
    g = bool(query.file_caption)
    captn = str()
    if id in custom_caption:
        captn = "Custom Caption"
    elif g is True:
        captn = "FNAC"
    elif f is True:
        captn = "Default Caption"
    else:
        captn = "No Caption"
    await cb.answer(text=Presets.VIEW_CONF.format(
        a if bool(query.s_chat) else "❎",
        b if bool(query.d_chat) else "❎",
        c if bool(query.from_id) else "1",
        d if bool(query.to_id) else "❎",
        "✅" if e is True else "❎",
        captn
    ), show_alert=True)


@Client.on_callback_query(filters.regex(r'^delay_btn$'))
async def delayed_clone(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    query = await query_msg(id)
    status = bool(query.delayed_clone)
    if status is True:
        await change_delay(id)
        await cb.answer(Presets.DELAY_OFF, True)
    else:
        await change_delay(id)
        await cb.answer(Presets.DELAY_ON, True)


@Client.on_callback_query(filters.regex(r'^caption_btn$'))
async def file_caption(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    query = await query_msg(id)
    status = bool(query.caption)
    if id in custom_caption:
        await cb.answer(Presets.CAPTION_ERROR, True)
        return
    else:
        if status is True:
            await opt_caption(id)
            await cb.answer(Presets.CAPTION_OFF, True)
        else:
            await opt_caption(id)
            await cb.answer(Presets.CAPTION_ON, True)


@Client.on_callback_query(filters.regex(r'^f_caption_btn$'))
async def file_name_caption(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    query = await query_msg(id)
    status = bool(query.file_caption)
    if id in custom_caption:
        await cb.answer(Presets.CAPTION_ERROR, True)
        return
    else:
        if status is True:
            await opt_FN_caption(id)
            await cb.answer(Presets.FN_AS_CAPT_OFF, True)
        else:
            await opt_FN_caption(id)
            await cb.answer(Presets.FN_AS_CAPT_ON, True)


@Client.on_callback_query(filters.regex(r'^view_types$'))
async def view_file_types(client: Bot, cb: CallbackQuery):
    await cb.answer(Presets.SELECTED_TYPE.format("🟡" if "document" in file_types else "🚫",
                                                 "🟡" if "audio" in file_types else "🚫",
                                                 "🟡" if "video" in file_types else "🚫",
                                                 "🟡" if "photo" in file_types else "🚫",
                                                 "🟡" if "voice" in file_types else "🚫",
                                                 "🟡" if "text" in file_types else "🚫",
                                                 ),
                    True
                    )


@Client.on_callback_query(filters.regex(r'^terminate_btn$'))
async def terminate_bot(client: Bot, cb: CallbackQuery):
    await cb.answer(Presets.TERMINATED_MSG, True)
    await cb.message.delete()
    sys.exit()


@Client.on_callback_query(filters.regex(r'^clear_btn$'))
async def clear_button(client: Bot, cb: CallbackQuery):
    try:
        if cb.message.reply_markup:
            await cb.message.edit_reply_markup(None)
    except Exception:
        pass


@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close(client: Bot, cb: CallbackQuery):
    await cb.message.delete()


@Client.on_callback_query(filters.regex(r'^rst_btn$'))
async def reset_settings(client: Bot, cb: CallbackQuery):
    file_types.clear()
    id = int(cb.from_user.id)
    file_types.extend(Presets.FILE_TYPES)
    await reset_all(id)
    await cb.answer(Presets.RST_MSG, True)
    await del_user_cfg(id)
    await update_type_buttons()


@Client.on_callback_query(filters.regex(r'^stop_clone$'))
async def stop_process(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    try:
        clone_cancel_key.pop(id)
    except Exception:
        pass
    await cb.answer(Presets.CLONE_REPORT_INFO, True)


# Call back function for clone: Random button clicks avoided
@Client.on_callback_query(filters.regex(r'^clone_btn$'))
async def clone(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    query = await query_msg(id)
    msg_a = int(query.s_chat)
    msg_b = int(query.d_chat)
    if str(msg_a).startswith('0') or str(msg_b).startswith("0"):
        await cb.answer(Presets.NOT_CONFIGURED, True)
        return
    else:
        if id in clone_btn_count:
            try:
                clone_btn_count.pop(id)
                await index_target_chat(client, cb.message)
            except Exception:
                pass


@Client.on_callback_query(filters.regex(r'^index_skip_btn$'))
async def skip_indexing(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    try:
        index_skip_key.pop(id)
    except Exception as e:
        pass


@Client.on_callback_query(filters.regex(r'^purge_skip_btn$'))
async def skip_purging(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    try:
        purge_skip_key.pop(id)
    except Exception:
        pass


@Client.on_callback_query(filters.regex(r'^purge_no_btn$'))
async def purge_no(client: Bot, cb: CallbackQuery):
    await clone_medias(client, cb.message)


@Client.on_callback_query(filters.regex(r'^purge_yes_btn$'))
async def purge_yes(client: Bot, cb: CallbackQuery):
    await purge_media(client, cb.message)


@Client.on_callback_query(filters.regex(r'^restart_btn$'))
async def restart_bot(client: Bot, cb: CallbackQuery):
    session = await client.USER.get_me()
    if cb.from_user.id == int(session.id):
        await cb.answer(Presets.RESTART_MSG, True)
        await cb.message.delete()
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        await cb.answer(Presets.RESTART_MSG_ERROR, True)


@Client.on_callback_query(filters.regex(r'^cust_captn_btn$'))
async def set_custom_caption(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    if id not in custom_caption:
        await cb.answer(Presets.CUSTOM_CAPTION_MSG, True)
    else:
        await cb.answer(Presets.CUSTOM_CAPTION_MSG_CLR, True)
        custom_caption.pop(id)


@Client.on_callback_query(filters.regex(r'^capt_cnf_yes_btn$'))
async def caption_yes_button(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    caption_text = str(cb.message.reply_to_message.text.html)
    if caption_text:
        custom_caption[id] = caption_text
        await cb.answer(Presets.CUSTOM_CAPTION_CNF, True)
        await cb.message.reply_to_message.delete()
        await cb.message.delete()

@Client.on_callback_query(filters.regex(r'^capt_cnf_no_btn$'))
async def caption_no_button(client: Bot, cb: CallbackQuery):
    await cb.message.reply_to_message.delete()
    await cb.message.delete()
