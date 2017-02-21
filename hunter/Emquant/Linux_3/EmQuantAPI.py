
# -*- coding:utf-8 -*-

__author__ = 'weijie'

"""
*   EmQuantAPI for python
*   version  1.0.1.1
*   c++ version 1.0.1.1
*   Copyright (c) EastMoney Corp. All rights reserved.
"""

from ctypes import *
import sys
import os
import platform
from datetime import datetime, date, time

######################################################################################
# data type define

eVT_null = 0
eVT_char = 1
eVT_byte = 2
eVT_bool = 3
eVT_short = 4
eVT_ushort = 5
eVT_int = 6
eVT_uInt = 7
eVT_int64 = 8
eVT_uInt64 = 9
eVT_float = 10
eVT_double = 11
eVT_byteArray = 12
eVT_asciiString = 13
eVT_unicodeString = 14


######################################################################################
# data struct define

class c_safe_union(Union):
    _fields_ = [
        ("charValue", c_char),
        ("boolValue", c_bool),
        ("shortValue", c_short),
        ("uShortValue", c_ushort),
        ("intValue", c_int),
        ("uIntValue", c_uint),
        ("int64Value", c_longlong),
        ("uInt64Value", c_ulonglong),
        ("floatValue", c_float),
        ("doubleValue", c_double)
    ]

class stEQChar(Structure):
    _fields_ = [
        ("pChar", c_char_p),
        ("nSize", c_uint)
    ]

class stEQCharArray(Structure):
    _fields_ = [
        ("pChArray", POINTER(stEQChar)),
        ("nSize", c_uint)
    ]

class stEQVarient(Structure):
    pass

stEQVarient._fields_ = [
    ("vtype", c_int),
    ("unionValues", c_safe_union),
    ("eqchar", stEQChar)
]

class stEQVarientArray(Structure):
    _fields_ = [
        ("pEQVarient", POINTER(stEQVarient)),
        ("nSize", c_uint)
    ]

class stEQData(Structure):
    _fields_ = [
        ("codeArray", stEQCharArray),
        ("indicatorArray", stEQCharArray),
        ("dateArray", stEQCharArray),
        ("valueArray", stEQVarientArray)
    ]

class stEQLoginInfo(Structure):
    _fields_ = [
        ("userName", c_char * 255),
        ("password", c_char * 255)
    ]

class stEQMessage(Structure):
    _fields_ = [
        ("version", c_int),
        ("msgType", c_int),
        ("err", c_int),
        ("requestID", c_int),
        ("serialID", c_int),
        ("pEQData", POINTER(stEQData))
    ]
    
class stEQCtrData(Structure):
    _fields_ = [
        ("row", c_int),
        ("column", c_int),
        ("indicatorArray", stEQCharArray),
        ("valueArray", stEQVarientArray)
    ]
    
class utils:

    @staticmethod
    def getbasedir():
        """
        获取EmQuantAPI.py所在目录
        :return:
        """
        
        apiPackagePath = "."
        site_pkg_name = "site-packages"
        for x in sys.path:
            xi = x.find(site_pkg_name)
            if(xi >= 0 and x[xi:] == site_pkg_name):
                apiPackagePath = x
                apiPackagePath = os.path.join(apiPackagePath, "EmQuantAPI.pth")
                if not os.path.exists(apiPackagePath):
                    continue
                pthFile = open(apiPackagePath, "r")
                baseDir = pthFile.readline()
                pthFile.close()
                if len(baseDir) > 0:
                    return baseDir
        return ""

    @staticmethod
    def getdlldir():
        """
        获取so文件所在目录
        :return:
        """
        baseDir = utils.getbasedir()
        if baseDir == None:
            return None
        bit = 32
        if sys.maxsize > 2 ** 32:
            bit = 64
        if bit == 64:
            baseDir = os.path.join(baseDir, "libs", "x64")
        else:
            baseDir = os.path.join(baseDir, "libs", "x86")
        return baseDir




######################################################################################
#

appLogCallback = None
appQuoteCallback = None
appQuoteFunctionDict = {}

c_LogCallback = CFUNCTYPE(c_int, c_char_p)
c_DataCallback = CFUNCTYPE(c_int, POINTER(stEQMessage), c_void_p)

c_encodeType = "utf-8"

class c:
    class EmQuantData:
        def __init__(self):
            self.ErrorCode = 0
            self.ErrorMsg = 'success'
            self.Codes = list()
            self.Indicators = list()
            self.Dates = list()
            self.RequestID = 0
            self.SerialID = 0
            self.Data = dict()

        def __str__(self):
            return "ErrorCode=%s, ErrorMsg=%s, Data=%s" % (self.ErrorCode, self.ErrorMsg, str(self.Data))

        def __repr__(self):
            return "ErrorCode=%s, ErrorMsg=%s, Data=%s" % (self.ErrorCode, self.ErrorMsg, str(self.Data))

        def resolve2RankData(self, indicatorData, **arga):
            for i in range(0, indicatorData.codeArray.nSize):
                self.Codes.append(indicatorData.codeArray.pChArray[i].pChar.decode(c_encodeType))
            for k in range(0, indicatorData.indicatorArray.nSize):
                self.Indicators.append(indicatorData.indicatorArray.pChArray[k].pChar.decode(c_encodeType))
            for j in range(0, indicatorData.dateArray.nSize):
                self.Dates.append(indicatorData.dateArray.pChArray[j].pChar.decode(c_encodeType))
            self.Data = []
            for i in range(0, len(self.Codes)):
                for j in range(0, len(self.Indicators)):
                    for k in range(0, len(self.Dates)):
                        self.Data.append(self.getIndicatorDataByIndex(i, j, k, indicatorData))

        def resolve25RankData(self, indicatorData, **arga):
            for i in range(0, indicatorData.codeArray.nSize):
                self.Codes.append(indicatorData.codeArray.pChArray[i].pChar.decode(c_encodeType))
            for k in range(0, indicatorData.indicatorArray.nSize):
                self.Indicators.append(indicatorData.indicatorArray.pChArray[k].pChar.decode(c_encodeType))
            for j in range(0, indicatorData.dateArray.nSize):
                self.Dates.append(indicatorData.dateArray.pChArray[j].pChar.decode(c_encodeType))
            for i in range(0, len(self.Codes)):
                stockCode = self.Codes[i]
                self.Data[stockCode] = []
                for j in range(0, len(self.Indicators)):
                    tempData = None
                    for k in range(0, len(self.Dates)):
                        tempData = self.getIndicatorDataByIndex(i, j, k, indicatorData)
                        self.Data[stockCode].append(tempData)

        def resolve26RankData(self, indicatorData, **arga):
            for i in range(0, indicatorData.codeArray.nSize):
                self.Codes.append(indicatorData.codeArray.pChArray[i].pChar.decode(c_encodeType))
            for k in range(0, indicatorData.indicatorArray.nSize):
                self.Indicators.append(indicatorData.indicatorArray.pChArray[k].pChar.decode(c_encodeType))
            for j in range(0, indicatorData.dateArray.nSize):
                self.Dates.append(indicatorData.dateArray.pChArray[j].pChar.decode(c_encodeType))
            self.Data = []
            for i in range(0, len(self.Codes)):
                for j in range(0, len(self.Indicators)):
                    tempData = []
                    for k in range(0, len(self.Dates)):
                        tempData.append(self.getIndicatorDataByIndex(i, j, k, indicatorData))
                    self.Data.append(tempData)

        def resolve3RankData(self, indicatorData, **arga):
            for i in range(0, indicatorData.codeArray.nSize):
                self.Codes.append(indicatorData.codeArray.pChArray[i].pChar.decode(c_encodeType))
            for k in range(0, indicatorData.indicatorArray.nSize):
                self.Indicators.append(indicatorData.indicatorArray.pChArray[k].pChar.decode(c_encodeType))
            for j in range(0, indicatorData.dateArray.nSize):
                self.Dates.append(indicatorData.dateArray.pChArray[j].pChar.decode(c_encodeType))
            for i in range(0, len(self.Codes)):
                stockCode = self.Codes[i]
                self.Data[stockCode] = []
                for j in range(0, len(self.Indicators)):
                    tempData = []
                    for k in range(0, len(self.Dates)):
                        tempData.append(self.getIndicatorDataByIndex(i, j, k, indicatorData))
                    self.Data[stockCode].append(tempData)

        def resolveCtrData(self, indicatorData, **arga):
            for i in range(0, indicatorData.column):
                self.Indicators.append(indicatorData.indicatorArray.pChArray[i].pChar.decode(c_encodeType))
            for r in range(0, indicatorData.row):
                list = []
                for n in range(0, indicatorData.column):
                    list.append(self.resolve(indicatorData.valueArray.pEQVarient[indicatorData.column * r + n]))
                self.Data[str(r)] = list

        def resolve(self, variant):
            if variant.vtype == eVT_null:
                return None
            elif variant.vtype == eVT_char:
                return variant.unionValues.charValue
            elif variant.vtype == eVT_bool:
                return variant.unionValues.boolValue
            elif variant.vtype == eVT_short:
                return variant.unionValues.shortValue
            elif variant.vtype == eVT_ushort:
                return variant.unionValues.uShortValue
            elif variant.vtype == eVT_int:
                return variant.unionValues.intValue
            elif variant.vtype == eVT_uInt:
                return variant.unionValues.uIntValue
            elif variant.vtype == eVT_int64:
                return variant.unionValues.int64Value
            elif variant.vtype == eVT_uInt64:
                return variant.unionValues.uInt64Value
            elif variant.vtype == eVT_float:
                return round(variant.unionValues.floatValue, 6)
            elif variant.vtype == eVT_double:
                return round(variant.unionValues.doubleValue, 6)
            elif variant.vtype == eVT_asciiString:
                if variant.eqchar.pChar != None:
                    return variant.eqchar.pChar.decode(c_encodeType)
                return ""
            elif variant.vtype == eVT_unicodeString:
                if variant.eqchar.pChar != None:
                    return variant.eqchar.pChar.decode(c_encodeType)
                return ""
            return None

        def getIndicatorDataByIndex(self, codeIndex, indicatorIndex, dateIndex, indicatorData):
            if indicatorData.valueArray.nSize == 0:
                return None
            codeSize = indicatorData.codeArray.nSize
            indicatorSize = indicatorData.indicatorArray.nSize
            dateSize = indicatorData.dateArray.nSize
            valueSize = indicatorData.valueArray.nSize
            if valueSize != codeSize * dateSize * indicatorSize:
                return None
            if codeIndex <= codeSize * indicatorSize * dateIndex + indicatorSize * codeIndex + indicatorIndex:
                tempIndex = codeSize * indicatorSize * dateIndex + indicatorSize * codeIndex + indicatorIndex
                return self.resolve(indicatorData.valueArray.pEQVarient[tempIndex])

   

    libsDir = os.path.join(utils.getbasedir(), "libs")
    bit = 32
    if sys.maxsize > 2 ** 32:
        bit = 64
    if bit == 64:
        apiDllPath = os.path.join(libsDir, "x64", "libEMQuantAPIx64.so")
    else:
        apiDllPath = os.path.join(libsDir, "x86", "libEMQuantAPI.so")

    quantLib = CDLL(apiDllPath)

    # function define

    quant_start = quantLib.start
    quant_start.restype = c_int
    quant_start.argtypes = [POINTER(stEQLoginInfo), c_char_p, c_LogCallback]

    quant_setserverlistdir = quantLib.setserverlistdir
    quant_setserverlistdir.restype = c_char_p
    quant_setserverlistdir.argtypes = []

    quant_stop = quantLib.stop
    quant_stop.restype = c_int
    quant_stop.argtypes = []

    quant_setcallback = quantLib.setcallback
    quant_setcallback.restype = c_int
    quant_setcallback.argtypes = [c_DataCallback]

    quant_geterrstring = quantLib.geterrstring
    quant_geterrstring.restype = c_char_p
    quant_geterrstring.argtypes = [c_int, c_int]

    quant_csd = quantLib.csd
    quant_csd.restype = c_int
    quant_csd.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_void_p]

    quant_css = quantLib.css
    quant_css.restype = c_int
    quant_css.argtypes = [c_char_p, c_char_p, c_char_p, c_void_p]

    quant_tradedates = quantLib.tradedates
    quant_tradedates.restype = c_int
    quant_tradedates.argtypes = [c_char_p, c_char_p, c_char_p, c_void_p]

    quant_sector = quantLib.sector
    quant_sector.restype = c_int
    quant_sector.argtypes = [c_char_p, c_char_p, c_char_p, c_void_p]

    quant_gettradedate = quantLib.gettradedate
    quant_gettradedate.restype = c_int
    quant_gettradedate.argtypes = [c_char_p, c_int, c_char_p, c_void_p]

    quant_csc = quantLib.csc
    quant_csc.restype = c_int
    quant_csc.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_void_p]

    quant_releasedata = quantLib.releasedata
    quant_releasedata.restype = c_int
    quant_releasedata.argtypes = [c_void_p]

    quant_csq = quantLib.csq
    quant_csq.restype = c_int
    quant_csq.argtypes = [c_char_p, c_char_p, c_char_p, c_DataCallback, c_void_p]

    quant_csqcancel = quantLib.csqcancel
    quant_csqcancel.restype = c_int
    quant_csqcancel.argtypes = [c_int]

    quant_cst = quantLib.cst
    quant_cst.restype = c_int
    quant_cst.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_DataCallback, c_void_p]

    quant_csqsnapshot = quantLib.csqsnapshot
    quant_csqsnapshot.restype = c_int
    quant_csqsnapshot.argtypes = [c_char_p, c_char_p, c_char_p, c_void_p]

    quant_ctr = quantLib.ctr
    quant_ctr.restype = c_int
    quant_ctr.argtypes = [c_char_p, c_char_p, c_char_p, c_void_p]

    @staticmethod
    def start(uname, password, options="", logcallback=None):
        """
        初始化和登陆(开始时调用)  options：附加参数 "TestLatency=1"
        :param uname: 用户名
        :param password: 密码
        :param options:可选参数
        :param logcallback:启动结果提示回调函数
        :return:
        """
        if(options.upper().find("LANGUAGEVERSION") == -1):
            options = "LANGUAGEVERSION=1,"+options
        data = c.EmQuantData()
        loginInfo = stEQLoginInfo()
        loginInfo.userName = bytes(uname, c_encodeType)
        loginInfo.password = bytes(password, c_encodeType)
    
        global appLogCallback
        if callable(logcallback):
            appLogCallback = c_LogCallback(logcallback)
        else:
            def log(logMessage):
                print("[EmQuantAPI Python]", logMessage.decode(c_encodeType))
                return 1
            appLogCallback = c_LogCallback(log)
        c.quant_setserverlistdir(utils.getdlldir().encode(c_encodeType))
        loginResult = c.quant_start(byref(loginInfo), options.encode(c_encodeType), appLogCallback)
        if loginResult != 0:
            data.ErrorCode = loginResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
        else:
            c.quant_setcallback(appQuoteCallback)
        return data

    @staticmethod
    def stop():
        """
        退出(结束时调用)
        :return: 0-成功
        """
        data = c.EmQuantData()
        data.ErrorCode = c.quant_stop()
        data.ErrorMsg = c.geterrstring(data.ErrorCode)
        return data

    @staticmethod
    def geterrstring(errcode, lang=1):
        """
        获取错误码文本说明
        :param errcode:错误代码
        :param lang:语言类型 0-中文  1-英文
        :return:
        """
        return c.quant_geterrstring(errcode, lang)

    @staticmethod
    def csd(codes, indicators, startdate=None, enddate=None, options="", *arga, **argb):
        """
        序列数据查询(同步请求)
        :param codes: 东财代码  多个代码间用半角逗号隔开，支持大小写。如 "300059.SZ,000002.SZ,000003.SZ,000004.SZ"
        :param indicators:东财指标 多个指标间用半角逗号隔开，支持大小写。如 "open,close,high"
        :param startdate:开始日期。如无分隔符，则必须为8位数字。格式支持:YYYYMMDD YYYY/MM/DD YYYY/M/D YYYY-MM-DD YYYY-M-D
        :param enddate:截止日期。如无分隔符，则必须为8位数字。格式支持:YYYYMMDD YYYY/MM/DD YYYY/M/D YYYY-MM-DD YYYY-M-D
        :param options:附加参数  多个参数以半角逗号隔开，"Period=1,Market=CNSESH,Order=1,Adjustflag=1,Curtype=1,Pricetype=1,Type=1"
        :return:EmQuantData
        """

        data = c.EmQuantData()

        if(enddate == None):
            enddate = datetime.today().strftime("%Y-%m-%d")
        if(startdate == None):
            startdate = enddate
        if(isinstance(startdate, datetime) or isinstance(startdate, date)):
            startdate = startdate.strftime("%Y-%m-%d")
        if(isinstance(enddate, datetime) or isinstance(enddate, date)):
            enddate = enddate.strftime("%Y-%m-%d")
        eqData = stEQData()
        refEqData = byref(pointer(eqData))
        coutResult = c.quant_csd(codes.encode(c_encodeType), indicators.encode(c_encodeType), startdate.encode(c_encodeType), enddate.encode(c_encodeType), options.encode(c_encodeType), refEqData)
        if coutResult != 0:
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
            return data
        tempData = refEqData._obj.contents
        if not isinstance(tempData, stEQData):
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
        else:
            data.resolve3RankData(tempData)
            c.quant_releasedata(pointer(tempData))
        return data

    @staticmethod
    def css(codes, indicators, options="", *arga, **argb):
        """
        截面数据查询(同步请求)
        :param codes:东财代码  多个代码间用半角逗号隔开，支持大小写。如 "300059.SZ,000002.SZ,000003.SZ,000004.SZ"
        :param indicators:东财指标 多个指标间用半角逗号隔开，支持大小写。如 "open,close,high"
        :param options:附加参数  多个参数以半角逗号隔开，"Period=1,Market=CNSESH,Order=1,Adjustflag=1,Curtype=1,Pricetype=1,Type=1"
        :return:EmQuantData
        """

        data = c.EmQuantData()

        eqData = stEQData()
        refEqData = byref(pointer(eqData))
        coutResult = c.quant_css(codes.encode(c_encodeType), indicators.encode(c_encodeType), options.encode(c_encodeType), refEqData)
        if coutResult != 0:
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
            return data
        tempData = refEqData._obj.contents
        if not isinstance(tempData, stEQData):
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
        else:
            # data.resolve3RankData(tempData)
            data.resolve25RankData(tempData)
            c.quant_releasedata(pointer(tempData))
        return data

    @staticmethod
    def tradedates(startdate=None, enddate=None, options="", *arga, **argb):
        """
        获取区间日期内的交易日(同步请求)
        :param startdate:开始日期。如无分隔符，则必须为8位数字。格式支持:YYYYMMDD YYYY/MM/DD YYYY/M/D YYYY-MM-DD YYYY-M-D
        :param enddate:截止日期。如无分隔符，则必须为8位数字。格式支持:YYYYMMDD YYYY/MM/DD YYYY/M/D YYYY-MM-DD YYYY-M-D
        :param options:附加参数  多个参数以半角逗号隔开，"Period=1,Market=CNSESH,Order=1,Adjustflag=1,Curtype=1,Pricetype=1,Type=1"
        :return:EmQuantData
        """

        data = c.EmQuantData()

        if(enddate == None):
            enddate = datetime.today().strftime("%Y-%m-%d")
        if(startdate == None):
            startdate = enddate
        if(isinstance(startdate, datetime) or isinstance(startdate, date)):
            startdate = startdate.strftime("%Y-%m-%d")
        if(isinstance(enddate, datetime) or isinstance(enddate, date)):
            enddate = enddate.strftime("%Y-%m-%d")
        eqData = stEQData()
        refEqData = byref(pointer(eqData))
        coutResult = c.quant_tradedates(startdate.encode(c_encodeType), enddate.encode(c_encodeType), options.encode(c_encodeType), refEqData)
        if coutResult != 0:
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
            return data
        tempData = refEqData._obj.contents
        if not isinstance(tempData, stEQData):
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
        else:
            data.resolve2RankData(tempData)
            c.quant_releasedata(pointer(tempData))
        return data

    @staticmethod
    def sector(pukeycode, tradedate, options="", *arga, **argb):
        """
        获取系统板块成分(同步请求)
        :param pukeycode:
        :param tradedate:交易日
        :param options:附加参数  多个参数以半角逗号隔开，"Period=1,Market=CNSESH,Order=1,Adjustflag=1,Curtype=1,Pricetype=1,Type=1"
        :param arga:
        :param argb:
        :return:
        """
        data = c.EmQuantData()

        if(tradedate == None):
            tradedate = datetime.today().strftime("%Y-%m-%d")
        if(isinstance(tradedate, datetime) or isinstance(tradedate, date)):
            tradedate = tradedate.strftime("%Y-%m-%d")
        eqData = stEQData()
        refEqData = byref(pointer(eqData))
        coutResult = c.quant_sector(pukeycode.encode(c_encodeType), tradedate.encode(c_encodeType), options.encode(c_encodeType), refEqData)
        if coutResult != 0:
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
            return data
        tempData = refEqData._obj.contents
        if not isinstance(tempData, stEQData):
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
        else:
            data.resolve2RankData(tempData)
            c.quant_releasedata(pointer(tempData))
        return data

    @staticmethod
    def getdate(tradedate, offday=0, options="", *arga, **argb):
        """
        获取偏移N的交易日(同步请求)
        :param tradedate:交易日期
        :param offday:偏移天数
        :param options:
        :param arga:
        :param argb:
        :return:
        """

        data = c.EmQuantData()
        if(tradedate == None):
            tradedate = datetime.today().strftime("%Y-%m-%d")
        if(isinstance(tradedate, datetime) or isinstance(tradedate, date)):
            tradedate = tradedate.strftime("%Y-%m-%d")
        eqData = stEQData()
        refEqData = byref(pointer(eqData))
        coutResult = c.quant_gettradedate(tradedate.encode(c_encodeType), offday, options.encode(c_encodeType), refEqData)
        if coutResult != 0:
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
            return data
        tempData = refEqData._obj.contents
        if not isinstance(tempData, stEQData):
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
        else:
            data.resolve2RankData(tempData)
            c.quant_releasedata(pointer(tempData))
        return data

    @staticmethod
    def csc(code, indicators, startdate=None, enddate=None, options="", *arga, **argb):
        """
        历史分钟K线(同步请求) //code只支持单个股票
        :param code: 东财代码  多个代码间用半角逗号隔开，支持大小写。如 "300059.SZ,000002.SZ,000003.SZ,000004.SZ"
        :param indicators:东财指标 多个指标间用半角逗号隔开，支持大小写。如 "open,close,high"
        :param startdate:开始日期。如无分隔符，则必须为8位数字。格式支持:YYYYMMDD YYYY/MM/DD YYYY/M/D YYYY-MM-DD YYYY-M-D
        :param enddate:截止日期。如无分隔符，则必须为8位数字。格式支持:YYYYMMDD YYYY/MM/DD YYYY/M/D YYYY-MM-DD YYYY-M-D
        :param options:附加参数  多个参数以半角逗号隔开，"Period=1,Market=CNSESH,Order=1,Adjustflag=1,Curtype=1,Pricetype=1,Type=1"
        :return:EmQuantData
        """

        data = c.EmQuantData()

        if(enddate == None):
            enddate = datetime.today().strftime("%Y-%m-%d")
        if(startdate == None):
            startdate = enddate
        if(isinstance(startdate, datetime) or isinstance(startdate, date)):
            startdate = startdate.strftime("%Y-%m-%d")
        if(isinstance(enddate, datetime) or isinstance(enddate, date)):
            enddate = enddate.strftime("%Y-%m-%d")
        eqData = stEQData()
        refEqData = byref(pointer(eqData))
        coutResult = c.quant_csc(code.encode(c_encodeType), indicators.encode(c_encodeType), startdate.encode(c_encodeType), enddate.encode(c_encodeType), options.encode(c_encodeType), refEqData)
        if coutResult != 0:
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
            return data
        tempData = refEqData._obj.contents
        if not isinstance(tempData, stEQData):
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
        else:
            data.resolve26RankData(tempData)
            c.quant_releasedata(pointer(tempData))
        return data

    @staticmethod
    def csq(codes, indicators, options="", fncallback=None, userparams=None, *arga, **argb):
        """
        实时行情(异步)  每次indicators最多为64个 options: Pushtype=0 增量推送  1全量推送
        :param codes:东财代码  多个代码间用半角逗号隔开，支持大小写。如 "300059.SZ,000002.SZ,000003.SZ,000004.SZ"
        :param indicators:东财指标 多个指标间用半角逗号隔开，支持大小写。如 "open,close,high"
        :param options:Pushtype=0 增量推送  1全量推送
        :param fncallback:不同的接口可以设定不同的回调，传NULL则使用默认的主回调函数
        :param userparams:用户参数,回调时原样返回
        :param arga:
        :param argb:
        :return:流水号
        """

        data = c.EmQuantData()

        if userparams != None:
            userparams = userparams.encode(c_encodeType)

        global appQuoteCallback
        data.SerialID = c.quant_csq(codes.encode(c_encodeType), indicators.encode(c_encodeType), options.encode(c_encodeType), appQuoteCallback, userparams)
        global appQuoteFunctionDict
        if not callable(fncallback):
            appQuoteFunctionDict[data.SerialID] = DemoCallback
        else:
            appQuoteFunctionDict[data.SerialID] = fncallback
        return data

    @staticmethod
    def csqcancel(serialID):
        """
        取消实时行情订阅
        :param serialID:
        :return:
        """
        data = c.EmQuantData()
        data.ErrorCode = c.quant_csqcancel(serialID)
        data.ErrorMsg = c.geterrstring(data.ErrorCode)
        return data

    @staticmethod
    def cst(codes, indicators, startdatetime, enddatetime, options = "", fncallback=None, userparams=None):
        '''
        日内跳价服务(异步)  startdatetime和enddatetime格式(YYYYMMDDHHMMSS或HHMMSS表示系统日期当天的时间，两者需使用同一种格式)
        :param codes:东财代码  多个代码间用半角逗号隔开，支持大小写。如 "300059.SZ,000002.SZ,000003.SZ,000004.SZ"
        :param indicators:东财指标 多个指标间用半角逗号隔开，支持大小写。如 "open,close,high"
        :param startdate:开始时间
        :param enddate:结束时间
        :param options:
        :param fncallback:不同的接口可以设定不同的回调，传NULL则使用默认的主回调函数
        :param userparams:用户参数,回调时原样返回
        :param arga:
        :param argb:
        :return:流水号
        '''
        
        data = c.EmQuantData()


        global appQuoteCallback
        data.SerialID = c.quant_cst(codes.encode(c_encodeType), indicators.encode(c_encodeType), startdatetime.encode(c_encodeType), enddatetime.encode(c_encodeType),options.encode(c_encodeType), appQuoteCallback, userparams)
        global appQuoteFunctionDict
        if not callable(fncallback):
            appQuoteFunctionDict[data.SerialID] = cstCallBack
        else:
            appQuoteFunctionDict[data.SerialID] = fncallback
        return data
    
    @staticmethod
    def csqsnapshot(codes, indicators, options=""):
        '''
        行情快照(同步请求) 每次indicators最多为64个
        :param codes:东财代码  多个代码间用半角逗号隔开，支持大小写。如 "300059.SZ,000002.SZ,000003.SZ,000004.SZ"
        :param indicators:东财指标 多个指标间用半角逗号隔开，支持大小写。如 "open,close,high"
        :param options:附加参数  多个参数以半角逗号隔开，"Period=1,Market=CNSESH,Order=1,Adjustflag=1,Curtype=1,Pricetype=1,Type=1"
        '''
        
        data = c.EmQuantData()
        eqData = stEQData()
        refEqData = byref(pointer(eqData))
        coutResult = c.quant_csqsnapshot(codes.encode(c_encodeType), indicators.encode(c_encodeType), options.encode(c_encodeType), refEqData)
        if coutResult != 0:
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
            return data
        tempData = refEqData._obj.contents
        if not isinstance(tempData, stEQData):
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
        else:
            data.resolve25RankData(tempData)
            c.quant_releasedata(pointer(tempData))
        return data

    @staticmethod
    def ctr(ctrName, indicators, options=""):
        '''
        获取专题报表(同步请求)
        :param ctrName:
        :param indicators:
        :param options:附加参数
        '''

        data = c.EmQuantData()

        eqData = stEQCtrData()
        refEqData = byref(pointer(eqData))
        coutResult = c.quant_ctr(ctrName.encode(c_encodeType), indicators.encode(c_encodeType), options.encode(c_encodeType), refEqData)
        if coutResult != 0:
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
            return data
        tempData = refEqData._obj.contents
        if not isinstance(tempData, stEQCtrData):
            data.ErrorCode = coutResult
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
        else:
            data.resolveCtrData(tempData)
            c.quant_releasedata(pointer(tempData))
        return data
    
    @staticmethod
    def __toStrArray(args):
        if(args==None or args == ""): return [""]
        if(isinstance(args, str)):
            return [args]
        if(isinstance(args, tuple)): return [str(x) for x in args]
        if(isinstance(args, list)): return [str(x) for x in args]
        if(isinstance(args, int) or isinstance(args, float)) : return [str(args)]
        if(str(type(args)) == "<type 'unicode'>" ): return [args]
        return None

    @staticmethod
    def __toNumArray(args):
        if(args == None or args == ""): return None
        if(isinstance(args, tuple)): return [int(x) for x in args]
        if(isinstance(args, list)): return [int(x) for x in args]
        if(isinstance(args, int)): return [args]
        return None

    @staticmethod
    def __toString(args, joinStr = ","):
        v = c.__toStrArray(args)
        if(v == None): return None
        return joinStr.join(v)


def QuoteCallback(quotemessage, userparams):
    """
    实时行情回调处理函数
    :param quotemessage:
    :param userparams:
    :return:
    """
    try:
        quoteReceiveData = quotemessage.contents
        # print "version=%d, requestID=%d, serialID=%d, msgType=%d" % (quoteReceiveData.version, quoteReceiveData.requestID, quoteReceiveData.serialID,quoteReceiveData.msgType)
        global appQuoteFunctionDict
        quotecallbackhandle = appQuoteFunctionDict.get(quoteReceiveData.serialID)
        if not callable(quotecallbackhandle):
            quotecallbackhandle = DemoCallback
        data =c.EmQuantData()
        data.SerialID = quoteReceiveData.serialID
        data.RequestID = quoteReceiveData.requestID
        if quoteReceiveData.msgType == 0 or quoteReceiveData.msgType == 3:
            data.ErrorCode = quoteReceiveData.err
            data.ErrorMsg = c.geterrstring(data.ErrorCode)
            return -1
        # data.resolve3RankData(quoteReceiveData.pEQData[0])
        data.resolve25RankData(quoteReceiveData.pEQData[0])
        # c.quant_releasedata(quoteReceiveData.pEQData)
        quotecallbackhandle(data)
    except Exception as e:
        print("QuoteCallback Exception", e)
    return 1

def DemoCallback(quantdata):
    """
    DemoCallback 是EM_CSQ订阅时提供的回调函数模板。该函数只有一个为c.EmQuantData类型的参数quantdata
    :param quantdata:c.EmQuantData
    :return:
    """
    print("QuoteCallback,", str(quantdata))

def cstCallBack(quantdata):
    '''
    cstCallBack 是日内跳价服务提供的回调函数模板
    '''
    for i in range(0, len(quantdata.Codes)):
        length = len(quantdata.Dates)
        for it in quantdata.Data.keys():
            print(it)
            for k in range(0, length):
                for j in range(0, len(quantdata.Indicators)):
                    print(quantdata.Data[it][j * length + k], " ", end = "")
                print()


appQuoteCallback = c_DataCallback(QuoteCallback)

