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


import time
import asyncio
import random
from Abg.helpers.human_read import get_readable_time
from pyrogram.types import Message

from Exon import Abishnoi
from Exon.modules.no_sql.afk_db import add_afk, is_afk, remove_afk


@Abishnoi.on_cmd(["afk", "brb"])
async def active_afk(_, message: Message):
    if message.sender_chat:
        return
    user_id = message.from_user.id
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))

            if afktype == "text":
                send = await message.reply_text(
                    f"**{message.from_user.first_name}** is back online and was away for {seenago}",
                    disable_web_page_preview=True,
                )
                await asyncio.sleep(60)
                await send.delete()

            if afktype == "text_reason":
                send = await message.reply_text(
                    f"**{message.from_user.first_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`",
                    disable_web_page_preview=True,
                )
                await asyncio.sleep(60)
                await send.delete()

            if afktype == "animation":
                if str(reasonafk) == "None":
                    send = await message.reply_animation(
                        data,
                        caption=f"**{message.from_user.first_name}** is back online and was away for {seenago}",
                    )
                    await asyncio.sleep(60)
                    await send.delete()
                else:
                    send = await message.reply_animation(
                        data,
                        caption=f"**{message.from_user.first_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`",
                    )
                    await asyncio.sleep(60)
                    await send.delete()

            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"**{message.from_user.first_name}** is back online and was away for {seenago}",
                    )
                    await asyncio.sleep(60)
                    await send.delete()
                else:
                    send = await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"**{message.from_user.first_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`",
                    )
                    await asyncio.sleep(60)
                    await send.delete()
        except Exception:
            send = await message.reply_text(
                f"**{message.from_user.first_name}** is back online.",
                disable_web_page_preview=True,
            )
            await asyncio.sleep(60)
            await send.delete()

    if len(message.command) == 1 and not message.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and not message.reply_to_message:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.animation:
        _data = message.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif len(message.command) > 1 and message.reply_to_message.animation:
        _data = message.reply_to_message.animation.file_id
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.photo:
        await Abishnoi.download_media(
            message.reply_to_message, file_name=f"{user_id}.jpg"
        )
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and message.reply_to_message.photo:
        await Abishnoi.download_media(
            message.reply_to_message, file_name=f"{user_id}.jpg"
        )
        _reason = message.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.sticker:
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await Abishnoi.download_media(
                message.reply_to_message, file_name=f"{user_id}.jpg"
            )
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
    elif len(message.command) > 1 and message.reply_to_message.sticker:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            await Abishnoi.download_media(
                message.reply_to_message, file_name=f"{user_id}.jpg"
            )
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)

    sticker_ids = [
        "CAACAgEAAxkBAAEJzIFkvnqdG0WplzGQ5pzSO_5o3Sfv5gACeQEAArr88hkbuqYUJn-say8E",
        "CAACAgEAAxkBAAEJzINkvnrKHt550W3T1xzBq-6DVsjZxgAC3AADuvzyGZMu1owN01-yLwQ",
        "CAACAgEAAxkBAAEJzMFkvnwtD8_mfgM01BzVTlug0dkE-wACFQEAArr88hm3XMuZH18jhi8E",
        "CAACAgEAAxkBAAEJzMNkvnw1eo-F4g9yJYquKLmZSV537QACGwEAArr88hm8Bk97XxFmJC8E",
        "CAACAgEAAxkBAAEJzIFkvnqdG0WplzGQ5pzSO_5o3Sfv5gACeQEAArr88hkbuqYUJn-say8E",
        "CAACAgEAAxkBAAEJzINkvnrKHt550W3T1xzBq-6DVsjZxgAC3AADuvzyGZMu1owN01-yLwQ",
        "CAACAgEAAxkBAAEJzIVkvnrlZFHUDst4vF661MfcfSza8gAC-wADuvzyGeFkCRSA-rCGLwQ",
        "CAACAgEAAxkBAAEJzIdkvnrwNSXJRwyOW-ZOtU1iD0n3TgAC4QADuvzyGagN2YYz-z1xLwQ",
        "CAACAgEAAxkBAAEJzIlkvnr16zvhOgSSTrorQiRt73FWhgACKgEAArr88hlsLpLpXlzm2C8E",
        "CAACAgEAAxkBAAEJzItkvnr5gkfHpr2nGXJtUQVKx2VHzwACKQEAArr88hmT3XyhkRmDei8E",
        "CAACAgEAAxkBAAEJzI1kvnsDHlGtCkrHh6QyIGFt7qDzpgACGAEAArr88hlkt1cr11v0ti8E",
        "CAACAgEAAxkBAAEJzJFkvnsTCmYxnn7VqDoUvyNde_RPUQACLQEAArr88hle-kwmp_O0hy8E",
        "CAACAgEAAxkBAAEJzJNkvnspc5eUbUo8dlQxgMJjX1vExQAC9wADuvzyGZpOxvQ3n6KfLwQ",
        "CAACAgEAAxkBAAEJzJVkvns2exC2Lc3O0Vp_pmyPTyPTuAACFwEAArr88hkRViTRyl-vBS8E",
        "CAACAgEAAxkBAAEJzJdkvns6XofBV0h5cHKXv6l3uKHhAwAC-gADuvzyGVzrNc6kcC7bLwQ",
        "CAACAgEAAxkBAAEJzJlkvntK5d6YqYXSgfybZrVoedloJAAC9QADuvzyGcwbuNY211RpLwQ",
        "CAACAgEAAxkBAAEJzJ1kvntVaklCLuXHtrV-aiUKPb2_FwACJQEAArr88hk85jb83qRcny8E",
        "CAACAgEAAxkBAAEJzJ9kvntwdnO3GNvDpaVB9NA9az_OFQAC7gADuvzyGeXuyBUPfIBFLwQ",
        "CAACAgEAAxkBAAEJzKFkvnt8ClZeP29o_A_r4SwopEYQcAAC6gADuvzyGTC36r-q2nqYLwQ",
        "CAACAgEAAxkBAAEJzKNkvnuMIh27WuIMT2A0YqbMU5GdqwAC7QADuvzyGUxh1Clr8jwULwQ",
        "CAACAgEAAxkBAAEJzKVkvnuYDT0LstwiE3mwZptwVZAVHwAC8QADuvzyGaeHW-H86XCULwQ",   
        "CAACAgEAAxkBAAEJzKdkvnudBSwfmcr9yyHuESHf2kX0dQACJAEAArr88hnsckruLKDxWC8E",
        "CAACAgEAAxkBAAEJzKlkvnut_upII3cdk-Tcmq-2EEajZAACCAEAArr88hl23EpXsYluSy8E",
        "CAACAgEAAxkBAAEJzKtkvnu2CXEB4xly9725LF4g2IAo-wACCgEAArr88hlKnB_mzREoQC8E",
        "CAACAgEAAxkBAAEJzK1kvnu-Qb9iQDKN0-Ju17RsAqYs2wACKAEAArr88hmIrG2eEuPKGy8E",
        "CAACAgEAAxkBAAEJzK9kvnvFAax52rwrTTgE2cC6-DdhgwACfAEAArr88hlGCxAcoCx3Xi8E",
        "CAACAgEAAxkBAAEJzLFkvnvS1aKAcVTayXTIm24PJfG1kwAC_gADuvzyGXdrX7pwtRlyLwQ",
        "CAACAgEAAxkBAAEJzLNkvnvgPi46E8v1x1fv8MxC4s_4ogAC9gADuvzyGao46Ts99csiLwQ",
        "CAACAgEAAxkBAAEJzLVkvnvo60azdj7YpBiFOJP1KOn_dQACegEAArr88hkfC8tRD0R7pi8E",
        "CAACAgEAAxkBAAEJzLdkvnvs0R9CbM3S3tRuBe2-fSC-owACAwEAArr88hkSA3kXL2h4ky8E",
        "CAACAgEAAxkBAAEJzLlkvnvzMtEvPXeoS0z3q6Q1361KWQACAQEAArr88hmoeqKPr9utMy8E",
        "CAACAgEAAxkBAAEJzLtkvnwBiTFevMzbupp9AAFa2qOw73sAAgIBAAK6_PIZ_OQ1ePi_xu8vBA",
        "CAACAgEAAxkBAAEJzL1kvnwQ0Uunt4AxD7U5Vdl2GszHZgACBQEAArr88hlE1ktsrcJUtC8E",
        "CAACAgEAAxkBAAEJzL9kvnwa9X9mvBy3rCJIn7mR8QIajAACBwEAArr88hl5S9mKzGwboi8E",
        "CAACAgEAAxkBAAEJzMFkvnwtD8_mfgM01BzVTlug0dkE-wACFQEAArr88hm3XMuZH18jhi8E",
        "CAACAgEAAxkBAAEJzMNkvnw1eo-F4g9yJYquKLmZSV537QACGwEAArr88hm8Bk97XxFmJC8E",
    ]
    
    await message.reply_sticker(random.choice(sticker_ids))
    gone = await message.reply_text(f"{message.from_user.first_name} is now afk!")
# Add a delay of 10 seconds before deleting the message
    await asyncio.sleep(60)
    await gone.delete()


__mod_name__ = "Afk"


# foR HELP MENU

# """
from Exon.modules.language import gs


def get_help(chat):
    return gs(chat, "afk_help")


# """
