# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module containing commands for interacting with dogbin(https://del.dog)."""
import os

from requests import exceptions, get, post

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register

DOGBIN_URL = "https://del.dog/"
NEKOBIN_URL = "https://nekobin.com/"


@register(outgoing=True, pattern=r"^\.paste( d)?([\s\S]*)")
async def paste(pstl):
    """For .paste command, pastes the text directly to nekobin/dogbin"""
    url_type = pstl.pattern_match.group(1)
    match = pstl.pattern_match.group(2).strip()
    replied = await pstl.get_reply_message()
    f_ext = ".txt"

    if not match and not pstl.is_reply:
        return await pstl.edit("`What should i paste ?`")

    if match:
        message = match
    elif replied:
        if replied.media:
            downloaded_file_name = await pstl.client.download_media(
                replied,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            f_ext = os.path.splitext(downloaded_file_name)[-1]
            with open(downloaded_file_name) as fd:
                try:
                    m_list = fd.readlines()
                except UnicodeDecodeError:
                    return await pstl.edit("`Can't paste this file.`")
            message = "".join(m_list)
            os.remove(downloaded_file_name)
        else:
            message = replied.message

    if not url_type:
        resp = post(NEKOBIN_URL + "api/documents", json={"content": message})
        if resp.status_code == 201:
            response = resp.json()
            key = response["result"]["key"]
            nekobin_final_url = NEKOBIN_URL + key + f_ext
            reply_text = (
                "`Pasted successfully!`\n\n"
                f"[Nekobin URL]({nekobin_final_url})\n"
                f"[View RAW]({NEKOBIN_URL}raw/{key})"
            )
        else:
            reply_text = "`Failed to reach Nekobin`"
    else:
        resp = post(DOGBIN_URL + "documents", data=message.encode("utf-8"))
        if resp.status_code == 200:
            response = resp.json()
            key = response["key"]
            dogbin_final_url = DOGBIN_URL + key + f_ext

            if response["isUrl"]:
                reply_text = (
                    "`Pasted successfully!`\n\n"
                    f"[Shortened URL]({dogbin_final_url})\n\n"
                    "`Original(non-shortened) URLs`\n"
                    f"[Dogbin URL]({DOGBIN_URL}v/{key})\n"
                    f"[View RAW]({DOGBIN_URL}raw/{key})"
                )
            else:
                reply_text = (
                    "`Pasted successfully!`\n\n"
                    f"[Dogbin URL]({dogbin_final_url})\n"
                    f"[View RAW]({DOGBIN_URL}raw/{key})"
                )
        else:
            reply_text = "`Failed to reach Dogbin`"

    await pstl.edit(reply_text)


@register(outgoing=True, pattern=r"^\.getpaste(?: |$)(.*)")
async def get_dogbin_content(dog_url):
    """For .getpaste command, fetches the content of a dogbin URL."""
    textx = await dog_url.get_reply_message()
    message = dog_url.pattern_match.group(1)
    await dog_url.edit("`Getting dogbin content...`")

    if textx:
        message = str(textx.message)

    format_normal = f"{DOGBIN_URL}"
    format_view = f"{DOGBIN_URL}v/"

    if message.startswith(format_view):
        message = message[len(format_view) :]
    elif message.startswith(format_normal):
        message = message[len(format_normal) :]
    elif message.startswith("del.dog/"):
        message = message[len("del.dog/") :]
    else:
        return await dog_url.edit("`Is that even a dogbin url?`")

    resp = get(f"{DOGBIN_URL}raw/{message}")

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await dog_url.edit(
            "Request returned an unsuccessful status code.\n\n" + str(HTTPErr)
        )
        return
    except exceptions.Timeout as TimeoutErr:
        await dog_url.edit("Request timed out." + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await dog_url.edit(
            "Request exceeded the configured number of maximum redirections."
            + str(RedirectsErr)
        )
        return

    reply_text = (
        "`Fetched dogbin URL content successfully!`" "\n\n`Content:` " + resp.text
    )

    await dog_url.edit(reply_text)
    if BOTLOG:
        await dog_url.client.send_message(
            BOTLOG_CHATID,
            "Get dogbin content query was executed successfully",
        )


@register(outgoing=True, pattern=r"^\.neko(?: |$)([\s\S]*)")
async def neko(nekobin):
    """For .paste command, pastes the text directly to dogbin."""
    nekobin_final_url = ""
    match = nekobin.pattern_match.group(1).strip()
    reply_id = nekobin.reply_to_msg_id

    if not match and not reply_id:
        return await nekobin.edit("`Cannot paste text.`")

    if match:
        message = match
    elif reply_id:
        message = await nekobin.get_reply_message()
        if message.media:
            downloaded_file_name = await nekobin.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = "".join(m.decode("UTF-8") for m in m_list)
            os.remove(downloaded_file_name)
        else:
            message = message.text

    # Nekobin
    await nekobin.edit("`Pasting text . . .`")
    resp = post(NEKOBIN_URL + "api/documents", json={"content": message})

    if resp.status_code == 201:
        response = resp.json()
        key = response["result"]["key"]
        nekobin_final_url = NEKOBIN_URL + key
        reply_text = (
            "`Pasted successfully!`\n\n"
            f"[Nekobin URL]({nekobin_final_url})\n"
            f"[View RAW]({NEKOBIN_URL}raw/{key})"
        )
    else:
        reply_text = "`Failed to reach Nekobin`"

    await nekobin.edit(reply_text)
    if BOTLOG:
        await nekobin.client.send_message(
            BOTLOG_CHATID,
            "Paste query was executed successfully",
        )


CMD_HELP.update(
    {
        "paste": ">`.paste <text/reply>`"
        "\nUsage: Create a paste or a shortened url using dogbin (https://del.dog/)"
        "\n\n>`.neko <text/reply>`"
        "\nUsage: Create a paste or a shortened url using nekobin (https://nekobin.com/)"
        "\n\n>`.getpaste`"
        "\nUsage: Gets the content of a paste or shortened url from dogbin (https://del.dog/)"
    }
)
