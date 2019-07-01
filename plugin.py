#!/usr/bin/env python3
# coding: utf-8 -*-
#
#           ZiBlue RfPlayer Plugin
#
#           Author:     zaraki673, 2017
#

"""
<plugin key="RFplayerNew" name="RFplayerNew" author="zaraki673" version="2.0.0" wikilink="http://www.domoticz.com/wiki/plugins/Ziblue-RFPlayer.html" externallink="http://rfplayer.com/">
    <params>
        <param field="SerialPort" label="Serial Port" width="150px" required="true" default=""/>
        <param field="Mode1" label="Mac Address" width="200px"/>
        <param field="Mode3" label="Jamalert" width="75px">
            <options>
                <option label="Disable" value="0"/>
                <option label="1" value="1"/>
                <option label="2" value="2"/>
                <option label="3" value="3"/>
                <option label="4" value="4"/>
                <option label="5" value="5"/>
                <option label="6" value="6"/>
                <option label="7" value="7" default="true"/>
                <option label="8" value="8"/>
                <option label="9" value="9"/>
                <option label="10" value="10"/>
            </options>
        </param>
        <param field="Mode4" label="Enable Learning Mode" width="75px">
            <options>
                <option label="Enable" value="True"/>
                <option label="Disable" value="False"  default="true" />
            </options>
        </param>
        <param field="Mode5" label="Manual Create devices" width="75px">
            <options>
                <option label="False" value="False"  default="true" />
                <option label="VISONIC - 433" value="1"/>
                <option label="VISONIC - 868" value="2"/>
                <option label="CHACON" value="3"/>
                <option label="DOMIA" value="4"/>
                <option label="X10" value="5"/>
                <option label="X2D - 433 - OPERATING_MODE" value="6"/>
                <option label="X2D - 433 - HEATING_SPEED" value="61"/>
                <option label="X2D - 433 - REGULATION" value="62"/>
                <option label="X2D - 433 - THERMIC_AREA_STATE" value="63"/>
                <option label="X2D - 868 - OPERATING_MODE" value="7"/>
                <option label="X2D - 868 - HEATING_SPEED" value="71"/>
                <option label="X2D - 868 - REGULATION" value="72"/>
                <option label="X2D - 868 - THERMIC_AREA_STATE" value="73"/>
                <option label="X2D - SHUTTER" value="8"/>
                <option label="RTS - SHUTTER" value="11"/>
                <option label="RTS - PORTAL" value="14"/>
                <option label="BLYSS" value="12"/>
                <option label="PARROT" value="13"/>
                <option label="KD101" value="16"/>
            </options>
        </param>
        <param field="Mode2" label="device ID" width="200px"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="None" value="0"  default="true" />
                <option label="Python Only" value="2"/>
                <option label="Basic Debugging" value="62"/>
                <option label="Basic+Messages" value="126"/>
                <option label="Connections Only" value="16"/>
                <option label="Connections+Python" value="18"/>
                <option label="Connections+Queue" value="144"/>
                <option label="All" value="-1"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import datetime
import json

from Modules.tools import ManualAddDevice, RFpConf, ReadConf, SendtoRfplayer, ReadData

class BasePlugin:
    enabled = False

    def __init__(self):
        self.RFMacAdress = Parameters["Mode1"]
        self.PDebugMode = Parameters["Mode6"]
        self.ManualDeviceType = Parameters["Mode5"]
        self.ManualDeviceID = Parameters["Mode2"]
        self.Phomefolder = Parameters["HomeFolder"]
        self.SerialConn = None
        self.lastHeartbeat = datetime.datetime.now()
        self.ReqRcv = ""
        self.isConnected = False
        self.LearningMode = Parameters["Mode4"]
        self.JamAlert = Parameters["Mode3"]
        Domoticz.Log("Plugin is init.")
        return

    def onStart(self):
        if self.PDebugMode != "0":
            Domoticz.Debugging(int(self.PDebugMode))
            DumpConfigToLog()
            with open(self.Phomefolder+"Debug.txt", "wt") as text_file:
                print("Started recording message for debug.", file=text_file)
        if self.ManualDeviceType != "False": # manual device creation
            ManualAddDevice(self,self.ManualDeviceType,self.ManualDeviceID)
        self.SerialConn = Domoticz.Connection(Name="RfP1000", Transport="Serial", Protocol="None", Address=Parameters["SerialPort"], Baud=115200)
        self.SerialConn.Connect()
        self.ReqRcv=''
        Domoticz.Log("Plugin is onStart.")
        return
    
    # present de base 
    def onStop(self):
        #Domoticz.disconnect()
        Domoticz.Log("Plugin is stopping.")

    # present de base 
    def onConnect(self, Connection, Status, Description):
        if (Status == 0):
            self.isConnected = True
            Domoticz.Status("Connected successfully to: "+Parameters["SerialPort"])
            # Run RFPlayer configuration
            RFpConf(self)
        else:
            Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"])
            Domoticz.Debug("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"]+" with error: "+Description)
        return True

    # present de base 
    def onMessage(self, Connection, Data):
        global Tmprcv
        ###########################################
        Tmprcv=Data.decode(errors='ignore')
        ################## check if more than 1 sec between two message, if yes clear ReqRcv
        self.lastHeartbeatDelta = (datetime.datetime.now()-self.lastHeartbeat).total_seconds()
        if (self.lastHeartbeatDelta > 1):
            self.ReqRcv=''
            Domoticz.Debug("Last Message was "+str(lastHeartbeatDelta)+" seconds ago, Message clear")
        #Wait not end of data '\r'
        if Tmprcv.endswith('\r',0,len(Tmprcv))==False :
            self.ReqRcv+=Tmprcv
        else : # while end of data is receive
            self.ReqRcv+=Tmprcv
            ########## TODO : verifier si une trame ZIA n est pas en milieu de message (2messages collés ou perturbation+ message accoller)
            if self.ReqRcv.startswith("ZIA--{"):
                Domoticz.Debug(ReqRcv)
                ReadConf(self,ReqRcv)
            if self.ReqRcv.startswith("ZIA33"):
                Domoticz.Debug(ReqRcv)
                ReadData(self, ReqRcv)
            self.ReqRcv=''
        self.lastHeartbeat = datetime.datetime.now()
        return

    # present de base action executer qd une commande est passé a Domoticz
    def onCommand(self, Unit, Command, Level, Hue):
        SendtoRfplayer(self, Unit, Command, Level, Hue)
        return True

    def onHeartbeat(self):
        ###########
        #infotype0  ==> ok
        #ReqRcv = 'ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-44", "floorNoise": "-99", "rfQuality": "10", "protocol": "6", "protocolMeaning": "DOMIA", "infoType": "0", "frequency": "433920"},"infos": {"subType": "0", "id": "235", "subTypeMeaning": "OFF", "idMeaning": "O12"}}}'
        ###########
        #infotype1 ==> ok
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-72", "floorNoise": "-106", "rfQuality": "8", "protocol": "4", "protocolMeaning": "CHACON", "infoType": "1", "frequency": "433920"},"infos": {"subType": "1", "id": "424539265", "subTypeMeaning": "ON"}}}'
        ###########
        #infotype2
        #==> ok
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-51", "floorNoise": "-103", "rfQuality": "10", "protocol": "2", "protocolMeaning": "VISONIC", "infoType": "2", "frequency": "433920"},"infos": {"subType": "0", "subTypeMeaning": "Detector/Sensor", "id": "335547184", "qualifier": "3", "qualifierMeaning": { "flags": ["Tamper","Alarm"]}}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-55", "floorNoise": "-102", "rfQuality": "10", "protocol": "2", "protocolMeaning": "VISONIC", "infoType": "2", "frequency": "433920"},"infos": {"subType": "0", "subTypeMeaning": "Detector/Sensor", "id": "2034024048", "qualifier": "1", "qualifierMeaning": { "flags": ["Tamper"]}}}}'
        #OK ==>  protocol = 3
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-66", "floorNoise": "-106", "rfQuality": "10", "protocol": "3", "protocolMeaning": "BLYSS", "infoType": "2", "frequency": "433920"},"infos": {"subType": "0", "subTypeMeaning": "Detector/Sensor", "id": "256292321", "qualifier": "0"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-84", "floorNoise": "-106", "rfQuality": "5", "protocol": "2", "protocolMeaning": "VISONIC", "infoType": "2", "frequency": "868950"},"infos": {"subType": "0", "subTypeMeaning": "Detector/Sensor", "id": "2039708784", "qualifier": "0", "qualifierMeaning": { "flags": []}}}}'
        ###########
        #infotype3 RTS Subtype0 ==> ok  // 
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-64", "floorNoise": "-103", "rfQuality": "9", "protocol": "9", "protocolMeaning": "RTS", "infoType": "3", "frequency": "433920"},"infos": {"subType": "0", "subTypeMeaning": "Shutter", "id": "14813191", "qualifier": "4", "qualifierMeaning": { "flags": ["My"]}}}}'
        ###########
        #infotype4
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-86", "floorNoise": "-100", "rfQuality": "3", "protocol": "5", "protocolMeaning": "OREGON", "infoType": "4", "frequency": "433920"},"infos": {"subType": "0", "id_PHY": "0xEA4C", "id_PHYMeaning": "THC238/268,THWR288,THRN122,THN122/132,AW129/131", "adr_channel": "21762", "adr": "85", "channel": "2", "qualifier": "33", "lowBatt": "1", "measures" : [{"type" : "temperature", "value" : "-17.8", "unit" : "Celsius"}, {"type" : "hygrometry", "value" : "0", "unit" : "%"}]}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-46", "floorNoise": "-105", "rfQuality": "10", "protocol": "5", "protocolMeaning": "OREGON", "infoType": "4", "frequency": "433920"},"infos": {"subType": "0", "id_PHY": "0x1A2D", "id_PHYMeaning": "THGR122/228/238/268,THGN122/123/132", "adr_channel": "63492", "adr": "248", "channel": "4", "qualifier": "32", "lowBatt": "0", "measures" : [{"type" : "temperature", "value" : "+20.3", "unit" : "Celsius"}, {"type" : "hygrometry", "value" : "41", "unit" : "%"}]}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-77", "floorNoise": "-100", "rfQuality": "5", "protocol": "5", "protocolMeaning": "OREGON", "infoType": "4", "frequency": "433920"},"infos": {"subType": "0", "id_PHY": "0xFA28", "id_PHYMeaning": "THGR810", "adr_channel": "64513", "adr": "252", "channel": "1", "qualifier": "48", "lowBatt": "0", "measures" : [{"type" : "temperature", "value" : "+21.0", "unit" : "Celsius"}, {"type" : "hygrometry", "value" : "35", "unit" : "%"}]}}}'
        ###########
        #infotype5
        ###########
        #infotype6
        ###########
        #infotype7
        ###########
        #infotype8 OWL ==> ok
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-85", "floorNoise": "-97", "rfQuality": "3", "protocol": "7", "protocolMeaning": "OWL", "infoType": "8", "frequency": "433920"},"infos": {"subType": "0", "id_PHY": "0x0002", "id_PHYMeaning": "CM180", "adr_channel": "35216",  "adr": "2201",  "channel": "0",  "qualifier": "1",  "lowBatt": "1", "measures" : [{"type" : "energy", "value" : "871295", "unit" : "Wh"}, {"type" : "power", "value" : "499", "unit" : "W"}]}}}'
        ###########
        #infotype9
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-91", "floorNoise": "-107", "rfQuality": "4", "protocol": "9", "protocolMeaning": "RTS", "infoType": "3", "frequency": "433920"},"infos": {"subType": "0", "subTypeMeaning": "Shutter", "id": "9378633", "qualifier": "7", "qualifierMeaning": { "flags": ["Up/On"]}}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-98", "floorNoise": "-107", "rfQuality": "2", "protocol": "9", "protocolMeaning": "RTS", "infoType": "3", "frequency": "433920"},"infos": {"subType": "0", "subTypeMeaning": "Shutter", "id": "1310793", "qualifier": "1", "qualifierMeaning": { "flags": ["Down/Off"]}}}}'
        ###########
        #infotype10
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-74", "floorNoise": "-108", "rfQuality": "8", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "GENERIC", "id": "1608089600", "area": "0", "qualifier": "36", "qualifierMeaning": { "flags": ["LowBatt"]}, "function": "12", "functionMeaning": "REGULATION", "state": "0", "stateMeaning": "OFF"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-73", "floorNoise": "-108", "rfQuality": "8", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "GENERIC", "id": "3755245568", "area": "0", "qualifier": "32", "qualifierMeaning": { "flags": []}, "function": "2", "functionMeaning": "OPERATING MODE", "state": "7", "stateMeaning": "AUTO"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-87", "floorNoise": "-108", "rfQuality": "5", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "8", "subTypeMeaning": "REC BIDIR", "id": "3962161153", "area": "1", "qualifier": "32", "qualifierMeaning": { "flags": []}, "function": "2", "functionMeaning": "OPERATING MODE", "state": "7", "stateMeaning": "AUTO"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-73", "floorNoise": "-108", "rfQuality": "8", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "GENERIC", "id": "1608089600", "area": "0", "qualifier": "36", "qualifierMeaning": { "flags": ["LowBatt"]}, "function": "1", "functionMeaning": "HEATING SPEED", "state": "1", "stateMeaning": "ON"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-73", "floorNoise": "-108", "rfQuality": "8", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "GENERIC", "id": "1608089600", "area": "0", "qualifier": "36", "qualifierMeaning": { "flags": ["LowBatt"]}, "function": "2", "functionMeaning": "OPERATING MODE", "state": "4", "stateMeaning": "STOP"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-89", "floorNoise": "-108", "rfQuality": "4", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "8", "subTypeMeaning": "REC BIDIR", "id": "3962161153", "area": "1", "qualifier": "32", "qualifierMeaning": { "flags": []}, "function": "2", "functionMeaning": "OPERATING MODE", "state": "4", "stateMeaning": "STOP"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-72", "floorNoise": "-108", "rfQuality": "9", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "GENERIC", "id": "3755245568", "area": "0", "qualifier": "32", "qualifierMeaning": { "flags": []}, "function": "12", "functionMeaning": "REGULATION", "state": "0", "stateMeaning": "OFF"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-74", "floorNoise": "-108", "rfQuality": "8", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "GENERIC", "id": "3755245568", "area": "0", "qualifier": "32", "qualifierMeaning": { "flags": []}, "function": "1", "functionMeaning": "HEATING SPEED", "state": "1", "stateMeaning": "ON"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-75", "floorNoise": "-108", "rfQuality": "8", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "GENERIC", "id": "1608089600", "area": "0", "qualifier": "36", "qualifierMeaning": { "flags": ["LowBatt"]}, "function": "12", "functionMeaning": "REGULATION", "state": "0", "stateMeaning": "OFF"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-76", "floorNoise": "-108", "rfQuality": "8", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "GENERIC", "id": "3755245568", "area": "0", "qualifier": "32", "qualifierMeaning": { "flags": []}, "function": "2", "functionMeaning": "OPERATING MODE", "state": "7", "stateMeaning": "AUTO"}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-93", "floorNoise": "-108", "rfQuality": "3", "protocol": "8", "protocolMeaning": "X2D", "infoType": "10", "frequency": "868350"},"infos": {"subType": "8", "subTypeMeaning": "REC BIDIR", "id": "3962161153", "area": "1", "qualifier": "32", "qualifierMeaning": { "flags": []}, "function": "2", "functionMeaning": "OPERATING MODE", "state": "7", "stateMeaning": "AUTO"}}}'
        ###########
        #infotype11 ==> ok
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-75", "floorNoise": "-99", "rfQuality": "6", "protocol": "8", "protocolMeaning": "X2D", "infoType": "11", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "Detector/Sensor", "id": "2888689920", "qualifier": "10", "qualifierMeaning": { "flags": ["Alarm","Supervisor/Alive"]}}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-57", "floorNoise": "-106", "rfQuality": "10", "protocol": "8", "protocolMeaning": "X2D", "infoType": "11", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "Detector/Sensor", "id": "1112729857", "qualifier": "2", "qualifierMeaning": { "flags": ["Alarm"]}}}}'
        #ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "1", "rfLevel": "-57", "floorNoise": "-106", "rfQuality": "10", "protocol": "8", "protocolMeaning": "X2D", "infoType": "11", "frequency": "868350"},"infos": {"subType": "0", "subTypeMeaning": "Detector/Sensor", "id": "1112729857", "qualifier": "0", "qualifierMeaning": { "flags": []}}}}'
        ###########
        #ReadData(ReqRcv)
        if (self.SerialConn.Connected() != True):
            self.SerialConn.Connect()
        return True


global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
        Domoticz.Debug("Options:         '" + str(Devices[x].Options) + "'")
    return

