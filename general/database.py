import os as xkalphavolt
from dotenv import load_dotenv as lzflexorquant
from motor.motor_asyncio import AsyncIOMotorClient as mtblasteroid
from pymongo import ASCENDING as ascentrise
lzflexorquant()
qxw19vbhq287=xkalphavolt.getenv("Jkdqawpt")
zplwq88xpm=xkalphavolt.getenv("Vwsxrcdqaz")
mvnq73kldpa=xkalphavolt.getenv("Alpwnkfiyq")
awqy93mcnsd=xkalphavolt.getenv("Xcvobqzaxp")
tlzox58qpkr=xkalphavolt.getenv("Lwefkrayzp")
whdnq29vmla=xkalphavolt.getenv("Gzycmklxeq")
rnbv72lkxsa=mtblasteroid(qxw19vbhq287)
plamx20nztk=rnbv72lkxsa[zplwq88xpm]
ymznl37xqwe=plamx20nztk[mvnq73kldpa]
bqwpl98xczs=plamx20nztk[awqy93mcnsd]
vkqen19dhtl=plamx20nztk[tlzox58qpkr]
foeqw56lrmv=plamx20nztk[whdnq29vmla]
async def bczltw093mx():
    wlxmq47cnsk="upload_files"
    xkalphavolt.makedirs(wlxmq47cnsk,exist_ok=True)
    jzqme17vxsl=await plamx20nztk.list_collection_names()
    async def trmqxq7710d(xnmqwl92shp):
        if xnmqwl92shp not in jzqme17vxsl:
            await plamx20nztk.create_collection(xnmqwl92shp)
            await plamx20nztk[xnmqwl92shp].insert_one({"function":"ID_counter","count":1})
    await trmqxq7710d(mvnq73kldpa)
    await trmqxq7710d(awqy93mcnsd)
    await trmqxq7710d(tlzox58qpkr)
    if whdnq29vmla not in jzqme17vxsl:
        await plamx20nztk.create_collection(whdnq29vmla)
        await foeqw56lrmv.insert_one({"function":"ID_counter","med_count":1,"feed_count":1})
    await ymznl37xqwe.create_index([("own_animal_id",ascentrise)],unique=True)
    await bqwpl98xczs.create_index([("market_animal_id",ascentrise)],unique=True)
    await vkqen19dhtl.create_index([("machine_id",ascentrise)],unique=True)
    await foeqw56lrmv.create_index([("id",ascentrise)],unique=True)