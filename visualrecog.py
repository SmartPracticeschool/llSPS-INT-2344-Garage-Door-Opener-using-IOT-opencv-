import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='ZCh5wehuL24VgR4VBcJCPg1ASZLMKrgjzoSeBW8QSE2Z')
with open(f'{x}', 'rb') as images_file: #x is the picname in the format of time stamp
    classes1 = visual_recognition.classify(
        images_file,
        threshold='0.55',  
	classifier_ids='celebrity_1626478899').get_result()  
a=classes1['images'][0]['classifiers'][0]['classes'][0]['class']
if a=="teja":
    string="Open the garage door"
else:
    string="Not the red car"
print(string)


