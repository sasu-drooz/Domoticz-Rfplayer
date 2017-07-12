#		   ZiBlue RfPlayer Plugin
#
#		   Author:	 zaraki673/Drooz, 2017
#
#################################################################################################
#################################################################################################
#
#TODO :
#  - Finir emission X2D et RTS (dim level)
#  - gestion des erreurs d absences de tag json
#  - gestion des type DIM pour les suptype 0 et 1
#  - verification des type et subtype des devices utilisés (en attente suite a future modification des appels aux devices)
#  - verification des data inserer
#  - ajout Mode configuration pour les modes transcoder\Parrot (en attente de pouvoir avoir acces a une page de conf pour les plugins python)
#
#################################################################################################
#################################################################################################
#
"""
<plugin key="RFplayer" name="RFplayer" author="zaraki673 - Drooz" version="1.0.2" wikilink="http://www.domoticz.com/wiki/plugins/Ziblue-RFPlayer.html" externallink="http://rfplayer.com/">
	<params>
		<param field="SerialPort" label="Serial Port" width="150px" required="true" default=""/>
		<param field="Mode1" label="Mac Address" width="200px"/>
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
		<param field="Mode2" label="devices ID" width="200px"/>
		<param field="Mode3" label="Area (For X2D)" width="200px"/>
		<param field="Mode6" label="Debug" width="75px">
			<options>
				<option label="True" value="Debug"/>
				<option label="False" value="Normal"  default="true" />
			</options>
		</param>
	</params>
</plugin>
"""
import Domoticz
import datetime
import json

global ReqRcv


class BasePlugin:
	enabled = False
	SerialConn = None
	lastHeartbeat = datetime.datetime.now()

	def __init__(self):
		return

	def onStart(self):
		global ReqRcv
		global SerialConn
		if Parameters["Mode6"] == "Debug":
			Domoticz.Debugging(1)
			with open(Parameters["HomeFolder"]+"Debug.txt", "wt") as text_file:
				print("Started recording message for debug.", file=text_file)
			#Domoticz.Log("Debugger started, use 'telnet 0.0.0.0 4444' to connect")
			#import rpdb
			#rpdb.set_trace()
		if Parameters["Mode5"] != "False":
			if Parameters["Mode5"] =="1": protocol="2" #visonic433
			if Parameters["Mode5"] =="2": protocol="2" #visonic868
			if Parameters["Mode5"] =="3": protocol="4" #chacon
			if Parameters["Mode5"] =="4": protocol="6" #domia
			if Parameters["Mode5"] =="5": protocol="1" #X10
			if Parameters["Mode5"] =="6" or Parameters["Mode5"] =="61" or Parameters["Mode5"] =="62" or Parameters["Mode5"] =="63": protocol="8" #X2D433
			if Parameters["Mode5"] =="7" or Parameters["Mode5"] =="71" or Parameters["Mode5"] =="72" or Parameters["Mode5"] =="73": protocol="8" #X2D868
			if Parameters["Mode5"] =="8": protocol="8" #X2DSHUTTER
			if Parameters["Mode5"] =="11" or Parameters["Mode5"] =="14": protocol="9" #RTS
			if Parameters["Mode5"] =="12": protocol="3" #BLYSS
			if Parameters["Mode5"] =="13": protocol="11" #PARROT
			if Parameters["Mode5"] =="16": protocol="10" #KD101
			id = Parameters["Mode2"]
			Area = Parameters["Mode3"]
			if Parameters["Mode5"] == "4" or Parameters["Mode5"] == "5" or Parameters["Mode5"] == "13" :
				infoType="0"
			if Parameters["Mode5"] == "3" or Parameters["Mode5"] == "12" or Parameters["Mode5"] == "16" :
				infoType="1"
			if Parameters["Mode5"] == "1" or Parameters["Mode5"] == "2" :
				infoType="2"
			if Parameters["Mode5"] == "11" or Parameters["Mode5"] == "14" :
				infoType="3"
			if Parameters["Mode5"] == "6" or Parameters["Mode5"] == "61" or Parameters["Mode5"] == "62" or Parameters["Mode5"] == "63" or Parameters["Mode5"] == "7" or Parameters["Mode5"] == "71" or Parameters["Mode5"] == "72" or Parameters["Mode5"] == "73" :
				infoType="10"
			if Parameters["Mode5"] == "8":
				infoType="11"
			if infoType == "0" or infoType == "1" :
				Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol)}
			if infoType == "2" and Parameters["Mode5"] =="1":
				Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "frequency":"433920"}
			if infoType == "2" and Parameters["Mode5"] =="2":
				Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "frequency":"868950"}
			if infoType == "3" and Parameters["Mode5"] =="11":
				Options = {"infoType": infoType, "id": str(id), "protocol": str(protocol), "subType": "0", "LevelActions": "|||||", "LevelNames": "Off/Down|My|On/Up|Assoc", "LevelOffHidden": "False", "SelectorStyle": "0"}
			if infoType == "3" and Parameters["Mode5"] =="14":
				Options = {"infoType": infoType, "id": str(id), "protocol": str(protocol), "subType": "1", "LevelActions": "||||", "LevelNames": "Off|Left button|Right button", "LevelOffHidden": "False", "SelectorStyle": "0"}
			if infoType == "10" and Parameters["Mode5"] =="6":
				Options = {"infoType":infoType, "id": str(id), "area": str(Area), "function": "2", "protocol": str(protocol), "subType": "0", "frequency":"433920", "LevelActions": "|||||||||", "LevelNames": "Off|Eco|Moderat|Medio|Comfort|Stop|Out of frost|Special|Auto|Centralised", "LevelOffHidden": "True", "SelectorStyle": "0"}
			if infoType == "10" and Parameters["Mode5"] =="61":
				Options = {"infoType":infoType, "id": str(id), "area": str(Area), "function": "1", "protocol": str(protocol), "subType": "0", "frequency":"433920"}
			if infoType == "10" and Parameters["Mode5"] =="62":
				Options = {"infoType":infoType, "id": str(id), "area": str(Area), "function": "12", "protocol": str(protocol), "subType": "0", "frequency":"433920"}
			if infoType == "10" and Parameters["Mode5"] =="63":
				Options = {"infoType":infoType, "id": str(id), "area": str(Area), "function": "26", "protocol": str(protocol), "subType": "0", "frequency":"433920"}
			if infoType == "10" and Parameters["Mode5"] =="7":
				Options = {"infoType":infoType, "id": str(id), "area": str(Area), "function": "2", "protocol": str(protocol), "subType": "0", "frequency":"868950", "LevelActions": "|||||||||", "LevelNames": "Off|Eco|Moderat|Medio|Comfort|Stop|Out of frost|Special|Auto|Centralised", "LevelOffHidden": "True", "SelectorStyle": "0"}
			if infoType == "10" and Parameters["Mode5"] =="71":
				Options = {"infoType":infoType, "id": str(id), "area": str(Area), "function": "1", "protocol": str(protocol), "subType": "0", "frequency":"868950"}
			if infoType == "10" and Parameters["Mode5"] =="72":
				Options = {"infoType":infoType, "id": str(id), "area": str(Area), "function": "12", "protocol": str(protocol), "subType": "0", "frequency":"868950"}
			if infoType == "10" and Parameters["Mode5"] =="73":
				Options = {"infoType":infoType, "id": str(id), "area": str(Area), "function": "26", "protocol": str(protocol), "subType": "0", "frequency":"868950"}
			if infoType == "11" :
				Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "subType": "1", "LevelActions": "|||", "LevelNames": "Off|On|Stop", "LevelOffHidden": "False", "SelectorStyle": "0"}
						
			IsCreated=False
			x=0
			nbrdevices=1
			Domoticz.Debug("Options to find or set : " + str(Options))
			#########check if devices exist ####################
			for x in Devices:
				if Devices[x].Options == Options :
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			########### create device if not find ###############
			if IsCreated == False :
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Manual Switch - " + Parameters["Mode2"], Unit=nbrdevices, Type=16, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue =0,sValue = "0",Options = Options)
			Domoticz.Log("Plugin has " + str(len(Devices)) + " devices associated with it.")
		DumpConfigToLog()
		#Domoticz.Transport("Serial", Parameters["SerialPort"], Baud=115200)
		#Domoticz.Protocol("None")  # None,XML,JSON,HTTP
		#Domoticz.Connect()
		SerialConn = Domoticz.Connection(Name="RfP1000", Transport="Serial", Protocol="None", Address=Parameters["SerialPort"], Baud=115200)
		SerialConn.Connect()
		ReqRcv=''
		return
	
	# present de base 
	def onStop(self):
		#Domoticz.disconnect()
		Domoticz.Log("Plugin is stopping.")

	# present de base 
	def onConnect(self, Connection, Status, Description):
		global isConnected
		if (Status == 0):
			isConnected = True
			Domoticz.Log("Connected successfully to: "+Parameters["SerialPort"])
			# Run RFPlayer configuration
			RFpConf()
		else:
			Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"])
			Domoticz.Debug("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"]+" with error: "+Description)
		return True

	# present de base 
	def onMessage(self, Connection, Data, Status, Extra):
		global Tmprcv
		global ReqRcv
		###########################################
		Tmprcv=Data.decode(errors='ignore')
		################## check if more than 1 sec between two message, if yes clear ReqRcv
		lastHeartbeatDelta = (datetime.datetime.now()-self.lastHeartbeat).total_seconds()
		if (lastHeartbeatDelta > 1):
			ReqRcv=''
			Domoticz.Debug("Last Message was "+str(lastHeartbeatDelta)+" seconds ago, Message clear")
		#Wait not end of data '\r'
		if Tmprcv.endswith('\r',0,len(Tmprcv))==False :
			ReqRcv+=Tmprcv
		else : # while end of data is receive
			ReqRcv+=Tmprcv
			########## TODO : verifier si une trame ZIA n est pas en milieu de message (2messages collés ou perturbation+ message accoller)
			if ReqRcv.startswith("ZIA--{"):
				Domoticz.Debug(ReqRcv)
				ReadConf(ReqRcv)
			if ReqRcv.startswith("ZIA33"):
				Domoticz.Debug(ReqRcv)
				ReadData(ReqRcv)
			ReqRcv=''
		self.lastHeartbeat = datetime.datetime.now()
		return

	# present de base action executer qd une commande est passé a Domoticz
	def onCommand(self, Unit, Command, Level, Hue):
		SendtoRfplayer(Unit, Command, Level, Hue)
		return True

	def onDisconnect(self, Connection):
		return

	def onHeartbeat(self):
		#ReqRcv='ZIA33{ "frame" :{"header": {"frameType": "0", "cluster": "0", "dataFlag": "0", "rfLevel": "-85", "floorNoise": "-97", "rfQuality": "3", "protocol": "7", "protocolMeaning": "OWL", "infoType": "8", "frequency": "433920"},"infos": {"subType": "0", "id_PHY": "0x0002", "id_PHYMeaning": "CM180", "adr_channel": "35216",  "adr": "2201",  "channel": "0",  "qualifier": "1",  "lowBatt": "1", "measures" : [{"type" : "energy", "value" : "871295", "unit" : "Wh"}, {"type" : "power", "value" : "499", "unit" : "W"}]}}}'
		#ReadData(ReqRcv)
		global SerialConn
		if (SerialConn.Connected() != True):
			SerialConn.Connect()
		return True

	def SetSocketSettings(self, power):
		return

	def GetSocketSettings(self):
		return

	def genericPOST(self, commandName):
		return
 

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

def onMessage(Connection, Data, Status, Extra):
	global _plugin
	_plugin.onMessage(Connection, Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
	global _plugin
	_plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
	global _plugin
	_plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
	global _plugin
	_plugin.onDisconnect(Connection)

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
		Domoticz.Debug("Device:		   " + str(x) + " - " + str(Devices[x]))
		Domoticz.Debug("Device ID:	   '" + str(Devices[x].ID) + "'")
		Domoticz.Debug("Device Name:	 '" + Devices[x].Name + "'")
		Domoticz.Debug("Device nValue:	" + str(Devices[x].nValue))
		Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
		Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
	return

def UpdateDevice(Unit, nValue, sValue, Image, SignalLevel, BatteryLevel):
	# Make sure that the Domoticz device still exists (they can be deleted) before updating it 
	if (Unit in Devices):
		if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (Devices[Unit].Image != Image) or (Devices[Unit].SignalLevel != SignalLevel) or (Devices[Unit].BatteryLevel != BatteryLevel) :
			Devices[Unit].Update(nValue, str(sValue),Image, SignalLevel, BatteryLevel)
			Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' SignalLevel:"+str(SignalLevel)+" batteryLevel:'"+str(BatteryLevel)+"%' ("+Devices[Unit].Name+")")
	return

	
	
	
	
	
def RFpConf():
	###################Configure Rfplayer ~##################
	lineinput='ZIA++RECEIVER + *'
	SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
	lineinput='ZIA++FORMAT JSON'
	SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
	if Parameters["Mode1"] != "" :
		lineinput='ZIA++SETMAC ' + Parameters["Mode1"]
		SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
	return
	
def ReadConf(ReqRcv):
	global RfPmac
	ReqRcv=ReqRcv.replace("ZIA--", "")
	DecData = json.loads(ReqRcv)
	RfPmac = DecData['systemStatus']['info'][2]['v']
	Domoticz.Log('rfp1000 mac :' + str(RfPmac))
	return RfPmac
	
	
def ReadData(ReqRcv):
	##############################################################################################################
	# decoding data from RfPlayer 
	##############################################################################################################
	ReqRcv=ReqRcv.replace("ZIA33", "")
	try:
		DecData = json.loads(ReqRcv)
		
		infoType = DecData['frame']['header']['infoType']
		Domoticz.Debug("infoType : " + infoType)
		IsCreated=False
		x=0
		nbrdevices=1
		##############################################################################################################
		#####################################Frame infoType 0					ON/OFF
		##############################################################################################################
		if infoType == "0":
			protocol = DecData['frame']['header']['protocol']
			SubType = DecData['frame']['infos']['subType']
			id = DecData['frame']['infos']['id']
			Domoticz.Debug("id : " + id)
			
			Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol)}
			Domoticz.Debug("Options to find or set : " + str(Options))
			#########check if devices exist ####################
			for x in Devices:
				if Devices[x].Options == Options :
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			########### create device if not find ###############
			if IsCreated == False and Parameters["Mode4"] == "True" :
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name=protocol + " - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue =int(SubType),sValue = str(SubType),Options = Options)
			elif IsCreated == True :
			############ update device if found###################
				Devices[nbrdevices].Update(nValue =int(SubType),sValue = str(SubType))
		##############################################################################################################
		#####################################Frame infoType 1					ON/OFF   error in API receive id instead of id_lsb and id_msb
		##############################################################################################################
		if infoType == "1":
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
			for x in Devices:
				if Devices[x].Options == Options :
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name=protocol + " - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue =int(SubType),sValue = str(SubType),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue =int(SubType),sValue = str(SubType))
		##############################################################################################################
		#####################################Frame infoType 2					Visonic###############################
		#############http://www.el-sys.com.ua/wp-content/uploads/MCR-300_UART_DE3140U0.pdf ###########################
		###########http://cpansearch.perl.org/src/BEANZ/Device-RFXCOM-1.142010/lib/Device/RFXCOM/Decoder/Visonic.pm ##
		#############https://forum.arduino.cc/index.php?topic=289554.0 ###############################################
		##############################################################################################################
		if infoType == "2":
			protocol = DecData['frame']['header']['protocol']
			frequency = DecData['frame']['header']['frequency']
			SubType = DecData['frame']['infos']['subType']
			if protocol == "2":
				id_= DecData['frame']['infos']['id']
				qualifier = list(bin(DecData['frame']['infos']['qualifier'])[2:])
				Domoticz.Debug("id : " + id + " subType :" + SubType)
			elif protocol == "3" :
				id = DecData['frame']['infos']['id']
				Domoticz.Debug("id : " + id + " subType :" + SubType)
			##############################################################################################################
			if SubType == "0" and protocol == "2": # Detector/sensor visonic
				Tamper=qualifier[0]
				Alarm=qualifier[1]
				Battery=qualifier[2]
				if Tamper=="0" and Alarm=="0" :
					status=0
				if Tamper=="1" and Alarm=="0" :
					status=10
				if Tamper=="0" and Alarm=="1" :
					status=20
				if Tamper=="1" and Alarm=="1" :
					status=30
				if Battery=="0" :
					Battery=100
				else :
					Battery=5
				Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType), "LevelActions": "||||", "LevelNames": "Off|Tamper|Alarm|Tamper+Alarm", "LevelOffHidden": "False", "SelectorStyle": "0"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
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
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name=protocol + " - " + id,  Unit=nbrdevices, Type=16, Switchtype=0, Options=Options).Create()
					Devices[nbrdevices].Update(nValue =0, sValue = "on", Options = Options)
				elif IsCreated == True :
					svalue = Devices[nbrdevices].nValue
					if svalue =="on": svalue="off"
					if svalue =="off": svalue="on"
					Devices[nbrdevices].Update(nValue =0, sValue = svalue)
			##############################################################################################################
			elif SubType == "1":  # remote
				Battery=qualifier[2]
				Signal=qualifier[0] + qualifier[1]
				button1=qualifier[4]
				button2=qualifier[5]
				button3=qualifier[6]
				button4=qualifier[7]
				Options = {"infoType":infoType, "id_lsb": str(id_lsb), "id_msb": str(id_msb), "protocol": str(protocol), "subType": str(SubType), "frequency": str(frequency), "button": "1"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name="Button 1 - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery, Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery)
				###########################################################################################################################
				IsCreated=False
				Options = {"infoType":infoType, "id_lsb": str(id_lsb), "id_msb": str(id_msb), "protocol": str(protocol), "subType": str(SubType), "frequency": str(frequency), "button": "2"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name="Button 2 - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery, Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery)
				############################################################################################################################
				IsCreated=False
				Options = {"infoType":infoType, "id_lsb": str(id_lsb), "id_msb": str(id_msb), "protocol": str(protocol), "subType": str(SubType), "frequency": str(frequency), "button": "3"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name="Button 3 - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery, Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery)
				###################################################################################################################################
				IsCreated=False
				Options = {"infoType":infoType, "id_lsb": str(id_lsb), "id_msb": str(id_msb), "protocol": str(protocol), "subType": str(SubType), "frequency": str(frequency), "button": "4"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name="Button 4 - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery, Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery)
		##############################################################################################################
		#####################################Frame infoType 3				RTS	 ##################################
		##############################################################################################################
		if infoType == "3":
			protocol = DecData['frame']['header']['protocol']
			SubType = DecData['frame']['infos']['subType']
			id = DecData['frame']['infos']['id']
			qualifier = DecData['frame']['infos']['qualifier']
			if SubType == "0" :
				if qualifier == "1" :
					level = 0
				elif qualifier == "4" :
					level = 10
				elif qualifier == "7" :
					level = 20
				elif qualifier == "13" :
					level = 30 
				else :
					Domoticz.Log("Unknow qualifier - please send log to dev team")
				#################################################################################################################
				Domoticz.Debug("id : " + id)		
				Options = {"infoType": infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType), "LevelActions": "|||||", "LevelNames": "Off/Down|My|On/Up|Assoc", "LevelOffHidden": "False", "SelectorStyle": "0"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					#Options = {"LevelActions": "|||||", "LevelNames": "Off/Down|My|On/Up|Assoc", "LevelOffHidden": "False", "SelectorStyle": "0"}
					Domoticz.Device(Name=" RTS - " + id,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
					Devices[nbrdevices].Update(nValue = 1,sValue = str(level),Options = Options)
				elif IsCreated == True :
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

				Domoticz.Debug("id : " + id)
				#####################################################################################################################
				Options = {"infoType": infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType), "LevelActions": "||||", "LevelNames": "Off|Left button|Right button", "LevelOffHidden": "False", "SelectorStyle": "0"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1				
					#Options = {"LevelActions": "||||", "LevelNames": "Off|Left button|Right button", "LevelOffHidden": "False", "SelectorStyle": "0"}
					Domoticz.Device(Name=" RTS - " + id,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
					Devices[nbrdevices].Update(nValue = 0,sValue = "0",Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue = 0,sValue = str(level))
					#Devices[nbrdevices].Update(nValue = 1,sValue = "0")
			else :
				Domoticz.Log("Unknow SubType - please send log to dev team")

		##############################################################################################################
		#####################################Frame infoType 4		Oregon thermo/hygro sensors  #####################
		#############http://www.connectingstuff.net/blog/encodage-protocoles-oregon-scientific-sur-arduino/###########
		##############################################################################################################
		if infoType == "4":
			protocol = DecData['frame']['header']['protocol']
			id_PHY = DecData['frame']['infos']['id_PHY']
			adr_channel = DecData['frame']['infos']['adr_channel']
			qualifier = DecData['frame']['infos']['qualifier']
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
			temphygro = temp + ';' + hygro + ';1'

			Domoticz.Debug("id_PHY : " + id_PHY + " adr_channel : " + adr_channel)
			
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Temp" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Temp - " + adr_channel, Unit=nbrdevices, Type=80, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 1,sValue = str(temp),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 1,sValue = str(temp))
			#####################################################################################################################
			IsCreated=False
			x=0
			nbrdevices=1
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Hygro" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Hygro - " + adr_channel, Unit=nbrdevices, Type=81, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = int(hygro),sValue = "1",Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = int(hygro),sValue = "1")
			#####################################################################################################################	
			IsCreated=False
			x=0
			nbrdevices=1
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "TempHygro" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Temp/Hygro - " + adr_channel, Unit=nbrdevices, Type=82, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 1,sValue = str(temphygro),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 1,sValue = str(temphygro))

		##############################################################################################################
		#####################################Frame infoType 5		Oregon thermo/hygro/pressure sensors  ############
		##############################################################################################################
		if infoType == "5":
			protocol = DecData['frame']['header']['protocol']
			id_PHY = DecData['frame']['infos']['id_PHY']
			adr_channel = DecData['frame']['infos']['adr_channel']
			qualifier = DecData['frame']['infos']['qualifier']
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

			Domoticz.Debug("id_PHY : " + id_PHY + " adr_channel : " + adr_channel)
			
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Temp" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Temp - " + adr_channel, Unit=nbrdevices, Type=80, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 0,sValue = str(temp),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 0,sValue = str(temp))
			#####################################################################################################################
			IsCreated=False
			x=0
			nbrdevices=1
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Hygro" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Hygro - " + adr_channel, Unit=nbrdevices, Type=81, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = int(hygro),sValue = "1",Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = int(hygro),sValue = "1")
			#####################################################################################################################
			IsCreated=False
			x=0
			nbrdevices=1
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Pressure" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Pressure - " + adr_channel, Unit=nbrdevices, Type=243, Subtype=26, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 0,sValue = str(pressure),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 0,sValue = str(pressure)+";0")
			#####################################################################################################################	
			IsCreated=False
			x=0
			nbrdevices=1
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "TempHygro" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Temp/Hygro - " + adr_channel, Unit=nbrdevices, Type=82, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 0,sValue = str(temphygro),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 0,sValue = str(temphygro))
			#####################################################################################################################	
			IsCreated=False
			x=0
			nbrdevices=1
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "TempHygropressure" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Temp/Hygro - " + adr_channel, Unit=nbrdevices, Type=84, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 0,sValue = str(temphygropress),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 0,sValue = str(temphygropress))

		##############################################################################################################
		#####################################Frame infoType 6		Oregon Wind sensors  #############################
		#############http://www.connectingstuff.net/blog/encodage-protocoles-oregon-scientific-sur-arduino/###########
		##############################################################################################################
		if infoType == "6":
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

			Domoticz.Debug("id_PHY : " + id_PHY + " adr_channel : " + adr_channel)
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Wind" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True" :
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Wind - " + adr_channel, Unit=nbrdevices, Type=86, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 0,sValue = str(Wind),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 0,sValue = str(Wind))
		
		##############################################################################################################
		#####################################Frame infoType 7		Oregon UV sensors  ############
		##############################################################################################################
		if infoType == "7":
			protocol = DecData['frame']['header']['protocol']
			id_PHY = DecData['frame']['infos']['id_PHY']
			adr_channel = DecData['frame']['infos']['adr_channel']
			qualifier = DecData['frame']['infos']['qualifier']
			UV = DecData['frame']['infos']['measures'][0]['value']
			try:
				lowBatt = DecData['frame']['infos']['lowBatt']
			except IndexError:
				lowbatt="0"
			Domoticz.Debug("id_PHY : " + id_PHY + " adr_channel : " + adr_channel)
			
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "UV" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="UV - " + adr_channel, Unit=nbrdevices, Type=80, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 0,sValue = str(int(UV)/10) + ';0',Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 0,sValue = str(int(UV)/10) + ';0')
		
		##############################################################################################################
		#####################################Frame infoType 8		OWL Energy/power sensors  ############
		##############################################################################################################
		if infoType == "8":
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
			Domoticz.Debug("id_PHY : " + id_PHY + " adr_channel : " + adr_channel)
			##################################################################################################################################
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Power&Energie" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Power & Energie - " + adr_channel, Unit=nbrdevices, Type=243, Subtype =29, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 0,sValue = str(Power + ';' + Energy),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 0,sValue = str(Power + ';' + Energy))		
			##################################################################################################################################
			if P1 != "" : 
				IsCreated=False
				x=0
				nbrdevices=1
				Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "P1" : "1"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options:
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name="P1 - " + adr_channel, Unit=nbrdevices, Type=248, Switchtype=0).Create()
					Devices[nbrdevices].Update(nValue = 0,sValue = str(P1),Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue = 0,sValue = str(P1))
			##################################################################################################################################
			if P2 != "" :
				IsCreated=False
				x=0
				nbrdevices=1
				Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "P2" : "1"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options:
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name="P2 - " + adr_channel, Unit=nbrdevices, Type=248, Switchtype=0).Create()
					Devices[nbrdevices].Update(nValue = 0,sValue = str(P2),Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue = 0,sValue = str(P2))	
			##################################################################################################################################
			if P3 != "" :
				IsCreated=False
				x=0
				nbrdevices=1
				Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "P3" : "1"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options:
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name="P3 - " + adr_channel, Unit=nbrdevices, Type=248, Switchtype=0).Create()
					Devices[nbrdevices].Update(nValue = 0,sValue = str(P3),Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue = 0,sValue = str(P3))	
		
		##############################################################################################################
		#####################################Frame infoType 9		Oregon Rain sensors  ############
		##############################################################################################################
		if infoType == "9":
			protocol = DecData['frame']['header']['protocol']
			id_PHY = DecData['frame']['infos']['id_PHY']
			adr_channel = DecData['frame']['infos']['adr_channel']
			qualifier = DecData['frame']['infos']['qualifier']
			try:
				lowBatt = DecData['frame']['infos']['lowBatt']
			except IndexError:
				lowbatt="0"
			try:
				TotalRain = DecData['frame']['infos']['measures'][0]['value']
			except IndexError:
				TotalRain = "0"
			try :
				CurrentRain = DecData['frame']['infos']['measures'][1]['value']
			except IndexError:
				CurrentRain = "0"

			Domoticz.Debug("id_PHY : " + id_PHY + " adr_channel : " + adr_channel)
			
			Options = {"infoType":infoType, "id_PHY": str(id_PHY), "adr_channel": str(adr_channel), "protocol": str(protocol), "Temp" : "1"}
			Domoticz.Debug("Options to find or set : " + str(Options))
			for x in Devices:
				if Devices[x].Options == Options:
					IsCreated = True
					Domoticz.Log("Devices already exist. Unit=" + str(x))
					Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
					nbrdevices=x
				if IsCreated == False :
					nbrdevices=x
			if IsCreated == False and Parameters["Mode4"] == "True":
				nbrdevices=nbrdevices+1
				Domoticz.Device(Name="Rain - " + adr_channel, Unit=nbrdevices, Type=85, Switchtype=0).Create()
				Devices[nbrdevices].Update(nValue = 0,sValue = str(CurrentRain),Options = Options)
			elif IsCreated == True :
				Devices[nbrdevices].Update(nValue = 0,sValue = str(CurrentRain))

		##############################################################################################################
		#####################################Frame infoType 10		  Thermostats  X2D protocol ######################
		##############################################################################################################
		if infoType == "10":
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
					status = 10
				if state == "1": #MODERAT 
					status = 20
				if state == "2": #MEDIO
					status = 30
				if state == "3": #COMFORT 
					status = 40
				if state == "4": #STOP 
					status = 50
				if state == "5": #OUT OF FROST 
					status = 60
				if state == "6": #SPECIAL 
					status = 70
				if state == "7": #AUTO 
					status = 80
				if state == "8": #CENTRALISED
					status = 90
				Options = {"infoType":infoType, "id": str(idd), "area": str(area), "function": str(function), "protocol": str(protocol), "subType": str(SubType), "frequency": str(frequency), "LevelActions": "|||||||||", "LevelNames": "Off|Eco|Moderat|Medio|Comfort|Stop|Out of frost|Special|Auto|Centralised", "LevelOffHidden": "True", "SelectorStyle": "0"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name=protocol + " - " + id,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue =0,sValue = str(status))
		##############################################################################################################
			else :
				Options = {"infoType":infoType, "id": str(id), "area": str(area), "function": str(function), "protocol": str(protocol), "subType": str(SubType), "frequency": str(frequency)}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name=protocol + " - " + id, Unit=nbrdevices, Type=16, Switchtype=0).Create()
					Devices[nbrdevices].Update(nValue =0,sValue = str(state), Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue =0,sValue = str(state))

		##############################################################################################################
		#####################################Frame infoType 11		 Alarm X2D protocol / Shutter ####################
		##############################################################################################################
		if infoType == "11":
			protocol = DecData['frame']['header']['protocol']
			SubType = DecData['frame']['infos']['subType']
			##############################################################################################################
			if SubType == "0" : # Detector/sensor
				id = DecData['frame']['infos']['id']
				qualifier = list(bin(DecData['frame']['infos']['qualifier'])[2:])
				Tamper=qualifier[0]
				Alarm=qualifier[1]
				Battery=qualifier[2]
				if Tamper=="0" and Alarm=="0" :
					status=0
				if Tamper=="1" and Alarm=="0" :
					status=10
				if Tamper=="0" and Alarm=="1" :
					status=20
				if Tamper=="1" and Alarm=="1" :
					status=30
				if Battery=="0" :
					Battery=100
				else :
					Battery=5
				Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType), "LevelActions": "||||", "LevelNames": "Off|Tamper|Alarm|Tamper+Alarm", "LevelOffHidden": "False", "SelectorStyle": "0"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					#Options = {"LevelActions": "||||", "LevelNames": "Off|Tamper|Alarm|Tamper+Alarm", "LevelOffHidden": "False", "SelectorStyle": "0"}
					Domoticz.Device(Name=protocol + " - " + id,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery, Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), BatteryLevel = Battery)
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
				Options = {"infoType":infoType, "id": str(id), "protocol": str(protocol), "subType": str(SubType), "LevelActions": "|||", "LevelNames": "Off|On|Stop", "LevelOffHidden": "False", "SelectorStyle": "0"}
				Domoticz.Debug("Options to find or set : " + str(Options))
				for x in Devices:
					if Devices[x].Options == Options :
						IsCreated = True
						Domoticz.Log("Devices already exist. Unit=" + str(x))
						Domoticz.Debug("Options find in DB: " + str(Devices[x].Options) + " for devices unit " + str(x))
						nbrdevices=x
					if IsCreated == False :
						nbrdevices=x
				if IsCreated == False and Parameters["Mode4"] == "True":
					nbrdevices=nbrdevices+1
					Domoticz.Device(Name=protocol + " - " + id,  Unit=nbrdevices, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
					Devices[nbrdevices].Update(nValue =0,sValue = str(status), Options = Options)
				elif IsCreated == True :
					Devices[nbrdevices].Update(nValue =0,sValue = str(status))

		
		if Parameters["Mode6"] == "Debug":
			writetofile(ReqRcv)
		ReqRcv=""
	except:
		Domoticz.Log("Error while decoding or reading JSON")
		Domoticz.Debug("Debug : Error Decoding/Reading  " + ReqRcv)
		return


def SendtoRfplayer(Unit, Command, Level, Hue):
	Options=Devices[Unit].Options
	Domoticz.Debug("SendtoRfplayer - Options find in DB: " + str(Devices[Unit].Options) + " for devices unit " + str(Unit))
	infoType = Options['infoType']
	protocol=Options['protocol']
	if protocol =="1": protocol="X10"
	if protocol =="2": 
		frequency=Options['frequency']
		if frequency == "433920":
			protocol="VISONIC433"
		if frequency == "868950":
			protocol="VISONIC868"
	if protocol =="3": protocol="BLYSS"
	if protocol =="4": protocol="CHACON"
	if protocol =="6": protocol="DOMIA"
	if protocol =="8" and infoType == "10":
		frequency=Options['frequency']
		if frequency == "433920":
			protocol="X2D433"
		if frequency == "868950":
			protocol="X2D868"
	if protocol =="8" and infoType == "11":
		protocol="X2DSHUTTER"
	if protocol =="9": protocol="RTS"
	if protocol =="10": protocol="KD101"
	if protocol =="11": protocol="PARROT"

	if infoType == "0" or infoType == "1" or infoType == "2":
		id=Options['id']
		lineinput='ZIA++' + str(Command.upper()) + " " + protocol + " ID " + id
		SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
		if Command == "On":
			Devices[Unit].Update(nValue =1,sValue = "on")
		if Command == "Off":
			Devices[Unit].Update(nValue =0,sValue = "off")
	
	if infoType == "3" :
		id=Options['id']
		qualifier=Options['subType']
		if qualifier=="0":
			if Level == 0 :
				lineinput='ZIA++' + str("DIM %1 " + protocol + " ID " + id + " QUALIFIER " + qualifier)
			if Level == 10 :
				lineinput='ZIA++' + str("DIM %4 " + protocol + " ID " + id + " QUALIFIER " + qualifier)
			if Level == 20 :
				lineinput='ZIA++' + str("DIM %2 " + protocol + " ID " + id + " QUALIFIER " + qualifier)
			if Level == 30 :
				lineinput='ZIA++' + str("ASSOC " + protocol + " ID " + id + " QUALIFIER " + qualifier)
		if qualifier=="1":
			if Level == 10 :
				lineinput='ZIA++' + str("ON " + protocol + " ID " + id + " QUALIFIER " + qualifier)
			if Level == 20 :
				lineinput='ZIA++' + str("OFF " + protocol + " ID " + id + " QUALIFIER " + qualifier)
			if Level == 30 :
				lineinput='ZIA++' + str("ASSOC " + protocol + " ID " + id + " QUALIFIER " + qualifier)
		SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
		Devices[Unit].Update(nValue =0,sValue = str(Level))
		
	if infoType == "10" :
		id=Options['id']
		Area=Options['area']
		if Level == 0 :
			lineinput='ZIA++' + str("DIM %0 " + protocol + " ID " + id )
		if Level == 10 :
			lineinput='ZIA++' + str("DIM %1 " + protocol + " ID " + id)
		if Level == 20 :
			lineinput='ZIA++' + str("DIM %2 " + protocol + " ID " + id)
		if Level == 30 :
			lineinput='ZIA++' + str("DIM %3 " + protocol + " ID " + id)
		if Level == 40 :
			lineinput='ZIA++' + str("DIM %4 " + protocol + " ID " + id)
		if Level == 50 :
			lineinput='ZIA++' + str("DIM %5 " + protocol + " ID " + id)
		if Level == 60 :
			lineinput='ZIA++' + str("DIM %6 " + protocol + " ID " + id)
		if Level == 70 :
			lineinput='ZIA++' + str("DIM %7 " + protocol + " ID " + id)
		if Level == 80 :
			lineinput='ZIA++' + str("DIM %8 " + protocol + " ID " + id)
		if Level == 90 :
			lineinput='ZIA++' + str("DIM %9 " + protocol + " ID " + id)
		SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
		Devices[Unit].Update(nValue =0,sValue = str(Level))

	if infoType == "11" :
		id=Options['id']
		if Level == 10 :
			lineinput='ZIA++' + str("ON " + protocol + " ID " + id + " QUALIFIER " + qualifier)
		if Level == 20 :
			lineinput='ZIA++' + str("OFF " + protocol + " ID " + id + " QUALIFIER " + qualifier)
		if Level == 30 :
			lineinput='ZIA++' + str("ASSOC " + protocol + " ID " + id + " QUALIFIER " + qualifier)
		SerialConn.Send(bytes(lineinput + '\n\r','utf-8'))
		Devices[Unit].Update(nValue =0,sValue = str(Level))
				
	return

def writetofile(ReqRcv):
	with open(Parameters["HomeFolder"]+"Response.txt", "at") as text_file:
		print(ReqRcv, file=text_file)
	return
