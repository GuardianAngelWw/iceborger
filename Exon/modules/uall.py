"""
MIT License

Copyright (c) 2022 ABISHNOI69

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1m
#     UPDATE   :- Abishnoi_bots
#     GITHUB :- ABISHNOI69 ""


import os
from time import sleep

from telethon import *
from telethon.errors import *
from telethon.errors import FloodWaitError, UserNotParticipantError
from telethon.tl import *
from telethon.tl import functions, types
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import *
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChatBannedRights,
)

from Exon import *
from Exon import LOGGER
from Exon.events import register

CMD_HELP = "/ !"


# ================================================


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await telethn(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


@register(pattern="^/unbanall$")
@register(pattern="^/unbanall@Exon_Robot$")
async def _(event):
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator
    if event.is_private:
        return await event.respond(
            "__THIs coMMAND cAN BE UsE IN GRoUPs AND cHANNELs!__"
        )

    is_admin = False
    try:
        cutiepii = await telethn(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(
            cutiepii.participant,
            (
                ChannelParticipantAdmin,
                ChannelParticipantCreator,
            ),
        ):
            is_admin = True
    if not is_admin:
        return await event.respond("__oNLY ADMINs cAN UNMUTEALL!__")

    if not admin and not creator:
        await event.reply("`I DoN'T HAvE ENoUGH PERMIssIoNs!`")
        return

    done = await event.reply("sEARcHING PARTIcIPANT LIsTs.")
    p = 0
    async for i in telethn.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await telethn(
                functions.channels.EditBannedRequest(event.chat_id, i, rights)
            )
        except FloodWaitError as ex:
            LOGGER.warn(f"sLEEPING foR {ex.seconds} sEcoNDs")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("No oNE Is BANNED IN THIs cHAT")
        return
    required_string = "sUccEssfULLY UNBANNED **{}** UsERs"
    await event.reply(required_string.format(p))


@register(pattern="^/unmuteall@Exon_Robot$")
@register(pattern="^/unmuteall$")
async def _(event):
    if event.is_private:
        return await event.respond(
            "__THIs coMMAND cAN BE UsE IN GRoUPS AND cHANNELS!__"
        )

    is_admin = False
    try:
        cutiepii = await telethn(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(
            cutiepii.participant,
            (
                ChannelParticipantAdmin,
                ChannelParticipantCreator,
            ),
        ):
            is_admin = True
    if not is_admin:
        return await event.respond("__oNLY ADMINS cAN UNMUTEALL!__")
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator

    # Well
    if not admin and not creator:
        await event.reply("`I DoN'T HAvE ENoUGH PERMISSIoNS!`")
        return

    done = await event.reply("WoRKING ...")
    p = 0
    async for i in telethn.iter_participants(
        event.chat_id, filter=ChannelParticipantsBanned, aggressive=True
    ):
        rights = ChatBannedRights(
            until_date=0,
            send_messages=False,
        )
        try:
            await telethn(
                functions.channels.EditBannedRequest(event.chat_id, i, rights)
            )
        except FloodWaitError as ex:
            LOGGER.warn(f"SLEEPING foR {ex.seconds} SEcoNDS")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("No oNE IS MUTED IN THIS cHAT")
        return
    required_string = "SUccESSfULLY UNMUTED **{}** USERS"
    await event.reply(required_string.format(p))


@register(pattern="^/gusers$")
async def get_users(show):
    if not show.is_group:
        return
    if not await is_register_admin(show.input_chat, show.sender_id):
        return
    info = await telethn.get_entity(show.chat_id)
    title = info.title or "this chat"
    mentions = f"USERS IN {title}: \n"
    async for user in telethn.iter_participants(show.chat_id):
        mentions += (
            f"\n DELETED AccoUNT {user.id}"
            if user.deleted
            else f"\n[{user.first_name}](tg://user?id={user.id}) {user.id}"
        )

    with open("userslist.txt", "w+") as file:
        file.write(mentions)
    await telethn.send_file(
        show.chat_id,
        "userslist.txt",
        caption=f"Users in {title}",
        reply_to=show.id,
    )

    os.remove("userslist.txt")


__mod_name__ = "Uall"

# foR HELP MENU

# """
from Exon.modules.language import gs


def get_help(chat):
    return gs(chat, "uall_help")


# """
