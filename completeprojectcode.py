#for face detection
import cv2
import datetime
import numpy as np
#object storage
import ibm_boto3
from ibm_botocore.client import Config, ClientError
#for visual recognition
import json
from watson_developer_cloud import VisualRecognitionV3
#for cloudant db
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
#for sending data to IOT platform
import time
import sys
import ibmiotf.application
import ibmiotf.device  
video=cv2.VideoCapture(0)
#ibm iot platform device details
organization = "kniccz"
deviceType = "rasberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"
# Constants for IBM COS values
COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "V1bhIqexbOdWLokhAOk5A1SIlxjrs8avX4ed8aYX6aH6" # eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
COS_RESOURCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/9aacef9e53274facb815997addccf24e:e61f1bd8-d6fc-4e3e-b130-086b7fb84f24::" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003abfb5d29761c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_RESOURCE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

try:
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
    deviceCli = ibmiotf.device.Client(deviceOptions)
    print("ibm iot connected")
except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()
deviceCli.connect()


def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))
def cloudantstorage():
    client =Cloudant("65eb56e4-a72d-4b13-b226-1626961c5389-bluemix", "899a62a1c1864b9ebf46c8b51ee287b2ffd3baf9314dee8400d1d1e1b33c137c", url="https://65eb56e4-a72d-4b13-b226-1626961c5389-bluemix:899a62a1c1864b9ebf46c8b51ee287b2ffd3baf9314dee8400d1d1e1b33c137c@65eb56e4-a72d-4b13-b226-1626961c5389-bluemix.cloudantnosqldb.appdomain.cloud")
    client.connect()

#Provide your database name

    database_name = "insidegarage"

    my_database = client.create_database(database_name)

    if my_database.exists():
        print(f"'{database_name}' successfully created.")
    return my_database

def visualrecog(x):
#Visual recognition
    visual_recognition = VisualRecognitionV3(
        '2018-03-19',
        iam_apikey='ZCh5wehuL24VgR4VBcJCPg1ASZLMKrgjzoSeBW8QSE2Z')
    with open(x, 'rb') as images_file:
        classes1 = visual_recognition.classify(
            images_file,
            threshold='0.55',
                classifier_ids='celebrity_1626478899').get_result()
    #print(json.dumps(classes1))
    a1=classes1['images'][0]['classifiers'][0]['classes'][0]['class']

    #print(a1)
    """with open('re.jpg', 'rb') as images_file:
        classes1 = visual_recognition.classify(
            images_file,
            threshold='0.6',
                    classifier_ids='cars_269609070').get_result()  
    a2=classes1['images'][0]['classifiers'][0]['classes'][0]['class']"""

    if a1==("teja"):
        string="Open"
    else:
        string="Don't open"
    return string
#Transferring data to ibm iot platform
def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)#Commands

def myOnPublishCallback(data):
    #print ("Published ",ini,"to IBM Watson")
    print ("Published ",data,"to IBM Watson")
    #s=deviceCli.publishEvent("Initial_Status", "json", ini, qos=0, on_publish=myOnPublishCallback)
    success = deviceCli.publishEvent("Current_Status", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not( success):
        print("Not connected to IoTF")
    time.sleep(2)
    
face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#It will read the first frame/image of the video


while True:
    #capture the first frame
    check,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#converts clr to black and white
    #detect the faces from the video using detectMultiScale function
    faces=face_classifier.detectMultiScale(gray,1.3,5)#dimensions
    print(faces)
    
    #drawing rectangle boundries for the detected face
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (127,0,255), 2)#127,0,255 is value for pink clr,so we have pink rectangle
        cv2.imshow('Face detection', frame)
        picname=datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        x=picname+'.jpg'
        cv2.imwrite(x,frame)
        multi_part_upload("insidegarage", x,x)
        my_database=cloudantstorage()
        json_document={"link":COS_ENDPOINT+"/"+"insidegarage"+"/"+x}
        new_document = my_database.create_document(json_document)
        # Check that the document exists in the database.
        if new_document.exists():
            print(f"Document successfully created.")
        a=visualrecog(x)
        deviceCli.commandCallback = myCommandCallback
        data = { "Initial_Status":"Closed","Current_Status": a}
        myOnPublishCallback(data)
        deviceCli.commandCallback = myCommandCallback 
    #waitKey(1)- for every 1 millisecond new frame will be captured
    Key=cv2.waitKey(1)
    if Key==ord('q'):
        #release the camera
        video.release()
        deviceCli.disconnect()
        #destroy all windows
        cv2.destroyAllWindows()
        break
#



