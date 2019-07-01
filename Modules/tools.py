#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673 & pipiche38
#
"""
    Module : tools.py

    Description: Rfplayer tools
"""




from Modules.infoType0 import DecodeInfoType0
from Modules.infoType1 import DecodeInfoType1
from Modules.infoType2 import DecodeInfoType2
from Modules.infoType3 import DecodeInfoType3
from Modules.infoType4 import DecodeInfoType4
from Modules.infoType5 import DecodeInfoType5
from Modules.infoType6 import DecodeInfoType6
from Modules.infoType7 import DecodeInfoType7
from Modules.infoType8 import DecodeInfoType8
from Modules.infoType9 import DecodeInfoType9
from Modules.infoType10 import DecodeInfoType10
from Modules.infoType11 import DecodeInfoType11

def ManualAddDevice (self, MDType, MDiD) :
    if MDType =="1": protocol="2" #visonic433
    if MDType =="2": protocol="2" #visonic868
    if MDType =="3": protocol="4" #chacon
    if MDType =="4": protocol="6" #domia
    if MDType =="5": protocol="1" #X10
    if MDType =="6" or MDType =="61" or MDType =="62" or MDType =="63": protocol="8" #X2D433
    if MDType =="7" or MDType =="71" or MDType =="72" or MDType =="73": protocol="8" #X2D868
    if MDType =="8": protocol="8" #X2DSHUTTER
    if MDType =="11" or MDType =="14": protocol="9" #RTS
    if MDType =="12": protocol="3" #BLYSS
    if MDType =="13": protocol="11" #PARROT
    if MDType =="16": protocol="10" #KD101
    
    id = MDiD
    area = int(id) & 255
    
    if MDType == "4" or MDType == "5" or MDType == "13" :
        infoType="0"
    if MDType == "3" or MDType == "12" or MDType == "16" :
        infoType="1"
    if MDType == "1" or MDType == "2" :
        infoType="2"
    if MDType == "11" or MDType == "14" :
        infoType="3"
    if MDType == "6" or MDType == "61" or MDType == "62" or MDType == "63" or MDType == "7" or MDType == "71" or MDType == "72" or MDType == "73" :
        infoType="10"
    if MDType == "8":
        infoType="11"
    if infoType == "0" or infoType == "1" :
        Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol)}
        stype=0
    if infoType == "2" and MDType =="1":
        Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "frequency":"433920"}
        stype=0
    if infoType == "2" and MDType =="2":
        Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "frequency":"868950"}
        stype=0
    if infoType == "3" and MDType =="11":
        Options = {"infoType": infoType, "id": str(id), "protocol": str(protocol), "subType": "0", "LevelActions": "|||||", "LevelNames": "Off/Down|My|On/Up|Assoc", "LevelOffHidden": "False", "SelectorStyle": "0"}
        stype=18
    if infoType == "3" and MDType =="14":
        Options = {"infoType": infoType, "id": str(id), "protocol": str(protocol), "subType": "1", "LevelActions": "||||", "LevelNames": "Off|Left button|Right button", "LevelOffHidden": "False", "SelectorStyle": "0"}
        stype=18
    if infoType == "10" and MDType =="6":
        Options = {"infoType":infoType, "id": str(id), "function": "2", "protocol": str(protocol), "frequency":"433920", "LevelActions": "|||||||||", "LevelNames": "Off|HG|Eco|Moderat|Medio|Comfort|Assoc", "LevelOffHidden": "False", "SelectorStyle": "0"}
        stype=18
    if infoType == "10" and MDType =="61":
        Options = {"infoType":infoType, "id": str(id), "function": "1", "protocol": str(protocol), "frequency":"433920"}
        stype=0
    if infoType == "10" and MDType =="62":
        Options = {"infoType":infoType, "id": str(id), "function": "12", "protocol": str(protocol), "frequency":"433920"}
        stype=0
    if infoType == "10" and MDType =="63":
        Options = {"infoType":infoType, "id": str(id), "function": "26", "protocol": str(protocol), "frequency":"433920"}
        stype=0
    if infoType == "10" and MDType =="7":
        Options = {"infoType":infoType, "id": str(id), "function": "2", "protocol": str(protocol), "frequency":"868950", "area": str(area), "LevelActions": "|||||||||", "LevelNames": "Off|HG|Eco|Moderat|Medio|Comfort|Assoc", "LevelOffHidden": "False", "SelectorStyle": "0"}
        stype=18
    if infoType == "10" and MDType =="71":
        Options = {"infoType":infoType, "id": str(id), "function": "1", "protocol": str(protocol), "frequency":"868950", "area": str(area)}
        stype=0
    if infoType == "10" and MDType =="72":
        Options = {"infoType":infoType, "id": str(id), "function": "12", "protocol": str(protocol), "frequency":"868950"}
        stype=0
    if infoType == "10" and MDType =="73":
        Options = {"infoType":infoType, "id": str(id), "function": "26", "protocol": str(protocol), "frequency":"868950"}
        stype=0
    if infoType == "11" :
        Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "subType": "1", "LevelActions": "|||", "LevelNames": "Off|On|Stop", "LevelOffHidden": "False", "SelectorStyle": "0"}
        stype=18        
    IsCreated=False
    x=0
    nbrdevices=1
    Domoticz.Debug("Options to find or set : " + str(Options))
    filters = ('id', 'protocol', 'infoType', 'function')
    #########check if devices exist ####################
    for x in Devices:
        DOptions = Devices[x].Options
        if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
            IsCreated = True
            nbrdevices=x
            Domoticz.Log("Devices already exists. Unit=" + str(x))
            Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
    ########### create device if not found ###############
    if IsCreated == False :
        nbrdevices=FreeUnit()
        if infoType =="3" :
            Domoticz.Device(Name="RTS - " + MDiD,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
        elif infoType=="10" and Options['function']=="2" :
            Domoticz.Device(Name="X2DELEC Switch - id " + Options['id'],  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
        else :
            Domoticz.Device(Name="Manual Switch - " + MDiD, Unit=nbrdevices, Type=16, Switchtype=stype).Create()
        Devices[nbrdevices].Update(nValue =0,sValue = "0",Options = Options)
    Domoticz.Log("Plugin has " + str(len(Devices)) + " devices associated with it.")

def UpdateDevice(Unit, nValue, sValue, Image, SignalLevel, BatteryLevel):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (Devices[Unit].Image != Image) or (Devices[Unit].SignalLevel != SignalLevel) or (Devices[Unit].BatteryLevel != BatteryLevel) :
            Devices[Unit].Update(nValue, str(sValue),Image, SignalLevel, BatteryLevel)
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' SignalLevel:"+str(SignalLevel)+" batteryLevel:'"+str(BatteryLevel)+"%' ("+Devices[Unit].Name+")")
    return

def RFpConf(self):
    ###################Configure Rfplayer ~##################
    '''
    lineinput='ZIA++REPEATER - *'
    SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
    lineinput='ZIA++RECEIVER - * + CHACON OREGONV2 OREGONV3/OWL X2D'
    SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
    '''
    lineinput='ZIA++RECEIVER + *'
    self.SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
    #'''
    lineinput='ZIA++FORMAT JSON'
    self.SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
    if self.MacAdress != "" :
        lineinput='ZIA++SETMAC ' + self.MacAdress
        self.SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
    if self.JamAlert == "0" :
            lineinput='ZIA++JAMMING ' + "0"
            SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
            Domoticz.Debug("JAMALERT DISABLE")
    if self.JamAlert != "0" :
            lineinput='ZIA++JAMMING ' + Parameters["Mode3"]
            SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
            Domoticz.Debug("JAMALERT is Enable with level = " + Parameters["Mode3"])

def ReadConf(self,Data):
    Data=Data.replace("ZIA--", "")
    DecData = json.loads(Data)
    self.RfPmac = DecData['systemStatus']['info'][2]['v']
    Domoticz.Log('rfp1000 mac :' + str(RfPmac))
    return self.RfPmac

def AreaToX10Code(a):
    f = lambda x: chr(ord('A')+x//16)+str((x%16)+1)
    if type(a) is int:
        if int(a) >= 0 and int(a) < 256:
            return f(a)
        else:
            raise ValueError('invalid aera value %s' % (a))
    else:
        a = a.upper()
        if (a[0] in 'ABCDEFGHIJKLMNOP') and int(a[1:]) >= 1 and int(a[1:]) <= 16:
            return a
        else:
            if int(a) >= 0 and int(a) < 256:
                return f(int(a))
            else:
                raise ValueError('invalid aera value %s' % (a))

def SendtoRfplayer(Unit, Command, Level, Hue):
    Options=Devices[Unit].Options
    Domoticz.Debug("SendtoRfplayer - Options found in DB: " + str(Devices[Unit].Options) + " for devices unit " + str(Unit))
    infoType = Options['infoType']
    protocol=Options['protocol']
    if protocol =="1": protocol="X10"
    if protocol =="2": 
        frequency=Options['frequency']
        if frequency == "433920":
            protocol="VISONIC433"
        if frequency == "868950":
            protocol="VISONIC868"
    if protocol =="3": protocol="BLYSS"
    if protocol =="4": protocol="CHACON"
    if protocol =="6": protocol="DOMIA"
    if protocol =="8" and infoType == "10":
        frequency=Options['frequency']
        if frequency == "433920":
            protocol="X2D433"
        if frequency == "868950":
            protocol="X2D868"
    if protocol =="8" and infoType == "11":
        protocol="X2DSHUTTER"
    if protocol =="9": protocol="RTS"
    if protocol =="10": protocol="KD101"
    if protocol =="11": protocol="PARROT"

    if infoType == "0" and  protocol == "PARROT":
        id=Options['id']
        lineinput='ZIA++' + str(Command.upper()) + " " + protocol + " " + id
        SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
        if Command == "On":
            Devices[Unit].Update(nValue =1,sValue = "on")
        if Command == "Off":
            Devices[Unit].Update(nValue =0,sValue = "off")
            
    if infoType == "0" and protocol != "PARROT":
        id=Options['id']
        lineinput='ZIA++' + str(Command.upper()) + " " + protocol + " ID " + id
        SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
        if Command == "On":
            Devices[Unit].Update(nValue =1,sValue = "on")
        if Command == "Off":
            Devices[Unit].Update(nValue =0,sValue = "off")
            
    if infoType == "1" or infoType == "2":
        id=Options['id']
        lineinput='ZIA++' + str(Command.upper()) + " " + protocol + " ID " + id
        SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
        if Command == "On":
            Devices[Unit].Update(nValue =1,sValue = "on")
        if Command == "Off":
            Devices[Unit].Update(nValue =0,sValue = "off")
                #Devices[Unit].Update(nValue =0,sValue = "off")
        
    if infoType == "3" :
        id=Options['id']
        qualifier=Options['subType']
        if qualifier=="0":
        ###start MAj from Deennoo
            if Level == 0 :
                lineinput='ZIA++' + str("OFF " + protocol + " ID " + id )
            if Level == 10 :
                lineinput='ZIA++' + str("DIM %50 " + protocol + " ID " + id )
            if Level == 20 :
                lineinput='ZIA++' + str("ON " + protocol + " ID " + id )
            if Level == 30 :
                lineinput='ZIA++' + str("ASSOC " + protocol + " ID " + id )
        ###End MAj from Deennoo
        if qualifier=="1":
            if Level == 10 :
                lineinput='ZIA++' + str("ON " + protocol + " ID " + id + " QUALIFIER " + qualifier)
            if Level == 20 :
                lineinput='ZIA++' + str("OFF " + protocol + " ID " + id + " QUALIFIER " + qualifier)
            if Level == 30 :
                lineinput='ZIA++' + str("ASSOC " + protocol + " ID " + id + " QUALIFIER " + qualifier)
        SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
        Devices[Unit].Update(nValue =0,sValue = str(Level))
        
    if infoType == "10" :
        area = AreaToX10Code(Options['area'])
        if Level == 0 : # Off
            lineinput="ZIA++ OFF X2DELEC "+area + " %4"
        if Level == 10 : # HG
            lineinput="ZIA++ ON X2DELEC "+area + " %5"
        if Level == 20 : # Eco
            lineinput="ZIA++ ON X2DELEC "+area + " %0"
        if Level == 30 : # confort-2
            lineinput="ZIA++ ON X2DELEC "+area + " %1"
        if Level == 40 : # confort-1
            lineinput="ZIA++ ON X2DELEC "+area + " %2"
        if Level == 50 : # confort
            lineinput="ZIA++ ON X2DELEC " +area + " %3"
        if Level == 60 : # assoc
            lineinput="ZIA++ ASSOC X2DELEC "+area
        SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
        nvalue = 0 if Level == 0 else 1
        Devices[Unit].Update(nValue = nvalue, sValue = str(Level))

    if infoType == "11" :
        subType=Options['subType']
        if subType == "1" :
            id=Options['id']
            if Level == 10 :
                lineinput='ZIA++' + str("ON " + protocol + " ID " + id )#+ " QUALIFIER " + qualifier)
            if Level == 20 :
                lineinput='ZIA++' + str("OFF " + protocol + " ID " + id ) #+ " QUALIFIER " + qualifier)
            if Level == 30 :
                lineinput='ZIA++' + str("ASSOC " + protocol + " ID " + id ) #+ " QUALIFIER " + qualifier)
            SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
            Devices[Unit].Update(nValue =0, sValue = str(Level))
                
    Domoticz.Debug("SendtoRfplayer - command : " + lineinput)

def FreeUnit() :
    FreeUnit=""
    for x in range(1,256):
        Domoticz.Debug("FreeUnit - does device " + str(x) + " exist ?")
        if x not in Devices :
            Domoticz.Debug("FreeUnit - device " + str(x) + "doesn't exist")
            FreeUnit=x
            return FreeUnit
    if FreeUnit =="" :
        FreeUnit=len(Devices)+1
    Domoticz.Debug("FreeUnit - Free Device Unit find : " + str(x))
    return FreeUnit

def ReadData(self, ReqRcv):
    ##############################################################################################################
    # decoding data from RfPlayer 
    ##############################################################################################################
    Domoticz.Debug("ReadData - " + ReqRcv)
    ReqRcv=ReqRcv.replace("ZIA33", "")
    try:
        DecData = json.loads(ReqRcv)
        infoType = DecData['frame']['header']['infoType']
        Domoticz.Debug("infoType : " + infoType)
        ##############################################################################################################
        #####################################Frame infoType 0                    ON/OFF
        ##############################################################################################################
        if infoType == "0":
            DecodeInfoType0(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 1                    ON/OFF   error in API receive id instead of id_lsb and id_msb
        ##############################################################################################################
        if infoType == "1":
            DecodeInfoType1(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 2                    Visonic###############################
        #############http://www.el-sys.com.ua/wp-content/uploads/MCR-300_UART_DE3140U0.pdf ###########################
        ###########http://cpansearch.perl.org/src/BEANZ/Device-RFXCOM-1.142010/lib/Device/RFXCOM/Decoder/Visonic.pm ##
        #############https://forum.arduino.cc/index.php?topic=289554.0 ###############################################
        ##############################################################################################################
        if infoType == "2":
            DecodeInfoType2(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 3                RTS     ##################################
        ##############################################################################################################
        if infoType == "3":
            DecodeInfoType3(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 4        Oregon thermo/hygro sensors  #####################
        #############http://www.connectingstuff.net/blog/encodage-protocoles-oregon-scientific-sur-arduino/###########
        ##############################################################################################################
        if infoType == "4":
            DecodeInfoType4(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 5        Oregon thermo/hygro/pressure sensors  ############
        ##############################################################################################################
        if infoType == "5":
            DecodeInfoType5(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 6        Oregon Wind sensors  #############################
        #############http://www.connectingstuff.net/blog/encodage-protocoles-oregon-scientific-sur-arduino/###########
        ##############################################################################################################
        if infoType == "6":
            DecodeInfoType6(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 7        Oregon UV sensors  ############
        ##############################################################################################################
        if infoType == "7":
            DecodeInfoType7(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 8        OWL Energy/power sensors  ############
        ##############################################################################################################
        if infoType == "8":
            DecodeInfoType8(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 9        Oregon Rain sensors  ############
        ##############################################################################################################
        if infoType == "9":
            DecodeInfoType9(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 10        Thermostats  X2D protocol ########################
        ##############################################################################################################
        if infoType == "10":
            DecodeInfoType10(self, DecData, infoType)
        ##############################################################################################################
        #####################################Frame infoType 11         Alarm X2D protocol / Shutter ####################
        ##############################################################################################################
        if infoType == "11":
            DecodeInfoType11(self, DecData, infoType)
    except:
        Domoticz.Log("Error while reading JSON Infotype")
        Domoticz.Debug("Debug : Error Decoding/Reading  " + ReqRcv)
        if Parameters["Mode6"] == "Debug":
            with open(Parameters["HomeFolder"]+"Debug.txt", "at") as text_file:
                print(ReqRcv, file=text_file)
        ReqRcv=""
        return

def writetofile(ReqRcv):
    with open(Parameters["HomeFolder"]+"Response.txt", "at") as text_file:
        print(ReqRcv, file=text_file)
    return

