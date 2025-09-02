from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import json
import os
from datetime import datetime

Builder.load_file("design.kv")

USERS_FILE = "./users.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)


class LoginScreen(Screen):
    error_message = StringProperty("")

    def login(self, username, password):
        with open(USERS_FILE) as file:
            users = json.load(file)

        if username in users and users[username]["password"] == password:
            self.error_message = ""
            self.manager.get_screen("login_screen_success").current_user = username
            self.manager.current = "login_screen_success"
        else:
            self.error_message = "Credenciales incorrectas. Intenta de nuevo."

    def forgot_password(self):
        popup = Popup(
            title="Forgot Password",
            content=Label(text="Pues ya ni modo"),
            size_hint=(0.6, 0.4),
        )
        popup.open()


class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    error_message = StringProperty("")

    def add_user(self, username, password):
        if not username or not password:
            self.error_message = "Ingresa usuario y contraseña."
            return

        with open(USERS_FILE) as file:
            users = json.load(file)

        if username in users:
            self.error_message = "El usuario ya existe."
            return

        users[username] = {
            "username": username,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "feelings": [],
        }

        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=4)

        self.error_message = ""
        self.manager.current = "sign_up_success"


class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    current_user = None

    def on_pre_enter(self):
        self.load_feelings()

    def logout(self):
        self.manager.transition.direction = "up"
        self.manager.current = "login_screen"

    def submit_feelings(self, feeling):
        if not feeling.strip():
            return

        with open(USERS_FILE) as file:
            users = json.load(file)

        users[self.current_user]["feelings"].append(
            {
                "text": feeling,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=4)

        self.ids.feelings.text = ""
        self.load_feelings()

    def load_feelings(self):
        self.ids.feelings_list.clear_widgets()

        with open(USERS_FILE) as file:
            users = json.load(file)

        feelings = users[self.current_user].get("feelings", [])
        for f in reversed(feelings):
            from kivy.uix.label import Label

            self.ids.feelings_list.add_widget(
                Label(
                    text=f"[{f['timestamp']}] {f['text']}",
                    size_hint_y=None,
                    height=40,
                    halign="left",
                    valign="middle",
                    text_size=(self.width - 50, None),
                )
            )


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
