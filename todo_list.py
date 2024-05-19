import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QCheckBox, QDateTimeEdit, QHBoxLayout, QLabel
from PyQt6.QtCore import QDateTime
from PyQt6.QtGui import QFont, QPalette, QColor

class TodoList(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)  # 创建布局并应用到当前窗体
        self.layout.setSpacing(10)  # 设置组件间距

        # 设置背景色和字体
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('white'))
        self.setPalette(palette)
        self.setFont(QFont('Arial', 10))  # 设置字体以支持中文

        # 任务输入区域
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("输入新任务")
        self.add_button = QPushButton("添加任务", self)
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.task_input)
        self.layout.addWidget(self.add_button)

        # 初始化几个基本任务
        self.add_predefined_task("药物A：两片")
        self.add_predefined_task("药物B：200ml开水冲服")
        self.add_predefined_task("药物C：睡前半粒")

        # 在底部添加伸缩项
        self.layout.addStretch(1)

    def add_task(self):
        task_name = self.task_input.text()
        if task_name:
            self.add_predefined_task(task_name)
            self.task_input.clear()  # 清空输入框

    def add_predefined_task(self, task_name):
        task_widget = QWidget()
        task_layout = QHBoxLayout(task_widget)
        cb = QCheckBox(task_name)
        reminder_time = QDateTimeEdit(QDateTime.currentDateTime())
        reminder_time.setCalendarPopup(True)
        task_layout.addWidget(cb)
        task_layout.addWidget(reminder_time)
        self.layout.insertWidget(self.layout.count() - 1, task_widget)  # 插入新任务至倒数第二个位置，保持伸缩项在最下方

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.setWindowTitle("Todo List Example")
    main_layout = QVBoxLayout(main_window)
    todo_list = TodoList()
    main_layout.addWidget(todo_list)
    main_window.show()
    sys.exit(app.exec())