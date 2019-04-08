#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType11.py

    Description: Rfplayer decode infotype 11
"""

def DecodeInfoType11(self, DecData, infoType):
    try :
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        protocol = DecData['frame']['header']['protocol']
        SubType = DecData['frame']['infos']['subType']
        frequency=DecData['frame']['header']['frequency']
        filters = ('id', 'protocol', 'infoType', 'function')
        ##############################################################################################################
        if SubType == "0" : # Detector/sensor
            id = DecData['frame']['infos']['id']
            qualifier = DecData['frame']['infos']['qualifier']
            if qualifier=="0":
                status=0
            if qualifier=="2":
                status=10
            if qualifier=="1":
                status=20
            if qualifier == "10":
                status=0
            Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "frequency": str(frequency), "subType": str(SubType), "LevelActions": "||||", "LevelNames": "Off|Tamper|Alarm|Tamper+Alarm", "LevelOffHidden": "False", "SelectorStyle": "0"}
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
            if IsCreated == False and self.LearningMode == "True":
                nbrdevices=FreeUnit()
                #Options = {"LevelActions": "||||", "LevelNames": "Off|Alarm|Tamper", "LevelOffHidden": "False", "SelectorStyle": "0"}
                Domoticz.Device(Name=protocol + " - " + id,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
                Devices[nbrdevices].Update(nValue =0,sValue = str(status), Options = Options)
            elif IsCreated == True :
                Devices[nbrdevices].Update(nValue =0,sValue = str(status))
        ##############################################################################################################
        elif SubType == "1":  # remote
            id = DecData['frame']['infos']['id']
            qualifier = DecData['frame']['infos']['qualifier']
            if qualifier=="1" :
                status=10
            if qualifier=="2" :
                status=0
            if qualifier=="3" :
                status=20
            Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "frequency": str(frequency), "subType": str(SubType), "LevelActions": "|||", "LevelNames": "Off|On|Stop", "LevelOffHidden": "False", "SelectorStyle": "0"}
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
            if IsCreated == False and self.LearningMode == "True":
                nbrdevices=FreeUnit()
                Domoticz.Device(Name=protocol + " - " + id,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
                Devices[nbrdevices].Update(nValue =0,sValue = str(status), Options = Options)
            elif IsCreated == True :
                Devices[nbrdevices].Update(nValue =0,sValue = str(status))
    except Exception as e:
        Domoticz.Log("Error while decoding Infotype11 frame " + repr(e))
        return

