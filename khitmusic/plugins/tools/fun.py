import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from khitmusic import app as bot
import httpx
import config 

# Define missing variables locally to fix ModuleNotFoundError
SEX_IMAGES = ["https://telegra.ph/file/d30d11c4365c025c25e3e.jpg"]

command_to_category = {
    "neko": "neko",
    "shinobu": "shinobu",
    "megumin": "megumin",
    "bully": "bully",
    "cuddle": "cuddle",
    "cry": "cry",
    "hug": "hug",
    "awoo": "awoo",
    "kiss": "kiss",
    "lick": "lick",
    "pat": "pat",
    "smug": "smug",
    "bonk": "bonk",
    "yeet": "yeet",
    "blush": "blush",
    "smile": "smile",
    "wave": "wave",
    "highfive": "highfive",
    "handhold": "handhold",
    "nom": "nom",
    "bite": "bite",
    "glomp": "glomp",
    "slap": "slap",
    "kill": "kill",
    "happy": "happy",
    "wink": "wink",
    "poke": "poke",
    "dance": "dance",
    "cringe": "cringe",
}

async def delete_after(message: Message, delay: int = 600):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass
    
COMMAND_PREFIXES = ["/", "!", "."]
BASE_URL = config.BASE_URL

# Command handler for /hug
@bot.on_message(filters.command("hug" , prefixes=COMMAND_PREFIXES) & filters.group)
async def hug_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        msg = await message.reply_text("𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿'𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝘀𝗲𝗻𝗱 𝗮 𝗵𝘂𝗴 𝗿𝗲𝗾𝘂𝗲𝘀𝘁.")
        asyncio.create_task(delete_after(msg))
        return

    user_a = message.from_user

    if message.reply_to_message:
        user_b = message.reply_to_message.from_user
    else:
        username = message.command[1]
        try:
            user_b = await client.get_users(username)
        except Exception as e:
            msg = await message.reply_text(f"𝗖𝗼𝘂𝗹𝗱 𝗻𝗼𝘁 𝗳𝗶𝗻𝗱 𝘂𝘀𝗲𝗿 {username}.")
            asyncio.create_task(delete_after(msg))
            return

    # Check if the bot is replying to its own message
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        msg = await message.reply_text("𝑁𝑜 𝑡ℎ𝑎𝑛𝑘𝑠, 𝐼 𝑑𝑜𝑛'𝑡 𝑛𝑒𝑒𝑑 𝑎 ℎ𝑢𝑔 𝑟𝑖𝑔ℎ𝑡 𝑛𝑜𝑤.")
        asyncio.create_task(delete_after(msg))
        return

    if user_a.id == user_b.id:
        msg = await message.reply_text("𝑌𝑜𝑢 𝑐𝑎𝑛𝑛𝑜𝑡 𝑠𝑒𝑛𝑑 𝑎 ℎ𝑢𝑔 𝑟𝑒𝑞𝑢𝑒𝑠𝑡 𝑡𝑜 𝑦𝑜𝑢𝑟𝑠𝑒𝑙𝑓.")
        asyncio.create_task(delete_after(msg))
        return

    # Create inline button for User B to accept
    inline_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("𝗔𝗰𝗰𝗲𝗽𝘁", callback_data=f"accept_hug:{user_a.id}:{user_b.id}")]
        ]
    )

    # Send the hug request message
    msg = await message.reply_text(
        f"🤗 **[{user_b.first_name}](tg://user?id={user_b.id})**, **[{user_a.first_name}](tg://user?id={user_a.id})** wants to send you a hug! 🤗\n\n"
        "Will you accept the hug?",
        reply_markup=inline_keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    asyncio.create_task(delete_after(msg))

# Callback handler for accepting the hug
@bot.on_callback_query(filters.regex(r"^accept_hug:(\d+):(\d+)$"))
async def accept_hug_callback(client: Client, callback_query):
    data = callback_query.data.split(":")
    user_a_id = int(data[1])
    user_b_id = int(data[2])

    user_a = await client.get_users(user_a_id)
    user_b = await client.get_users(user_b_id)

    if callback_query.from_user.id != user_b.id:
        await callback_query.answer("𝗼𝗻𝗹𝘆 𝘁𝗵𝗲 𝗿𝗲𝗰𝗶𝗽𝗶𝗲𝗻𝘁 𝗰𝗮𝗻 𝗮𝗰𝗰𝗲𝗽𝘁 𝘁𝗵𝗶𝘀 𝗵𝘂𝗴 𝗿𝗲𝗾𝘂𝗲𝘀𝘁.", show_alert=True)
        return

    # Get a random hug image URL
    hug_image_url = await fetch_image("hug")

    # Delete the acceptance message with the inline button
    await callback_query.message.delete()

    # Send the hug accepted message with the image
    msg = await client.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=hug_image_url,
        caption=f"💞 **[{user_b.first_name}](tg://user?id={user_b.id})** accepted the hug from **[{user_a.first_name}](tg://user?id={user_a.id})**! 💞",
        parse_mode=ParseMode.MARKDOWN
    )
    asyncio.create_task(delete_after(msg))

    await callback_query.answer()

# Command handler for /kill
@bot.on_message(filters.command("kill"  , prefixes=COMMAND_PREFIXES) & filters.group)
async def kill_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        msg = await message.reply_text("𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿'𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝗸𝗶𝗹𝗹 𝘁𝗵𝗲𝗺.")
        asyncio.create_task(delete_after(msg))
        return

    user_a = message.from_user

    if message.reply_to_message:
        user_b = message.reply_to_message.from_user
    else:
        username = message.command[1]
        try:
            user_b = await client.get_users(username)
        except Exception as e:
            msg = await message.reply_text(f"Could not find user {username}.")
            asyncio.create_task(delete_after(msg))
            return

    # Check if the bot is being killed
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        msg = await message.reply_text("You can't kill a bot! 🛡️")
        asyncio.create_task(delete_after(msg))
        return

    if user_a.id == user_b.id:
        msg = await message.reply_text("You can't kill yourself. That's a bit dramatic.")
        asyncio.create_task(delete_after(msg))
        return

    # Get a random kill image URL
    kill_image_url = await fetch_image("kill")

    # Send the kill message with the image
    msg = await client.send_photo(
        chat_id=message.chat.id,
        photo=kill_image_url,
        caption=f"💀 **[{user_a.first_name}](tg://user?id={user_a.id})** has killed **[{user_b.first_name}](tg://user?id={user_b.id})**! 😱",
        parse_mode=ParseMode.MARKDOWN
    )
    asyncio.create_task(delete_after(msg))

# Command handler for /kiss
@bot.on_message(filters.command("kiss"  , prefixes=COMMAND_PREFIXES) & filters.group)
async def kiss_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        msg = await message.reply_text("𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿'𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝘀𝗲𝗻𝗱 𝗮 𝗸𝗶𝘀𝘀 𝗿𝗲𝗾𝘂𝗲𝘀𝘁.")
        asyncio.create_task(delete_after(msg))
        return

    user_a = message.from_user

    if message.reply_to_message:
        user_b = message.reply_to_message.from_user
    else:
        username = message.command[1]
        try:
            user_b = await client.get_users(username)
        except Exception as e:
            msg = await message.reply_text(f"Could not find user {username}.")
            asyncio.create_task(delete_after(msg))
            return

    # Check if the bot is replying to its own message
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        msg = await message.reply_text("Get lost!, I don't want a kiss from you.")
        asyncio.create_task(delete_after(msg))
        return

    if user_a.id == user_b.id:
        msg = await message.reply_text("Why are you single? You know, nowadays everyone is committed except you!")
        asyncio.create_task(delete_after(msg))
        return

    # Create inline button for User B to accept
    inline_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("𝗔𝗰𝗰𝗲𝗽𝘁", callback_data=f"accept_kiss:{user_a.id}:{user_b.id}")]
        ]
    )

    # Send the kiss request message
    msg = await message.reply_text(
        f"💞 **[{user_b.first_name}](tg://user?id={user_b.id})** see **[{user_a.first_name}](tg://user?id={user_a.id})** wants to kiss you! 💞\n\n"
        "Will you accept the kiss?",
        reply_markup=inline_keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    asyncio.create_task(delete_after(msg))

# Callback handler for accepting the kiss
@bot.on_callback_query(filters.regex(r"^accept_kiss:(\d+):(\d+)$"))
async def accept_kiss_callback(client: Client, callback_query):
    data = callback_query.data.split(":")
    user_a_id = int(data[1])
    user_b_id = int(data[2])

    user_a = await client.get_users(user_a_id)
    user_b = await client.get_users(user_b_id)

    if callback_query.from_user.id != user_b.id:
        await callback_query.answer("𝗼𝗻𝗹𝘆 𝘁𝗵𝗲 𝗿𝗲𝗰𝗶𝗽𝗶𝗲𝗻𝘁 𝗰𝗮𝗻 𝗮𝗰𝗰𝗲𝗽𝘁 𝘁𝗵𝗶𝘀 𝗸𝗶𝘀𝘀 𝗿𝗲𝗾𝘂𝗲𝘀𝘁.", show_alert=True)
        return

    # Get a random kiss image URL
    kiss_image_url = await fetch_image("kiss")

    # Delete the acceptance message with the inline button
    await callback_query.message.delete()

    # Send the kiss accepted message with the image
    msg = await client.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=kiss_image_url,
        caption=f"💓 **[{user_b.first_name}](tg://user?id={user_b.id})** accepted the kiss from **[{user_a.first_name}](tg://user?id={user_a.id})**! 💓",
        parse_mode=ParseMode.MARKDOWN
    )
    asyncio.create_task(delete_after(msg))

    await callback_query.answer()

# Command handler for /pat
@bot.on_message(filters.command("pat"  , prefixes=COMMAND_PREFIXES) & filters.group)
async def pat_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        msg = await message.reply_text("𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿'𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝗽𝗮𝘁 𝘁𝗵𝗲𝗺.")
        asyncio.create_task(delete_after(msg))
        return

    user_a = message.from_user

    if message.reply_to_message:
        user_b = message.reply_to_message.from_user
    else:
        username = message.command[1]
        try:
            user_b = await client.get_users(username)
        except Exception as e:
            msg = await message.reply_text(f"Could not find user {username}.")
            asyncio.create_task(delete_after(msg))
            return

    # Check if the bot is being patted
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        msg = await message.reply_text("You can't pat a bot, but thanks for the gesture!")
        asyncio.create_task(delete_after(msg))
        return

    if user_a.id == user_b.id:
        msg = await message.reply_text("You can't pat yourself. You deserve pats from others!")
        asyncio.create_task(delete_after(msg))
        return

    # Get a random pat image URL
    pat_image_url = await fetch_image("pat")

    # Send the pat message with the image
    msg = await client.send_photo(
        chat_id=message.chat.id,
        photo=pat_image_url,
        caption=f"🤗 **[{user_a.first_name}](tg://user?id={user_a.id})** gave a warm pat to **[{user_b.first_name}](tg://user?id={user_b.id})**! So sweet! 💖",
        parse_mode=ParseMode.MARKDOWN
    )
    asyncio.create_task(delete_after(msg))


# Command handler for /sex
@bot.on_message(filters.command("sex"  , prefixes=COMMAND_PREFIXES) & filters.group)
async def sex_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        msg = await message.reply_text("𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿'𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝘀𝗲𝗻𝗱 𝗮 𝘀𝗲𝘅 𝗿𝗲𝗾𝘂𝗲𝘀𝘁.")
        asyncio.create_task(delete_after(msg))
        return

    user_a = message.from_user

    if message.reply_to_message:
        user_b = message.reply_to_message.from_user
    else:
        username = message.command[1]
        try:
            user_b = await client.get_users(username)
        except Exception as e:
            msg = await message.reply_text(f"Could not find user {username}.")
            asyncio.create_task(delete_after(msg))
            return

    # Check if the bot is the target of the request
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        msg = await message.reply_text("Get lost, I don't want to have sex with you.")
        asyncio.create_task(delete_after(msg))
        return

    if user_a.id == user_b.id:
        msg = await message.reply_text("Why are you single? You know, nowadays everyone is committed except you!")
        asyncio.create_task(delete_after(msg))
        return

    # Create inline button for User B to accept
    inline_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("𝗔𝗰𝗰𝗲𝗽𝘁", callback_data=f"accept_sex:{user_a.id}:{user_b.id}")]
        ]
    )

    # Send the sex request message
    msg = await message.reply_text(
        f"💞 **[{user_b.first_name}](tg://user?id={user_b.id})** see **[{user_a.first_name}](tg://user?id={user_a.id})** wants to have sex with you! 💞\n\n"
        "Will you accept?",
        reply_markup=inline_keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    asyncio.create_task(delete_after(msg))

# Callback handler for accepting the sex request
@bot.on_callback_query(filters.regex(r"^accept_sex:(\d+):(\d+)$"))
async def accept_sex_callback(client: Client, callback_query):
    data = callback_query.data.split(":")
    user_a_id = int(data[1])
    user_b_id = int(data[2])

    user_a = await client.get_users(user_a_id)
    user_b = await client.get_users(user_b_id)

    if callback_query.from_user.id != user_b.id:
        await callback_query.answer("Only the recipient can accept this sex request.", show_alert=True)
        return

    # Get a random sex image URL
    sex_image_url = random.choice(SEX_IMAGES)

    # Delete the acceptance message with the inline button
    await callback_query.message.delete()

    # Send the sex accepted message with the image
    msg = await client.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=sex_image_url,
        caption=f"💓 **[{user_b.first_name}](tg://user?id={user_b.id})** had done sex with **[{user_a.first_name}](tg://user?id={user_a.id})**! 💓\n\nWhat do you think will they have a baby ?..",
        parse_mode=ParseMode.MARKDOWN
    )
    asyncio.create_task(delete_after(msg))

    await callback_query.answer()



# Command handler for /slap
@bot.on_message(filters.command("slap"  , prefixes=COMMAND_PREFIXES) & filters.group)
async def slap_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        msg = await message.reply_text("𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿'𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝘀𝗹𝗮𝗽 𝘁𝗵𝗲𝗺.")
        asyncio.create_task(delete_after(msg))
        return

    user_a = message.from_user

    if message.reply_to_message:
        user_b = message.reply_to_message.from_user
    else:
        username = message.command[1]
        try:
            user_b = await client.get_users(username)
        except Exception as e:
            msg = await message.reply_text(f"𝖢𝗈𝗎𝗅𝖽 𝗇𝗈𝗍 𝖿𝗂𝗇𝖽 𝗎𝗌𝖾𝗋 {username}.")
            asyncio.create_task(delete_after(msg))
            return

    # Check if the bot is being slapped
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        msg = await message.reply_text("𝖧𝖾𝗒, 𝖽𝗈𝗇'𝗍 𝗌𝗅𝖺𝗉 𝗆𝖾! 𝖨'𝗆 𝗃𝗎𝗌𝗍 𝖺 𝖻𝗈𝗍.")
        asyncio.create_task(delete_after(msg))
        return

    if user_a.id == user_b.id:
        msg = await message.reply_text("𝖸𝗈𝗎 𝖼𝖺𝗇𝗇𝗈𝗍 𝗌𝗅𝖺𝗉 𝗒𝗈𝗎𝗋𝗌𝖾𝗅𝖿. 𝖳𝗁𝖺𝗍'𝗌 𝗐𝖾𝗂𝗋𝖽.")
        asyncio.create_task(delete_after(msg))
        return

    # Get a random slap image URL
    slap_image_url = await fetch_image("slap")

    # Send the slap message with the image
    msg = await client.send_photo(
        chat_id=message.chat.id,
        photo=slap_image_url,
        caption=f"👋 **[{user_a.first_name}](tg://user?id={user_a.id})** slapped **[{user_b.first_name}](tg://user?id={user_b.id})**! That must've hurt! 💥",
        parse_mode=ParseMode.MARKDOWN
    )
    asyncio.create_task(delete_after(msg))
    

# Function to fetch the image from the API
async def fetch_image(category: str) -> str:
    """Fetch an image URL from the waifu.pics API."""
    url = f"{BASE_URL}/sfw/{category}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise HTTP exceptions for non-2xx status codes
            data = response.json()
            return data.get("url", None)
    except httpx.RequestError as e:
        return None
    except ValueError as e:
        return None
    except Exception as e:
        return None

# Separate commands that have interactive handlers (group only) from those that don't.
# Interactive commands should only trigger the generic handler in private chats.
interactive_cmds = ["hug", "kill", "kiss", "pat", "slap"]
interactive_in_keys = [c for c in command_to_category.keys() if c in interactive_cmds]
other_cmds = [c for c in command_to_category.keys() if c not in interactive_cmds]

@bot.on_message(filters.command(other_cmds, prefixes=COMMAND_PREFIXES) | (filters.command(interactive_in_keys, prefixes=COMMAND_PREFIXES) & filters.private))
async def send_waifu_image(client: Client, message: Message):
    """Send an image for the requested category."""
    # Extract command and resolve the category
    command = message.command[0].lower()
    category = command_to_category.get(command, command)  # Get mapped category or fallback to the command itself

    try:
        image_url = await fetch_image(category)
        if image_url:
            msg = await message.reply_photo(photo=image_url)
            asyncio.create_task(delete_after(msg))
        else:
            msg = await message.reply_text(
                f"𝖲𝗈𝗋𝗋𝗒, 𝖨 𝖼𝗈𝗎𝗅𝖽𝗇'𝗍 𝖿𝖾𝗍𝖼𝗁 𝖺𝗇 𝗂𝗆𝖺𝗀𝖾 𝖿𝗈𝗋 '{𝖼𝖺𝗍𝖾𝗀𝗈𝗋𝗒}'. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗍𝗋𝗒 𝖺𝗀𝖺𝗂𝗇 𝗅𝖺𝗍𝖾𝗋."
            )
            asyncio.create_task(delete_after(msg))
    except Exception as e:
        msg = await message.reply_text(
            "𝖠𝗇 𝗎𝗇𝖾𝗑𝗉𝖾𝖼𝗍𝖾𝖽 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗍𝗋𝗒 𝖺𝗀𝖺𝗂𝗇 𝗅𝖺𝗍𝖾𝗋 𝗈𝗋 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗍𝗁𝖾 𝖻𝗈𝗍 𝖺𝖽𝗆𝗂𝗇."
        )
        asyncio.create_task(delete_after(msg))
    
__module__ = "𝖥𝗎𝗇"


__help__ = """**𝖴𝗌𝖾𝗋 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:**
   ✧ `/𝗇𝖾𝗄𝗈`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗇𝖾𝗄𝗈 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗌𝗁𝗂𝗇𝗈𝖻𝗎`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖲𝗁𝗂𝗇𝗈𝖻𝗎 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗆𝖾𝗀𝗎𝗆𝗂𝗇`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖬𝖾𝗀𝗎𝗆𝗂𝗇 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝖻𝗎𝗅𝗅𝗒`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖻𝗎𝗅𝗅𝗒 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝖼𝗎𝖽𝖽𝗅𝖾`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖼𝗎𝖽𝖽𝗅𝖾 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝖼𝗋𝗒`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖼𝗋𝗒 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗁𝗎𝗀`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗁𝗎𝗀 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝖺𝗐𝗈𝗈`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖺𝗐𝗈𝗈 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗄𝗂𝗌𝗌`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗄𝗂𝗌𝗌 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗅𝗂𝖼𝗄`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗅𝗂𝖼𝗄 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗉𝖺𝗍`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗉𝖺𝗍 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗌𝗆𝗎𝗀`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗌𝗆𝗎𝗀 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝖻𝗈𝗇𝗄`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖻𝗈𝗇𝗄 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗒𝖾𝖾𝗍`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗒𝖾𝖾𝗍 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝖻𝗅𝗎𝗌𝗁`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖻𝗅𝗎𝗌𝗁 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗌𝗆𝗂𝗅𝖾`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗌𝗆𝗂𝗅𝖾 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗐𝖺𝗏𝖾`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗐𝖺𝗏𝖾 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗁𝗂𝗀𝗁𝖿𝗂𝗏𝖾`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗁𝗂𝗀𝗁-𝖿𝗂𝗏𝖾 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗁𝖺𝗇𝖽𝗁𝗈𝗅𝖽`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗁𝖺𝗇𝖽-𝗁𝗈𝗅𝖽𝗂𝗇𝗀 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗇𝗈𝗆`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗇𝗈𝗆 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝖻𝗂𝗍𝖾`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖻𝗂𝗍𝖾 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗀𝗅𝗈𝗆𝗉`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗀𝗅𝗈𝗆𝗉 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗌𝗅𝖺𝗉`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗌𝗅𝖺𝗉 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗄𝗂𝗅𝗅`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗄𝗂𝗅𝗅 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗁𝖺𝗉𝗉𝗒`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗁𝖺𝗉𝗉𝗒 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗐𝗂𝗇𝗄`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗐𝗂𝗇𝗄 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝗉𝗈𝗄𝖾`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝗉𝗈𝗄𝖾 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝖽𝖺𝗇𝖼𝖾`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖽𝖺𝗇𝖼𝖾 𝗂𝗆𝖺𝗀𝖾.
   ✧ `/𝖼𝗋𝗂𝗇𝗀𝖾`**:** 𝖥𝖾𝗍𝖼𝗁𝖾𝗌 𝖺 𝗋𝖺𝗇𝖽𝗈𝗆 𝖼𝗋𝗂𝗇𝗀𝖾 𝗂𝗆𝖺𝗀𝖾.
 
𝖴𝗌𝖾 𝗍𝗁𝖾𝗌𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽𝗌 𝗍𝗈 𝗀𝖾𝗍 𝗋𝖺𝗇𝖽𝗈𝗆 𝖺𝗇𝗂𝗆𝖾-𝗌𝗍𝗒𝗅𝖾 𝗂𝗆𝖺𝗀𝖾𝗌
"""
