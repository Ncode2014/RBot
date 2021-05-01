# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio

from faker import Faker
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.genadd(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    cc = Faker()
    name = cc.name()
    adre = cc.address()
    zipcd = cc.zipcode

    await edit_or_reply(
        event,
        f"__**👤 NAME :- **__\n`{name}`\n\n__**🏡 ADDRESS :- **__\n`{adre}`\n\n__**🏘️  ZIPCODE :- **__\n`{zipcd}`",
    )


@register(outgoing=True, pattern=r"^\.gen(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("**Silahkan masukan bin yang mau di generate!**")
    await event.edit(f"```Generated CC {query}..```")
    async with bot.conversation("@Carol5_bot") as conv:
        try:
            send = await conv.send_message(f"/gen {query}")
            await asyncio.sleep(8)
            get = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @Carol5_bot or chat them")
        if get.text.startswith("Wait for result..."):
            return await event.edit(f"Failed generate {query}!")
        await event.edit(get.message)
        await event.client.delete_messages(conv.chat_id, [send.id, get.id])


@register(outgoing=True, pattern=r"^\.chk(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("**Silahkan masukan cc yang mau di check!**")
    await event.edit("```Checking CC Number..```")
    async with bot.conversation("@Carol5_bot") as conv:
        try:
            send = await conv.send_message(f"/ss {query}")
            await asyncio.sleep(20)
            get = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @Carol5_bot or chat them")
        if get.text.startswith("Wait for result..."):
            return await event.edit(f"Failed Check {query}!")
        await event.edit(get.message)
        await event.client.delete_messages(conv.chat_id, [send.id, get.id])


@register(outgoing=True, pattern="^\\.fakemail(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await fake.edit("```reply to text message```")
        return
    chat = "@fakemailbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Reply to actual users message.```")
        return
    await event.edit("```Sit tight while I sending some data from Microsoft```")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=177914997)
            )
            await bot.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock @fakemailbot and try again```")
            return
        if response.text.startswith("send"):
            await event.edit(
                "```can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await event.edit(f"{response.message.message}")


@register(outgoing=True, pattern=r"^\.bin(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("**Silahkan masukan BIN yang mau di check!**")
    await event.edit(f"```Checking BIN {query}```")
    async with bot.conversation("@Carol5_bot") as conv:
        try:
            send = await conv.send_message(f"/bin {query}")
            await asyncio.sleep(10)
            get = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @Carol5_bot or chat them")
        if get.text.startswith("Wait for result..."):
            return await event.edit(f"Bin {query} Invalid!")
        await event.edit(get.message)
        await event.client.delete_messages(conv.chat_id, [send.id, get.id])


@register(outgoing=True, pattern=r"^\.skey(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("**Silahkan masukan SK-KEY yang mau di check!**")
    await event.edit(f"```Checking SK KEY {query}```")
    async with bot.conversation("@Carol5_bot") as conv:
        try:
            send = await conv.send_message(f"/bin {query}")
            await asyncio.sleep(10)
            get = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @Carol5_bot or chat them")
        if get.text.startswith("Wait for result..."):
            return await event.edit("SK KEY Invalid!")
        await event.edit(get.message)
        await event.client.delete_messages(conv.chat_id, [send.id, get.id])


@register(outgoing=True, pattern=r"^\.alc(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit(
            "**Silahkan masukan cc yang mau di cek Alive apa Dead**"
        )
    await event.edit("```Checking CC Number..```")
    async with bot.conversation("@Carol5_bot") as conv:
        try:
            send = await conv.send_message(f"/ch {query}")
            await asyncio.sleep(20)
            get = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @Carol5_bot or chat them")
        if get.text.startswith("Wait for result..."):
            return await event.edit(f"Failed Check {query}!")
        await event.edit(get.message)
        await event.client.delete_messages(conv.chat_id, [send.id, get.id])


CMD_HELP.update(
    {
        "anu": ">`.gen` **<bin>**"
        "\nUsage: to generate cc with bin.."
        "\n\n>  `.genadd`"
        "\nUsage: Generator Random Address Using Faker"
        "\n\n> `.chk` **<cc>**"
        "\nUsage: to check respond cc."
        "\n\n> `.bin` **<bin number>**"
        "\nUsage: to check your bin information."
        "\n\n> `.skey` **<SK-Key Number>**"
        "\nUsage: to check your bin information."
        "\n\n> `.alc` **<CC|D|Y|Number>**"
        "\nUsage: to check Your bin is dead or Alive."
        "\n\n> `.fakemail`"
        "\nUsage: to get fake email."
    }
)
