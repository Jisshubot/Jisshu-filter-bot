from pyrogram import Client, filters
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
from utils import users_broadcast, groups_broadcast, temp, get_readable_time
import asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup 

lock = asyncio.Lock()

@Client.on_callback_query(filters.regex(r'^broadcast_cancel'))
async def broadcast_cancel(bot, query):
    _, ident = query.data.split("#")
    if ident == 'users':
        await query.message.edit("ᴛʀʏɪɴɢ ᴛᴏ ᴄᴀɴᴄᴇʟ ᴜsᴇʀs ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...")
        temp.USERS_CANCEL = True
    elif ident == 'groups':
        temp.GROUPS_CANCEL = True
        await query.message.edit("ᴛʀʏɪɴɢ ᴛᴏ ᴄᴀɴᴄᴇʟ ɢʀᴏᴜᴘs ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...")
       
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_users(bot, message):
    try:
        # Check if lock is active
        if lock.locked():
            return await message.reply('Currently broadcast processing, wait for it to complete.')

        # Ask if message should be pinned
        msg = await message.ask(
            '<b>Do you want to pin this message to users?</b>',
            reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True, resize_keyboard=True)
        )
        if msg.text == 'Yes':
            is_pin = True
        elif msg.text == 'No':
            is_pin = False
        else:
            return await message.reply('Wrong Response!')

        await msg.delete()

        # Fetch users
        users = await db.get_all_users()
        total_users = await db.total_users_count()
        b_msg = message.reply_to_message

        b_sts = await message.reply_text('<b>Broadcasting your message to users ⌛️</b>')
        start_time = time.time()
        done = success = failed = 0

        async with lock:
            async for user in users:
                try:
                    time_taken = get_readable_time(time.time() - start_time)

                    # Handle cancellation
                    if temp.USERS_CANCEL:
                        temp.USERS_CANCEL = False
                        await b_sts.edit(
                            f"Broadcast cancelled!\nCompleted in {time_taken}\n\n"
                            f"Total Users: <code>{total_users}</code>\n"
                            f"Completed: <code>{done} / {total_users}</code>\n"
                            f"Success: <code>{success}</code>"
                        )
                        return

                    # Broadcast to user
                    sts = await users_broadcast(int(user['id']), b_msg, is_pin)
                    if sts == 'Success':
                        success += 1
                    else:
                        failed += 1

                    done += 1

                    # Update status message every 20 users
                    if done % 20 == 0:
                        btn = [[InlineKeyboardButton('CANCEL', callback_data='broadcast_cancel#users')]]
                        await b_sts.edit(
                            f"Broadcast in progress...\n\n"
                            f"Total Users: <code>{total_users}</code>\n"
                            f"Completed: <code>{done} / {total_users}</code>\n"
                            f"Success: <code>{success}</code>",
                            reply_markup=InlineKeyboardMarkup(btn)
                        )

                except Exception as e:
                    logger.error(f"Failed to broadcast to user {user['id']}: {e}")
                    failed += 1

        # Final status update
        time_taken = get_readable_time(time.time() - start_time)
        await b_sts.edit(
            f"Broadcast completed.\nCompleted in {time_taken}\n\n"
            f"Total Users: <code>{total_users}</code>\n"
            f"Completed: <code>{done} / {total_users}</code>\n"
            f"Success: <code>{success}</code>"
        )

    except Exception as e:
        logger.exception(f"Error in broadcast command: {e}")
        await message.reply(f"An error occurred: {e}")
        
@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_group(bot, message):
    msg = await message.ask('<b>Do you want pin this message in groups?</b>', reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True, resize_keyboard=True))
    if msg.text == 'Yes':
        is_pin = True
    elif msg.text == 'No':
        is_pin = False
    else:
        return await msg.edit('Wrong Response!')
    await msg.delete()
    chats = await db.get_all_chats()
    b_msg = message.reply_to_message
    b_sts = await message.reply_text(text='<b>ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ʏᴏᴜʀ ᴍᴇssᴀɢᴇs ᴛᴏ ɢʀᴏᴜᴘs ⏳</b>')
    start_time = time.time()
    total_chats = await db.total_chat_count()
    done = 0
    failed = 0
    success = 0
    
    async with lock:
        async for chat in chats:
            time_taken = get_readable_time(time.time()-start_time)
            if temp.GROUPS_CANCEL:
                temp.GROUPS_CANCEL = False
                await b_sts.edit(f"Groups broadcast Cancelled!\nCompleted in {time_taken}\n\nTotal Groups: <code>{total_chats}</code>\nCompleted: <code>{done} / {total_chats}</code>\nSuccess: <code>{success}</code>\nFailed: <code>{failed}</code>")
                return
            sts = await groups_broadcast(int(chat['id']), b_msg, is_pin)
            if sts == 'Success':
                success += 1
            elif sts == 'Error':
                failed += 1
            done += 1
            if not done % 20:
                btn = [[
                    InlineKeyboardButton('CANCEL', callback_data=f'broadcast_cancel#groups')
                ]]
                await b_sts.edit(f"Groups groadcast in progress...\n\nTotal Groups: <code>{total_chats}</code>\nCompleted: <code>{done} / {total_chats}</code>\nSuccess: <code>{success}</code>\nFailed: <code>{failed}</code>", reply_markup=InlineKeyboardMarkup(btn))    
        await b_sts.edit(f"Groups broadcast completed.\nCompleted in {time_taken}\n\nTotal Groups: <code>{total_chats}</code>\nCompleted: <code>{done} / {total_chats}</code>\nSuccess: <code>{success}</code>\nFailed: <code>{failed}</code>")
        
