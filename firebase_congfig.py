import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyCzKExs7Vh61Pw_q2eIIclBUb_NYAvA5jU",
  "authDomain": "topup-45f9d.firebaseapp.com",
  "databaseURL": "https://topup-45f9d-default-rtdb.firebaseio.com",
  "projectId": "topup-45f9d",
  "storageBucket": "topup-45f9d.appspot.com",
  "messagingSenderId": "310783137068",
  "appId": "1:310783137068:web:9b6fbf2ced577a54360889",
  "measurementId": "G-RF9X1DRJ18"
};
firebase = pyrebase.initialize_app(firebaseConfig)
db= firebase.database()
auth=firebase.auth()