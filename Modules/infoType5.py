#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#
"""
    Module : infoType5.py

    Description: Rfplayer decode infotype 5
"""

def DecodeInfoType5(self, DecData, infoType):
    try :
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        protocol = DecData['frame']['header']['protocol']
        id_PHY = DecData['frame']['infos']['id_PHY']
        adr_channel = DecData['frame']['infos']['adr_channel']
        qualifier = DecData['frame']['infos']['qualifier']
        filters = ('id', 'protocol', 'infoType', 'function')
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
        try :
            pressure = DecData['frame']['infos']['measures'][2]['value']
        except IndexError:
            pressure = "0"
        temphygro = temp + ';' + hygro + ';1'
        temphygropress = temphygro + ';' + pressure + ';1'

        Domoticz.Debug("id : " + id_PHY + " adr_channel : " + adr_channel)
        
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Temp" : "1"}
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
            Domoticz.Device(Name="Temp - " + adr_channel, Unit=nbrdevices, Type=80, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = 0,sValue = str(temp),Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 0,sValue = str(temp))
        #####################################################################################################################
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Hygro" : "1"}
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
            Domoticz.Device(Name="Hygro - " + adr_channel, Unit=nbrdevices, Type=81, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = int(hygro),sValue = "1",Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = int(hygro),sValue = "1")
        #####################################################################################################################
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Pressure" : "1"}
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
            Domoticz.Device(Name="Pressure - " + adr_channel, Unit=nbrdevices, Type=243, Subtype=26, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = 0,sValue = str(pressure),Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 0,sValue = str(pressure)+";0")
        #####################################################################################################################    
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "TempHygro" : "1"}
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
            Domoticz.Device(Name="Temp/Hygro - " + adr_channel, Unit=nbrdevices, Type=82, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = 0,sValue = str(temphygro),Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 0,sValue = str(temphygro))
        #####################################################################################################################    
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "TempHygropressure" : "1"}
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
            Domoticz.Device(Name="Temp/Hygro - " + adr_channel, Unit=nbrdevices, Type=84, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = 0,sValue = str(temphygropress),Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 0,sValue = str(temphygropress))
    except  Exception as e:
        Domoticz.Log("Error while decoding Infotype5 frame " + repr(e))
        return