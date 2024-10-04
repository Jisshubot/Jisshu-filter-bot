# powered by Jisshu_bots and ZISHAN KHAN
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("link"))
async def generate_link(client, message):
    command_text = message.text.split(maxsplit=1)
    if len(command_text) < 2:
        await message.reply("Please provide the name for the movie! Example: `/link game of thrones`")
        return
    movie_name = command_text[1].replace(" ", "-")
    link = f"https://telegram.me/NehaTestBot?start=getfile-{movie_name}"
    
    await message.reply(
        text=f"Here is your link: {link}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={link}")]]
        )
    )
