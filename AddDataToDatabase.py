import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("/Users/trongphan/Downloads/FacialDetection_DB/facerecognitionrealtime-746da-firebase-adminsdk-d6luq-ccd6437c55.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecognitionrealtime-746da-default-rtdb.firebaseio.com/'
})
ref = db.reference("People")
data = {
    '321654':
        {
            'name': 'Hassan',
            'major': 'Robotic',
            'starting_year': 2017,
            'total_attendance':6,
            'year':4,
            'last_attendance_time':'2022-12-11 00:54:34'
        },
        '852741':
        {
            'name': 'Emily',
            'major': 'Econs',
            'starting_year': 2018,
            'total_attendance':10,
            'year':3,
            'last_attendance_time':'2022-12-11 00:54:34'
        },'963825':
        {
            'name': 'Elon',
            'major': 'CS',
            'starting_year': 2015,
            'total_attendance':100,
            'year':1,
            'last_attendance_time':'2022-12-11 00:54:34'
        },'100000':
        {
            'name': 'Phan',
            'major': 'Play',
            'starting_year': 2017,
            'total_attendance':6,
            'year':4,
            'last_attendance_time':'2022-12-11 00:54:34'
        },
        '100300':
            {
                'name': 'em hong',
                'major': 'di ia',
                'starting_year': 2016,
                'total_attendance': 7,
                'year': 9,
                'last_attendance_time':'2022-12-11 00:53:33'
            },
        '111111':
            {
                'name': 'dang beo',
                'major': 'di ia',
                'starting_year': 2017,
                'total_attendance': 10,
                'year': 10,
                'last_attendance_time':'2022-12-11 00:55:44'    
            },
        '222222':
            {
                'name': 'a duong beo',
                'major': 'di ngu',
                'starting_year': 2018,
                'total_attendance': 99,
                'year':1,
                'last_attendance_time':'2022-12-11 00:55:44'
            }
}
for key, value in data.items(): 
    ref.child(key).set(value)
