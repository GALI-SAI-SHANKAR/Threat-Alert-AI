from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window


Window.size = (350, 600)


class ThreatAlertApp(MDApp):
    def build(self):
        client_id = "1009296076055-tb7fo1faftjulb5ep8k7ghnnnih60h0e.apps.googleusercontent.com"
        client_secret = "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"
        initialize_google(self.after_login, self.error_listener, client_id, client_secret)
        return Builder.load_file('main.kv')

    def after_login(self, name, email, photo_url):
        self.root.ids.profile_icon.source = f"{photo_url}"
        self.root.ids.name.text = f"Name : {name}"
        self.root.ids.email.text = f"Email : {email}"
        self.root.transition.direction = "left"
        self.root.current = "home"

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
