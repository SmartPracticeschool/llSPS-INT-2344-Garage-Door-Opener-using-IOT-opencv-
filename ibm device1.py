import time
import sys
import ibmiotf.application
import ibmiotf.device
#Provide your IBM Watson Device Credentials
organization = "kniccz"
deviceType = "rasberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.connect()

while True:

        
        #Send data to IOT platform
        data = { "Initial_Status":"Closed","Current_Status": string} #string is obtained from the visualrecognition code
        
        #print (data)
        def myOnPublishCallback():
            print ("Published ",data,"to IBM Watson")

        success = deviceCli.publishEvent("Garage Door", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
