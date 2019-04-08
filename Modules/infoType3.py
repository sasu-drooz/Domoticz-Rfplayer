#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType3.py

    Description: Rfplayer decode infotype 3
"""

def DecodeInfoType3(self, DecData, infoType):
    try :
        Domoticz.Debug("Decoding infotype RTS frame")
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        protocol = DecData['frame']['header']['protocol']
        SubType = DecData['frame']['infos']['subType']
        id = DecData['frame']['infos']['id']
        Domoticz.Debug("id : " + id)
        qualifier = DecData['frame']['infos']['qualifier']
        Domoticz.Debug("protocol : " + str(protocol) + " - SubType : " + str(SubType) +" - id : " + str(id) + " - Qualifier : " + str(qualifier))
        filters = ('id', 'protocol', 'infoType', 'function')
#        if len(str(id))== 8 :
#            Domoticz.Debug("len id = 8")
#            idb= bin(int(id))[2:]
#            id= int(idb[1:],2)
        if SubType == "0" :
            Domoticz.Debug("subtype = 0")
            if qualifier == "1" :
                Domoticz.Debug("qualifier == 1")
                level = 0
            elif qualifier == "4" :
                Domoticz.Debug("qualifier == 4")
                level = 10
            elif qualifier == "7" :
                Domoticz.Debug("qualifier == 7")
                level = 20
            elif qualifier == "13" :
                Domoticz.Debug("qualifier == 13")
                level = 30 
            else :
                Domoticz.Log("Unknow qualifier - please send log to dev team")
            #################################################################################################################
            Domoticz.Debug("id : " + str(id))
            Options = {"infoType": infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType), "LevelActions": "|||||", "LevelNames": "Off/Down|My|On/Up|Assoc", "LevelOffHidden": "False", "SelectorStyle": "0"}
            Domoticz.Debug("Options to find or set : " + str(Options))
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
            if IsCreated == False and self.LearningMode == "True":
                Domoticz.Debug("Create devices : " + str(x))
                nbrdevices=FreeUnit()
                #Options = {"LevelActions": "|||||", "LevelNames": "Off/Down|My|On/Up|Assoc", "LevelOffHidden": "False", "SelectorStyle": "0"}
                Domoticz.Device(Name=" RTS - " + str(id),  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
                Devices[nbrdevices].Update(nValue = 1,sValue = str(level),Options = Options)
            elif IsCreated == True :
                Domoticz.Debug("isCreated = True")
                Devices[nbrdevices].Update(nValue = 1,sValue = str(level))
                #Devices[nbrdevices].Update(nValue = 1,sValue = "0")
            ###############################################################################################################
        elif SubType == "1" :
            if qualifier == "5" :
                level = 10
            elif qualifier == "6" :
                level = 20
            else :
                Domoticz.Log("Unknow qualifier - please send log to dev team")
            Domoticz.Debug("id : " + str(id))
            #####################################################################################################################
            Options = {"infoType": infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType), "LevelActions": "||||", "LevelNames": "Off|Left button|Right button", "LevelOffHidden": "False", "SelectorStyle": "0"}
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
                #Options = {"LevelActions": "||||", "LevelNames": "Off|Left button|Right button", "LevelOffHidden": "False", "SelectorStyle": "0"}
                Domoticz.Device(Name=" RTS - " + str(id),  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
                Devices[nbrdevices].Update(nValue = 0,sValue = "0",Options = Options)
            elif IsCreated == True :
                Devices[nbrdevices].Update(nValue = 0,sValue = str(level))
                #Devices[nbrdevices].Update(nValue = 1,sValue = "0")
        else :
            Domoticz.Log("Unknow SubType - please send log to dev team")
    except Exception as e:
        Domoticz.Log("Error while decoding Infotype3 frame " + repr(e))
        return