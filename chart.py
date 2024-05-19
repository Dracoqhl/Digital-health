import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt6.QtGui import QPen, QColor, QFont
from PyQt6.QtCore import Qt
import numpy as np
import pyqtgraph as pg

# 自定义按钮样式
button_style = """
QPushButton {
    border-radius: 10px;
    background-color: #34495e; /* 更深的背景颜色 */
    border: none;
    padding: 10px;
    color: white;
    font-size: 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #5a8dee;
}

QPushButton:pressed {
    background-color: #145cc2;
}
"""

# 设置全局字体
font = QFont('Arial', 12)

class ChartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout(self)

        label = QLabel("血糖监测图表")
        label.setFont(font)
        label.setStyleSheet("color: #2c3e50;")
        self.layout.addWidget(label, 0, 0, 1, 1)

        # 创建PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget, 1, 0, 11, 11)

        # 设置背景颜色和透明度
        background_color = QColor(236, 240, 241, 200)  # RGB: #ecf0f1, Alpha: 200
        self.plot_widget.setBackground(background_color)

        # 设置窗口的背景为透明
        self.setStyleSheet("QWidget { background: transparent; }")

        # 初始化曲线数据
        self.x = np.arange(24)
        self.y = np.random.randint(80, 120, size=24)
        self.pen = QPen(QColor(68, 102, 242), 0.15, style=Qt.PenStyle.SolidLine)  # 更改为深蓝色曲线
        self.curve = self.plot_widget.plot(pen=self.pen)

        # 绘制曲线图
        self.plot_widget.setLabel('left', '血糖 (mg/dL)', color='#2c3e50', font=font)
        self.plot_widget.setLabel('bottom', '小时(hour)', color='#2c3e50', font=font)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.curve.setData(self.x, self.y)
        self.plot_widget.setXRange(min(self.x), max(self.x))
        self.plot_widget.setYRange(min(self.y), max(self.y))

        # 创建刷新数据按钮，并设置样式
        self.refresh_button = QPushButton("刷新数据")
        self.refresh_button.clicked.connect(self.refresh_data)
        self.refresh_button.setFont(font)
        self.refresh_button.setStyleSheet(button_style)
        self.layout.addWidget(self.refresh_button, 12, 5, 1, 1)

        self.setLayout(self.layout)

    def refresh_data(self):
        self.y = np.random.randint(80, 120, size=24)
        self.curve.setData(self.x, self.y)
        self.plot_widget.setXRange(min(self.x), max(self.x))
        self.plot_widget.setYRange(min(self.y), max(self.y))


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置主窗口的标题和大小
        self.setWindowTitle('测试窗口')
        self.setGeometry(100, 100, 800, 600)

        # 创建一个垂直布局作为中心窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 创建对话框窗口和图表窗口的实例
        # self.dialog_window = DialogWindow()
        self.chart_window = ChartWindow()

        # 将对话框窗口和图表窗口添加到布局中
        # layout.addWidget(self.dialog_window)
        layout.addWidget(self.chart_window)

        # 设置中心窗口的布局
        central_widget.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    main_window = TestWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
