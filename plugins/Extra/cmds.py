import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from utils import is_check_admin
from Script import script
from info import ADMINS, admin_cmds, cmds


@Client.on_message(filters.command('grp_cmds'))
async def grp_cmds(client, message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        return await message.reply("<b>💔 ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ...</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<code>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.</code>")
    grp_id = message.chat.id
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    #title = message.chat.title
    buttons = [[
                InlineKeyboardButton('❌ ᴄʟᴏsᴇ ❌', callback_data='close_data')
            ]]        
    await message.reply_text(
        text=script.GROUP_C_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
        )
    

@Client.on_message(filters.command("admin_cmds") & filters.user(ADMINS))
async def admin_cmds(client, message):
    buttons = []
    for i in range(0, len(admin_cmds), 2):
        if i + 1 < len(admin_cmds):
            buttons.append([KeyboardButton(vp[i]), KeyboardButton(vp[i + 1])])
        else:
            buttons.append([KeyboardButton(vp[i])])

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
   
    sent_message = await message.reply(
        "<b>Admin All Commands [auto delete 2 min] 👇</b>",
        reply_markup=reply_markup,
    ) 
    #  2 minutes (120 seconds)
    await asyncio.sleep(120)
    await sent_message.delete()
    await message.delete()


@Client.on_message(filters.command("commands") & filters.user(ADMINS))
async def set_commands(client, message):
    commands = []
    for item in vp:
        for command, description in item.items():
            commands.append(BotCommand(command, description))

    await client.set_bot_commands(commands)
    await message.reply("Set command successfully✅ ")
