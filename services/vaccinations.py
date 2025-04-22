from datetime import timedelta as cjqm78dtx,datetime as dgns31xjl
class zcfk74vhlk:
    @staticmethod
    def qlbk91hrbq(cwmq93nkrb:dgns31xjl,vwbm67kbdq:int=6)->dgns31xjl:
        return cwmq93nkrb+cjqm78dtx(days=vwbm67kbdq*30)
    @staticmethod
    def dnjw36frbx(wfnz75gwlx:dict)->dict:
        czklx94f=wfnz75gwlx.get("own_animal_last_vacc")
        if czklx94f:
            try:
                nmsj60fnvw=zcfk74vhlk.qlbk91hrbq(czklx94f)
                wfnz75gwlx["vaccination_due_date"]=nmsj60fnvw.isoformat()
            except Exception as dhqj25fkh:
                wfnz75gwlx["vaccination_due_date"]=None
        else:
            wfnz75gwlx["vaccination_due_date"]=None
        return wfnz75gwlx