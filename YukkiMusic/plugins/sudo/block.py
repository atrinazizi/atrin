from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import add_gban_user, remove_gban_user
from YukkiMusic.utils.decorators.language import language

# Command
BLOCK_COMMAND = get_command("BLOCK_COMMAND")
UNBLOCK_COMMAND = get_command("UNBLOCK_COMMAND")
BLOCKED_COMMAND = get_command("BLOCKED_COMMAND")


@app.on_message(filters.command(BLOCK_COMMAND , prefixes=["", "/"]) & SUDOERS)
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in BANNED_USERS:
            return await message.reply_text(_["block_1"].format(user.mention))
        await add_gban_user(user.id)
        BANNED_USERS.add(user.id)
        await message.reply_text(_["block_2"].format(user.mention))
        return
    if message.reply_to_message.from_user.id in BANNED_USERS:
        return await message.reply_text(
            _["block_1"].format(message.reply_to_message.from_user.mention)
        )
    await add_gban_user(message.reply_to_message.from_user.id)
    BANNED_USERS.add(message.reply_to_message.from_user.id)
    await message.reply_text(
        _["block_2"].format(message.reply_to_message.from_user.mention)
    )


@app.on_message(filters.command(UNBLOCK_COMMAND , prefixes=["", "/"]) & SUDOERS)
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in BANNED_USERS:
            return await message.reply_text(_["block_3"])
        await remove_gban_user(user.id)
        BANNED_USERS.remove(user.id)
        await message.reply_text(_["block_4"])
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in BANNED_USERS:
        return await message.reply_text(_["block_3"])
    await remove_gban_user(user_id)
    BANNED_USERS.remove(user_id)
    await message.reply_text(_["block_4"])


@app.on_message(filters.command(BLOCKED_COMMAND , prefixes=["", "/"]) & SUDOERS)
@language
async def sudoers_list(client, message: Message, _):
    if not BANNED_USERS:
        return await message.reply_text(_["block_5"])
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    for users in BANNED_USERS:
        try:
            user = await app.get_users(users)
            user = user.first_name if not user.mention else user.mention
            count += 1
        except Exception:
            continue
        msg += f"{count}➤ {user}\n"
    if count == 0:
        return await mystic.edit_text(_["block_5"])
    else:
        return await mystic.edit_text(msg)


__MODULE__ = "لیست مسدود"
__HELP__ = """
<b>✧ /blacklistchat</b> [آیدی چت] - مسدود کردن هر چت از استفاده از ربات موزیک
<b>✧ /whitelistchat</b> [آیدی چت] - لیست سفید کردن هر چت مسدود شده از استفاده از ربات موزیک
<b>✧ /blacklistedchat</b> - بررسی تمام چت‌های مسدود شده.

<b>✧ /block</b> [نام کاربری یا پاسخ به یک کاربر] - جلوگیری از استفاده یک کاربر از دستورات ربات.
<b>✧ /unblock</b> [نام کاربری یا پاسخ به یک کاربر] - حذف یک کاربر از لیست مسدودشدگان ربات.
<b>✧ /blockedusers</b> - بررسی لیست کاربران مسدود شده.

<b>✧ /gban</b> [نام کاربری یا پاسخ به یک کاربر] - مسدود کردن یک کاربر از چت‌های سرو شده ربات و جلوگیری از استفاده او از ربات شما.
<b>✧ /ungban</b> [نام کاربری یا پاسخ به یک کاربر] - حذف یک کاربر از لیست مسدودشدگان ربات و اجازه استفاده او از ربات شما.
<b>✧ /gbannedusers</b> - بررسی لیست کاربران مسدود شده به صورت جهانی.
"""
