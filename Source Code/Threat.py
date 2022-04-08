import librosa
import speech_recognition as sr
import pyttsx3
import requests
import numpy as np
import tensorflow as tf


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


obj = ThreatAlert()
while True:
    print('Listening...')
    voice_data = obj.record_audio
    print(voice_data)
    obj.Threat(voice_data)
