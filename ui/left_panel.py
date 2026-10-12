from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QButtonGroup, QLabel
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, QSize
from ui.icons import svg_icon, CALENDAR, NOTE, BOT, CODE, BOOK, VIDEO
from ui.theme import Theme


def make_icon(svg: str, color: str = None) -> QIcon:
    color = color or Theme.LEFT_TEXT
    return QIcon(svg_icon(svg, color, 18))


class SectionLabel(QLabel):
    def __init__(self, icon_svg: str, text: str):
        super().__init__()
        pixmap = svg_icon(icon_svg, Theme.LEFT_ACCENT, 14)
        self.setPixmap(pixmap)
        self.setText(f"  {text.upper()}")
        self.setStyleSheet(f"""
            color: {Theme.LEFT_ACCENT};
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 1.5px;
            padding: 16px 8px 6px 8px;
            background-color: transparent;
        """)


class LeftPanel(QWidget):
    signal_nav = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("leftPanel")
        self.setFixedWidth(260)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(2)

        title = QLabel("KAI AGGREGATOR")
        title.setObjectName("appTitle")
        layout.addWidget(title)

        layout.addSpacing(8)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        sections = [
            (CALENDAR, "Расписание", [
                ("today", CALENDAR, "Сегодня"),
                ("tomorrow", CALENDAR, "Завтра"),
                ("week", CALENDAR, "Неделя"),
            ]),
            (NOTE, "Учёба", [
                ("classroom", NOTE, "Classroom"),
                ("tasks", NOTE, "Задания"),
                ("notes", BOOK, "Заметки"),
            ]),
            (CODE, "Разработка", [
                ("cdev", CODE, "C / C++"),
            ]),
            (BOT, "DeepSeek", [
                ("deepseek", BOT, "Чат"),
            ]),
            (VIDEO, "Конференции", [
                ("meet", VIDEO, "Google Meet"),
            ]),
        ]

        first_btn = None
        for section_icon, section_name, items in sections:
            layout.addWidget(SectionLabel(section_icon, section_name))

            for key, icon_svg, label in items:
                btn = QPushButton(f"   {label}")
                btn.setObjectName("navButton")
                btn.setCheckable(True)
                btn.setIcon(make_icon(icon_svg))
                btn.setIconSize(QSize(18, 18))
                btn.clicked.connect(lambda _, k=key: self.signal_nav.emit(k))
                layout.addWidget(btn)
                self.group.addButton(btn)
                if first_btn is None:
                    first_btn = btn

        if first_btn:
            first_btn.setChecked(True)

        layout.addStretch()