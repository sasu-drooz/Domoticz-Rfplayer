#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType2.py

    Description: Rfplayer decode infotype 2
"""

def DecodeInfoType2(self, DecData, infoType):
    #try :
    IsCreated=False
    x=0
    nbrdevices=0
    protocol = DecData['frame']['header']['protocol']
    frequency = DecData['frame']['header']['frequency']
    SubType = DecData['frame']['infos']['subType']
    Domoticz.Debug("Protocol : " + str(protocol))
    filters = ('id', 'protocol', 'infoType', 'function')
    if protocol == "2":
        id= DecData['frame']['infos']['id']
        qualifier = DecData['frame']['infos']['qualifier']
        Domoticz.Debug("id : " + str(id) + " qualifier :" + str(qualifier))
    if protocol == "3" :
        id = DecData['frame']['infos']['id']
        Domoticz.Debug("id : " + str(id) + " subType :" + str(SubType))
    ##############################################################################################################
    if SubType == "0" and protocol == "2": # Detector/sensor visonic
        #Qualifier Meaning for MCT-320
        #"qualifier": "6", "qualifierMeaning": { "flags": ["Alarm","LowBatt"]}}}}
        #"qualifier": "4", "qualifierMeaning": { "flags": ["LowBatt"]}}}}
        #"qualifier": "2", "qualifierMeaning": { "flags": ["Alarm"]}}}}
        #"qualifier": "0", "qualifierMeaning": { "flags": []}}}}
        #"qualifier": "8", "qualifierMeaning": { "flags": ["Supervisor/Alive"]}}}}
        #"qualifier": "12", "qualifierMeaning": { "flags": ["LowBatt","Supervisor/Alive"]}}}}
        if qualifier =="8" or qualifier=="4" or qualifier=="12" or qualifier=="0":#Close
            status=0
        if qualifier == "1" :
            status=10
        if qualifier =="7" or qualifier=="2" or qualifier=="6":#Open
            status=20
        if qualifier == "3" :
            status=30
        Battery=99            #Default Value
        if qualifier == "4" or qualifier =="6" or qualifier =="12":
            Battery=10    
        Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType), "LevelActions": "||||", "LevelNames": "Off|Tamper|Alarm|Tamper+Alarm", "LevelOffHidden": "False", "SelectorStyle": "0"}
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
        if IsCreated == False and self.LearningMode == "True":
            nbrdevices=FreeUnit()
            #Options = {"LevelActions": "||||", "LevelNames": "Off|Tamper|Alarm|Tamper+Alarm", "LevelOffHidden": "False", "SelectorStyle": "0"}
            Domoticz.Device(Name=protocol + " - " + id,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
            Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery, Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery)
    ##############################################################################################################
    ##############################################################################################################
    if SubType == "0" and protocol == "3" : # blyss 
        Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType) }
        Domoticz.Debug("Options to find or set : " + str(Options))
        for x in Devices:
            #JJE - start
            if {k: DOptions.get(k, None) for k in filters} == {k: Options.get(k, None) for k in filters}:
                #JJE - end
                IsCreated = True
                nbrdevices=x
                Domoticz.Log("Devices already exists. Unit=" + str(x))
                Domoticz.Debug("Options found in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
                #No need to walk on the other devices
        if IsCreated == False and self.LearningMode == "True":
            nbrdevices=FreeUnit()
            Domoticz.Device(Name=protocol + " - " + id,  Unit=nbrdevices, Type=16, Switchtype=0, Options=Options).Create()
            Devices[nbrdevices].Update(nValue =0, sValue = "on", Options = Options)
        elif IsCreated == True :
            svalue = Devices[nbrdevices].nValue
            if svalue =="on": svalue="off"
            if svalue =="off": svalue="on"
            Devices[nbrdevices].Update(nValue =0, sValue = str(svalue))
    ##############################################################################################################
    elif SubType == "1":  # remote
        Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType), "frequency": str(frequency)}
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
        if IsCreated == False and self.LearningMode == "True":
            nbrdevices=FreeUnit()
            Domoticz.Device(Name="Button 1 - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue =0,sValue = "0", BatteryLevel = Battery, Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue =0,sValue = "0", BatteryLevel = Battery)
#    except:
#        Domoticz.Log("Error while decoding Infotype2 frame")
#        return