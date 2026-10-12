from PyQt6.QtWidgets import QWidget, QSplitter, QVBoxLayout
from PyQt6.QtCore import Qt

from ui.left_panel import LeftPanel
from ui.right_panel import RightPanel
from data.fake_data import get_today_lessons, get_tomorrow_lessons


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.left = LeftPanel()
        self.right = RightPanel()

        splitter.addWidget(self.left)
        splitter.addWidget(self.right)
        splitter.setSizes([260, 840])
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

        self.left.signal_nav.connect(self.on_nav)

        self.right.show_schedule("СЕГОДНЯ", get_today_lessons())

    def on_nav(self, key: str):
        if key == "today":
            self.right.show_schedule("СЕГОДНЯ", get_today_lessons())
        elif key == "tomorrow":
            self.right.show_schedule("ЗАВТРА", get_tomorrow_lessons())
        elif key == "week":
            self.right.show_placeholder("НЕДЕЛЯ — скоро")
        elif key == "classroom":
            self.right.show_placeholder("CLASSROOM — скоро")
        elif key == "tasks":
            self.right.show_placeholder("ЗАДАНИЯ — скоро")
        elif key == "notes":
            self.right.show_notes()
        elif key == "cdev":
            self.right.show_c_editor()
        elif key == "deepseek":
            self.right.show_deepseek()
        elif key == "meet":
            self.right.show_meet()
