import os
import json

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QMessageBox, QDialog,
    QLineEdit, QFormLayout
)
from PyQt6.QtGui import QDesktopServices, QFont
from PyQt6.QtCore import Qt, QUrl
from ui.theme import Theme


CONFIG_DIR = os.path.expanduser("~/.kai_aggregator")
CONFIG_FILE = os.path.join(CONFIG_DIR, "meet_links.json")


BTN_PRIMARY = """
QPushButton {
    background-color: #00b377;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #00d98a;
}
QPushButton:pressed {
    background-color: #009962;
}
"""

BTN_GHOST_DANGER = """
QPushButton {
    background-color: transparent;
    color: #d32f2f;
    border: 1px solid #d32f2f;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #d32f2f;
    color: #ffffff;
}
"""

BTN_OPEN = """
QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #1d4ed8;
}
"""

BTN_DIALOG_OK = """
QPushButton {
    background-color: #00b377;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #00d98a;
}
"""

BTN_DIALOG_CANCEL = """
QPushButton {
    background-color: transparent;
    color: #6c7086;
    border: 1px solid #d0d0d5;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #f5f5f7;
    color: #1e1e2e;
}
"""


def load_links() -> list:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_links(links: list):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, indent=2, ensure_ascii=False)


class AddLinkDialog(QDialog):
    def __init__(self, parent=None, title="Новая ссылка",
                 name="", url=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(460)
        self.setStyleSheet("QDialog { background-color: #ffffff; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        form = QFormLayout()
        form.setSpacing(10)

        self.name_input = QLineEdit(name)
        self.name_input.setPlaceholderText("Например: Консультация по лабе")
        self.name_input.setStyleSheet(self._input_style())
        form.addRow(self._label("Название:"), self.name_input)

        self.url_input = QLineEdit(url)
        self.url_input.setPlaceholderText("https://meet.google.com/xxx-xxxx-xxx")
        self.url_input.setStyleSheet(self._input_style())
        form.addRow(self._label("Ссылка:"), self.url_input)

        layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        cancel = QPushButton("Отмена")
        cancel.setStyleSheet(BTN_DIALOG_CANCEL)
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.setAutoDefault(False)
        cancel.setDefault(False)
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)

        ok = QPushButton("OK")
        ok.setStyleSheet(BTN_DIALOG_OK)
        ok.setCursor(Qt.CursorShape.PointingHandCursor)
        ok.setAutoDefault(False)
        ok.setDefault(False)
        ok.clicked.connect(self.accept)
        btn_row.addWidget(ok)

        layout.addLayout(btn_row)

    def _label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "color: #1e1e2e; font-size: 14px; font-weight: bold;"
            "background-color: transparent;"
        )
        return lbl

    def _input_style(self):
        return """
            QLineEdit {
                background-color: #ffffff;
                color: #1e1e2e;
                border: 1px solid #d0d0d5;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                selection-background-color: #00b377;
                selection-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #00b377;
            }
        """

    def values(self):
        return self.name_input.text().strip(), self.url_input.text().strip()


class MeetView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {Theme.RIGHT_BG};")

        self.links = load_links()

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(20)

        header_row = QHBoxLayout()
        header = QLabel("Google Meet")
        header.setStyleSheet(
            f"color: {Theme.TEXT_DARK}; font-size: 24px; font-weight: bold;"
        )
        header_row.addWidget(header)
        header_row.addStretch()

        btn_add = QPushButton("+  Добавить ссылку")
        btn_add.setStyleSheet(BTN_PRIMARY)
        btn_add.setFixedHeight(38)
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self.add_link)
        header_row.addWidget(btn_add)

        root.addLayout(header_row)

        hint = QLabel(
            "Сохрани ссылки на постоянные конференции — "
            "клик открывает встречу в системном браузере."
        )
        hint.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 13px;")
        root.addWidget(hint)

        self.list = QListWidget()
        self.list.setStyleSheet(f"""
            QListWidget {{
                background-color: transparent;
                color: {Theme.TEXT_DARK};
                border: none;
                padding: 0;
                font-size: 14px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 14px;
                border-radius: 10px;
                margin-bottom: 4px;
                border: 1px solid {Theme.CARD_BORDER};
                background-color: #ffffff;
            }}
            QListWidget::item:selected {{
                border: 1px solid {Theme.ACCENT_DARK};
                background-color: #f0faf5;
            }}
            QListWidget::item:hover {{
                background-color: #f0faf5;
            }}
        """)
        self.list.itemDoubleClicked.connect(self.open_selected)
        root.addWidget(self.list, stretch=1)

        actions = QHBoxLayout()
        actions.setSpacing(8)

        btn_open = QPushButton("Открыть в браузере")
        btn_open.setStyleSheet(BTN_OPEN)
        btn_open.setFixedHeight(38)
        btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_open.clicked.connect(self.open_selected)
        actions.addWidget(btn_open)

        actions.addStretch()

        btn_delete = QPushButton("Удалить")
        btn_delete.setStyleSheet(BTN_GHOST_DANGER)
        btn_delete.setFixedHeight(38)
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.clicked.connect(self.delete_link)
        actions.addWidget(btn_delete)

        root.addLayout(actions)

        self.refresh_list()

    def refresh_list(self):
        self.list.clear()
        for link in self.links:
            item = QListWidgetItem(f"{link['name']}\n{link['url']}")
            item.setData(Qt.ItemDataRole.UserRole, link)
            font = QFont()
            font.setPointSize(13)
            item.setFont(font)
            self.list.addItem(item)

    def add_link(self):
        dlg = AddLinkDialog(self, "Новая ссылка")
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        name, url = dlg.values()
        if not name or not url:
            QMessageBox.warning(self, "Ошибка", "Заполни оба поля")
            return
        self.links.append({"name": name, "url": url})
        save_links(self.links)
        self.refresh_list()

    def open_selected(self):
        items = self.list.selectedItems()
        if not items:
            return
        link = items[0].data(Qt.ItemDataRole.UserRole)
        QDesktopServices.openUrl(QUrl(link["url"]))

    def delete_link(self):
        items = self.list.selectedItems()
        if not items:
            return
        link = items[0].data(Qt.ItemDataRole.UserRole)
        confirm = QMessageBox.question(
            self, "Удалить?",
            f"Удалить ссылку «{link['name']}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        self.links = [l for l in self.links if l != link]
        save_links(self.links)
        self.refresh_list()
