import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt6.QtGui import QPen, QColor, QFont
from PyQt6.QtCore import Qt
import numpy as np
import pyqtgraph as pg
import pandas as pd

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
# 时间  血糖值  收缩压  舒张压  心率    体温
# 标签映射字典
data_dic = {'0':'血糖值',
            '1':'收缩压',
            '2':'舒张压',
            '3':'心率',
            '4':'体温'}

class ChartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadData()

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
        self.current_index = 0
        self.pen=pg.mkPen(color=(68, 102, 242), width=4)
        self.curve = self.plot_widget.plot(pen=self.pen)

        # 绘制曲线图
        # 绘制初始曲线图
        self.plot_widget.setLabel('left', '值', color='#2c3e50', font=font)
        self.plot_widget.setLabel('bottom', '时间', color='#2c3e50', font=font)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)

        # 绘制下一个数据，并设置样式
        self.refresh_button = QPushButton("下一数据")
        self.refresh_button.clicked.connect(self.refresh_data)
        self.refresh_button.setFont(font)
        self.refresh_button.setStyleSheet("background-color: #3498db; color: white;")
        self.layout.addWidget(self.refresh_button, 12, 5, 1, 1)

        self.setLayout(self.layout)

    def loadData(self):
        # 从Excel文件加载数据
        self.data = pd.read_excel('comprehensive_health_data.xlsx')
        print(self.data['时间'].values)
        print(self.data[data_dic[str(self.current_index)]].values)
        self.columns = self.data.columns[1:]  # 第一列是时间，后面的列是生理指标
        self.time_str = self.data['时间'].values
        self.time = np.array([int(t.split(':')[0]) + int(t.split(':')[1])/60.0 for t in self.time_str])
        
        self.current_index = 0
        self.update_plot()

    def update_plot(self):
        self.y = self.data[data_dic[str(self.current_index)]].values
        self.plot_widget.setLabel('left', self.columns[self.current_index], color='#2c3e50', font=font)
        self.curve.setData(self.time, self.y)
        self.plot_widget.setXRange(min(self.time), max(self.time))
        self.plot_widget.setYRange(min(self.y), max(self.y))

    def refresh_data(self):
        # 更新当前显示的生理指标
        self.current_index = (self.current_index + 1) % len(self.columns)
        self.update_plot()


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
    # print(data_dic[str(0)])
