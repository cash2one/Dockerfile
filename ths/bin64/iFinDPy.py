# -*- coding: utf-8 -*-
"""
版本：1.0.0.1
作者：邓猛 dengmeng@myhexin.com 时间：20141106
更新时间：20141106 增加数据接口
文档介绍：iFinD Python接口程序。需与FTDataInterface.dll一起使用
修改历史：
版权：同花顺iFinD
"""

from ctypes import *
import sys
import re
import string
import types
import platform
import os
import threading
from datetime import datetime,date,time,timedelta

def THS_iFinDLogin(username, password):
    return iFinD.FT_iFinDLogin(username, password);

def THS_iFinDLogout():
    return iFinD.FT_iFinDLogout();

def THS_HighFrequenceSequence(thscode, jsonIndicator, jsonparam, begintime, endtime):
    return iFinD.FTQuerySynTHS_HighFrequenceSequence(thscode, jsonIndicator, jsonparam, begintime, endtime);

def THS_RealtimeQuotes(thscode, jsonIndicator, jsonparam):
    return iFinD.FTQuerySynTHS_RealtimeQuotes(thscode,jsonIndicator,jsonparam);

def THS_HistoryQuotes(thscode, jsonIndicator, jsonparam, begintime, endtime):
    return iFinD.FTQuerySynTHS_HisQuote(thscode,jsonIndicator,jsonparam,begintime,endtime);

def THS_BasicData(thsCode, indicatorName, paramOption):
    return iFinD.FTQuerySynTHS_BasicData(thsCode,indicatorName,paramOption);

def THS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime):
    return iFinD.FTQuerySynTHS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime);

def THS_DataPool(DataPoolname,paramname,FunOption):
    return iFinD.FTQuerySynTHS_DataPool(DataPoolname,paramname,FunOption)
def THS_EDBQuery(indicators, begintime, endtime):
    return iFinD.FT_EDBQuery(indicators,begintime,endtime)
'''    
def THS_DataStatistics():
    return iFinD.FT_DataStastics()

def THS_GetErrorInfo(errorcode):
    return iFinD.FT_GetErrorInfo(errorcode);
def THS_DateQuery(exchange, params, begintime, endtime):
    return iFinD.FT_DateQuery(exchange, params, begintime, endtime)
def THS_DateOffset(exchange, params, endtime):
    return iFinD.FT_DateOffset(exchange, params, endtime)
def THS_DateCount(exchange, params, begintime, endtime):
    return iFinD.FT_DateCount(exchange, params, begintime, endtime)
'''	

def THS_AsyHighFrequenceSequence(thscode, jsonIndicator, jsonparam, begintime, endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_HighFrequenceSequence(thscode, jsonIndicator, jsonparam, begintime, endtime,Callback,pUser,iD)
    
def THS_AsyRealtimeQuotes(thscode, jsonIndicator, jsonparam,Callback,pUser,ID):
    return iFinD.FTQueryTHS_RealtimeQuotes(thscode,jsonIndicator,jsonparam,Callback,pUser,ID);

def THS_AsyHistoryQuotes(thscode, jsonIndicator, jsonparam, begintime, endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_HisQuote(thscode,jsonIndicator,jsonparam,begintime,endtime,Callback,pUser,iD);

def THS_AsyBasicData(thsCode, indicatorName, paramOption,Callback,pUser,iD):
    return iFinD.FTQueryTHS_BasicData(thsCode,indicatorName,paramOption,Callback,pUser,iD);

def THS_AsyDateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime,Callback,pUser,iD);

def THS_AsyEDBQuery(indicators, begintime, endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_EDBQuery(indicators,begintime,endtime,Callback,pUser,iD)
    
def THS_AsyDataPool(DataPoolname,paramname,FunOption,Callback,pUser,iD):
    return iFinD.FTQueryTHS_DataPool(DataPoolname,paramname,FunOption,Callback,pUser,iD)

def THS_QuotesPushing(thscode):
    return iFinD.FTQueryTHS_QuotesPushing(thscode)

def THS_UnQuotesPushing():
    return iFinD.FTQueryTHS_QuotesPushing('')

def THS_Trans2DataFrame(Data):
    import numpy as np,pandas as pd
    if  ((Data.has_key('errorcode'))and(Data['errorcode']==0)):
        codelength=len(Data['tables']);
        dataframe = pd.DataFrame()
        for x in range(codelength):
            #EDB处理
            if  Data['tables'][x].has_key('id'):
                EdbId = Data['tables'][x]['id'][0]
                Edblength = len(Data['tables'][x]['time'])
                Edblist = list()
                for y in range(Edblength):
                    Edblist.append(EdbId)
                dataframe1 = pd.DataFrame()
                dataframe1.insert(0,'value',Data['tables'][x]['value'])
                dataframe1.insert(0,'id',Edblist)
                dataframe1.insert(0,'time',Data['tables'][x]['time'])
            else:#除EDB之外的业务
                dataframe1 = pd.DataFrame(Data['tables'][x]['table'])#先从字典转换到dataframe
                if  (Data['tables'][x].has_key('thscode'))and(len(Data['tables'][x]['thscode'])>0):#有股票
                    if dataframe1.size>0:#有股票有值   实时行情  基础数据  数据池
                        keys = Data['tables'][x]['table'].keys()
                        if len(keys)>0:
                            keyname=keys[0]
                            valuelength=len(Data['tables'][0]['table'][keyname])
                            codelist  = list()
                            for y in range(valuelength):
                                codelist.append(Data['tables'][x]['thscode'])
                            dataframe1.insert(0,'thscode',codelist)
                    else:
                        dataframe1.insert(0,'thscode',[Data['tables'][x]['thscode']])
                if  (Data['tables'][x].has_key('time'))and(len(Data['tables'][x]['time'])>0):
                    dataframe1.insert(0,'time',Data['tables'][x]['time'])        
            dataframe = dataframe.append(dataframe1,ignore_index=True)
        return dataframe
        
    else:
        return Data
        
        

def OnRealTimeCallback(pUderdata,id,sResult,len,errorcode,reserved):
    import json
    out=json.loads(sResult.decode('utf8'))
    print(out)
    return 0
    
def OnFTAsynCallback(pUserdata,id,sResult,len,errorcode,reserved):
    global g_FunctionMgr
    global g_Funclock
    g_Funclock.acquire();
    userfunc = g_FunctionMgr[id]
    del(g_FunctionMgr[id])
    g_Funclock.release()
    if(callable(userfunc)):
        userfunc(pUserdata,id,sResult,len,errorcode,reserved)
    return 0
    
CMPTHSREALTIMEFUNC=CFUNCTYPE(c_int,c_void_p,c_int32,c_char_p,c_int32,c_int32,c_int32)

pRealTimeFunc=CMPTHSREALTIMEFUNC(OnRealTimeCallback)
pAsyFunc=CMPTHSREALTIMEFUNC(OnFTAsynCallback)
nRegRTID = 0;

g_FunctionMgr={};
g_Funclock=threading.Lock();

    
class iFinD:

    decodeMethod = "utf-8";
    isWin = 'Windows' in platform.system()
    version=sys.version  
    #print(version);
    verss=version.split()[0].split('.');
    ver=int(verss[0])+float(verss[1])/10;
    isless3 = True
    if(ver  >= 3.0):
        isless3 = False
    sitepath=".";           
    for x in sys.path:
        ix=x.find('site-packages')
        if( ix>=0 and x[ix:]=='site-packages'):
          sitepath=x;
          break;
    if(isWin):
        sitepath=sitepath+"\\iFinDPy.pth"
    else:
        sitepath=sitepath+"/iFinDPy.pth"
    pathfile=open(sitepath)
    dllpath=pathfile.readlines();
    pathfile.close();
    dllpath=''.join(dllpath).strip('\n')
    #print(dllpath)
    if(isWin):
        bit=int(sys.version.split(' bit ')[0].split()[-1]);
        if(bit==32 ):
            sitepath=dllpath+"\\ShellExport.dll"
        else:
            sitepath=dllpath+"\\ShellExport.dll"
    else:
        architecture = platform.architecture();
        if(architecture[0]== '32bit'):
            sitepath=dllpath+"/libShellExport.so";
        else:
            sitepath=dllpath+"/libShellExport.so";  
    #print(sitepath)
    c_iFinDlib=cdll.LoadLibrary(sitepath)

    #FT_ifinDLoginPy
    c_FT_ifinDLoginPy=c_iFinDlib.THS_iFinDLoginPython;
    c_FT_ifinDLoginPy.restype=c_int32;
    c_FT_ifinDLoginPy.argtypes=[c_char_p,c_char_p]
	   

    #FTQueryTHS_SynHFQByJsonPy
    c_FTQueryTHS_SynHFQByJsonPy=c_iFinDlib.THS_HighFrequenceSequencePython;
    c_FTQueryTHS_SynHFQByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynHFQByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]


    #FTQueryTHS_SynDateSeriesByJsonPy
    c_FTQueryTHS_SynDateSeriesByJsonPy=c_iFinDlib.THS_DateSequencePython;
    c_FTQueryTHS_SynDateSeriesByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynDateSeriesByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynRTByJsonPy
    c_FTQueryTHS_SynRTByJsonPy=c_iFinDlib.THS_RealtimeQuotesPython;
    c_FTQueryTHS_SynRTByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynRTByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynBasicDataPy
    c_FTQueryTHS_SynBasicDataPy=c_iFinDlib.THS_BasicDataPython;
    c_FTQueryTHS_SynBasicDataPy.restype=c_void_p;
    c_FTQueryTHS_SynBasicDataPy.argtypes=[c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynDataPoolByJsonPy
    c_FTQueryTHS_SynDataPoolByJsonPy=c_iFinDlib.THS_DataPoolPython;
    c_FTQueryTHS_SynDataPoolByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynDataPoolByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynHisQuoteByJsonPy
    c_FTQueryTHS_SynHisQuoteByJsonPy=c_iFinDlib.THS_HistoryQuotesPython;
    c_FTQueryTHS_SynHisQuoteByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynHisQuoteByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]


    #FT_ifinDLogoutPy
    c_FT_ifinDLogoutPy=c_iFinDlib.THS_ifinDLogoutPython;
    c_FT_ifinDLogoutPy.restype=c_int32;
    c_FT_ifinDLogoutPy.argtypes=[]
    
	#FT_EDBQuery
    C_FT_ifinDEDBQuery=c_iFinDlib.THS_EDBQueryPython;
    C_FT_ifinDEDBQuery.restype=c_void_p;
    C_FT_ifinDEDBQuery.argtypes=[c_char_p,c_char_p,c_char_p]

 
    #FTQueryTHS_AsynRTByJsonPy
    C_FTQueryTHS_AsynRTByJsonPy=c_iFinDlib.THS_AsyRealtimeQuotesPython;
    C_FTQueryTHS_AsynRTByJsonPy.restype=c_int32;
    C_FTQueryTHS_AsynRTByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p,c_bool,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_HighFrequenceSequencePy
    c_FTQueryTHS_HighFrequenceSequencePy=c_iFinDlib.THS_AsyHighFrequenceSequencePython;
    c_FTQueryTHS_HighFrequenceSequencePy.restype=c_int32;
    c_FTQueryTHS_HighFrequenceSequencePy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)];

    #FTQueryTHS_DateSequencePy
    c_FTQueryTHS_DateSequencePy=c_iFinDlib.THS_AsyDateSequencePython;
    c_FTQueryTHS_DateSequencePy.restype=c_int32;
    c_FTQueryTHS_DateSequencePy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_RealtimeQuotesPy
    c_FTQueryTHS_RealtimeQuotesPy=c_iFinDlib.THS_AsyRealtimeQuotesPython;
    c_FTQueryTHS_RealtimeQuotesPy.restype=c_int32;
    c_FTQueryTHS_RealtimeQuotesPy.argtypes=[c_char_p,c_char_p,c_char_p,c_bool,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_BasicDataPy
    c_FTQueryTHS_BasicDataPy=c_iFinDlib.THS_AsyBasicDataPython;
    c_FTQueryTHS_BasicDataPy.restype=c_int32;
    c_FTQueryTHS_BasicDataPy.argtypes=[c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_DatapoolPy
    c_FTQueryTHS_DatapoolPy=c_iFinDlib.THS_AsyDataPoolPython;
    c_FTQueryTHS_DatapoolPy.restype=c_int32;
    c_FTQueryTHS_DatapoolPy.argtypes=[c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_HisQuotePy
    c_FTQueryTHS_HisQuotePy=c_iFinDlib.THS_AsyHistoryQuotesPython;
    c_FTQueryTHS_HisQuotePy.restype=c_int32;
    c_FTQueryTHS_HisQuotePy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]
                                      
    #FTQueryTHS_EDBQueryPy
    c_FTQueryTHS_EDBQueryPy=c_iFinDlib.THS_AsyEDBQueryPython;
    c_FTQueryTHS_EDBQueryPy.restype=c_int32;
    c_FTQueryTHS_EDBQueryPy.argtypes=[c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]
                                     
    #SetValue
    c_SetValue=c_iFinDlib.SetValue;
    c_SetValue.restype=c_int;
    c_SetValue.argtypes=[c_int,POINTER(c_int)]
    
    #DeleteMm
    c_DeleteMm=c_iFinDlib.DeleteMemory;
    c_DeleteMm.restype=c_int;
    c_DeleteMm.argtypes=[c_void_p];
                        
                         
    @staticmethod
    def FT_iFinDLogin(username,password):
        """登陆入口函数"""
        if(iFinD.isWin or iFinD.isless3):
            username=c_char_p(username);
            password=c_char_p(password);
        else:
            username=c_char_p(bytes(username,'utf8'));
            password=c_char_p(bytes(password,'utf8'));
        out=iFinD.c_FT_ifinDLoginPy(username.value,password.value);
        return out;
    #FT_ifinDLoginPy=staticmethod(FT_ifinDLoginPy)

    @staticmethod
    def FT_iFinDLogout():
         """登出入口函数"""
         out=iFinD.c_FT_ifinDLogoutPy();
         return out;
     #FT_ifinDLogoutPy=staticmethod(FT_ifinDLogoutPy)

    @staticmethod
    def FTQuerySynTHS_HighFrequenceSequence(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """高频序列"""
        if(iFinD.isWin or iFinD.isless3):
            thscode=c_char_p(thscode);
            jsonIndicators=c_char_p(jsonIndicator);
            jsonparams=c_char_p(jsonparam);
            begintime=c_char_p(begintime);
            endtime=c_char_p(endtime);
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));
        
        ptr=iFinD.c_FTQueryTHS_SynHFQByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;


    @staticmethod
    def FTQuerySynTHS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """日期序列"""
        if(iFinD.isWin or iFinD.isless3):
            thscode=c_char_p(thscode);
            jsonIndicators=c_char_p(jsonIndicator);
            jsonparams=c_char_p(jsonparam);
            begintime=c_char_p(begintime);
            endtime=c_char_p(endtime);
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));
        ptr=iFinD.c_FTQueryTHS_SynDateSeriesByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySynTHS_RealtimeQuotes(thscode,jsonIndicator,jsonparam):
        import json
        """实时行情"""
        if(iFinD.isWin or iFinD.isless3):
            thscode=c_char_p(thscode);
            jsonIndicators=c_char_p(jsonIndicator);
            jsonparams=c_char_p(jsonparam);
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
        ptr=iFinD.c_FTQueryTHS_SynRTByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySynTHS_BasicData(code,Indicatorname,paramname):
        import json
        """基础数据"""
        if(iFinD.isWin or iFinD.isless3):
            codes=c_char_p(code)
            indicator=c_char_p(Indicatorname);
            params=c_char_p(paramname);
        else:
            codes=c_char_p(bytes(code,'utf8'))
            indicator=c_char_p(bytes(Indicatorname,'utf8'));
            params=c_char_p(bytes(paramname,'utf8'));
        ptr=iFinD.c_FTQueryTHS_SynBasicDataPy(codes.value,indicator.value,params.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySynTHS_DataPool(DataPoolname,paramname,FunOption):
        import json
        """数据池"""
        if(iFinD.isWin or iFinD.isless3):
            DataPoolnames=c_char_p(DataPoolname);
            params=c_char_p(paramname);
            FunOptions=c_char_p(FunOption);
        else:
            DataPoolnames=c_char_p(bytes(DataPoolname,'utf8'));
            params=c_char_p(bytes(paramname,'utf8'));
            FunOptions=c_char_p(bytes(FunOption,'utf8'));
        ptr=iFinD.c_FTQueryTHS_SynDataPoolByJsonPy(DataPoolnames.value,params.value,FunOptions.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;
    
    @staticmethod
    def FTQuerySynTHS_HisQuote(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """历史行情"""
        if(iFinD.isWin or iFinD.isless3 ):
            thscode=c_char_p(thscode);
            jsonIndicators=c_char_p(jsonIndicator);
            jsonparams=c_char_p(jsonparam);
            begintime=c_char_p(begintime);
            endtime=c_char_p(endtime);
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));        
        ptr=iFinD.c_FTQueryTHS_SynHisQuoteByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;
        
        
    @staticmethod		
    def FT_EDBQuery(indicators, begintime, endtime):
        """查询EDB"""
        import json
        if(iFinD.isWin or iFinD.isless3):
            Indicators=c_char_p(indicators);
            Begintime=c_char_p(begintime);
            Endtime=c_char_p(endtime);
        else:
            Indicators=c_char_p(bytes(indicators,'utf8'));
            Begintime=c_char_p(bytes(begintime,'utf8'));
            Endtime=c_char_p(bytes(endtime,'utf8'));
        ptr=iFinD.C_FT_ifinDEDBQuery(Indicators.value, Begintime.value, Endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;
        
    @staticmethod
    def FTQueryTHS_BasicData(thsCode, indicatorName, paramOption,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin or iFinD.isless3):
            thsCode=c_char_p(thsCode);
            indicatorName=c_char_p(indicatorName);
            paramOption=c_char_p(paramOption);
        else:
            thsCode=c_char_p(bytes(thsCode,'utf8'));
            indicatorName=c_char_p(bytes(indicatorName,'utf8'));
            paramOption=c_char_p(bytes(paramOption,'utf8'));
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_BasicDataPy(thsCode.value,indicatorName.value,paramOption.value,pAsyFunc,pUser,byref(pIQueryID)) 
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;
        
    @staticmethod
    def FTQueryTHS_DataPool(DataPool,indicatorName,ParamOption,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin or iFinD.isless3):
            DataPool=c_char_p(DataPool);
            indicatorName=c_char_p(indicatorName);
            ParamOption=c_char_p(ParamOption);
        else:
            DataPool=c_char_p(bytes(DataPool,'utf8'));
            indicatorName=c_char_p(bytes(indicatorName,'utf8'));
            ParamOption=c_char_p(bytes(ParamOption,'utf8'));   
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_DatapoolPy(DataPool.value,indicatorName.value,ParamOption.value,pAsyFunc,pUser,byref(pIQueryID));
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;
        
    @staticmethod
    def FTQueryTHS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin or iFinD.isless3):
            thscode=c_char_p(thscode);
            jsonIndicators=c_char_p(jsonIndicator);
            jsonparams=c_char_p(jsonparam);
            begintime=c_char_p(begintime);
            endtime=c_char_p(endtime);
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));    
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_DateSequencePy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;
        
    @staticmethod
    def FTQueryTHS_RealtimeQuotes(thscode,jsonIndicator,jsonparam,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin or iFinD.isless3):
            thscode=c_char_p(thscode);
            jsonIndicators=c_char_p(jsonIndicator);
            jsonparams=c_char_p(jsonparam);
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));      
        onlyonce=c_bool(True);
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_RealtimeQuotesPy(thscode.value,jsonIndicators.value,jsonparams.value,onlyonce,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;
        
    @staticmethod
    def FTQueryTHS_HighFrequenceSequence(thscode,jsonIndicator,jsonparam,begintime,endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin or iFinD.isless3):
            thscode=c_char_p(thscode);
            jsonIndicators=c_char_p(jsonIndicator);
            jsonparams=c_char_p(jsonparam);
            begintime=c_char_p(begintime);
            endtime=c_char_p(endtime);
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));      
        pIQueryID=c_int(0);
        #CBResultsFunc=CMPTHSREALTIMEFUNC(CBResultsFunc);
        #out=iFinD.c_FTQueryTHS_HighFrequenceSequencePy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value,CBResultsFunc,c_void_p(pUser),byref(piQueryID))
        out=iFinD.c_FTQueryTHS_HighFrequenceSequencePy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_HisQuote(thscode,jsonIndicator,jsonparam,begintime,endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin or iFinD.isless3):
            thscode=c_char_p(thscode);
            jsonIndicators=c_char_p(jsonIndicator);
            jsonparams=c_char_p(jsonparam);
            begintime=c_char_p(begintime);
            endtime=c_char_p(endtime);
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));     
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_HisQuotePy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;  
        
    @staticmethod
    def FTQueryTHS_EDBQuery(indicators, begintime, endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin or iFinD.isless3):
            indicators=c_char_p(indicators);
            begintime=c_char_p(begintime);
            endtime=c_char_p(endtime);
        else:
            indicators=c_char_p(bytes(indicators,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));   
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_EDBQueryPy(indicators.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_QuotesPushing(thscode):
        import json
        """实时行情"""
        global nRegRTID
        if(iFinD.isWin or iFinD.isless3):
            thscode=c_char_p(thscode);
            jsonIndicators=c_char_p('');
            jsonparams=c_char_p('');
        else:
            thscode=c_char_p(bytes(thscode,'utf-8'));
            jsonIndicators=c_char_p(bytes('','utf-8'));
            jsonparams=c_char_p(bytes('','utf-8'));
        
        onlyOnce=c_bool(0);
        RegId=c_int32(nRegRTID);
        if thscode == '' and nRegRTID != 0:
            #解注册
            out=iFinD.C_FTQueryTHS_AsynRTByJsonPy(tmpCode.value,jsonIndicators.value,jsonparams.value,onlyOnce,pRealTimeFunc,c_void_p(0),byref(RegId));
            nRegRTID=0;
        elif thscode != '' and nRegRTID != 0:
            #全局只有一个注册，如果有了，先解注册之前的
            tmpCode='';
            tmpCode=c_char_p(tmpCode);
            out=iFinD.C_FTQueryTHS_AsynRTByJsonPy(tmpCode.value,jsonIndicators.value,jsonparams.value,onlyOnce,pRealTimeFunc,c_void_p(0),byref(RegId));
            nRegRTID=0;
            out=iFinD.C_FTQueryTHS_AsynRTByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,onlyOnce,pRealTimeFunc,c_void_p(0),byref(RegId));
        else:
            out=iFinD.C_FTQueryTHS_AsynRTByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,onlyOnce,pRealTimeFunc,c_void_p(0),byref(RegId));
        nRegRTID=RegId.value;
        return out;
