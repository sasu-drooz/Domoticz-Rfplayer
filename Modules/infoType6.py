#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673 
#
"""
    Module : infoType6.py

    Description: Rfplayer decode infotype 6
"""

def DecodeInfoType6(self, DecData, infoType):
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
            speed = DecData['frame']['infos']['measures'][0]['value']
        except IndexError:
            speed = "0"
        try:
            direction = DecData['frame']['infos']['measures'][1]['value']
        except IndexError:
            direction = "0"
        if 22 <= int(direction) << 68 : 
            sens = 'NE'
        if 68 <= int(direction) << 112 : 
            sens = 'E'
        if 112 <= int(direction) << 157 : 
            sens = 'SE'
        if 157 <= int(direction) <= 202 : 
            sens = 'S'
        if 202 <= int(direction) <= 247 : 
            sens = 'SO'
        if 247 <= int(direction) <= 292 : 
            sens = 'O'
        if 292 <= int(direction) <= 337 : 
            sens = 'NO'
        if 337 <= int(direction) or int(direction) <= 22 : 
            sens = 'N'
        
        Wind = direction + ';' + sens + ';' + speed + ';0;0;0' #form need : 0;N;0;0;0;0

        Domoticz.Debug("id : " + id_PHY + " adr_channel : " + adr_channel)
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Wind" : "1"}
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
        if IsCreated == False and self.LearningMode == "True" :
            nbrdevices=FreeUnit()
            Domoticz.Device(Name="Wind - " + adr_channel, Unit=nbrdevices, Type=86, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = 0,sValue = str(Wind),Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 0,sValue = str(Wind))
    except Exception as e:
        Domoticz.Log("Error while decoding Infotype6 frame " + repr(e))
        return