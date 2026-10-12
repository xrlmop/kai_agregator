from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
)
from PyQt6.QtCore import Qt
from ui.icons import svg_icon, CLOCK, PIN, USER
from ui.theme import Theme


class MetaRow(QWidget):
    def __init__(self, icon_svg: str, text: str, color: str):
        super().__init__()
        self.setStyleSheet("background-color: transparent;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        icon_label = QLabel()
        icon_label.setPixmap(svg_icon(icon_svg, color, 16))
        icon_label.setStyleSheet("background-color: transparent;")
        layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setStyleSheet(
            f"color: {color}; font-size: 13px; background-color: transparent;"
        )
        layout.addWidget(text_label)
        layout.addStretch()


class LessonCard(QFrame):
    def __init__(self, lesson: dict):
        super().__init__()
        self.setObjectName("lessonCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            #lessonCard {{
                background-color: {Theme.CARD_BG};
                border: none;
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 16, 20, 16)

        title = QLabel(f"{lesson['index']}. {lesson['name']}")
        title.setStyleSheet(
            f"color: {Theme.TEXT_DARK}; font-size: 16px; font-weight: bold;"
            "background-color: transparent;"
        )
        layout.addWidget(title)

        layout.addWidget(MetaRow(CLOCK, lesson["time"], Theme.TEXT_MUTED))
        layout.addWidget(MetaRow(
            PIN,
            f"{lesson['room']}  —  {lesson['address']}",
            Theme.ACCENT_DARK,
        ))
        layout.addWidget(MetaRow(USER, lesson["teacher"], Theme.TEXT_MUTED))