import os
import re
import subprocess
import tempfile

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
    QPushButton, QLabel
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal

from ui.theme import Theme


DEFAULT_CODE = """#include <stdio.h>

int main() {
    printf("Привет, мир!\\n");
    return 0;
}
"""


BTN_RUN = """
QPushButton {
    background-color: #00b377;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 12px 28px;
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

BTN_PUSH = """
QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 8px;
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

EDITOR_STYLE = """
QPlainTextEdit {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 10px;
    padding: 14px;
    font-family: "JetBrains Mono", "Menlo", monospace;
    font-size: 13px;
    selection-background-color: #00b377;
    selection-color: #ffffff;
}
"""

OUTPUT_STYLE = """
QPlainTextEdit {
    background-color: #151522;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 10px;
    padding: 14px;
    font-family: "JetBrains Mono", "Menlo", monospace;
    font-size: 13px;
    selection-background-color: #00b377;
    selection-color: #ffffff;
}
"""


class CEditorView(QWidget):
    push_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {Theme.RIGHT_BG};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(14)

        header = QLabel("C / C++ песочница")
        header.setStyleSheet(
            f"color: {Theme.TEXT_DARK}; font-size: 24px; font-weight: bold;"
        )
        layout.addWidget(header)

        hint = QLabel(
            "Пиши код, жми «Запустить». Если рыгнет — объясню по-человечески."
        )
        hint.setStyleSheet(
            f"color: {Theme.TEXT_MUTED}; font-size: 13px;"
        )
        layout.addWidget(hint)

        font = QFont("JetBrains Mono", 13)
        font.setStyleHint(QFont.StyleHint.Monospace)

        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet(EDITOR_STYLE)
        self.editor.setPlainText(DEFAULT_CODE)
        self.editor.setFont(font)
        layout.addWidget(self.editor, stretch=3)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.push_btn = QPushButton("Пуш в DeepSeek")
        self.push_btn.setStyleSheet(BTN_PUSH)
        self.push_btn.setFixedHeight(46)
        self.push_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.push_btn.clicked.connect(self.push)
        btn_row.addWidget(self.push_btn)

        hint_label = QLabel(
            "друже если ты пишешь полную ху..) ты понял, "
            "безоговорочно пуш в дип сик"
        )
        hint_label.setStyleSheet(
            "color: #a0a0a8; font-size: 11px; font-style: italic;"
            "background-color: transparent;"
        )
        hint_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        btn_row.addWidget(hint_label, stretch=1)

        self.run_btn = QPushButton("▶  Запустить")
        self.run_btn.setStyleSheet(BTN_RUN)
        self.run_btn.setFixedHeight(46)
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self.run_code)
        btn_row.addWidget(self.run_btn)

        layout.addLayout(btn_row)

        self.output = QPlainTextEdit()
        self.output.setStyleSheet(OUTPUT_STYLE)
        self.output.setReadOnly(True)
        self.output.setFont(font)
        self.output.setPlainText("Здесь появится результат…")
        layout.addWidget(self.output, stretch=2)

    def push(self):
        code = self.editor.toPlainText().strip()
        if not code:
            return
        self.push_requested.emit(code)

    def run_code(self):
        code = self.editor.toPlainText()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".c", delete=False, dir=tempfile.gettempdir()
        ) as f:
            f.write(code)
            src_path = f.name

        bin_path = src_path.replace(".c", ".out")

        try:
            compile_proc = subprocess.run(
                ["gcc", src_path, "-o", bin_path],
                capture_output=True,
                text=True,
                timeout=15,
            )
        except FileNotFoundError:
            self.output.setPlainText(
                "gcc не найден.\n\n"
                "На macOS запусти в терминале:\n"
                "    xcode-select --install"
            )
            self.cleanup(src_path, bin_path)
            return

        if compile_proc.returncode != 0:
            self.output.setPlainText(self.explain_error(compile_proc.stderr, code))
            self.cleanup(src_path, bin_path)
            return

        try:
            run_proc = subprocess.run(
                [bin_path], capture_output=True, text=True, timeout=5
            )
            out = run_proc.stdout or ""
            err = run_proc.stderr or ""

            if run_proc.returncode != 0:
                self.output.setPlainText(
                    "Оно скомпилилось, но упало при запуске:\n\n" + err
                )
            else:
                result = out if out.strip() else "(пусто — программа ничего не вывела)"
                self.output.setPlainText("Отработало без ошибок:\n\n" + result)
        except subprocess.TimeoutExpired:
            self.output.setPlainText(
                "Программа работает больше 5 секунд — похоже, бесконечный цикл.\n"
                "Проверь условия в while / for."
            )

        self.cleanup(src_path, bin_path)

    def explain_error(self, stderr: str, code: str) -> str:
        lines = stderr.splitlines()
        error_line = None
        error_msg = None

        for line in lines:
            m = re.match(r".*?:(\d+):(\d+):\s*(error|warning):\s*(.+)", line)
            if m:
                error_line = int(m.group(1))
                error_msg = m.group(4)
                break

        if error_line is None:
            return "Не запускается. Компилятор говорит:\n\n" + stderr

        code_lines = code.splitlines()
        snippet = ""
        if 1 <= error_line <= len(code_lines):
            snippet = code_lines[error_line - 1]

        friendly = self.friendly_reason(error_msg)

        return (
            f"У тебя рыгает в строке {error_line}:\n\n"
            f"   {snippet}\n\n"
            f"Почему: {friendly}\n\n"
            f"Что сказал компилятор:\n   {error_msg}"
        )

    def friendly_reason(self, msg: str) -> str:
        m = msg.lower()
        if "expected ';'" in m or "expected ';' before" in m:
            return "скорее всего забыл точку с запятой `;` в конце строки."
        if "expected declaration" in m or "expected expression" in m:
            return "похоже, строка не закончена или что-то лишнее в выражении."
        if "undeclared" in m or "was not declared" in m:
            return "используешь переменную или функцию, которую не объявил."
        if "implicit declaration" in m:
            return "вызываешь функцию, но не подключил нужный заголовок (#include)."
        if "expected ')'" in m:
            return "где-то не закрыл круглую скобку `)`."
        if "expected '}'" in m:
            return "где-то не закрыл фигурную скобку `}`."
        if "format" in m and "expects" in m:
            return "в printf формат не совпадает с типом аргумента (%d для int, %s для строки)."
        return "компилятор что-то не понял. Смотри сообщение ниже."

    def cleanup(self, *paths):
        for p in paths:
            try:
                os.remove(p)
            except OSError:
                pass