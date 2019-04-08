#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType9.py

    Description: Rfplayer decode infotype 9
"""

def DecodeInfoType9(self, DecData, infoType):
    try :
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        protocol = DecData['frame']['header']['protocol']
        id_PHY = DecData['frame']['infos']['id_PHY']
        adr_channel = DecData['frame']['infos']['adr_channel']
        qualifier = DecData['frame']['infos']['qualifier']
        try:
            lowBatt = DecData['frame']['infos']['lowBatt']
        except IndexError:
            lowbatt="0"
        try:
            TotalRain = DecData['frame']['infos']['measures'][0]['value']
        except IndexError:
            TotalRain = "0"
        try :
            CurrentRain = DecData['frame']['infos']['measures'][1]['value']
        except IndexError:
            CurrentRain = "0"
        Domoticz.Debug("id : " + id_PHY + " adr_channel : " + adr_channel)
        
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Temp" : "1"}
        Domoticz.Debug("Options to find or set : " + str(Options))
        filters = ('id', 'protocol', 'infoType', 'function')
        for x in Devices:
            #JJE - start
            DOptions = Devices[x].Options
            if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
                #JJE - end
                IsCreated = True
                nbrdevices=x
                Domoticz.Log("Devices already exists. Unit=" + str(x))
                Domoticz.Debug("Options found in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
        if IsCreated == False and self.LearningMode == "True":
            nbrdevices=FreeUnit()
            Domoticz.Device(Name="Rain - " + adr_channel, Unit=nbrdevices, Type=85, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = 0,sValue = str(CurrentRain) + ";" + str(TotalRain),Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 0,sValue = str(CurrentRain) + ";" + str(TotalRain))
    except Exception as e:
        Domoticz.Log("Error while decoding Infotype9 frame " + repr(e))
        return