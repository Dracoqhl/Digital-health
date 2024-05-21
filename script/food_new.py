import sys
import random
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLineEdit, QDialog, QDialogButtonBox, QLabel)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt

class SmartRecipeBook(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主布局
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # 字体设置
        self.setFont(QFont('Arial', 12))

        # 设置背景颜色和透明度
        self.setAutoFillBackground(True)
        p = self.palette()
        background_color = QColor(236, 240, 241, 200)  # RGB: #ecf0f1, Alpha: 200
        p.setColor(self.backgroundRole(), background_color)
        self.setPalette(p)

        # 调整字体颜色
        text_color = QColor(44, 62, 80)  # 深色字体
        self.setStyleSheet(f"* {{ color: rgb({text_color.red()}, {text_color.green()}, {text_color.blue()}); }}")

        # 食谱数据
        self.recipes = {
            '早餐': ['燕麦片、蔬菜鸡蛋卷、全麦面包', '低脂牛奶、全麦面包、猕猴桃', '杂粮粥、水煮蛋、西柚', '豆浆、番茄三明治', '燕麦片、烤鸡胸肉、草莓'],
            '午餐': ['荞麦面、蔬菜沙拉、黄瓜', '海鲜意面、蔬菜沙拉、苦瓜', '低脂牛肉、蔬菜汤、洋葱', '三文鱼、花椰菜、黄瓜', '烤鱼、青菜汤、黄瓜'],
            '晚餐': ['全麦杂粮粥、烤鲑鱼、坚果', '燕麦片、素食寿司卷', '低脂牛奶、白灼鱼片', '低脂牛奶、豆腐、橘子', '全麦杂粮粥、水煮蛋、石榴']
        }

        # 创建食谱选择布局
        self.recipe_layouts = {}
        for meal in ['早餐', '午餐', '晚餐']:
            panel = QVBoxLayout()  # 改为垂直布局
            label = QPushButton(f"{meal}: 未选择")  # 按钮显示选择的食谱
            label.clicked.connect(lambda _, m=meal: self.show_recipe_dialog(m))
            # 调整按钮样式
            label.setStyleSheet("""
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
            panel.addWidget(label)
            self.layout.addLayout(panel)
            self.recipe_layouts[meal] = label

    def show_recipe_dialog(self, meal):
        # 创建对话框
        dialog = QDialog(self)
        dialog.setWindowTitle(f"选择 {meal}")

        # 垂直布局
        layout = QVBoxLayout(dialog)

        # 说明文字
        label = QLabel(f"今天您的 {meal} 智能食谱推荐为：")
        layout.addWidget(label)

        # 随机选择三个食谱
        recipes = random.sample(self.recipes[meal], 3)
        for recipe in recipes:
            btn = QPushButton(recipe)
            btn.clicked.connect(lambda _, r=recipe, m=meal: self.set_meal_recipe(r, m))
            # 调整按钮样式
            btn.setStyleSheet("""
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
            layout.addWidget(btn)

        # 自定义输入
        custom_input = QLineEdit()
        custom_input.setPlaceholderText("在此自定义")
        custom_input.setMinimumWidth(200)  # 增加输入框长度
        layout.addWidget(custom_input)

        # 使用 Ok 和 Cancel 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(lambda: self.set_meal_recipe(custom_input.text(), meal))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()

    def set_meal_recipe(self, recipe, meal):
        # 更新对应栏目的食谱
        if recipe.strip():
            self.recipe_layouts[meal].setText(f"{meal}: {recipe}")
        
        # 关闭当前弹窗
        self.sender().parent().close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SmartRecipeBook()
    ex.show()
    sys.exit(app.exec())
