import sys
import requests

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from requests import RequestException
from urllib3.exceptions import HTTPError


class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Введите город:", self)
        self.city_enter = QLineEdit(self)
        self.get_weather_button = QPushButton("Прогноз", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel( self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Прогноз Погоды")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_enter)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_enter.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_enter.setObjectName("city_enter")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Arial;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLabel#city_enter{
                font-size: 40px;
            }
            QLineEdit#city_enter{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji
            }
            QLabel#description_label{
                font-size: 40px;
            }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "adf963a54d8246a2cae6629a37965209"
        city = self.city_enter.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_erorr("Bad request:\nПожалуйста проверьте ваш запрос")
                case 401:
                    self.display_erorr("Unauthorized:\nНеверный API ключ")
                case 403:
                    self.display_erorr("Forbidden:\nДоступ запрещён")
                case 404:
                    self.display_erorr("Not found:\nГород не найден")
                case 500:
                    self.display_erorr("Internal Server:\nПожалуйста попробуйте позже")
                case 502:
                    self.display_erorr("Bad Gateway:\nНеверный ответ от сервера")
                case 503:
                    self.display_erorr("Service Unavailable:\nСервер не отвечает")
                case 504:
                    self.display_erorr("Geteway Timeout:\nнет ответа от сервере")
                case _:
                    self.display_erorr(f"HTTP error occored\n{http_error}")


        except requests.exceptions.ConnectionError:
            self.display_erorr("Connection Error:\nПроверьите ваше подключсение к сети")
        except requests.exceptions.Timeout:
            self.display_erorr("Timeout Error:\nThe request timed out ")
        except requests.exceptions.TooManyRedirects:
            self.display_erorr("Too Many Redirects:\nПроверьте ваш URL")
        except requests.exceptions.RequestException  as req_error:
            self.display_erorr(f"Request Error:\n{req_error}")


    def display_erorr(self, message):
        self.temperature_label.setText(message)
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.0f}C")
        self.emoji_label.setText(self.get_weather_emogi(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emogi(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌧️"
        elif 500 <= weather_id <= 531:
            return "☔"
        elif 600 <= weather_id <= 622:
            return "❄︎"
        elif 700 <= weather_id <= 741:
            return "༄.°"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁︎"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    whiter_app = WeatherApp()
    whiter_app.show()
    sys.exit(app.exec_())