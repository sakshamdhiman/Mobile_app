from kivy.app import App
from kivy.lang import Builder                                       #for connecting kivy and py
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
from datetime import datetime as dt
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
"""
Heirarchy in kivy -
1]MainApp(App)
    2]ScreenManager(RootManager)
        3]Screen(LoginScreen)
            4]GridLayout
                etc....
"""

Builder.load_file('design.kv')                                      #loading the kivy file 

class LoginScreen(Screen):                                          #every rule has to be represented by a class in the python file,Inheriting from the Screen object
    def sign_up(self):                                              #inheriting from Screen
        self.manager.current = "signup_screen"                      #connecting to the signup screen

    def login(self,uname ,pword):
        with open(r"APP\\users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:    #authenticating the username and password
            self.manager.current = "login_screen_success"
        else:
            self.ids.authenticate.text = "Incorrect username or Passsword"


class SignupScreen(Screen):                     
    def add_user(self, uname, pword):
        with open(r"APP\\users.json") as data:
            users = json.load(data)
        users[uname] = {'username': uname,'password':pword, 'created':dt.now().strftime("%Y-%m-%d-%H-%M-%S")}

        with open(r"APP\\users.json", 'w') as file:
            json.dump(users,file)                                   #writing the entire json file with old and added data
        print(users)
        self.manager.current = "signup_screen_success"

class SignupScreenSuccess(Screen):
    def login_redirect(self):
        self.manager.transition.direction = "right"                 #for getting the page transition from left to right
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    
    def get_quote(self,emotion):
        emotion = emotion.lower()
        available_emotions = glob.glob(r"APP\\quotes\\*txt")        #getting available files
        available_emotions = [Path(filename).stem for filename in available_emotions]       #stem gives the name of the file without file format and previous address
        if emotion in available_emotions:
            with open(f"App/quotes/{emotion}.txt",encoding =  "utf8") as file:              #opening the file with the emotion name inputed
                quotes = file.readlines()                                                   
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "try another feeling"

class ImageButton( ButtonBehavior, HoverBehavior, Image):           #class that brings the 3 classes in one 
    pass

class RootWidget(ScreenManager):
    pass                                                            #inheriting from ScreenManager class

class MainApp(App):                                                 #inheriting from App
    def build(self):                                                #calling the build function of App
        return RootWidget()                                         #returning the RootWidget() object instance not the class
        
if __name__ == "__main__":
    MainApp().run()                                                 #running an instance of the main app 

# \ => allows you to break 1 big line into multiple lines 
# any big line with any kind of braces can be split into multiple lines 
#making APK on windows or mac is very hard so we use linux ubuntu 
#library used for making apk is buildozer