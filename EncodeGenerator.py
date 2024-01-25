import cv2 
import face_recognition
import pickle
import os 

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("/Users/trongphan/Downloads/FacialDetection_DB/facerecognitionrealtime-746da-firebase-adminsdk-d6luq-ccd6437c55.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecognitionrealtime-746da-default-rtdb.firebaseio.com/',
    'storageBucket': 'facerecognitionrealtime-746da.appspot.com'
})

#Importing images
folderPath = '/Users/trongphan/Downloads/FacialDetection_DB/Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])
    
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName) 
    
print(len(imgList))

def findEncoding(imageList):
    encodeList = []
    for img in imageList:
        #convert BGR to RGB since opencv & face_recognition use different format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList 

print("Encoding Started ...")
encodeListKnown = findEncoding(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete!")

file = open("EncodingList.p", "wb")
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File saved!")
