#----------------------------------- https://github.com/m4mallu/clonebot ----------------------------------------------#
import os
import csv
import time
import shutil
import asyncio
import itertools
from presets import Presets
from datetime import datetime
from library.sql import reset_all
from pyrogram.errors import FloodWait
from plugins.cb_input import update_type_buttons
from pyrogram.enums import ChatType, ChatMemberStatus
from library.sql import file_types, msg_id_limit, to_msg_id_cnf_db, master_index


# Function to find last message id of supported types
async def find_msg_id(client, id, chat_id):
    id_last_msg = int()
    try:
        async for user_message in client.USER.get_chat_history(chat_id):
            messages = await client.USER.get_messages(chat_id, user_message.id, replies=0)
            for file_type in file_types:
                media = getattr(messages, file_type, None)
                if media is not None:
                    id_last_msg = str(messages.id).split(" ")[0]
                    await msg_id_limit(id, id_last_msg)
                    await to_msg_id_cnf_db(id, id_last_msg)
                    file_types.clear()
                    file_types.extend(Presets.FILE_TYPES)
                    return
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception:
        pass


# Function to find percentage of the total process
async def calc_percentage(sp, ep, msg_id):
    const = pct = int()
    const = (ep - sp) + 1
    pct = ((msg_id + const) - ep) / const * 100  # Credits to my wife to find a formula !
    return pct


# Function to show the process graph
async def calc_progress(pct):
    progress = int()
    progress = (int(pct)//10 * "◼" + (10-int(pct)//10) * "◻")
    return progress


# Function to find DC ID:
async def find_dc(chat_status):
    dc = chat_status.dc_id
    dc_id = {dc == 1: "𝙼𝚒𝚊𝚖𝚒 𝙵𝙻, 𝚄𝚂𝙰 [𝐃𝐂 𝟏]", dc == 2: "𝙰𝚖𝚜𝚝𝚎𝚛𝚍𝚊𝚖, 𝙽𝙻 [𝐃𝐂 𝟐]", dc == 3: "𝙼𝚒𝚊𝚖𝚒 𝙵𝙻, 𝚄𝚂𝙰 [𝐃𝐂 𝟑]",
             dc == 4: "𝙰𝚖𝚜𝚝𝚎𝚛𝚍𝚊𝚖, 𝙽𝙻 [𝐃𝐂 𝟒]", dc == 5: "𝐒𝐢𝐧𝐠𝐚𝐩𝐨𝐫𝐞, 𝐒𝐆 [𝐃𝐂 𝟓]"}.get(True)
    return dc_id


# Function to save the target chat index.
async def save_target_cfg(id, target_chat):
    cfg_save_dir = os.getcwd() + "/" + "cfg" + "/" + str(id)
    if not os.path.isdir(cfg_save_dir):
        os.makedirs(cfg_save_dir)
    chat_id = str(target_chat).split('-100')[1]
    save_csv_path = cfg_save_dir + "/" + str(chat_id) + ".csv"
    with open(save_csv_path, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(master_index)


# Function to import the cfg data to master list
async def import_cfg_data(id, target_chat):
    chat_id = str(target_chat).split("-100")[1]
    cfg_file = os.getcwd() + "/" + "cfg" + "/" + str(id) + "/" + str(chat_id) + ".csv"
    with open(cfg_file, 'r') as file:
        read = list(csv.reader(file))
        index = list(itertools.chain.from_iterable(read))
        for i in index:
            master_index.append(i)
        try:
            os.remove(cfg_file)
        except Exception:
            pass


# Function to remove the cfg files stored by the user.
async def del_user_cfg(id):
    cfg_path = os.getcwd() + "/" + "cfg" + "/" + str(id)
    if os.path.exists(cfg_path):
        try:
            shutil.rmtree(cfg_path)
        except Exception:
            pass


# Function to calculate the time and date difference between two dates
async def date_time_calc(start_date, start_time, cur_date, cur_time):
    time_diff = time.strftime("%Hh %Mm", time.gmtime(cur_time - start_time))
    date_diff = (datetime.strptime(cur_date, "%d/%m/%y") - datetime.strptime(start_date, "%d/%m/%y")).days
    return f'{date_diff}D', time_diff


# Functions to set the bot vaiables to default values
async def set_to_defaults(id):
    await reset_all(id)
    file_types.clear()
    file_types.extend(Presets.FILE_TYPES)
    await update_type_buttons()


# function to get the chat type of the source/target chat
async def get_chat_type(chat_status):
    x = chat_status.type
    chat_status = {
                           x == ChatType.CHANNEL: 'CHANNEL',
                           x == ChatType.SUPERGROUP: 'SUPERGROUP',
                           x == ChatType.GROUP: 'GROUP',
                           x == ChatType.PRIVATE: 'PRIVATE',
                           x == ChatType.BOT: 'BOT'
    }.get(True)
    return chat_status


# Function to get the status of the chat member in groups and supergroups
async def get_chat_member_status(member):
    x = member.status
    chat_member_status = {
                           x == ChatMemberStatus.OWNER: 'OWNER',
                           x == ChatMemberStatus.ADMINISTRATOR: 'ADMINISTRATOR',
                           x == ChatMemberStatus.MEMBER: 'MEMBER',
                           x == ChatMemberStatus.RESTRICTED: 'RESTRICTED',
                           x == ChatMemberStatus.LEFT: 'LEFT',
                           x == ChatMemberStatus.BANNED: 'BANNED'
    }.get(True)
    return chat_member_status
