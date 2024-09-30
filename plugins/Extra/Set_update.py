from pyrogram import Client, filters , enums
from info import ADMINS
import re
from database.users_chats_db import db

@Client.on_message(filters.command("set_muc") & filters.user(ADMINS))
async def set_muc_id(client, message):
    try:
        id = message.command[1]
        if id and str(id).startswith('-100') and len(str(id)) == 14:
            is_suc = await db.movies_update_channel_id(id)
            if is_suc:
                await message.reply("Successfully set movies update  channel id : " + id)
            else:
                await message.reply("Failed to set movies update channel id : " + id)
        else:
            await message.reply("Invalid channel id : " + id)
    except Exception as e:
        print('Err in set_muc_id', e)
        await message.reply("Failed to set movies channel id! Because : " + str(e))

