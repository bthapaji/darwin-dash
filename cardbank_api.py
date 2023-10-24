import pyrebase

firebaseConfigs = {
  "apiKey": "AIzaSyBCCTeBS3Oj2FG1PAKi6EcWjURElkdkzSo",
  "authDomain": "dordash-d4c80.firebaseapp.com",
  "databaseURL": "https://dordash-d4c80-default-rtdb.firebaseio.com",
  "projectId": "dordash-d4c80",
  "storageBucket": "dordash-d4c80.appspot.com",
  "messagingSenderId": "242358179681",
  "appId": "1:242358179681:web:8b0ed895674389672cd720",
  "measurementId": "G-V6FNEYNN5Z"
};
firebases = pyrebase.initialize_app(firebaseConfigs)
db_cardbank= firebases.database()
auth_cardbank=firebases.auth()