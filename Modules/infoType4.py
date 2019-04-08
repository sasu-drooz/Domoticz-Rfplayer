#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType4.py

    Description: Rfplayer decode infotype 4
"""



def DecodeInfoType4(self, DecData, infoType):
    global InfoType4SubTypes

    InfoType4SubTypes = {}
     #                             T/H T  H
    InfoType4SubTypes['0x1A2D'] = (1, 1, 1) # THGR122/228/238/268, THGN122/123/132 Thermo+hygro V2
    InfoType4SubTypes['0xCA2C'] = (4, 1, 1) # THGR328 Thermo+hygro V2
    InfoType4SubTypes['0x0ACC'] = (3, 1, 1) # RTGR328 Thermo+hygro V2
    InfoType4SubTypes['0xEA4C'] = (1, 2, 1) # THC238/268, THWR288,THRN122,THN122/132,AW129/131 thermometer V2
    InfoType4SubTypes['0x1A3D'] = (6, 1, 1) # THGR918/928, THGRN228, THGN50 Thermo+hygro V2
    InfoType4SubTypes['0x5A6D'] = (1, 1, 1) # THGR918N Temp+Pressure V2
    InfoType4SubTypes['0xCA48'] = (1, 3, 1) # THWR800 S. pool thermo V3
    InfoType4SubTypes['0xFA28'] = (2, 1, 1) # THGR810, THGN800 Thermo+hygro V3 

    try :
        protocol = DecData['frame']['header']['protocol']
        id_PHY = DecData['frame']['infos']['id_PHY']
        adr_channel = DecData['frame']['infos']['adr_channel']
        channel = DecData['frame']['infos']['channel']
        qualifier = DecData['frame']['infos']['qualifier']
        filters = ('id', 'adr_channel', 'protocol', 'infoType', 'sensorType')
        
        try:
            lowBatt = DecData['frame']['infos']['lowBatt']
        except IndexError:
            lowbatt="0"
        try:
            temp = DecData['frame']['infos']['measures'][0]['value']
        except IndexError:
            temp = "0"
        try :
            hygro = DecData['frame']['infos']['measures'][1]['value']
        except IndexError:
            hygro = "0"
        battery_level = 100 if DecData['frame']['infos']['lowBatt'] == "0" else 0
        signal_level = int(DecData['frame']['header']['rfQuality'])
        temphygro = temp + ';' + hygro + ';1'
        Domoticz.Debug("id : " + id_PHY + " adr_channel : " + adr_channel)
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        sensorType = 80
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Temp" : "1", "sensorType" : str(sensorType) }
        Domoticz.Debug("Options to find or set : " + str(Options))
        for x in Devices:
            #JJE - start
            DOptions = Devices[x].Options
            if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
                #JJE - end
                IsCreated = True
                nbrdevices=x
                Domoticz.Log("Devices already exists. Unit=" + str(x))
                Domoticz.Debug("Options found in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
                #No need to walk on the other devices
        subType = 0
        if id_PHY in InfoType4SubTypes:
            subType = InfoType4SubTypes[id_PHY][1]
        if IsCreated == False and self.LearningMode == "True":
            nbrdevices=FreeUnit()
            Domoticz.Device(Name="Temp - " + adr_channel + ' (channel ' + channel + ')', Unit=nbrdevices, Type=80, Subtype=subType, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = 1,sValue = str(temp), SignalLevel=signal_level , BatteryLevel=battery_level, Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 1,sValue = str(temp), SignalLevel=signal_level , BatteryLevel=battery_level)
        #####################################################################################################################
        IsCreated=False
        x=0
        nbrdevices=0
        sensorType = 81
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Hygro" : "1", "sensorType" : str(sensorType) }
        Domoticz.Debug("Options to find or set : " + str(Options))
        for x in Devices:
            #JJE - start
            DOptions = Devices[x].Options
            if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
                #JJE - end
                IsCreated = True
                nbrdevices=x
                Domoticz.Log("Devices already exists. Unit=" + str(x))
                Domoticz.Debug("Options found in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
                #No need to walk on the other devices
        subType = 0
        if id_PHY in InfoType4SubTypes:
            subType = InfoType4SubTypes[id_PHY][2]
        if IsCreated == False and self.LearningMode == "True":
            nbrdevices=FreeUnit()
            Domoticz.Device(Name="Hygro - " + adr_channel + ' (channel ' + channel + ')', Unit=nbrdevices, Type=81, Subtype=subType, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = int(hygro),sValue = "1", SignalLevel=signal_level , BatteryLevel=battery_level, Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = int(hygro),sValue = "1", SignalLevel=signal_level , BatteryLevel=battery_level)
        #####################################################################################################################    
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        sensorType = 82
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "TempHygro" : "1", "sensorType" : str(sensorType) }
        Domoticz.Debug("Options to find or set : " + str(Options))
        for x in Devices:
            #JJE - start
            DOptions = Devices[x].Options
            if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
                #JJE - end
                    IsCreated = True
                    nbrdevices=x
                    Domoticz.Log("Devices already exists. Unit=" + str(x))
                    Domoticz.Debug("Options found in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
                    # No need to walk on the other devices
        subType = 0
        if id_PHY in InfoType4SubTypes:
            subType = InfoType4SubTypes[id_PHY][0]
        if IsCreated == False and self.LearningMode == "True":
            nbrdevices=FreeUnit()
            Domoticz.Device(Name="Temp/Hygro - " + adr_channel + ' (channel ' + channel + ')', Unit=nbrdevices, Type=82, Subtype=subType, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = 1,sValue = str(temphygro), SignalLevel=signal_level , BatteryLevel=battery_level, Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 1,sValue = str(temphygro), SignalLevel=signal_level , BatteryLevel=battery_level)
    except Exception as e:
        Domoticz.Log("Error while decoding Infotype4 frame " + repr(e))
        return