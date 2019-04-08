#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: zaraki673
#

"""
    Module : infoType8.py

    Description: Rfplayer decode infotype 8
"""

def DecodeInfoType8(self, DecData, infoType):
    try :
        IsCreated=False
        x=0
        # New device will start at 1 or at last + 1
        nbrdevices=0
        protocol = DecData['frame']['header']['protocol']
        id_PHY = DecData['frame']['infos']['id_PHY']
        adr_channel = DecData['frame']['infos']['adr_channel']
        qualifier = DecData['frame']['infos']['qualifier']
        
        Energy = DecData['frame']['infos']['measures'][0]['value']   #♣ watt/hour
        Power = DecData['frame']['infos']['measures'][1]['value']  #♣ total watt with u=230v
        try:
            P1 = DecData['frame']['infos']['measures'][2]['value']   #♣ watt with u=230v
            P2 = DecData['frame']['infos']['measures'][3]['value']   #♣ watt with u=230v
            P3 = DecData['frame']['infos']['measures'][4]['value']   #♣ watt with u=230v
        except:
            P1 = ""
            P2 = ""
            P3 = ""
        Domoticz.Debug("id : " + id_PHY + " adr_channel : " + adr_channel)
        ##################################################################################################################################
        Options = {"infoType":infoType, "id": str(id_PHY), "id": str(adr_channel), "protocol": str(protocol), "Power&Energie" : "1"}
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
            Domoticz.Device(Name="Power & Energie - " + adr_channel, Unit=nbrdevices, Type=243, Subtype =29, Switchtype=0).Create()
            Devices[nbrdevices].Update(nValue = 0,sValue = str(Power + ';' + Energy),Options = Options)
        elif IsCreated == True :
            Devices[nbrdevices].Update(nValue = 0,sValue = str(Power + ';' + Energy))        
        ##################################################################################################################################
        if P1 != "" : 
            IsCreated=False
            x=0
            # New device will start at 1 or at last + 1
            nbrdevices=0
            Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "P1" : "1"}
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
                Domoticz.Device(Name="P1 - " + adr_channel, Unit=nbrdevices, Type=248, Switchtype=0).Create()
                Devices[nbrdevices].Update(nValue = 0,sValue = str(P1),Options = Options)
            elif IsCreated == True :
                Devices[nbrdevices].Update(nValue = 0,sValue = str(P1))
        ##################################################################################################################################
        if P2 != "" :
            IsCreated=False
            x=0
            # New device will start at 1 or at last + 1
            nbrdevices=0
            Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "P2" : "1"}
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
                Domoticz.Device(Name="P2 - " + adr_channel, Unit=nbrdevices, Type=248, Switchtype=0).Create()
                Devices[nbrdevices].Update(nValue = 0,sValue = str(P2),Options = Options)
            elif IsCreated == True :
                Devices[nbrdevices].Update(nValue = 0,sValue = str(P2))    
        ##################################################################################################################################
        if P3 != "" :
            IsCreated=False
            x=0
            # New device will start at 1 or at last + 1
            nbrdevices=0
            Options = {"infoType":infoType, "id": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "P3" : "1"}
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
                    Domoticz.Device(Name="P3 - " + adr_channel, Unit=nbrdevices, Type=248, Switchtype=0).Create()
                    Devices[nbrdevices].Update(nValue = 0,sValue = str(P3),Options = Options)
            elif IsCreated == True :
                Devices[nbrdevices].Update(nValue = 0,sValue = str(P3))
    except Exception as e:
        Domoticz.Log("Error while decoding Infotype8 frame " + repr(e))
        return