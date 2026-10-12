from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.cards import LessonCard
from ui.c_editor import CEditorView
from ui.notes_view import NotesView
from ui.deepseek_view import DeepSeekView
from ui.meet_view import MeetView
from ui.theme import Theme


class Divider(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(2)
        self.setStyleSheet(f"""
            background-color: {Theme.ACCENT_DARK};
            border: none;
            margin: 4px 0;
        """)


class ScheduleView(QScrollArea):
    def __init__(self, title: str, lessons: list):
        super().__init__()
        self.setWidgetResizable(True)
        self.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Theme.RIGHT_BG};
                border: none;
            }}
        """)

        container = QWidget()
        container.setStyleSheet(f"background-color: {Theme.RIGHT_BG};")
        layout = QVBoxLayout(container)
        layout.setSpacing(0)
        layout.setContentsMargins(24, 0, 24, 24)

        header = QLabel(title)
        header.setObjectName("dayHeader")
        layout.addWidget(header)

        for i, lesson in enumerate(lessons):
            layout.addWidget(LessonCard(lesson))
            if i < len(lessons) - 1:
                layout.addWidget(Divider())

        layout.addStretch()
        self.setWidget(container)


class PlaceholderView(QWidget):
    def __init__(self, text: str):
        super().__init__()
        self.setStyleSheet(f"background-color: {Theme.RIGHT_BG};")
        layout = QVBoxLayout(self)
        label = QLabel(text)
        label.setObjectName("dayHeader")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


class RightPanel(QStackedWidget):
    push_to_deepseek = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("rightPanel")
        self.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {Theme.RIGHT_BG};
            }}
        """)
        self.deepseek_view = None

    def show_schedule(self, title: str, lessons: list):
        view = ScheduleView(title, lessons)
        self.addWidget(view)
        self.setCurrentWidget(view)

    def show_placeholder(self, text: str):
        view = PlaceholderView(text)
        self.addWidget(view)
        self.setCurrentWidget(view)

    def show_c_editor(self):
        view = CEditorView()
        view.push_requested.connect(self.push_to_deepseek.emit)
        self.addWidget(view)
        self.setCurrentWidget(view)

    def show_notes(self):
        view = NotesView()
        view.push_requested.connect(self.push_to_deepseek.emit)
        self.addWidget(view)
        self.setCurrentWidget(view)

    def show_meet(self):
        view = MeetView()
        self.addWidget(view)
        self.setCurrentWidget(view)

    def show_deepseek(self):
        if self.deepseek_view is None:
            self.deepseek_view = DeepSeekView()
            self.addWidget(self.deepseek_view)
        self.setCurrentWidget(self.deepseek_view)

    def push_text_to_deepseek(self, text: str):
        self.show_deepseek()
        if self.deepseek_view:
            self.deepseek_view.push_text(text)
