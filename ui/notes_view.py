import os

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit,
    QListWidget, QListWidgetItem, QPushButton, QMessageBox,
    QSplitter, QDialog, QLineEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from ui.theme import Theme


NOTES_DIR = os.path.expanduser("~/Documents/aggregator/notes")


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

BTN_GHOST = """
QPushButton {
    background-color: transparent;
    color: #00b377;
    border: 1px solid #00b377;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #00b377;
    color: #ffffff;
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

BTN_PUSH = """
QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 12px 28px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #1d4ed8;
}
QPushButton:pressed {
    background-color: #1e40af;
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
QPushButton:pressed {
    background-color: #009962;
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


class NoteNameDialog(QDialog):
    def __init__(self, parent=None, title="Новая заметка",
                 label="Название:", initial=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(380)
        self.setStyleSheet("QDialog { background-color: #ffffff; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        lbl = QLabel(label)
        lbl.setStyleSheet(
            "color: #1e1e2e; font-size: 14px; font-weight: bold;"
            "background-color: transparent;"
        )
        layout.addWidget(lbl)

        self.input = QLineEdit(initial)
        self.input.setStyleSheet("""
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
        """)
        self.input.selectAll()
        layout.addWidget(self.input)

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

        self.input.returnPressed.connect(self.accept)

    def value(self) -> str:
        return self.input.text().strip()


class NotesView(QWidget):
    push_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {Theme.RIGHT_BG};")
        os.makedirs(NOTES_DIR, exist_ok=True)

        self.current_file = None
        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.setInterval(600)
        self.save_timer.timeout.connect(self.save_current)

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(20)

        header_row = QHBoxLayout()
        header = QLabel("Заметки на пару")
        header.setStyleSheet(
            f"color: {Theme.TEXT_DARK}; font-size: 24px; font-weight: bold;"
        )
        header_row.addWidget(header)
        header_row.addStretch()

        self.btn_new = QPushButton("+  Новая заметка")
        self.btn_new.setStyleSheet(BTN_PRIMARY)
        self.btn_new.setFixedHeight(38)
        self.btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new.clicked.connect(self.create_note)
        header_row.addWidget(self.btn_new)

        root.addLayout(header_row)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {Theme.CARD_BORDER};
            }}
        """)

        left = QWidget()
        left.setStyleSheet(f"background-color: {Theme.RIGHT_BG};")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 16, 0)
        left_layout.setSpacing(12)

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
                padding: 12px 14px;
                border-radius: 8px;
                margin-bottom: 2px;
            }}
            QListWidget::item:selected {{
                background-color: #e6f7f1;
                color: {Theme.ACCENT_DARK};
                font-weight: bold;
            }}
            QListWidget::item:hover {{
                background-color: #f0faf5;
            }}
        """)
        self.list.itemSelectionChanged.connect(self.on_select)
        left_layout.addWidget(self.list, stretch=1)

        actions = QHBoxLayout()
        actions.setSpacing(8)

        self.btn_rename = QPushButton("Переименовать")
        self.btn_rename.setStyleSheet(BTN_GHOST)
        self.btn_rename.setFixedHeight(34)
        self.btn_rename.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_rename.clicked.connect(self.rename_note)
        actions.addWidget(self.btn_rename)

        self.btn_delete = QPushButton("Удалить")
        self.btn_delete.setStyleSheet(BTN_GHOST_DANGER)
        self.btn_delete.setFixedHeight(34)
        self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete.clicked.connect(self.delete_note)
        actions.addWidget(self.btn_delete)

        actions.addStretch()
        left_layout.addLayout(actions)

        right = QWidget()
        right.setStyleSheet(f"background-color: {Theme.RIGHT_BG};")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(16, 0, 0, 0)
        right_layout.setSpacing(12)

        self.title_label = QLabel("Выбери заметку")
        self.title_label.setStyleSheet(
            f"color: {Theme.TEXT_DARK}; font-size: 15px; font-weight: bold;"
        )
        right_layout.addWidget(self.title_label)

        self.editor = QPlainTextEdit()
        self.editor.setObjectName("notesArea")
        font = QFont("JetBrains Mono", 14)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.editor.setFont(font)
        self.editor.setPlaceholderText("Пиши тут…")
        self.editor.textChanged.connect(lambda: self.save_timer.start())
        right_layout.addWidget(self.editor, stretch=1)

        push_row = QHBoxLayout()
        push_row.setSpacing(12)

        hint_label = QLabel(
            "А ну-ка, маленький, давай посмотрим, что ты настрочил.\n"
            "Если ты сам препода не понял — пуш"
        )
        hint_label.setStyleSheet(
            "color: #a0a0a8; font-size: 11px; font-style: italic;"
            "background-color: transparent;"
        )
        hint_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        push_row.addWidget(hint_label, stretch=1)

        self.push_btn = QPushButton("Пуш в DeepSeek")
        self.push_btn.setStyleSheet(BTN_PUSH)
        self.push_btn.setFixedHeight(44)
        self.push_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.push_btn.clicked.connect(self.push)
        push_row.addWidget(self.push_btn)

        right_layout.addLayout(push_row)

        self.status = QLabel("")
        self.status.setStyleSheet(
            f"color: {Theme.TEXT_MUTED}; font-size: 12px;"
        )
        right_layout.addWidget(self.status)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([220, 560])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        root.addWidget(splitter, stretch=1)

        self.refresh_list()

    def refresh_list(self):
        self.list.clear()
        if not os.path.isdir(NOTES_DIR):
            return
        for f in sorted(os.listdir(NOTES_DIR)):
            full = os.path.join(NOTES_DIR, f)
            if os.path.isfile(full) and f.endswith(".txt"):
                item = QListWidgetItem(f"  {f[:-4]}")
                item.setData(Qt.ItemDataRole.UserRole, f)
                self.list.addItem(item)

    def create_note(self):
        dlg = NoteNameDialog(self, "Новая заметка", "Название:")
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        name = dlg.value()
        if not name:
            return
        filename = f"{name}.txt"
        path = os.path.join(NOTES_DIR, filename)
        if os.path.exists(path):
            QMessageBox.warning(self, "Ошибка", "Такая заметка уже есть")
            return
        open(path, "w").close()
        self.refresh_list()
        for i in range(self.list.count()):
            item = self.list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == filename:
                self.list.setCurrentItem(item)
                break

    def on_select(self):
        items = self.list.selectedItems()
        if not items:
            return
        self.save_current()
        filename = items[0].data(Qt.ItemDataRole.UserRole)
        path = os.path.join(NOTES_DIR, filename)
        self.current_file = path
        self.title_label.setText(f"Заметка: {filename[:-4]}")
        self.editor.blockSignals(True)
        with open(path, "r", encoding="utf-8") as f:
            self.editor.setPlainText(f.read())
        self.editor.blockSignals(False)
        self.status.setText("")

    def save_current(self):
        if not self.current_file:
            return
        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(self.editor.toPlainText())
        self.status.setText("Сохранено")

    def rename_note(self):
        items = self.list.selectedItems()
        if not items:
            return
        old = items[0].data(Qt.ItemDataRole.UserRole)
        dlg = NoteNameDialog(self, "Переименовать", "Новое имя:",
                             initial=old[:-4])
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        new_name = dlg.value()
        if not new_name:
            return
        new = f"{new_name}.txt"
        old_path = os.path.join(NOTES_DIR, old)
        new_path = os.path.join(NOTES_DIR, new)
        if os.path.exists(new_path):
            QMessageBox.warning(self, "Ошибка", "Такое имя уже есть")
            return
        os.rename(old_path, new_path)
        self.current_file = new_path
        self.refresh_list()

    def delete_note(self):
        items = self.list.selectedItems()
        if not items:
            return
        filename = items[0].data(Qt.ItemDataRole.UserRole)
        confirm = QMessageBox.question(
            self, "Удалить?",
            f"Удалить заметку «{filename[:-4]}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        os.remove(os.path.join(NOTES_DIR, filename))
        self.current_file = None
        self.editor.clear()
        self.title_label.setText("Выбери заметку")
        self.refresh_list()

    def push(self):
        text = self.editor.toPlainText().strip()
        if not text:
            QMessageBox.information(self, "Пусто", "Заметка пустая")
            return
        self.push_requested.emit(text)