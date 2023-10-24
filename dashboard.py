from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty
from firebase_congfig import db
from firebase_congfig import auth


class cardDetail(Screen):
    user = ObjectProperty(None)
    user_info = ObjectProperty(None)


    def perform_insert(self):
        user_data=db.child("users").child(self.user.uid).get().val()
        display_name=user_data["display_name"]
        email=user_data['email']
        print(display_name)
        print(email)


class Dash(MDApp):
    def build(self):
        return cardDetail()

if __name__=="__main__":
    Window.size=(360,640)
    Dash().run()
