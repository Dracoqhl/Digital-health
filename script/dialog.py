import sys
from PyQt6.QtWidgets import QGridLayout,QLabel,QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit
# from PyQt6.QtCharts import QChart, QChartView, QLineSeries
from PyQt6.QtGui import QPainter
from pyqtgraph import PlotWidget
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt
import numpy as np

class DialogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 创建一个文本输入框
        self.line_edit = QLineEdit(self)

        # 创建一个按钮
        button = QPushButton('确认', self)
        button.clicked.connect(self.on_confirm)

        # 将文本输入框和按钮添加到布局中
        layout.addWidget(self.line_edit)
        layout.addWidget(button) 

        # 设置窗口的布局
        self.setLayout(layout)

    def on_confirm(self):
        # 当按钮被点击时，获取输入框的内容并处理
        text = self.line_edit.text()
        print(f'用户输入: {text}')
        # 这里可以添加处理输入的逻辑