from datetime import datetime
import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("/Users/trongphan/Downloads/FacialDetection_DB/facerecognitionrealtime-746da-firebase-adminsdk-d6luq-ccd6437c55.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecognitionrealtime-746da-default-rtdb.firebaseio.com/',
    'storageBucket': 'facerecognitionrealtime-746da.appspot.com'
})

bucket = storage.bucket()

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

imgBackground =  cv2.imread('/Users/trongphan/Downloads/FacialDetection_DB/Resources/background.png')
folderModePath = '/Users/trongphan/Downloads/FacialDetection_DB/Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

#Take the mode list in Modes and append to modePathList
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(imgModeList) 

#Load the encoding file
print("Loading the encoded file ...")
file = open("EncodingList.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds 
# print(studentIds)
print("Loading the encoded file complete!")

counter = 0
modeType = 3
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    faceCurFrame = face_recognition.face_locations(imgS) #faces in the frame
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame) #encode faces in the current frame
    
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("Matches: ", matches)
            # print("FaceDistance: ", faceDis)
            matchId = np.argmin(faceDis)
            # print("Matched Index: ", matchId)
            
            #check if the matchId in the matches array is True, if same then matched else unknown
            if matches[matchId]:
                # print("Known Face Detected")
                # print(studentIds[matchId])
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                bbox =  55+x1, 162+y1, x2-x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt = 0)
                
                id = studentIds[matchId]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading...", (275,400))
                    cv2.imshow("Face Attendance", imgBackground)
                    # cv2.waitKey(1)
                    counter = 1
                    modeType = 1
            else:
                print("Unknown Face")
                        
        if counter != 0:
            if counter == 1:
                #Get the data
                studentInfo = db.reference(f'People/{id}').get()
                print(studentInfo) 
                #Get the image from storage
                blob = bucket.get_blob(f'/Users/trongphan/Downloads/FacialDetection_DB/Images/{id}.png')
                print(blob)
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                #Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], 
                                                '%Y-%m-%d %H:%M:%S')
                secondElapsed =  (datetime.now() - datetimeObject).total_seconds()
                print(secondElapsed)
                
                if secondElapsed > 30:
                    ref = db.reference(f'People/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 0
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType] 
                        
                        
            if modeType != 0:  
                if 100 < counter < 200:
                    modeType = 2
                    
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    
                    
                if counter <= 100:
                    cvzone.putTextRect(imgBackground, studentInfo['name'], (275,400))
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                    
                    imgBackground[175:175+216, 909:909+216] = imgStudent 
                
                counter += 1
                
                if counter >= 200: 
                    counter = 0
                    modeType = 3
                    studentInfo = []
                    imgStudent = []
                    
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 3
        counter = 0
             
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
    