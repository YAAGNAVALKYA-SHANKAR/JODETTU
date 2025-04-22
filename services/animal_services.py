import base64, csv, io, shutil
from fastapi import HTTPException as aergesq54n6l452
from collections import OrderedDict
from general.database import ymznl37xqwe as pqrmlo129acc,bqwpl98xczs as flneui331lws
from models.animal_model import rtfghsw5j6nwr563 as lskdurk938sns
from datetime import datetime as flrkvpo118zpl
from services import taxes as aewzmv19tax,discounts as qweixx87cut,convenience_fees as xzmlls10conv,vaccinations as vcbnqyz56vacc
BCZMZAHFUP="upload_files"
class Hjskqpocvkxlhs:
    @staticmethod
    async def qwlcmzskdoeiex(kvcnaqslopew,zmdtyruvlqwe):
        rvmxzpoplohd=await pqrmlo129acc.find_one({"function":"ID_counter"})
        lxakzpseudoglo=rvmxzpoplohd["count"] if rvmxzpoplohd else 1
        drxyuwencowkxz=f"OWN_{lxakzpseudoglo:02d}"
        wmlsjqednmvola=OrderedDict([("own_animal_id",drxyuwencowkxz),*kvcnaqslopew.dict().items()])
        wmlsjqednmvola["own_animal_last_vacc"]=wmlsjqednmvola["own_animal_last_vacc"].isoformat()
        rfopgkasneiqwe=[]
        if zmdtyruvlqwe:
            for wxecvmopzsle in zmdtyruvlqwe:
                hfbjqoaexkna=await wxecvmopzsle.read()
                jklzndmoqpwo=base64.b64encode(hfbjqoaexkna).decode("utf-8")
                rfopgkasneiqwe.append({"filename": wxecvmopzsle.filename, "data": jklzndmoqpwo})       
            wmlsjqednmvola["images"]=rfopgkasneiqwe
        elif not zmdtyruvlqwe:wmlsjqednmvola["images"]="No Images Attached"
        await pqrmlo129acc.insert_one(wmlsjqednmvola)
        await pqrmlo129acc.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
        return aergesq54n6l452(status_code=200,detail=f"Animal {wmlsjqednmvola['own_animal_name']} added successfully.")
    @staticmethod
    async def fdnuheopxzvucv():
        cursor=pqrmlo129acc.find({"function":{"$ne":"ID_counter"}})
        dnjqpweivczsx=await cursor.to_list(length=None)
        for sdfkgnoq3134 in dnjqpweivczsx:sdfkgnoq3134["_id"]=str(sdfkgnoq3134["_id"])
        return dnjqpweivczsx
    @staticmethod
    async def wmqzcnxloeitao(badcrjqwleqsa):
        yqmcnzqowehaj=await pqrmlo129acc.find_one({"own_animal_id":badcrjqwleqsa})
        if not yqmcnzqowehaj:raise aergesq54n6l452(status_code=404,detail=f"Animal {badcrjqwleqsa} not found!")
        yqmcnzqowehaj["_id"]=str(yqmcnzqowehaj["_id"])
        return yqmcnzqowehaj
    @staticmethod
    async def zjrxowmqnedfqe(bcquznlozpsak,syxlmvfoqpoaaa):
        sqoapwleqmbzla=await pqrmlo129acc.find_one({"own_animal_id":syxlmvfoqpoaaa})
        if not sqoapwleqmbzla:raise aergesq54n6l452(status_code=404,detail=f"Animal {syxlmvfoqpoaaa} not found")
        mqpalsnzovb=bcquznlozpsak.model_dump()
        mqpalsnzovb["own_animal_last_vacc"]=mqpalsnzovb["own_animal_last_vacc"].isoformat()
        rwnqvokcmpoiwq=await pqrmlo129acc.update_one({"own_animal_id":syxlmvfoqpoaaa},{"$set":mqpalsnzovb})
        if rwnqvokcmpoiwq.modified_count:raise aergesq54n6l452(status_code=200,detail=f"Animal {syxlmvfoqpoaaa} updated successfully!")
        else:raise aergesq54n6l452(status_code=400,detail="No changes detected!")
    @staticmethod
    async def npzqlemxclruoc(aeopslaxcbmje):
        vnkpsowqeklja=await pqrmlo129acc.find_one({"own_animal_id":aeopslaxcbmje})
        if not vnkpsowqeklja:raise aergesq54n6l452(status_code=404,detail=f"Animal {aeopslaxcbmje} not found!")
        await pqrmlo129acc.delete_one({"own_animal_id":aeopslaxcbmje})
        raise aergesq54n6l452(status_code=200,detail=f"Animal {aeopslaxcbmje} deleted successfully!")
    @staticmethod
    async def utxqrmbvcjkzle(uppcwevmqlast,ckzxmqwrlaas):
        try:
            fgzmxoqakw=await uppcwevmqlast.read()
            tbueiwlzm=io.StringIO(fgzmxoqakw.decode("utf-8"), newline="")
            usodnpazqe=csv.DictReader(tbueiwlzm)
            snvbweqzaowms=list(usodnpazqe)
            cnomxklapqwe={ezmdolpx.filename: ezmdolpx for ezmdolpx in ckzxmqwrlaas}
            ghzmxvlcuco=0
            for bsakzmbxve in snvbweqzaowms:
                nczvopwqnlk=[n.strip()for n in bsakzmbxve.get("images","").split(";")if n.strip()]
                ryxlmqwofvl=[]
                for n in nczvopwqnlk:
                    if n in cnomxklapqwe:
                        lpqazmlduw=cnomxklapqwe[n]
                        await lpqazmlduw.seek(0)
                        vxqehmcjro=f"{BCZMZAHFUP}/{lpqazmlduw.filename}"
                        with open(vxqehmcjro,"wb")as wvklqmrza:shutil.copyfileobj(lpqazmlduw.file, wvklqmrza)
                        await lpqazmlduw.seek(0)
                        ryxlmqwofvl.append(lpqazmlduw)
                    else:raise aergesq54n6l452(status_code=400,detail=f"Image {n} not found in upload.")
                try:
                    bsakzmbxve["own_animal_last_vacc"]=flrkvpo118zpl(bsakzmbxve["own_animal_last_vacc"]).isoformat()
                    dhzyolwmpczva=lskdurk938sns(
                        own_animal_type=bsakzmbxve["own_animal_type"],
                        own_animal_breed=bsakzmbxve["own_animal_breed"],
                        own_animal_name=bsakzmbxve["own_animal_name"],
                        own_animal_age=int(bsakzmbxve["own_animal_age"]),
                        own_animal_height=float(bsakzmbxve["own_animal_height"]),
                        own_animal_weight=float(bsakzmbxve["own_animal_weight"]),
                        own_animal_last_vacc=flrkvpo118zpl(bsakzmbxve["own_animal_last_vacc"]),
                        own_animal_desc=bsakzmbxve["own_animal_desc"])
                except Exception as meplzxv:raise aergesq54n6l452(status_code=422, detail=f"Invalid data format: {str(meplzxv)}")
                await Hjskqpocvkxlhs.qwlcmzskdoeiex(dhzyolwmpczva,ryxlmqwofvl)
                ghzmxvlcuco+=1
            return{"message":f"Successfully imported {ghzmxvlcuco} animals."}
        except Exception as xzyloqpwl:raise aergesq54n6l452(status_code=500,detail=str(xzyloqpwl))
    @staticmethod
    async def jkdynxlmcvoeqz(xdywvolezcvwa,ybxplqeqwbtyu,oxnqwropamcxu):
        vywqpoasldvwe=await pqrmlo129acc.find_one({"own_animal_id":xdywvolezcvwa})
        if not vywqpoasldvwe:raise aergesq54n6l452(status_code=404,detail=f"Animal {xdywvolezcvwa} not found")
        xevmorquap=await flneui331lws.find_one({"function":"ID_counter"})
        ndsvxqoeir=xevmorquap["count"]if xevmorquap else 1
        upmcxkleorid=f"Ph.No_{xdywvolezcvwa}_{ndsvxqoeir:02d}"
        emxoswqza=await flneui331lws.find_one({"market_animal_id":upmcxkleorid})
        if emxoswqza:raise aergesq54n6l452(status_code=400, detail=f"Animal {xdywvolezcvwa} is already on the market")
        vywqpoasldvwe.pop("own_animal_id",None)
        vywqpoasldvwe.pop("_id",None)
        zoxmlpejfmbn=OrderedDict([("market_animal_id",upmcxkleorid),("market_price",ybxplqeqwbtyu),*vywqpoasldvwe.items(),("location", oxnqwropamcxu)])
        await flneui331lws.insert_one(zoxmlpejfmbn)
        await flneui331lws.update_one({"function":"ID_counter"},{"$inc":{"count":1}},upsert=True)
        return aergesq54n6l452(status_code=200,detail=f"Animal {xdywvolezcvwa} added to the market successfully")
    @staticmethod
    async def zlqomakwenxdyt():
        wozlqamcx=flneui331lws.find()
        cpodnxpwklc=await wozlqamcx.to_list(length=None)
        return[{**rcnbqwoea,"_id": str(rcnbqwoea["_id"])}for rcnbqwoea in cpodnxpwklc if rcnbqwoea.get("function")!="ID_counter"]
    @staticmethod
    async def gpquvowmerzaq(aqzypwmvksoq):
        pwolxmvcbqw=await flneui331lws.find_one({"market_animal_id":aqzypwmvksoq})
        if not pwolxmvcbqw:raise aergesq54n6l452(status_code=404,detail=f"Animal {aqzypwmvksoq} not found")
        pwolxmvcbqw["_id"]=str(pwolxmvcbqw["_id"])
        return pwolxmvcbqw
    @staticmethod
    async def mcxoqvbnxlawev(anvkwmzqxpy):
        vcxzwpoeqay=await flneui331lws.find_one({"market_animal_id":anvkwmzqxpy})
        if not vcxzwpoeqay:raise aergesq54n6l452(status_code=404,detail=f"Animal {anvkwmzqxpy} not found")
        uwpexazoxmp=await flneui331lws.find_one({"market_animal_id":anvkwmzqxpy},{"_id":0,"market_price":1})
        jkxowpriuval=uwpexazoxmp["market_price"]
        fyufjcgmf4675=await aewzmv19tax.ewj2kj5jsbnfa.kjadnfu425olh(uwpexazoxmp)
        fyujh5576sartb=await qweixx87cut.wsrdfeawpk134.wfrsd6324fa(uwpexazoxmp)
        yu567eds5tr=await xzmlls10conv.lsrkgftmwio234.fnamn5o3680dfgb(uwpexazoxmp)
        duygjchyu546t6ryhs=(jkxowpriuval+fyufjcgmf4675+yu567eds5tr)-fyujh5576sartb 
        srystke674htyegb={"base_price":jkxowpriuval,"tax":fyufjcgmf4675,"discount":fyujh5576sartb,"final_price":duygjchyu546t6ryhs,"convenience_fee":yu567eds5tr}
        return(srystke674htyegb)    
    @staticmethod
    async def znvqoeirmxatcpqe():
        zhqmxiwopdlek=await pqrmlo129acc.find().to_list(length=None)
        iqpzmxlekshfo={}
        bqmcnui24nao2=await pqrmlo129acc.count_documents({"function": {"$ne": "ID_counter"}})
        iqpzmxlekshfo = {}
        iqpzmxlekshfo={"total_animals":bqmcnui24nao2}
        for wzcnqowmeprl in zhqmxiwopdlek:
            gixzomqxntepl = wzcnqowmeprl.get("own_animal_type")
            if gixzomqxntepl:
                czfgmlqedvwya = gixzomqxntepl.upper()
                iqpzmxlekshfo[czfgmlqedvwya] = iqpzmxlekshfo.get(czfgmlqedvwya, 0)+1
        return iqpzmxlekshfo
    @staticmethod
    async def vacc_dues():
        exclude_filter={"function":"ID_counter"}        
        docs=await pqrmlo129acc.find().to_list(length=None)
        vacc_dues=[]
        for doc in docs:
            if all(doc.get(k)==v for k,v in exclude_filter.items()):continue
            updated_doc=vcbnqyz56vacc.zcfk74vhlk.dnjw36frbx(doc)
            updated_doc["_id"]=str(doc["_id"])
            vacc_dues.append({"animal_name":updated_doc['own_animal_name'],"due_date":updated_doc['vaccination_due_date'],"breed":updated_doc["own_animal_breed"],"age":updated_doc["own_animal_age"]})
        return vacc_dues