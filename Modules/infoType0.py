#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType0.py

    Description: Rfplayer decode infotype 0
"""

def DecodeInfoType0(self, DecData, infoType):
    try :
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        protocol = DecData['frame']['header']['protocol']
        SubType = DecData['frame']['infos']['subType']
        id = DecData['frame']['infos']['id']
        Domoticz.Debug("id : " + str(id))
        
        Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol)}
        Domoticz.Debug("Options to find or set : " + str(Options))
        filters = ('id', 'protocol', 'infoType', 'function')
        #########check if devices exist ####################
        for x in Devices:
            #JJE - start
            DOptions = Devices[x].Options
    #                if Devices[x].Options == Options :
            if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
                #JJE - end
                IsCreated = True
                nbrdevices=x
                Domoticz.Log("Device already exists. Unit=" + str(x))
                Domoticz.Debug("Options found in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
        ########### create device if not find ###############
        if IsCreated == False and self.LearningMode == "True" :
            nbrdevices=FreeUnit()
            Domoticz.Device(Name=protocol + " - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue =int(SubType),sValue = str(SubType),Options = Options)
        elif IsCreated == True :
        ############ update device if found###################
            Devices[nbrdevices].Update(nValue =int(SubType),sValue = str(SubType))
    except Exception as e:
        Domoticz.Log("Error while decoding Infotype0 frame " + repr(e))
        return