#coding:utf8
import socket
import binascii
import struct
import time
import threading
import math
import random

import csv
import os
from datetime import datetime, timedelta

class DeviceSystem_Modbus_garram:
    @staticmethod
    def get_ModuleName(VirtualDevice, requireCRC = False):
        print("取得ModbusName")
        byte = [id, 0x3]
        _ModuleName = VirtualDevice.ModuleName.encode("utf8")
        byte.append(_ModuleName // 0x100)
        byte.append(_ModuleName % 0x100)
        byte += struct.pack(str(_ModuleName.__len__())+"b", *_ModuleName)
        return [id, 0x3, 0x00, 0x00, 0x00, 0x32] if not requireCRC else [id, 0x3, 0x00, 0x00, 0x00, 0x32]

    @staticmethod
    def get_Version(VirtualDevice, requireCRC = False):
        print("取得Version")
        byte = [id, 0x3, 0x0, 0x2] #資料長度
        byte.append(VirtualDevice.Version // 0x100)
        byte.append(VirtualDevice.Version % 0x100)
        return byte if not requireCRC else byte

    @staticmethod
    def get_Source_id(VirtualDevice, requireCRC = False):
        print("取得Source_id")
        byte = [id, 0x3, 0x0, 0x2] #資料長度
        byte.append(VirtualDevice.Source_id // 0x100)
        byte.append(VirtualDevice.Source_id % 0x100)
        return byte if not requireCRC else byte

    @staticmethod
    def get_baudrate(VirtualDevice, requireCRC = False):
        print("取得baudrate")
        byte = [id, 0x3, 0x0, 0x2] #資料長度
        byte.append(VirtualDevice.Baudrate // 0x100)
        byte.append(VirtualDevice.Baudrate % 0x100)
        return byte if not requireCRC else byte

    @staticmethod
    def get_StopParity(VirtualDevice, requireCRC = False):
        print("取得Stopbit, Paritybit, Databit")
        byte = [id, 0x3, 0x0, 0x6]
        byte.append(VirtualDevice.Stopbit // 0x100)
        byte.append(VirtualDevice.Stopbit % 0x100)
        byte.append(VirtualDevice.Paritybit // 0x100)
        byte.append(VirtualDevice.Paritybit % 0x100)
        byte.append(VirtualDevice.Databit // 0x100)
        byte.append(VirtualDevice.Databit % 0x100)
        return byte if not requireCRC else byte

    @staticmethod
    def get_Chnum(VirtualDevice, requireCRC = False):
        print("取得Chnum")
        byte = [id, 0x3, 0x0, 0x2]
        byte.append(VirtualDevice.Chnum // 0x100)
        byte.append(VirtualDevice.Chnum % 0x100)
        return byte if not requireCRC else byte

    @staticmethod
    def get_ip(VirtualDevice, requireCRC = False):
        print("取得ip")
        _ip = VirtualDevice.ip.split(".")
        byte = [_ip.__len__() * 2]
        for i in range(_ip):
            _val = int(_ip[i])
            byte += _val // 0x100
            byte += _val % 0x100
        byte.insert(0, VirtualDevice.id)
        byte.insert(1, 0x3)
        return byte if not requireCRC else byte

    @staticmethod
    def get_mask(VirtualDevice, requireCRC = False):
        print("取得mask")
        _mask = VirtualDevice.mask.split(".")
        byte = [_mask.__len__() * 2]
        for i in range(_mask):
            _val = int(_mask[i])
            byte += _val // 0x100
            byte += _val % 0x100
        byte.insert(0, VirtualDevice.id)
        byte.insert(1, 0x3)
        return byte if not requireCRC else byte
    
    @staticmethod
    def get_gateway(VirtualDevice, requireCRC = False):
        print("取得gateway")
        _gateway = VirtualDevice.gateway.split(".")
        byte = [_gateway.__len__() * 2]
        for i in range(_gateway):
            _val = int(_gateway[i])
            byte += _val // 0x100
            byte += _val % 0x100
        byte.insert(0, VirtualDevice.id)
        byte.insert(1, 0x3)
        return byte if not requireCRC else byte
    
    @staticmethod
    def get_mac(VirtualDevice, requireCRC = False):
        print("取得mac")
        byte = [id, 0x3, VirtualDevice.mac.__len__()]
        for i in range(0, VirtualDevice.mac__len__(), 2):
            _val = int(VirtualDevice.mac[i:i+2])
            byte += _val // 0x100
            byte += _val % 0x100
        byte.insert(0, VirtualDevice.id)
        byte.insert(1, 0x3)

#建置虛擬頻道
class VirtualChannel:
    def __init__(self,chTagName, TagName, type, unit, datatype, Source_ID, Source_Address, Source_DataType, Source_Gain, Source_Off_set, Source_Function, Source_WordOrder, Source_ByteOrder, Source_Interface, Source_Interval, Source_IP, AIEnable, Point):
        print("定義虛擬頻道")
        self.chTagName = chTagName
        self.TagName = TagName
        self.type = type
        self.unit = unit
        self.datatype = datatype
        self.Source_ID = Source_ID
        self.Source_Address = Source_Address
        self.Source_DataType = Source_DataType
        self.Source_Gain = Source_Gain
        self.Source_Off_set = Source_Off_set
        self.Source_Function = Source_Function
        self.Source_WordOrder = Source_WordOrder
        self.Source_ByteOrder = Source_ByteOrder
        self.Source_Interface = Source_Interface
        self.Source_Interval = Source_Interval
        self.Source_IP = Source_IP
        self.AIEnable = AIEnable
        self.Point = Point
        self.value = None

    @staticmethod
    def returnChannel(TagName, unit):
        channelName = VirtualChannel.strtounicode(TagName, 32) 
        channelUnit = VirtualChannel.strtounicode(unit, 32)
        databytes = list(channelName + channelUnit) + [0,1,0,0,0,1,0,2,39,16,0,0,0,4,1,0,0,5,0,2,0,0,0,0,0,0,0,0,0,0,170,170,0,1,0,1]
        #databytes = [0,67,0,72,0,45,0,48 + index,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     #3,118,0,103,0,47,0,109,0,51,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     #0,1,0,0,0,1,0,2,39,16,0,0,0,4,1,0,0,5,0,2,0,0,0,0,0,0,0,0,0,0,170,170,0,1,0,1]
        #databytes = [0,67,0,72,0,45,0,48 + index,0,0,63,128,0,0,0,0,0,0,66,200,0,0,0,0,5,1,0,0,5,0,0,0,0,37,0,0,0,0,0,0,0,0,66,200,0,0,0,0,5,1,0,0,5,0,0,0,0,0,63,128,99,192,0,0,0,1,0,0,0,1,0,2,39,16,0,0,0,4,1,0,0,5,0,2,0,0,0,0,0,0,0,0,0,0,170,170,0,1,0,1]
        return databytes

    @staticmethod
    def strtounicode(value, makeupbits):
        bytes = ()
        for i in range(len(value)):
            _byte2 = ord(value[i])
            bytes += (_byte2 // 0x100, _byte2 % 0x100)
        if(len(bytes) < makeupbits):
            for a in range(len(bytes), 32, 1):
                bytes += (0,)
        return bytes

#建置虛擬設備
class VirtualDevice:
    def __init__(self, ModuleName, version = 0.0, source_id = 1, baudrate = 0, Stopbit = 0, Paritybit = 0, Databit = 0, Chnum = 120, ip = "192.168.2.67", mask = "255.255.255.0", gateway = "192.168.0.253", mac = "0a256d88219a"):
        self.ModbusName = ModuleName
        self.Version = version
        self.Source_id = source_id
        self.Baudrate = baudrate
        self.Stopbit = Stopbit
        self.Paritybit = Paritybit
        self.Databit = Databit
        self.Chnum = Chnum
        self.ip = ip
        self.mask = mask
        self.gateway = gateway
        self.mac = mac

        self.channels = [] #設備的通訊

        #ModbusName, vesion, source_id, baudrate, stopbit, parityid, databit, chnum, ip, mask, gateway, mac 
        #以下參考
        #(10, 13, 0, 0, 0, 103, -> 1, 3, 100, 54, 73, 87, 32, 98, 101, 3, 8, 0, 0, 0, 0, 0, 1, 0, 0, 0, 8, 0, 6, 0, 0, 0, 0, 170, 170, 255, 255, 170, 170, 0, 192, 0, 168, 0, 2, 0, 138, 0, 255, 0, 255, 0, 240, 0, 0, 0, 192, 0, 168, 0, 0, 0, 253, 0, 2, 0, 26, 0, 177, 0, 2, 0, 131, 0, 105, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170)
                                             #54, 73, 87, 32, 98, 101, 3, 8, 0, 1, 0, 0, 0, 0, 0, 0, 0, 8, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 0, 0, 0, 0, 0, 1, 0, 255, 0, 255, 0, 255, 0, 0, 0, 192, 0, 168, 0, 0, 0, 253, 0, 1, 0, 129, 0, 26, 0, 35, 0, 194, 0, 119
        self.modbus = []
        self.modbus += byte_to_Asc(list(bytes(self.ModbusName, 'big5'))) #(1) ----加入ModbusName
        self.modbus += self.handlerVersion(self.Version) #(2) ------------加入Version
        self.modbus += [self.Source_id // 0x100, self.Source_id % 0x100] #(3) ----------------加入Source_id
        self.modbus += [self.Baudrate // 0x100, self.Baudrate % 0x100] #(4) ----------------加入baudrate
        self.modbus += [self.Stopbit // 0x100, self.Stopbit % 0x100] #(5) ----------------加入stopbit
        self.modbus += [self.Paritybit // 0x100, self.Paritybit % 0x100] #(6) ----------------加入payitybit
        self.modbus += [self.Databit // 0x100, self.Databit % 0x100] #(7) ----------------加入databit
        self.modbus += [self.Chnum // 0x100, self.Chnum % 0x100] #(8) ----------------加入chnum
        
        self.modbus += [0,0,0,0,0,0,0,0,0,0] #暫不處理的空白字元(com1, com2, reset, empty, empty)

        self.modbus += self.handlerIP4Format(self.ip) #(9) ----------------加入ip
        self.modbus += self.handlerIP4Format(self.mask) #(10) ----------------加入mask
        self.modbus += self.handlerIP4Format(self.gateway) #(11) ----------------加入gateway
        self.modbus += self.handlerIP6Format(self.mac) #(12) ----------------加入mac

        self.modbus = tuple(self.modbus)
    
    #回傳頻道資料
    def returnChannel(self, channelIndex):
        print("the channelIndex: " + str(channelIndex))
        return tuple(self.channels[int(channelIndex)])
        
    #加入虛擬設備
    def AddVirtualChannel(self, virtualChannel): #暫先加入假的
        self.channels.append(virtualChannel)

    def handlerVersion(self, value):
        ver = value.split(".")
        result = []
        result += [int(ver[0], 10), int(ver[1], 10)]
        return result

    #處理ip4類型的字元格 to bytes
    def handlerIP4Format(self, value):
        singleip = value.split(".")
        result = []
        for i in range(singleip.__len__()):
            result += [int(singleip[i]) // 0x100, int(singleip[i]) % 0x100] #共佔8個位元
        return result

    #處理ip4類型的字元格 to bytes
    def handlerIP6Format(self, value):
        result = []
        for i in range(0, value.__len__(), 2):
            tmp = int(value[i:i+2], 16)
            result += [tmp // 0x100, tmp % 0x100] #共佔12個位元
        return result

    #隨機產生特定頻道數值
    def getRandomFloat(self, channelCount, condition):
        result = []
        for i in range(channelCount):
            thefloat = random.uniform(condition['min'], condition['max'])
            #print("頻道" + str(i) + "隨機即時值: " + str(thefloat))
            thevalue = struct.pack('f', thefloat)
            val = [thevalue[1], thevalue[0], thevalue[3], thevalue[2]]
            result += list(val)
        return tuple(result)
    
#取得本機對外連線的私有網路
def comm_getselfIP():
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            myip = s.getsockname()[0]
            return myip
        except:
            return None    
        finally:
            s.close()

#(1) 進行大小端位對調
def byte_to_Asc(bytelist):
    new_bytes = []
    #python迴圈判斷 參考: https://medium.com/ccclub/ccclub-python-for-beginners-tutorial-4990a5757aa6
    for i in range(0, bytelist.__len__(), 2): #開始, 結束, 遞增值
        tmp_value = (bytelist[i] * 0x100) + bytelist[i + 1]
        new_bytes.append(tmp_value % 0x100)
        new_bytes.append(tmp_value >> 8)
    return new_bytes

#這裡針對I6_Web進行處理
def funcHandler_1(id, payload, vDevice):
    print("處理Function_1 的機制")

def funcHandler_2(id, payload, vDevice):
    print("處理Function_2 的機制")

def funcHandler_3(id, payload, vDevice):
    print("處理Function_3 的機制")
    address = (payload[0] * 0x100) + payload[1]
    len = (payload[2] * 0x100) + payload[3]
    if address == 0x0: #ModbusName
       print("ModbusName")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address == 0x3: #Version
       print("Version")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address == 0x4: #source_id
       print("source_id")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address == 0x5: #Baudrate
       print("baudrate")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address == 0x6: #stopparitybit
       print("StopParitybit")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address == 0x9: #CHnum
       print("Chnum")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address == 0xF: #ip
       print("ip")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address == 0x13: #mask
       print("mask")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address == 0x17: #gateway
       print("gateway")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address == 0x1B: #mac
       print("mac")
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       return Header + MyDevice.modbus[address * 2:(address + len) * 2]

    elif address >= 0x100 and address % 0x0100 == 0: 
       _index = int(address / 0x0100) - 1
       print("取得頻道索引: " + str(_index))
       Header = (id, 0x3, len * 2) #id, FuncNum, payload_len
       payload = vDevice.returnChannel(_index)
       return Header + payload

def funcHandler_4(id, payload, vDevice):
    try:
        print("處理即時值<FuncNum:4>")
        #address = (payload[0] * 0x100) + payload[1]
        _len = (payload[2] * 0x100) + payload[3]
        Header = (id, 0x4, _len//2) #id, FuncNum, payload_len
        #return Header + (195, 234, 69, 221, 69, 112, 69, 220, 222, 240, 68, 181, 118, 6, 69, 220, 180, 248, 69, 220, 241, 87, 66, 98, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0, 80, 0, 64, 0)
        return Header + MyDevice.getRandomFloat(_len//2, {'min':100.0, 'max':140.00})#120//4
    except:
        print("func4 error")

def handlerModbusCommand(id, funcNum, payload, vDevice):
    return {
        1: funcHandler_1,
        2: funcHandler_2,
        3: funcHandler_3,
        4: funcHandler_4
    }[funcNum](id, payload, vDevice)

#建置TCP標頭
def TCPHeader(payload): #Modbus TCP加戴標頭(6bit)
    return (0x0E, 0x2F, 0x0, 0x0, 0x0, 0x6) + payload

def jobHandler(*args):
    while(True):
        try:
            RaspMessage = args[0].recv(1024) #取得RaspBerry發佈來的Modbus Tcp Request
            #判斷RaspBerry要的是什麼資料
            print("Modbus Request:--")
            print(RaspMessage)
            #print("check the byte length: " + str(len(RaspMessage)))
            msg = struct.unpack(str(len(RaspMessage))+'B', RaspMessage)
            msglen = msg[5] #封包的長度
            realmsg = msg[6:] #主要處理封包內容
        
            if msglen != realmsg.__len__():
                return

            #取得要回傳的payload(範例如ttt)
            payload = handlerModbusCommand(realmsg[0], realmsg[1], realmsg[2:], args[2])
            #ttt = (10, 13, 0, 0, 0, 6, 1, 3, 0, 0, 0, 77) #讀取系統值
            #requestMsg = struct.pack(str(len(ttt))+'B', *ttt)
            payload = TCPHeader(payload)
            #print(payload)
            requestMsg = None
            #if payload[8] == 4:
                #requestMsg = struct.pack("!9B"+str(len(payload)-9)+'f', *payload)
            #else:
            requestMsg = struct.pack(str(len(payload))+'B', *payload)
            #requestMsg = struct.pack("!9i"+str(len(payload)-9)+'B', *payload)
            args[0].send(requestMsg)
            #args[0].close()
        except:
            print("error happened")
            args[0].close() #即中斷連線
            return
        finally:
            if args[0] is not None:
                #args[0].close()
                pass

#處理HTML request的部分
def jobHTMLHandler(*args):
    try:
        print("STEP_1")
        package_width = 0#要紀錄post的 Content-Length
        with args[0] as c:
            ve = b''
            while True:
                print("STEP_2")
                slice = c.recv(1024)
                #if (len(slice) < 1): break
                print(slice)
                ve += slice
                print("STEP_3")                
                #以下為判斷是否接收完畢
                #若標頭裡包含Content-Length, 則以該Content-Length的值作為依據
                if(b'Content-Length: ' in ve):
                    if(package_width == 0):
                        sub_ve = ve[ve.index(b'Content-Length: ') + 0x10:] #0x10是'Content-Length: '的字元長度
                        if sub_ve.find(b'\r\n') >= 0:
                            package_width = int(sub_ve[0:sub_ve.index(b'\r\n')].lstrip().rstrip().decode('utf-8'))
                        else:
                            package_width = int(sub_ve[0:].lstrip().rstrip().decode('utf-8'))
                    if(b'\r\n\r\n' in ve):
                        if(len(ve[ve.index(b'\r\n\r\n') + 0x4:]) == package_width): break#0x4是'\r\n\r\n'的字元長度
                else:
                    if(b'\r\n\r\n' in ve):
                        break
                #應該要多一個timeout機制
                
            try:
                # (1)處理檔案二進位的部分
                #ve.index(b'WebKitFormBoundary') #這裡若出錯ValueError, 代表該request非上傳檔
                content = ve.split(b'\r\n\r\n')
                if(b'WebKitFormBoundary' in content[0]):#ve
                    #content = ve.split(b'\r\n\r\n')
                    Attr = HttpParse(content[0].decode('utf-8')) #(1)標題部分
                    formData = FormDataParse(content[1].decode('utf-8')) #(2)formData部分
                    #(3)檔案內容二進位

                    payload = content[2].split(formData['WebKitFormBoundary'].encode('utf-8'))[0] #Blob[2].split(b'\r\n')[0]
                    c = HttpRouteChunked(Attr, formData, payload, c) #
                elif(b'/ChunkedDemo' in content[0]):
                    #content = ve.split(b'\r\n\r\n')
                    Attr = HttpParse(content[0].decode('utf-8')) #(1)標題部分
                    body = content[1].decode('utf-8')
                    c = HttpRoutedChunked2(Attr, body, c)#
                elif(b'.mp4' in content[0]): #處理mp4的檔案
                    #content = ve.split(b'\r\n\r\n')
                    Attr = HttpParse(content[0].decode('utf-8')) #(1)標題部分
                    #body = content[1].decode('utf-8')
                    body = MP4FileHandler(Attr)
                    c = HttpRoutedChunked3(Attr, body, c)
                elif(b'data.csv' in content[0] or b'data.CSV' in content[0]): #下載CSV檔部分
                    Attr = HttpParse(content[0].decode('utf-8')) #(1)標題部分
                    print(Attr)
                    requestAttr = Attr["body"]["attr"].split("&") #再分別取startTime, endTime, interval
                    start = requestAttr[1].split("=")[1] #啟始時間
                    end = requestAttr[2].split("=")[1] #結束時間
                    interval = requestAttr[3].split("=")[1] #間隔
                    _start = getDateTime(start)
                    _end = getDateTime(end)

                    #回傳相關的data.csv檔
                    #writeCSV(startTime, endTime, interval)
                    writeCSV(_start, _end, interval) #datetime(2021,11,26,0,0,0)
                    print("-------- STOP HERE!(1) --------")
                    csvContent = readCSV(os.getcwd() + "\\data_" + _start.strftime("%Y%m%d%H%M%S") + "_" + _end.strftime("%Y%m%d%H%M%S") + ".csv")
                    print("-------- STOP HERE!(2) --------")
                    httpHeader = "HTTP/1.0 200 OK\r\nContent-Type:text/csv; charset=utf-8\r\n"
                    httpHeader += "ModuleName: CTR100\r\n"
                    httpHeader += "Content-Disposition: attachment;filename=data.csv" + "\r\n\r\n" #取得其內容值
                    #httpHeader += "Content-Length: " + str(len(csvContent)) + "\r\n\r\n"
                    
                    
                    print("SAM CHECK THE LENGTH: " + str(len(csvContent)))
                    print("SAM CHECK THE LAST 1 BIT:" + str(csvContent[csvContent.__len__()-1]))
                    
                    header_byte = httpHeader.encode(encoding="utf-8")
                    #content = struct.pack('!'+str(csvContent.__len__())+'B', *csvContent)
                    package = header_byte + csvContent
                    c.send(package)
                    if(os.path.isfile(os.getcwd() + "\\data_" + _start.strftime("%Y%m%d%H%M%S") + "_" + _end.strftime("%Y%m%d%H%M%S") + ".csv")):
                        os.remove(os.getcwd() + "\\data_" + _start.strftime("%Y%m%d%H%M%S") + "_" + _end.strftime("%Y%m%d%H%M%S") + ".csv")
                        #pass
                else:
                    # (2)處理一般的檔案, API部分
                    #完全上傳二進位檔案
                    content = ve.decode('utf-8')
                    #globals.addText(globals._response, content)
                    #*******這裡將接收到的訊息, 紀錄到form*******
                    #if(globals.console_enable):
                        #globals.addText(globals._response, content)
                    Attr = HttpParse(content)
                    print("***** 進來處理http request " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    Attr['header']['uri'] = unquote(Attr['header']['uri'], 'utf-8')
                    response = HttpRoute(Attr) #主處理作業
                    #應該依Header的內容(method, content-type,..等決定是否要解析body)
                    print("***** 完成進來處理http request" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    #res_byte = response.encode("utf-8")
                    package = struct.pack('!'+str(response.__len__())+'B', *response)
                    c.send(package)
                    #if(globals.console_enable):
                        #globals.addText(globals._request, response)
                    # ******** 這裡加要發佈的值 紀錄到form介面 ********
            except ValueError as e:
                print("value error")
            finally:
                pass
                
    except IOError as er:
        print("http Socket error")
    except Exception as e:
        print("normal error")
    finally:
        args[0].close()
        print("disconnected.")

#將明宏的時間文字轉換為時間物件
def getDateTime(timestr):
    try:
        gapTime = timestr.split("-")
        return datetime(int(gapTime[0]), int(gapTime[1]), int(gapTime[2]), int(gapTime[3]), int(gapTime[4]), 0)
    except Exception as e:
        return None
        
#寫入CSV檔案
def writeCSV(startTime, endTime, interval):
    try:
        contextPath=os.getcwd()
        path=contextPath + "\\data_" + startTime.strftime("%Y%m%d%H%M%S") + "_" + endTime.strftime("%Y%m%d%H%M%S") + ".csv"
        print(path)
        #fields = ["Time","a","室外溫度(°C)","室外濕度(%)","室外CO2()","1F溫度-1(°C)","1F溫度-2(°C)","1F溫度-3(°C)","1F濕度-1(%)","1F濕度-2(%)","1F濕度-3(%)","1F CO2(ppm)","1F內部平均溫度(°C)","外部溫度-內部溫度(°C)","1F內部平均濕度()","內部濕度-外部濕度(%)","情境:外界濕度過低(mS/cm","情境:換季時，雨天()","情境:冬天超低溫()","情境:夏日超高溫()","情境:高濕度換氣()","情境:夏日高溫(白天)()","情境:夏夜高溫()","情境:夏夜換氣()","情境:冬日換氣(內部)()","情境:冬日換氣(溫差)()","情境:冬夜換氣()","情境:冬日低溫()","情境:白日一般(內部)()","情境:白日一般(溫差)()","情境:白日低溫()","CH-30()","CH-31()","CH-32()","CH-33()","CH-34()","CH-35()","CH-36()","CH-37()","CH-38()","CH-39()","CH-40()","CH-41()","CH-42()","CH-43()","CH-44()","CH-45()","CH-46()","CH-47()","CH-48()","CH-49()","CH-50()","CH-51()","CH-52()","CH-53()","CH-54()","CH-55()","CH-56()","CH-57()","CH-58()","CH-59()","CH-60()","CH-61()","CH-62()","CH-63()","CH-64()","CH-65()","CH-66()","CH-67()","CH-68()","CH-69()","CH-70()","CH-71()","CH-72()","CH-73()","CH-74()","CH-75()","CH-76()","CH-77()","CH-78()","CH-79()","CH-80()","CH-81()","CH-82()","CH-83()","CH-84()","CH-85()","CH-86()","CH-87()","CH-88()","CH-89()","CH-90()","CH-91()","CH-92()","CH-93()","CH-94()","CH-95()","CH-96()","CH-97()","CH-98()","CH-99()","CH-100()","CH-101()","CH-102()","CH-103()","CH-104()","CH-105()", "CH-106()", "CH-107()", "CH-108()", "CH-109()", "CH-110()", "CH-111()", "CH-112()", "CH-113()", "CH-114()", "CH-115()", "CH-116()", "CH-117()", "CH-118()", "CH-119()", "CH-120()", "地點", "經度", "緯度", "海拔"]
        fields = ["Time"," ","室外溫度(°C)","室外濕度(%)","室外CO2()","1F溫度-1(°C)","1F溫度-2(°C)","1F溫度-3(°C)","1F濕度-1(%)","1F濕度-2(%)","1F濕度-3(%)","1F CO2(ppm)","1F內部平均溫度(°C)","外部溫度-內部溫度(°C)","1F內部平均濕度()","內部濕度-外部濕度(%)","情境:外界濕度過低(mS/cm","情境:換季時，雨天()","情境:冬天超低溫()","情境:夏日超高溫()","情境:高濕度換氣()","情境:夏日高溫(白天)()","情境:夏夜高溫()","情境:夏夜換氣()","情境:冬日換氣(內部)()","情境:冬日換氣(溫差)()","情境:冬夜換氣()","情境:冬日低溫()","情境:白日一般(內部)()","情境:白日一般(溫差)()","情境:白日低溫()","CH-30()","CH-31()","CH-32()","CH-33()","CH-34()","CH-35()","CH-36()","CH-37()","CH-38()","CH-39()","CH-40()","CH-41()","CH-42()","CH-43()","CH-44()","CH-45()","CH-46()","CH-47()","CH-48()","CH-49()","CH-50()","CH-51()","CH-52()","CH-53()","CH-54()","CH-55()","CH-56()","CH-57()","CH-58()","CH-59()","CH-60()","CH-61()","CH-62()","CH-63()","CH-64()","CH-65()","CH-66()","CH-67()","CH-68()","CH-69()","CH-70()","CH-71()","CH-72()","CH-73()","CH-74()","CH-75()","CH-76()","CH-77()","CH-78()","CH-79()","CH-80()","CH-81()","CH-82()","CH-83()","CH-84()","CH-85()","CH-86()","CH-87()","CH-88()","CH-89()","CH-90()","CH-91()","CH-92()","CH-93()","CH-94()","CH-95()","CH-96()","CH-97()","CH-98()","CH-99()","CH-100()","CH-101()","CH-102()","CH-103()","CH-104()","CH-105()", "CH-106()", "CH-107()", "CH-108()", "CH-109()", "CH-110()", "CH-111()", "CH-112()", "CH-113()", "CH-114()", "CH-115()", "CH-116()", "CH-117()", "CH-118()", "CH-119()", "CH-120()", "地點", "經度", "緯度", "海拔"]
        data_row = []
        
        #查詢檔案是否存在
        if not os.path.isfile(path):
            file = open(path, "a+")
            file.close()
        
        with open(path,'w', newline="", encoding="utf8") as f:
            csv_write = csv.writer(f)
            #逐一處理寫入
            loop = True
            csv_write.writerow(fields) #輸入欄位
            while(loop):
                for i in range(0, fields.__len__()):
                    if i == 0:
                        data_row.append(startTime.strftime("%y/%m/%d")) #加入日期
                    elif i == 1:
                        data_row.append(startTime.strftime("%H:%M:%S")) #加入時間
                    else:
                        data_row.append(str(round(random.uniform(0.1, 230.0), 2))) #加入隨機數值
                csv_write.writerow(data_row) #寫入欄位名稱
                data_row.clear()    
                startTime = startTime + timedelta(seconds=int(interval))
                loop = True if(startTime <= endTime) else False #若時間仍在其範圍中, 則仍繼續運行

    except Exception as e:
        print("some error happened..")

#讀取csv檔
def readCSV(path):
    if(os.path.isfile(path)):
        #以二進位讀取
        with open(path, "rb") as f:
            content=f.read()#一次讀取所有檔案內容
            return content
    else:
        return None

#讀取標頭
def HttpParse(content):
    msg = content.split("\r\n\r\n")
    Header = {}
    Body = {}
    allheader = msg[0].split('\r\n')
    for i in range(allheader.__len__()):
        if "HTTP/" in allheader[i]:
            Header['method'], Header['uri'], Header['version'] = allheader[0].split(' ')
            if Header['method'] == 'GET' and '?' in Header['uri']:
                uriattr = Header['uri'].split('?')
                Header['uri'] = uriattr[0]
                Body["attr"] =  uriattr[1]
                
            elif Header['method'] == 'POST':
                if(msg.__len__() > 1):
                    Body['attr'] = msg[1]

        if "Content-Type" in allheader[i]:
            Header['Content-Type'] = allheader[i].split(":")[1].strip()
        if "User-Agent" in allheader[i]:
            Header['User-Agent'] = allheader[i].split(":")[1].strip()
        if "Accept" in allheader[i]:
            Header['Accept'] = allheader[i].split(":")[1].strip()
        if "Host" in allheader[i]:
            Header['Host'] = allheader[i].split(":")[1].strip()
            if len(allheader[i].split(":")) > 2:
                Header['Post'] = allheader[i].split(":")[2]
        if "Accept-Encoding" in allheader[i]:
            Header['Accept-Encoding'] = allheader[i].split(":")[1].strip()
        if "Connection" in allheader[i]:
            Header['Connection'] = allheader[i].split(":")[1].strip()
        if "Content-Length" in allheader[i]:
            Header['Content-Length'] = allheader[i].split(":")[1].strip()
        if "Postman-Token" in allheader[i]:
            Header['Postman-Token'] = allheader[i].split(":")[1].strip()
        #以下是後來加入的
        if "Origin" in allheader[i]:
            Header['Origin'] = allheader[i].split(":")[1].strip()
        if "Accept-Language" in allheader[i]:
            Header['Accept-Language'] = allheader[i].split(":")[1].strip()
        if "Referer" in allheader[i]:
            Header['Referer'] = allheader[i].split(":")[1].strip()
        if "Content-Disposition" in allheader[i]:
            Header['Content-Disposition'] = allheader[i].split(":")[1].strip()

    return {'header':Header, 'body':Body}

#自動產生CSV檔案     
def generalCSV(*args):
    if(args.Count < 2): #起碼須要2個參數(啟始時間 / 結束時間)
        return
    startTime = args[0] #啟始時間
    endTime = args[1] #結束時間
    
if __name__ == '__main__':
    print("模擬設備運行!..")
    selfIP = comm_getselfIP()
    MyDevice = VirtualDevice("I6 Web", "2.88", 1, 0, 0, 1, 8, 4, selfIP, "255.255.255.0", "192.168.0.253", "01811a23c277")
    MyDevice.AddVirtualChannel(VirtualChannel.returnChannel("PM2.5", "μg/m3"))
    MyDevice.AddVirtualChannel(VirtualChannel.returnChannel("溫度", "m3"))
    MyDevice.AddVirtualChannel(VirtualChannel.returnChannel("濕度", "m3"))
    MyDevice.AddVirtualChannel(VirtualChannel.returnChannel("二氧化碳", "°C"))
    print(MyDevice.modbus)
    
    HOST = selfIP
    PORT = 504
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(20) #等待連線佇列
    
    #測試自動產生CSV檔案
    #writeCSV(datetime(2021,11,26,0,0,0), datetime(2021,11,26,0,1,0), 1)
    #CSV_content=readCSV(os.getcwd()+"\\data.csv")
    #print(CSV_content)
    
    while(True):
        print("模擬設備已啟動! 準備偵聽 " + str(PORT))
        conn, addr= server.accept()
        print("取得連線!!")
        ppp = threading.Thread(target = jobHTMLHandler, daemon = True, args=(conn, addr, MyDevice))
        ppp.start()


    