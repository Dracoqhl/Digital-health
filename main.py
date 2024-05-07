import sys
from PyQt6.QtWidgets import QGridLayout,QLabel,QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit
# from PyQt6.QtCharts import QChart, QChartView, QLineSeries
from PyQt6.QtGui import QPainter
from pyqtgraph import PlotWidget
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt
import numpy as np
from chart import ChartWindow
from dialog import DialogWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置主窗口的标题和大小
        self.setWindowTitle('PyQt6 示例')
        self.setGeometry(100, 100, 800, 600)

        # 创建一个垂直布局作为中心窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个布局
        self.layout = QGridLayout(self)  # 使用self作为布局的父组件

        # 创建对话框窗口和图表窗口的实例
        self.dialog_window = DialogWindow()
        self.chart_window = ChartWindow()

        # 将对话框窗口和图表窗口添加到布局中
        self.layout.addWidget(self.dialog_window,0,0,1,1)
        self.layout.addWidget(self.chart_window,0,1,1,1)

        # 设置中心窗口的布局
        central_widget.setLayout(self.layout)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
