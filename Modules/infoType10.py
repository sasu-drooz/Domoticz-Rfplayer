#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType10.py

    Description: Rfplayer decode infotype 10
"""

def DecodeInfoType10(self, DecData, infoType):
    try :
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        protocol = DecData['frame']['header']['protocol']
        frequency = DecData['frame']['header']['frequency']
        SubType = DecData['frame']['infos']['subType']
        id = DecData['frame']['infos']['id']
        area = DecData['frame']['infos']['area']
        function = DecData['frame']['infos']['function']
        state = DecData['frame']['infos']['state']
        
        #########################################################################################
        ######################### calcul id_lsb and id_msb from id ##############################
        #########################################################################################
        idb= bin(int(id))[2:]
        Domoticz.Debug("id binary : " + str(idb))
        Unit=idb[-6:]
        idd=idb[:-6]
        Domoticz.Debug("area b: " + str(Unit))
        Domoticz.Debug("id decode b: " + str(idd))
        Domoticz.Debug("area i: " + str(int(Unit,2)+1))
        Domoticz.Debug("id decode i: " + str(int(idd,2)))
        Domoticz.Debug("id decode h: " + str(hex(int(idd,2)))[2:])
        #########################################################################################
        #########################################################################################
        
        if function == "2" :
            if state == "0": #ECO 
                status = 20
            if state == "1": #MODERAT 
                status = 30
            if state == "2": #MEDIO
                status = 40
            if state == "3": #COMFORT 
                status = 50
            if state == "4": #STOP 
                status = 0
            if state == "5": #OUT OF FROST 
                status = 10
            if state == "6": #SPECIAL 
                status = 60
            if state == "7": #AUTO 
                status = 70
            if state == "8": #CENTRALISED
                status = 80
            Options = {"infoType":infoType, "id": str(id), "area": str(area), "function": str(function), "protocol": str(protocol), "subType": str(SubType), "frequency": str(frequency), "LevelActions": "|||||||||", "LevelNames": "Off|HG|Eco|Moderat|Medio|Comfort|Assoc", "LevelOffHidden": "False", "SelectorStyle": "0"}
            Domoticz.Debug("Options to find or set : " + str(Options))
            filters = ('id', 'protocol', 'infoType', 'function')
            for x in Devices:
                DOptions = Devices[x].Options
                Domoticz.Debug("scanning devices: " + repr(x) + repr(DOptions))
                if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
                    IsCreated = True
                    nbrdevices=x
                    Domoticz.Log("Devices already exists. Unit=" + str(x))
                    Domoticz.Debug("Options found in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
                    break
            if IsCreated == False and self.LearningMode == "True":
                nbrdevices=FreeUnit()
                Domoticz.Device(Name=protocol + " - " + id,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
                Devices[nbrdevices].Update(nValue =0, sValue = str(status), Options = Options)
            elif IsCreated == True :
                svalue = str(status)
                nvalue = 0 if state == '4' else 1
                if Devices[nbrdevices].sValue != svalue:
                    Devices[nbrdevices].Update(nValue = nvalue,sValue = svalue)
    ##############################################################################################################
        else :
            Options = {"infoType":infoType, "id": str(id), "area": str(area), "function": str(function), "protocol": str(protocol), "subType": str(SubType), "frequency": str(frequency)}
            Domoticz.Debug("Options to find or set : " + str(Options))
            filters = ('id', 'protocol', 'infoType', 'function')
            for x in Devices:
                DOptions = Devices[x].Options
                Domoticz.Debug("scanning devices: " + repr(x) + repr(DOptions))
                if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
                    IsCreated = True
                    nbrdevices=x
                    Domoticz.Log("Devices already exists. Unit=" + str(x))
                    Domoticz.Debug("Options found in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
                    break
            if IsCreated == False and self.LearningMode == "True":
                nbrdevices=FreeUnit()
                Domoticz.Device(Name=protocol + " - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
                Devices[nbrdevices].Update(nValue =0,sValue = str(state), Options = Options)
            elif IsCreated == True :
                svalue = 'Off' if state == 0 else 'On'
                nvalue = 0 if state == '0' else 1
                if Devices[nbrdevices].sValue != svalue:
                    Devices[nbrdevices].Update(nValue = nvalue, sValue = svalue)
    except Exception as e:
        Domoticz.Log("Error while decoding Infotype10 frame: " + repr(e))
        return