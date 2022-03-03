import speech_recognition as sr
import pyttsx3
import requests


class ThreatAlert:
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
            except sr.UnknownValueError:
                print('Sorry, I did not get that')
            except sr.RequestError:
                print('Sorry, my speech service is down')
            return audio_data

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
        elif 'bachao' in Voice_data:
            self.Alert()
        elif 'raksha in chandi' in Voice_data:
            self.Alert()


obj = ThreatAlert()
while True:
    print('Listening...')
    voice_data = obj.record_audio()
    print(voice_data)
    obj.Threat(voice_data)


