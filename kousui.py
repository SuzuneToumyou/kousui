#!/usr/bin/python3
# coding: utf-8

import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('降水確率')
        self.setGeometry(300, 300, 300, 360)

        self.label = QLabel('降水確率を取得中...', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Arial', 24))  # フォントサイズを24に設定

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont('Arial', 24))  # フォントサイズを24に設定

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("大阪")
        self.combo_box.addItem("東京")
        self.combo_box.currentIndexChanged.connect(self.get_precipitation_probability)

        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        self.get_precipitation_probability()

    def get_precipitation_probability(self):
        try:
            location = self.combo_box.currentText()
            if location == "大阪":
                url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json'
            elif location == "東京":
                url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json'

            response = requests.get(url)
            response.raise_for_status()  # エラーレスポンスをチェック

            data = response.json()
            time_series = data[0]['timeSeries'][1]['areas'][0]['pops']

            if time_series:
                forecast = ""
                for time, precip in zip(data[0]['timeSeries'][1]['timeDefines'], time_series):
                    forecast += f"{time[11:16]}: {precip}%\n"
                self.text_edit.setText(forecast)
                self.label.setText(f'{location}の降水確率')
            else:
                self.label.setText('降水確率を取得できませんでした。')

        except requests.exceptions.RequestException as e:
            self.label.setText(f'エラー: {e}')
        except Exception as e:
            self.label.setText(f'予期せぬエラー: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
