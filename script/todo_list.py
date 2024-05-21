import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QCheckBox, QTimeEdit, QHBoxLayout
from PyQt6.QtGui import QFont, QPalette, QColor

class TodoList(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)  # 创建布局并应用到当前窗体
        self.layout.setSpacing(10)  # 设置组件间距

        # 设置背景色和字体
        self.setAutoFillBackground(True)
        palette = self.palette()
        background_color = QColor(236, 240, 241, 200)  # 与SmartRecipeBook相同的背景色
        palette.setColor(QPalette.ColorRole.Window, background_color)
        self.setPalette(palette)
        self.setFont(QFont('Arial', 12))  # 设置字体以支持中文

        # 字体颜色
        text_color = QColor(44, 62, 80)  # 深色字体
        self.setStyleSheet(f"* {{ color: rgb({text_color.red()}, {text_color.green()}, {text_color.blue()}); }}")

        # 任务输入区域
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("输入新任务")
        self.task_input.setStyleSheet(f"color: rgb({text_color.red()}, {text_color.green()}, {text_color.blue()});")

        self.add_button = QPushButton("添加任务", self)
        self.add_button.clicked.connect(self.add_task)
        self.add_button.setStyleSheet("""
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

        # 创建一个新的水平布局，用于任务输入区域
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)

        # 初始化几个基本任务
        self.add_predefined_task("二甲双胍:500mg 随早餐服用一片")
        self.add_predefined_task("格列吡嗪:5mg 午餐前30分钟服用一片")
        self.add_predefined_task("甘精胰岛素:10单位 每天固定时间注射")

        # 在底部添加伸缩项
        self.layout.addStretch(1)
        # 将任务输入区域添加到布局的最后
        self.layout.addLayout(input_layout)

    def add_task(self):
        task_name = self.task_input.text()
        if task_name:
            self.add_predefined_task(task_name)
            self.task_input.clear()  # 清空输入框

    def add_predefined_task(self, task_name):
        task_widget = QWidget()
        task_layout = QHBoxLayout(task_widget)
        cb = QCheckBox(task_name)
        text_color = QColor(44, 62, 80)  # 深色字体
        cb.setStyleSheet(f"color: rgb({text_color.red()}, {text_color.green()}, {text_color.blue()});")

        reminder_time = QTimeEdit()
        reminder_time.setStyleSheet(f"color: rgb({text_color.red()}, {text_color.green()}, {text_color.blue()});")
        reminder_time.setDisplayFormat('HH:mm')  # 只显示小时和分钟

        task_layout.addWidget(cb)
        task_layout.addWidget(reminder_time)
        self.layout.insertWidget(self.layout.count() - 2, task_widget)  # 插入新任务至倒数第二个位置，保持伸缩项在最下方

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.setWindowTitle("Todo List Example")
    main_layout = QVBoxLayout(main_window)
    todo_list = TodoList()
    main_layout.addWidget(todo_list)
    main_window.show()
    sys.exit(app.exec())
