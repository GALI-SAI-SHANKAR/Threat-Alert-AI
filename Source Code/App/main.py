from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

import librosa
import speech_recognition as sr
import pyttsx3
import requests
import numpy as np
import tensorflow as tf
import smtplib
from email.message import EmailMessage

from kivymd.uix.dialog import MDDialog

Window.size = (350, 600)

KV = """

ScreenManager:
    BaseScreen:
    LoginScreen:
    HomeScreen:

<BaseScreen>:
    name: 'base'
    MDFloatLayout:
        Image:     # This part doesn't seem to work
            source: "../Threat Alert-logos.jpeg"
            allow_stretch: True
            keep_ratio: False
            size_hint: 1, 1
        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": .5,"center_y": .2}
            on_release: 
                root.manager.current = 'login'
                
<LoginScreen>:
    name: 'login'
    MDCard:
        size_hint: None, None
        size: 300, 400
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 25
        spacing: 25
        orientation: 'vertical'
        
        MDLabel:
            id: welcome_label
            text: "Threat Alert AI"
            font_size: 40
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 5

        MDTextFieldRound:
            id: user
            hint_text: "Name"
            icon_right: "account"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5}

        MDTextFieldRound:
            id: phone
            hint_text: "Phone Number"
            icon_right: "card-account-phone"
            size_hint_x: None
            max_text_length: 10
            width: 200
            font_size: 18
            pos_hint: {"center_x": 0.5}

        MDRoundFlatButton:
            text: "LOG IN"
            font_size: 12
            pos_hint: {"center_x": 0.5}
            on_press: 
                root.manager.current = 'home'
                app.after_login()
        
        Widget:
            size_hint_y: None
            height: 10


    
<HomeScreen>:
    name: 'home'
    MDBoxLayout:
        orientation:'vertical'
        
        MDToolbar:
            title: 'Threat Alert'
            md_bg_color: .2, .2, .2, 1
            specific_text_color: 1, 1, 1, 1

        MDBottomNavigation:
            MDBottomNavigationItem:
                name: 'home'
                text: 'Home'
                icon: 'home'
                
                Button:
                    text: "MIC"
                    font_size: 12
                    pos_hint: {"center_x": .5, "center_y": .5}
                    size: 200, 200
                    size_hint: None, None
                    background_color: (0, 0, 0, 0)
                    on_release:
                        app.threat()

                    AsyncImage:
                        source: 'https://media3.giphy.com/media/gjaM79X86H0VYJ3cpu/giphy.gif'
                        size: 200, 200
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y

            MDBottomNavigationItem:
                name: 'profile'
                text: 'Profile'
                icon: 'account-circle'
                md_bg_color:0, 0, 0, 0

                MDCard:
                    orientation: "vertical"
                    padding: "8dp"
                    size_hint: None, None
                    size: "280dp", "250dp"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    AsyncImage:
                        # id : profile_icon
                        source: 'https://static.vecteezy.com/system/resources/thumbnails/006/898/692/small_2x/avatar-face-icon-female-social-profile-of-business-woman-woman-portrait-support-service-call-center-illustration-free-vector.jpg'
                        size: self.texture_size
                    MDLabel:
                        id: name
                        text: "Name : Aadhya"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        id: phone_number
                        text: "Phone Number : 9848142207"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:
                        height: "10dp"

                    MDRaisedButton:
                        text: "Logout"
                        pos_hint: {"center_x": .5,"center_y": .2}
                        on_release: 
                            root.manager.current = 'base' 
                            app.logout()
"""


class ThreatAlert:

    @property
    def record_audio(self):
        # Recognizer
        r = sr.Recognizer()
        # speech recognition using Microphone
        with sr.Microphone(device_index=1) as source:
            # Noise cancellation
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            audio_data = ''
            try:
                # speech to text
                audio_data = r.recognize_google(audio)
                with open("audio_file.wav", "wb") as file:
                    file.write(audio.get_wav_data())
            except sr.UnknownValueError:
                print('Sorry, I did not get that')
            except sr.RequestError:
                print('Sorry, my speech service is down')
            return audio_data

    def MFCCs(self, audio):
        data, sampling_rate = librosa.load(audio)
        X = []
        mfcc_feature = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        X.append(mfcc_feature)
        MFCCs = np.array(X)
        return MFCCs

    def SER(self, audio):
        MFCCs = self.MFCCs(audio)
        emotions = {
            '0': 'angry',
            '1': 'disgust',
            '2': 'fear',
            '3': 'happy',
            '4': 'neutral',
            '5': 'sad'
        }

        model = tf.keras.models.load_model('../Speech Emotion Dection\models')
        p = model.predict(MFCCs, verbose=0)
        yhat_classes = np.argmax(p, 1)
        output = emotions.get(str(yhat_classes[0]))

        return output

    def location(self):
        # r = requests.get('https://get.geojs.io/')

        ip_request = requests.get('https://get.geojs.io/v1/ip.json')
        ip_address = ip_request.json()['ip']
        # print(ip_address)

        url = 'https://get.geojs.io/v1/ip/geo/' + ip_address + '.json'
        geo_request = requests.get(url)
        geo_location = geo_request.json()
        print(geo_location)

        Longitude = geo_location['longitude']
        Latitude = geo_location['latitude']
        Organization = geo_location['organization_name']
        City = geo_location['city']
        Region = geo_location['region']
        Country = geo_location['country']

        print('Longitude : ', Longitude)
        print('Latitude : ', Latitude)
        print('Network Provider : ', Organization)
        print('City : ', City)
        print('Region : ', Region)
        print('Country : ', Country)

        Name = 'Aadhya'
        Phone_Number = '9848142207'

        msg_body = 'Name : '+Name+'\nPhone Number : '+Phone_Number+'\nLongitude : ' + str(Longitude) + '\nLatitude : ' + str(Latitude) + '\nNetwork Provider : ' + str(
            Organization) + '\nCity : ' + str(City) + '\nCountry : ' + str(Country)

        def email_alert(subject, body, to):
            msg = EmailMessage()
            msg.set_content(body)
            msg['subject'] = subject
            msg['to'] = to

            user = "gss.threatalertai@gmail.com"
            msg['from'] = user
            password = "eibohhlapcfhoxog"

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
            server.quit()

        email_alert("Threat", msg_body, "2010030054@klh.edu.in")

    def Alert(self):
        # Text to Speech
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        engine.say('Threat Alert AI sending alert to police')
        engine.runAndWait()
        self.location()

    def Threat(self, Voice_data):
        Voice_data = Voice_data.lower()
        if 'help' in Voice_data:
            self.Alert()
            return True
        elif 'bachao' in Voice_data:
            self.Alert()
            return True
        elif 'raksha in chandi' in Voice_data:
            self.Alert()
            return True


class BaseScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(BaseScreen(name='base'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(HomeScreen(name='home'))


class ThreatAlertApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def after_login(self):
        sm.current = 'home'
        print(sm.current)

    def threat(self):
        obj = ThreatAlert()
        flag = True
        if sm.current == 'home':
            while flag:
                print('Listening...')
                # self.alert_dialog('Listening...')
                voice_data = obj.record_audio
                print(voice_data)
                SER = obj.SER('audio_file.wav')
                print(SER)
                if SER == 'fear' or SER == 'sad':
                    if obj.Threat(voice_data):
                        self.alert_dialog('Threat Alert AI sending alert to police')
                        flag = False

    def alert_dialog(self, text):
        dialog = MDDialog(title='Alert', text=text, size=(0.7, 1))
        dialog.open()
        return dialog.open()

    def logout(self):
        sm.current_screen = 'base'


if __name__ == '__main__':
    ThreatAlertApp().run()
