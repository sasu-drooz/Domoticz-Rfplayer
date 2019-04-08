#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType7.py

    Description: Rfplayer decode infotype 7
"""

def DecodeInfoType7(self, DecData, infoType):
    try :
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        protocol = DecData['frame']['header']['protocol']
        id_PHY = DecData['frame']['infos']['id_PHY']
        adr_channel = DecData['frame']['infos']['adr_channel']
        qualifier = DecData['frame']['infos']['qualifier']
        UV = DecData['frame']['infos']['measures'][0]['value']
        try:
            lowBatt = DecData['frame']['infos']['lowBatt']
        except IndexError:
            lowbatt="0"
        Domoticz.Debug("id : " + id_PHY + " adr_channel : " + adr_channel)
        
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "UV" : "1"}
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
            Domoticz.Device(Name="UV - " + adr_channel, Unit=nbrdevices, TypeName="UV").Create()
            Devices[nbrdevices].Update(nValue = 0,sValue = str(int(UV)/10) + ';0',Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 0,sValue = str(int(UV)/10) + ';0')
    except:
        Domoticz.Log("Error while decoding Infotype7 frame")
        return