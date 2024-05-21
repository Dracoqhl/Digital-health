

import sys
import json
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor, QFont
from zhipuai.core._jwt_token import generate_token  # type: ignore
# 设置全局字体
font = QFont('Arial', 12)
class ZhipuAILLM:
    def __init__(self, api_key, model="glm-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    def generate_response(self, prompt):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        token = generate_token(self.api_key)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return json.loads(response.text)["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Zhipu AI: {str(e)}")

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        # 设置主窗口的标题和大小
        self.setWindowTitle('测试窗口')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        label = QLabel("Zhipu AI Interface")
        label.setFont(font)
        label.setStyleSheet("color: #2c3e50;")
        self.layout.addWidget(label)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("请输入问题...")
        self.layout.addWidget(self.text_edit)

        self.button = QPushButton("获取答案", self)
        self.button.clicked.connect(self.on_click)
        self.layout.addWidget(self.button)

        self.answer_label = QLabel("答案将在这里显示", self)
        self.answer_label.setWordWrap(True)
        self.layout.addWidget(self.answer_label)

        self.setLayout(self.layout)

    def on_click(self):
        question = self.text_edit.toPlainText()
        try:
            response = llm.generate_response(question)
            self.answer_label.setText(response)
        except Exception as e:
            self.answer_label.setText(str(e))
      

# Initialize the API key and LLM instance
api_key = "20d3eb6d7db71a080e8c3185ff8fe1cd.JWDCLpQkwFGbn8Ai"
llm = ZhipuAILLM(api_key)

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置主窗口的标题和大小
        self.setWindowTitle('测试窗口')
        self.resize(500, 400)

        # 设置样式表
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('banner06.jpg');
                background-position: center;
                background-repeat: no-repeat;
            }
            QTextEdit, QLabel, QPushButton {
                background: transparent;
                color: white;
            }
        """)

        # 创建对话框窗口的实例
        self.chat_window = ChatWindow()

        # 设置中心窗口的布局
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.chat_window)
        self.setCentralWidget(central_widget)
  

def main():
    app = QApplication(sys.argv)
    main_window = TestWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()