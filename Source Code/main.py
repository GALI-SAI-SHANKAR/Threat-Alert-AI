from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.toast import toast

import librosa
import speech_recognition as sr
import pyttsx3
import requests
import numpy as np
import tensorflow as tf

Window.size = (350, 600)

KV = """
#:import hex kivy.utils.get_color_from_hex

ScreenManager:
    MDScreen:
        name: "login"
        MDFloatLayout:
            Image:     # This part doesn't seem to work
                source: "Threat Alert-logos.jpeg"
                allow_stretch: True
                keep_ratio: False
                size_hint: 1, 1
            MDRaisedButton:
                text: "Login with Google"
                pos_hint: {"center_x": .5,"center_y": .2}
                on_release: app.login()

    MDScreen:
        name: "home"
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
                    badge_icon: "numeric-10"

                    AsyncImage
                        source: 'https://media3.giphy.com/media/gjaM79X86H0VYJ3cpu/giphy.gif'
                        size: self.texture_size
                        
                    MDLabel:
                        id: threat
                        text:''
                        theme_text_color: "Secondary"
                        pos_hint: {"center_x": .5,"center_y": .2}

               #MDBottomNavigationItem:
                   #name: 'sos'
                   #text: 'SOS'
                   #icon: 'account-alert'
                   #badge_icon: "face-man-profile"

                   #MDLabel:
                       #text: 'SOS'
                       #halign: 'center'

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
                            id : profile_icon
                            source: ''
                            size: self.texture_size
                        MDLabel:
                            id: name
                            text: ""
                            theme_text_color: "Secondary"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            id: email
                            text: ""
                            theme_text_color: "Secondary"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDSeparator:
                            height: "10dp"

                        MDRaisedButton:
                            text: "Logout"
                            pos_hint: {"center_x": .5,"center_y": .2}
                            on_release: app.logout()
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
                SER = self.SER('audio_file.wav')
                print(SER)
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

        model = tf.keras.models.load_model('./Speech Emotion Dection\models')
        p = model.predict(MFCCs, verbose=0)
        yhat_classes = np.argmax(p, 1)
        output = emotions.get(str(yhat_classes[0]))
        if output == 'fear':
            return 'Threat'
        else:
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


class ThreatAlertApp(MDApp):
    def build(self):
        client_id = "1009296076055-tb7fo1faftjulb5ep8k7ghnnnih60h0e.apps.googleusercontent.com"
        client_secret = "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"
        initialize_google(self.after_login, self.error_listener, client_id, client_secret)
        return Builder.load_string(KV)

    def after_login(self, name, email, photo_url):
        self.root.ids.profile_icon.source = f"{photo_url}"
        self.root.ids.name.text = f"Name : {name}"
        self.root.ids.email.text = f"Email : {email}"
        self.root.transition.direction = "left"
        self.root.current = "home"

        if self.root.current == 'home':
            self.threat()

    def threat(self):
        obj = ThreatAlert()
        while True:
            voice_data = obj.record_audio
            print('listening...')
            print(voice_data)
            if obj.Threat(voice_data):
                self.root.ids.threat.text = f"Threat Alert AI sending alert to police"
                toast('Threat Alert AI sending alert to police')

    def error_listener(self):
        print("Login Failed")

    def login(self):
        login_google()

    def logout(self):
        logout_google(self.after_logout)

    def after_logout(self):
        self.root.ids.name.text = ""
        self.root.transition.direction = "right"
        self.root.current = "login"


if __name__ == '__main__':
    ThreatAlertApp().run()
