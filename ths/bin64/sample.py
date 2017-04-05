# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:57:58 2017

@author: viruser
"""
from iFinDPy import *
from ctypes import *
import sys
import json
def OnCallback(puser,ID,sResult,length,errorcode,reserve):
    out=json.loads(sResult.decode('utf-8'));
    print(out)
    return 0
CALLBACKRESULT=CFUNCTYPE(c_int,c_void_p,c_int32,c_char_p,c_int32,c_int32,c_int32)
pCallbackFunc=CALLBACKRESULT(OnCallback)


if __name__=="__main__":
    sys.stdin.read(1)
    THS_iFinDLogin("ifind_e001","ifinde001")
    '''
    highfrequence = THS_HighFrequenceSequence('300033.SZ','open;high;low;close','CPS:0,MaxPoints:50000,Fill:Previous,Interval:1','2017-03-20 09:15:00','2017-03-20 15:15:00')
    print(highfrequence)
    realtime      = THS_RealtimeQuotes('300033.SZ','close;open;high;low;new','pricetype:1')
    print(realtime)
    history = THS_HistoryQuotes('300033.SZ','open;high;low;close','period:D,pricetype:1,rptcategory:0,fqdate:1900-01-01,hb:YSHB','2017-01-20','2017-03-27')
    print(history)
    basicdata = THS_BasicData('600000.SH,600004.SH,600006.SH,600007.SH,600008.SH','ths_gpjc_stock','')
    print(basicdata)
    datesequence = THS_DateSequence('300033.SZ','close_pre;open;high;low','CPS:0,Days:Tradedays,Fill:Previous,Interval:D,Currency:ORIGINAL','2017-02-27','2017-03-27')
    print(datesequence)
    datapool = THS_DataPool('block','2017-03-27;001005260','date:Y,security_name:Y,thscode:Y')
    print(datapool)
    edb = THS_EDBQuery('M001620326;M002822183;M002834227','2010-03-27','2017-03-27')
    print(edb)
    '''
    
    ID=c_int32(0)
    
    THS_AsyHighFrequenceSequence('300033.SZ','open;high;low;close','CPS:0,MaxPoints:50000,Fill:Previous,Interval:1','2017-03-09 09:30:00','2017-03-09 09:35:00',pCallbackFunc,c_void_p(0),byref(ID))
    THS_AsyRealtimeQuotes('600000.SH,600004.SH','close;open;high;low;change','pricetype:1',pCallbackFunc,c_void_p(0),byref(ID))
    THS_AsyHistoryQuotes('600000.SH,600004.SH,600005.SH','lastclose;open;low','period:D,pricetype:1,rptcategory:0,fqdate:1900-01-01,hb:YSHB','2016-02-23','2017-02-23',pCallbackFunc,c_void_p(0),byref(ID))
    THS_AsyBasicData('600000.SH,600004.SH,600005.SH','ths_gpdm_stock','',pCallbackFunc,c_void_p(0),byref(ID))
    THS_AsyDateSequence('600000.SH,600004.SH,600005.SH','stockname;stockcode;thscode','CPS:0,Days:Tradedays,Fill:Previous,Interval:D,Currency:ORIGINAL','2017-01-23','2017-02-23',pCallbackFunc,c_void_p(0),byref(ID))
    THS_AsyDataPool('block','2017-02-23;001005260','date:Y,security_name:Y,thscode:Y',pCallbackFunc,c_void_p(0),byref(ID))
    THS_AsyEDBQuery('M001620326;M002822183;M002834227','2010-02-23','2017-02-23',pCallbackFunc,c_void_p(0),byref(ID))
    
    #THS_QuotesPushing('300033.SZ')
    sys.stdin.read(1)