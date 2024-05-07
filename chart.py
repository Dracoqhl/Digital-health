import sys
from PyQt6.QtWidgets import QGridLayout,QLabel,QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit
# from PyQt6.QtCharts import QChart, QChartView, QLineSeries
from PyQt6.QtGui import QPainter
from pyqtgraph import PlotWidget
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt
import numpy as np

# 自定义按钮样式
button_style = """
QPushButton {
    border-radius: 10px; /* 设置圆角，值越高越圆 */
    background-color: #1a73e8; /* 设置背景颜色 */
    border: none; /* 无边框 */
    padding: 5px; /* 内边距 */
    color: white; /* 文字颜色 */
    font-size: 10px; /* 字体大小 */
}

QPushButton:hover {
    background-color: #5a8dee; /* 鼠标悬停时的背景颜色 */
}

QPushButton:pressed {
    background-color: #145cc2; /* 按钮按下时的背景颜色 */
}
"""

class ChartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个折线图系列
        self.layout = QGridLayout(self)  # 使用self作为布局的父组件

        label = QLabel("Section 1 Content")
        self.layout.addWidget(label, 0, 0, 1, 1)

        # 创建PlotWidget
        self.plot_widget = PlotWidget()
        self.layout.addWidget(self.plot_widget, 1, 0, 10, 10)

        # 设置背景颜色为白色
        self.plot_widget.setBackground((255, 255, 255))
        # 初始化曲线数据
        self.x = np.arange(24)
        self.y = np.random.randint(80, 120, size=24)
        self.pen = QPen(QColor(35, 119, 250), 0.1, style=Qt.PenStyle.SolidLine)
        self.curve = self.plot_widget.plot(pen=self.pen)  # 获取折线对象

        # 绘制曲线图
        self.plot_widget.setLabel('left', '血糖 (mg/dL)')
        self.plot_widget.setLabel('bottom', '小时(hour)')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.5)
        self.curve.setData(self.x, self.y)
        self.plot_widget.setXRange(min(self.x), max(self.x))
        self.plot_widget.setYRange(min(self.y), max(self.y))
  

        # # 将图表视图添加到布局中
        # self.layout.addWidget(self.plot_widget)

        # 创建刷新数据按钮，并设置样式
        self.refresh_button = QPushButton("刷新数据")
        self.refresh_button.clicked.connect(self.refresh_data)
        self.refresh_button.setStyleSheet(button_style)
        self.layout.addWidget(self.refresh_button, 12, 4, 1, 1)

        # 设置窗口的布局
        self.setLayout(self.layout)

    def refresh_data(self):
        # 更新曲线数据
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
