import sys
import requests
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Enter your message:")
        self.layout.addWidget(self.label)

        self.input = QLineEdit()
        self.layout.addWidget(self.input)

        self.button = QPushButton("Send")
        self.button.clicked.connect(self.send_message)
        self.layout.addWidget(self.button)

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def send_message(self):
        message = self.input.text()
        response = requests.get(f"http://127.0.0.1:8000/message/{message}")
        data = response.json()
        self.result_label.setText(f"Server response at {data['timestamp']}:\n{data['message']}\nConfig:\n{data['config']}")

def main():

    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
