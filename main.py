from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty,StringProperty
from firebase_congfig import db
from firebase_congfig import auth
from cardbank_api import db_cardbank
from kivymd.uix.button import MDFloatingActionButton

class loginWindow(Screen):
    email=ObjectProperty(None)
    pwd=ObjectProperty(None)
    def perform_login(self):
        email=self.email.text
        password=self.pwd.text
        try:
            auth.sign_in_with_email_and_password(email,password)
            self.manager.current="dashboard_screen"
            print("Login Successful")
        except Exception as e:
            print("Login Failed",e)

class dashboardWindow(Screen):
    u_cardnumber = StringProperty()
    u_amount = StringProperty()
    def on_enter(self):
        user = auth.current_user
        if user:
                user_id=user['localId']
                card_info = db.child("users").child(user_id).child("card info").get().val()
                if card_info:
                    print("user card info is:",card_info)
                    self.u_cardnumber=card_info.get('cardnumber')
                    self.u_amount=card_info.get('card_amount')
                else:
                    print("No card info found for the user",user)
        else:
                print("User is not authenticated. Please sign in first.")

    def perform_card(self):
            self.manager.current="card_details"

    def add_bank(self):
        self.manager.current="bank_card"

    def bank_topup(self):
        self.manager.current="bank_trans"


class carddetailWindow(Screen):
    u_cardnumber = ObjectProperty(None)
    u_pinnumber = ObjectProperty(None)

    def card_detail(self):
        card_ref = db_cardbank.child("cardinfo")
        card_info = card_ref.get().val()
        card_amount=card_info.get("amount")
        user_Card = self.u_cardnumber.text
        user_pin = self.u_pinnumber.text
        data_insert = {"cardnumber": user_Card,
                       "pinnumber": user_pin
                       }
        user = auth.current_user

        if user:
            print("current user", user)
            if card_info:
                card_numbers = [str(card['cardnumber']) for card in card_info.values()]
                print(f"card numbers{card_numbers}")
                if user_Card in card_numbers:
                    user_id = user['localId']
                    print(f"User UID: {user_id}")
                    user_data = db.child("users/").child(user_id).child("card info").set(data_insert)
                    print(f"data insert successfully: {user_data}")
                else:
                    print(f"Card number {user_Card} does not exist.")
        else:
            print("User not authenticated")



class bankdetailWindow(Screen):
    u_bankcard=ObjectProperty(None)
    u_expiry= ObjectProperty(None)
    u_cvv=ObjectProperty(None)

    def bank_detail(self):
        bank_ref=db_cardbank.child("db_register")
        bank_info=bank_ref.get().val()
        user_cardnumber,user_expiry,user_cvv=self.u_bankcard.text,self.u_expiry.text,self.u_cvv.text
        user=auth.current_user
        if user:
            if bank_info:
                bank_card_numbers=[]
                bank_expiries=[]
                bank_cvv_values=[]
                for card in bank_info.values():
                    if 'cardnumber' in card and 'expery' in card and 'cvv' in card:
                        bank_card_numbers.append(card['cardnumber'])
                        bank_expiries.append(card['expery'])
                        bank_cvv_values.append(card['cvv'])

                if user_cardnumber in bank_card_numbers:
                    index=bank_card_numbers.index(user_cardnumber)
                    if user_expiry==bank_expiries[index] and user_cvv==bank_cvv_values[index]:
                        user_id=user['localId']
                        user_data=db.child("users").child(user_id).child("bankdetail").set({
                            "cardnumber":user_cardnumber,
                             "expiry":user_expiry,
                             "cvv":user_cvv})
                        print("data insert successfully")
                    else:
                        print("Bank information is incorrect")
                else:
                    print("no bank information is incorrect")
            else:
                print("bank information is not available")
        else:
            print("user is not authenticated")



class banktransactionWindow(Screen):
    u_bankcvv=ObjectProperty(None)
    u_amounts=ObjectProperty(None)
    def bank_trans(self):

        user=auth.current_user
        if user:
            userid=user['localId']
            get_bank_info=db.child("users").child(userid).get().val()
            if get_bank_info:
                u_cardinfo_amount=get_bank_info.get("card info",{}).get("card_amount","")
                print("recent card amount",u_cardinfo_amount)
                u_bank_account=get_bank_info.get("bankdetail",{}).get("cardnumber","")
                bank_cvv=get_bank_info.get("bankdetail",{}).get("cvv","")
                if bank_cvv==self.u_bankcvv.text:
                    card_info=db_cardbank.child("db_register").get()
                    card_info_data = card_info.val()
                    print(card_info_data)
                    if card_info_data:
                        # Initialize variables to store card number and amount
                        card_number = None
                        amount = None

                        for key, info in card_info_data.items():
                            if "cardnumber" in info and "bamount" in info:
                                card_number = info.get("cardnumber")
                                amount = info.get("bamount")
                            if u_bank_account == card_number:
                                newamount=int(amount) - int(self.u_amounts.text)
                                newcardamount = int(u_cardinfo_amount) + int(self.u_amounts.text)
                                db_cardbank.child("db_register").child(key).update({"bamount": newamount})
                                db.child("users").child(userid).child("card info").update({"card_amount":newcardamount})
                                print("Now amount is:",newamount)
                                print("user bank card", u_bank_account)
                                print("database cardnumber ", card_number)
                        else:
                            print("No valid 'cardnumber' and 'amount' fields found in card_info_data")
                    else:
                        print("No card information found in card_info_data")

                        print("BANK ACCOUNT EXIST")

            else:
                print("Users don't exist")



class MainApp(App):
    def build(self):
        screen_manager=ScreenManager()
        screen_manager.add_widget(loginWindow(name="login"))
        screen_manager.add_widget(dashboardWindow(name="dashboard_screen"))
        screen_manager.add_widget(carddetailWindow(name="card_details"))
        screen_manager.add_widget(bankdetailWindow(name="bank_card"))
        screen_manager.add_widget(banktransactionWindow(name="bank_trans"))
        return screen_manager

if __name__ == '__main__':
    Window.size=(360,640)
    MainApp().run()
