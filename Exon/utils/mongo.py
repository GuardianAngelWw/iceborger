from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
import os

mongo = MongoCli("mongodb+srv://mogenius:mogenius@quickers.rlx3b3f.mongodb.net/?retryWrites=true&w=majority")
db = mongo.Exon

coupledb = db.couple


async def _get_lovers(chat_id: int):
    lovers = await coupledb.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["couple"]
    else:
        lovers = {}
    return lovers


async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    else:
        return False


async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    await coupledb.update_one(
        {"chat_id": chat_id},
        {"$set": {"couple": lovers}},
        upsert=True,
    )