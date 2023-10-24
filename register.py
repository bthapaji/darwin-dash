from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty
from firebase_congfig import db
from firebase_congfig import auth



#Registration code
class registerWindow(Screen):
     usernames = ObjectProperty(None)
     password = ObjectProperty(None)
     number=ObjectProperty(None)
     address=ObjectProperty(None)


     def perform_register(self):
         uname=self.usernames.text
         pas=self.password.text

         data_insert={
                      "number":self.number.text,
                      "address":self.address.text}
         try:
             user=auth.create_user_with_email_and_password(uname, pas)
             auth_uid=user['localId']
             db.child("users/").child(auth_uid).push(data_insert)
             self.usernames.text=""
             self.password.text=""
             self.number.text=""
             self.address.text=""
             print("data insert succesful")
         except Exception as e:
             print("unscessful",str(e))
         pass
class Register(MDApp):
    def build(self):
        return registerWindow()

if __name__ == '__main__':
    Window.size=(360,640)
    Register().run()