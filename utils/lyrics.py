from secret_keys import GENIUS_CLIENT_KEY
import calendar
import discord
import os
import time

from lyricsgenius import Genius

genius = Genius(GENIUS_CLIENT_KEY)


def get_lyrics(title, artist):
    song = genius.search_song(title=title, artist=artist)

    if not song:
        return None

    return song.lyrics


async def send_lyrics(channel, label, lyrics, plain):
    if plain:
        await channel.send(f"**{label}**")

        length = len(lyrics)
        sent_length = 0

        while sent_length < length:
            if len(lyrics[sent_length:sent_length +
                          2000]) < 2000:

                await channel.send(lyrics[sent_length:sent_length+2000])
                break
            else:
                last_new_line = lyrics[sent_length:sent_length +
                                       2000].rfind("\n")
                await channel.send(lyrics[sent_length:sent_length+last_new_line])

            sent_length += last_new_line

    else:
        cursecs = calendar.timegm(time.gmtime())
        filename = f"{cursecs}_{label}.txt"
        f = open(filename, "w")
        f.write(lyrics)
        f.close()

        await channel.send(label, file=discord.File(filename, f"{label}.txt"))
        os.remove(filename)
