import os
import json

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit,
    QPushButton
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QThread, pyqtSignal
from openai import OpenAI

from ui.theme import Theme


CONFIG_DIR = os.path.expanduser("~/.kai_aggregator")
MASTER_FILE = os.path.join(CONFIG_DIR, "master_plain.json")


def load_master_key() -> str:
    if not os.path.exists(MASTER_FILE):
        return ""
    try:
        with open(MASTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("key", "")
    except Exception:
        return ""


def save_master_key(key: str):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        json.dump({"key": key}, f, indent=2)


class StreamWorker(QThread):
    chunk = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, api_key: str, messages: list):
        super().__init__()
        self.api_key = api_key
        self.messages = messages

    def run(self):
        try:
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com",
            )
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=self.messages,
                stream=True,
            )
            for event in stream:
                delta = event.choices[0].delta.content
                if delta:
                    self.chunk.emit(delta)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class DeepSeekView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {Theme.RIGHT_BG};")
        self.messages = []
        self.worker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(14)

        header = QLabel("DeepSeek")
        header.setStyleSheet(
            f"color: {Theme.TEXT_DARK}; font-size: 24px; font-weight: bold;"
        )
        layout.addWidget(header)

        hint = QLabel(
            "Мастер-ключ DeepSeek задаётся в root-панели администратором."
        )
        hint.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 13px;")
        layout.addWidget(hint)

        self.chat = QPlainTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setObjectName("notesArea")
        font = QFont("JetBrains Mono", 13)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.chat.setFont(font)
        self.chat.setPlaceholderText("Тут будет переписка с DeepSeek…")
        layout.addWidget(self.chat, stretch=1)

        input_row = QHBoxLayout()

        self.input = QPlainTextEdit()
        self.input.setObjectName("notesArea")
        self.input.setFont(font)
        self.input.setPlaceholderText("Спроси что-нибудь…")
        self.input.setFixedHeight(80)
        input_row.addWidget(self.input, stretch=1)

        self.send_btn = QPushButton("Отправить")
        self.send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.ACCENT_DARK};
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Theme.ACCENT};
                color: {Theme.BG};
            }}
        """)
        self.send_btn.setFixedHeight(80)
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.clicked.connect(self.send)
        input_row.addWidget(self.send_btn)

        layout.addLayout(input_row)

    def send(self):
        text = self.input.toPlainText().strip()
        if not text:
            return

        key = load_master_key()
        if not key:
            self.chat.appendPlainText(
                "Мастер-ключ DeepSeek не задан.\n"
                "Обратись к администратору.\n"
            )
            return

        self.input.clear()
        self.messages.append({"role": "user", "content": text})
        self.chat.appendPlainText(f"Ты: {text}\n")
        self.chat.appendPlainText("DeepSeek: ")

        self.worker = StreamWorker(key, self.messages)
        self.worker.chunk.connect(self.on_chunk)
        self.worker.finished.connect(self.on_finish)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_chunk(self, text: str):
        cursor = self.chat.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(text)
        self.chat.setTextCursor(cursor)

    def on_finish(self):
        self.chat.appendPlainText("\n")

    def on_error(self, msg: str):
        self.chat.appendPlainText(f"\nОшибка: {msg}\n")

    def push_text(self, text: str):
        prompt = f"Объясни простыми словами:\n\n{text}"
        self.input.setPlainText(prompt)
        self.send()
