
import sys
import json
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from docx import Document
from zhipuai.core._jwt_token import generate_token  # type: ignore
import pandas as pd
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
# 设置全局字体
font = QFont('Arial', 12)
class ZhipuAILLM:
    def __init__(self, api_key, model="glm-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        
    def clean_response(self, response):
        cleaned_response = response.replace("#", "*").strip()
        cleaned_response = "\n".join(line for line in cleaned_response.splitlines() if line.strip())
        return cleaned_response

    def analyze_document(self, document_content):
        prompt = (
        "请根据提供的数据进行分析并给出相应的建议：\n"
        "1. 如果提供的是血糖数据，请根据指标值分析具体的身体状况，并给出适当的饮食、休息、用药等方面的建议。\n"
        "2. 如果提供的是用药数据，请统计用药情况，给出下一个疗程的建议，并提醒需要注意的事项。\n"
        "3. 如果提供的是饮食数据，请分析饮食情况，给出改善饮食的建议，以帮助控制血糖。\n"
        "请在300字以内回答以下问题：{document_content}"
    ).format(document_content=document_content)
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        token = generate_token(self.api_key)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()
        raw_res = json.loads(response.text)["choices"][0]["message"]["content"]
        return self.clean_response(raw_res)

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("糖尿病智能医疗助手")
        self.resize(500, 400)
        self.setupUI()

    def setupUI(self):
        # 设置主窗口的标题和大小
        main_layout = QVBoxLayout()

        # 设置背景色和字体
        self.setAutoFillBackground(True)
        palette = self.palette()
        background_color = QColor(236, 240, 241, 200)  # 与SmartRecipeBook相同的背景色
        palette.setColor(QPalette.ColorRole.Window, background_color)
        self.setPalette(palette)

        # 字体颜色
        text_color = QColor(44, 62, 80)  # 深色字体
        self.setStyleSheet(f"* {{ color: rgb({text_color.red()}, {text_color.green()}, {text_color.blue()}); }}")


        self.overall_button = QPushButton("综合评价", self)
        self.overall_button.clicked.connect(lambda: self.on_button_click('overall'))
        self.overall_button.setStyleSheet("""
            QPushButton {
                background-color: #5d1370;
                color: white;
                border: 1px solid #5d1370;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #7d3c98;  /* 修改为方案1的悬停颜色 */
            }
            QPushButton:pressed {
                background-color: #4a1057;  /* 修改为方案1的按下颜色 */
            }
        """)
        main_layout.addWidget(self.overall_button)

        buttons_layout = QHBoxLayout()
        self.body_button = QPushButton("身体", self)
        self.body_button.clicked.connect(lambda: self.on_button_click('body'))
        self.body_button.setStyleSheet("""
            QPushButton {
                background-color: #5d1370;
                color: white;
                border: 1px solid #5d1370;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #7d3c98;  /* 修改为方案1的悬停颜色 */
            }
            QPushButton:pressed {
                background-color: #4a1057;  /* 修改为方案1的按下颜色 */
            }
        """)
        buttons_layout.addWidget(self.body_button)

        self.drug_button = QPushButton("药品", self)
        self.drug_button.clicked.connect(lambda: self.on_button_click('drug'))
        self.drug_button.setStyleSheet("""
            QPushButton {
                background-color: #5d1370;
                color: white;
                border: 1px solid #5d1370;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #7d3c98;  /* 修改为方案1的悬停颜色 */
            }
            QPushButton:pressed {
                background-color: #4a1057;  /* 修改为方案1的按下颜色 */
            }
        """)
        buttons_layout.addWidget(self.drug_button)

        self.food_button = QPushButton("食物", self)
        self.food_button.clicked.connect(lambda: self.on_button_click('food'))
        self.food_button.setStyleSheet("""
            QPushButton {
                background-color: #5d1370;
                color: white;
                border: 1px solid #5d1370;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #7d3c98;  /* 修改为方案1的悬停颜色 */
            }
            QPushButton:pressed {
                background-color: #4a1057;  /* 修改为方案1的按下颜色 */
            }
        """)
        buttons_layout.addWidget(self.food_button)

        main_layout.addLayout(buttons_layout)

        self.answer_label = QLabel("分析结果将在这里显示", self)
        self.answer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 水平居中
        self.answer_label.setWordWrap(True)
        main_layout.addWidget(self.answer_label)

        self.setLayout(main_layout)
        
    def on_button_click(self, category):
        file_paths = {
            'body': "./data/comprehensive_health_data.xlsx",  # 替换为血糖文件的实际路径
            'drug': "./data/糖尿病用药记录.docx",  # 替换为药品文件的实际路径
            'food': './data/糖尿病饮食记录.docx',  # 替换为饮食文件的实际路径
        }

        if category == 'overall':
            contents = []
            for key in file_paths:
                if key == 'body':
                    contents.append(self.read_excel(file_paths[key]))
                else:
                    contents.append(self.read_docx(file_paths[key]))
            document_content = ' '.join(contents)  # 合并所有文档的内容
        elif category == 'body':
            document_content = self.read_excel(file_paths[category])
        else:
            document_content = self.read_docx(file_paths[category])

        try:
            response = llm.analyze_document(document_content)
            self.answer_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 左对齐
            self.answer_label.setText(response)
        except Exception as e:
            self.answer_label.setText(str(e))


    def read_docx(self, file_path):
        doc = Document(file_path)
        return ' '.join([paragraph.text for paragraph in doc.paragraphs])
    def read_excel(self, file_path):
        df = pd.read_excel(file_path)
        return df.to_string(index=False)


# Initialize the API key and LLM instance
# 读取配置文件
with open('config.json') as config_file:
    config = json.load(config_file)

# 获取 API 密钥
api_key = config['api_key']
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