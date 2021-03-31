# Copyright (C) 2020 Yusuf Usta.
# Copyright (C) 2021 Ncode2014.
# Licensed under the GPL-3.0 License;
# you may not use this file except in compliance with the License.

# Re-Port By Ncode2014
# source from
# https://github.com/ErdemBey1/SiriUserBot/blob/master/userbot/modules/shazam.py

from pydub import AudioSegment
from json import dumps
from userbot.events import register
from telethon.tl.types import DocumentAttributeAudio
from userbot.utils.FastTelethon import download_file
from .shazam_helper.communication import recognize_song_from_signature
from .shazam_helper.algorithm import SignatureGenerator
from requests import get
from os import remove
import urllib.parse
from userbot import CMD_HELP, LOGS


@register(outgoing=True, pattern=r"^\.shazam (.*)")
async def shazam(event):
    if not event.is_reply:
        return await event.edit("`Please Respond To An Audio File!`")
    else:
        await event.edit("`⬇️ Uploading audio file ...`")
        reply_message = await event.get_reply_message()
        replied = await replay_message.download_media()

        await event.edit("`🛠 The audio file is converted to fingerprint format...`")
        audio = AudioSegment.from_file(replied)
        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)

        signature_generator = SignatureGenerator()
        signature_generator.feed_input(audio.get_array_of_samples())

        signature_generator.MAX_TIME_SECONDS = 12
        if audio.duration_seconds > 12 * 3:
            signature_generator.samples_processed += 16000 * (
                int(audio.duration_seconds / 2) - 6
            )

        results = '{"error": "Not found"}'
        song = None
        await event.edit("`🎧 🎤 Shazamed...`")
        while True:
            signature = signature_generator.get_next_signature()
            if not signature:
                song = results
                break
            results = recognize_song_from_signature(signature)
            if results["matches"]:
                song = results
                break
            else:
                await event.edit(
                    f"`First {(signature_generator.samples_processed / 16000)} nothing found per second ... Im trying a little more.`"
                )

        if "track" not in song:
            return await event.edit(
                "`Ehh Shazam did not understand the voice you gave 😔. Can you send a little lighter voice?`"
            )
        await event.edit("`✅ Found the Music... Data Collecting...`")
        caption = f'**Music:** [{song["track"]["title"]}]({song["track"]["url"]})\n'
        if "artists" in song["track"]:
            caption += f'**Artist(lar):** [{song["track"]["subtitle"]}](https://www.shazam.com/artist/{song["track"]["artists"][0]["id"]})\n'
        else:
            caption += f'**Artist(lar):** `{song["track"]["subtitle"]}`\n'

        if "genres" in song["track"]:
            caption += f'**Genre:** `{song["track"]["genres"]["primary"]}`\n'

        if song["track"]["sections"][0]["type"] == "SONG":
            for metadata in song["track"]["sections"][0]["metadata"]:
                caption += f'**{"The" if metadata["title"] == "get" else metadata["title"]}:** `{metadata["text"]}`\n'

        caption += "\n**Music Platforms:** "
        for provider in song["track"]["hub"]["providers"]:
            if provider["actions"][0]["uri"].startswith("spotify:track"):
                url = provider["actions"][0]["uri"].replace(
                    "spotify:track:", "http://open.spotify.com/track/"
                )
            elif provider["actions"][0]["uri"].startswith(
                "intent:#Intent;action=android.media.action.MEDIA_PLAY_FROM_SEARCH"
            ):
                url = f"https://open.spotify.com/search/" + urllib.parse.quote(
                    song["track"]["subtitle"] + " - " + song["track"]["title"]
                )
            elif provider["actions"][0]["uri"].startswith("deezer"):
                url = provider["actions"][0]["uri"].replace(
                    "deezer-query://", "https://"
                )
            else:
                url = provider["actions"][0]["uri"]
            caption += f'[{provider["type"].capitalize()}]({url}) '
        for section in song["track"]["sections"]:
            if section["type"] == "VIDEO":
                if "youtubeurl" in section:
                    youtube = get(section["youtubeurl"]).json()
                else:
                    return

                caption += (
                    f'\n**Video Clip:** [youtube]({youtube["actions"][0]["uri"]})'
                )

        if "images" in song["track"] and len(song["track"]["images"]) >= 1:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                song["track"]["images"]["coverarthq"]
                if "coverarthq" in song["track"]["images"]
                else song["track"]["images"]["background"],
                caption=caption,
                reply_to=reply_message,
            )
        else:
            await event.edit(caption)
        remove(replied)


CMD_HELP.update(
    {
        "shazam": "\n\n`>.shazam <song/response>`"
        "\nUsage: Searches the audio file and search actuall song."
    }
)
