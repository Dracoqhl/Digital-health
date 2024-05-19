import sys
import random
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QMessageBox, QLineEdit, QDialog, QDialogButtonBox, QLabel)
from PyQt6.QtGui import QFont

class SmartRecipeBook(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主布局
        self.layout = QVBoxLayout(self)

        # 字体设置
        self.setFont(QFont('Arial', 12))

        # 食谱数据
        self.recipes = {
            'Breakfast': ['煎蛋', '牛奶燕麦', '水果沙拉'],
            'Lunch': ['蔬菜汤', '牛肉面', '三明治'],
            'Dinner': ['意面', '寿司', '炒饭']
        }

        # 创建食谱选择布局
        self.recipe_layouts = {}
        for meal in ['Breakfast', 'Lunch', 'Dinner']:
            panel = QVBoxLayout()  # 改为垂直布局
            label = QPushButton(f"{meal}: 未选择")  # 按钮显示选择的食谱
            label.clicked.connect(lambda _, m=meal: self.show_recipe_dialog(m))
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
        label = QLabel(f"选择您的 {meal} 食谱：")
        layout.addWidget(label)

        # 随机选择三个食谱
        recipes = random.sample(self.recipes[meal], 3)
        for recipe in recipes:
            btn = QPushButton(recipe)
            btn.clicked.connect(lambda _, r=recipe, m=meal: self.set_meal_recipe(r, m))
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