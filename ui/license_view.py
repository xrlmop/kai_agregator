from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.license import (
    save_user_license, validate_license, load_user_license,
)
from core.machine import get_machine_id
from ui.theme import Theme


class LicenseView(QWidget):
    activated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {Theme.RIGHT_BG};")

        root = QVBoxLayout(self)
        root.setContentsMargins(60, 60, 60, 60)
        root.setSpacing(20)
        root.addStretch()

        title = QLabel("KAI AGGREGATOR")
        title.setStyleSheet(
            "color: #732dcf; font-size: 32px; font-weight: bold;"
            "letter-spacing: 2px; background-color: transparent;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        sub = QLabel("Введите лицензионный ключ для активации")
        sub.setStyleSheet(
            f"color: {Theme.TEXT_MUTED}; font-size: 14px;"
            "background-color: transparent;"
        )
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(sub)

        root.addSpacing(20)

        mid_label = QLabel("Ваш Machine ID (отправьте админу):")
        mid_label.setStyleSheet(
            f"color: {Theme.TEXT_MUTED}; font-size: 12px;"
            "background-color: transparent;"
        )
        mid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(mid_label)

        mid_row = QHBoxLayout()
        mid_row.setSpacing(8)

        self.machine_input = QLineEdit(get_machine_id())
        self.machine_input.setReadOnly(True)
        self.machine_input.setFont(QFont("JetBrains Mono", 13))
        self.machine_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.machine_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #f5f5f7;
                color: {Theme.TEXT_DARK};
                border: 1px solid {Theme.CARD_BORDER};
                border-radius: 8px;
                padding: 10px 14px;
            }}
        """)
        mid_row.addWidget(self.machine_input, stretch=1)

        btn_copy_mid = QPushButton("Скопировать")
        btn_copy_mid.setFixedHeight(40)
        btn_copy_mid.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_copy_mid.setStyleSheet(f"""
            QPushButton {{
                background-color: #e6f7f1;
                color: {Theme.ACCENT_DARK};
                border: 1px solid {Theme.ACCENT_DARK};
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Theme.ACCENT_DARK};
                color: #ffffff;
            }}
        """)
        btn_copy_mid.clicked.connect(self.copy_machine_id)
        mid_row.addWidget(btn_copy_mid)

        root.addLayout(mid_row)

        root.addSpacing(20)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Вставьте лицензионный ключ")
        self.key_input.setFont(QFont("JetBrains Mono", 13))
        self.key_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #ffffff;
                color: {Theme.TEXT_DARK};
                border: 1px solid {Theme.CARD_BORDER};
                border-radius: 10px;
                padding: 14px 18px;
                font-size: 14px;
                selection-background-color: {Theme.ACCENT_DARK};
                selection-color: #ffffff;
            }}
            QLineEdit:focus {{
                border: 1px solid {Theme.ACCENT_DARK};
            }}
        """)
        self.key_input.returnPressed.connect(self.activate)
        root.addWidget(self.key_input)

        btn = QPushButton("Активировать")
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.ACCENT_DARK};
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 14px 24px;
                font-size: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Theme.ACCENT};
                color: {Theme.BG};
            }}
        """)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(48)
        btn.clicked.connect(self.activate)
        root.addWidget(btn)

        self.status = QLabel("")
        self.status.setStyleSheet(
            "color: #d32f2f; font-size: 13px;"
            "background-color: transparent;"
        )
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setWordWrap(True)
        root.addWidget(self.status)

        root.addStretch()

        footer = QLabel(
            "Нет лицензии? Обратись к администратору проекта."
        )
        footer.setStyleSheet(
            f"color: {Theme.TEXT_MUTED}; font-size: 12px;"
            "background-color: transparent;"
        )
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(footer)

    def copy_machine_id(self):
        QApplication.clipboard().setText(get_machine_id())
        self.status.setStyleSheet(
            f"color: {Theme.ACCENT_DARK}; font-size: 13px;"
            "background-color: transparent;"
        )
        self.status.setText("Machine ID скопирован")

    def activate(self):
        key = self.key_input.text().strip()
        if not key:
            self.status.setText("Введи ключ")
            return

        existing = load_user_license()
        if existing:
            self.status.setText("Уже активировано на этом устройстве")
            self.activated.emit()
            return

        result = validate_license(key)
        if not result["valid"]:
            self.status.setText(f"Не активировано: {result['reason']}")
            return

        save_user_license(key)
        self.status.setStyleSheet(
            f"color: {Theme.ACCENT_DARK}; font-size: 13px;"
            "background-color: transparent;"
        )
        self.status.setText("Лицензия активирована навсегда. Запуск...")
        self.activated.emit()
