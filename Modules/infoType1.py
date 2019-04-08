#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType1.py

    Description: Rfplayer decode infotype 1
"""

def DecodeInfoType1(self, DecData, infoType):
    try :
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        protocol = DecData['frame']['header']['protocol']
        SubType = DecData['frame']['infos']['subType']
        id = DecData['frame']['infos']['id']
        Domoticz.Debug("id : " + id)
        #########################################################################################
        ######################### calcul id_lsb and id_msb from id ##############################
        #########################################################################################
        idb= bin(int(id))[2:]
        Domoticz.Debug("id binary : " + str(idb))
        Unit=idb[-6:]
        idd=idb[:-6]
        Domoticz.Debug("Unit b: " + str(Unit))
        Domoticz.Debug("id decode b: " + str(idd))
        Domoticz.Debug("Unit i: " + str(int(Unit,2)+1))
        Domoticz.Debug("id decode i: " + str(int(idd,2)))
        Domoticz.Debug("id decode h: " + str(hex(int(idd,2)))[2:])
        #########################################################################################
        #########################################################################################
        Options = {"infoType":infoType, "id": str(id), "id_lsb": str(hex(int(idd,2)))[2:], "id_msb": str(int(Unit,2)+1), "protocol": str(protocol)}
        Domoticz.Debug("Options to find or set : " + str(Options))
        filters = ('id', 'protocol', 'infoType', 'function')
        for x in Devices:
            #JJE - start
            DOptions = Devices[x].Options
            Domoticz.Debug("DOptions : " + str(DOptions))
            if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
                #JJE - end
                IsCreated = True
                nbrdevices=x
                Domoticz.Log("Devices already exists. Unit=" + str(x))
                Domoticz.Debug("Options found in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
                #No need to walk on the other devices
        if IsCreated == False and self.LearningMode == "True" :
            nbrdevices=FreeUnit()
            Domoticz.Device(Name=protocol + " - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue =int(SubType),sValue = str(SubType),Options = Options)
        elif IsCreated == True :
            Domoticz.Debug("update devices : " + str(x))
            Devices[nbrdevices].Update(nValue =int(SubType),sValue = str(SubType))
    except Exception as e:
        Domoticz.Log("Error while decoding Infotype1 frame " + repr(e))
        return