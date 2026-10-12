class Theme:
    BG = "#0a0a0f"
    LEFT_BG = "#732dcf"
    LEFT_BORDER = "#5e24a8"
    LEFT_HOVER = "#8642dd"
    LEFT_ACTIVE = "#5e24a8"
    LEFT_TEXT = "#ffffff"
    LEFT_TEXT_MUTED = "#e0d0f5"
    LEFT_ACCENT = "#00ff88"
    RIGHT_BG = "#ffffff"
    CARD_BG = "#ffffff"
    CARD_BORDER = "#e0e0e0"
    CARD_HOVER_BORDER = "#00b377"
    CARD_HOVER_BG = "#f5fffb"
    ACCENT = "#00ff88"
    ACCENT_DARK = "#00b377"
    SECONDARY = "#cba6f7"
    TEXT = "#fbfbfe"
    TEXT_DARK = "#1e1e2e"
    TEXT_MUTED = "#6c7086"
    BORDER = "#2b2a33"
    EDITOR_BG = "#1e1e2e"
    EDITOR_TEXT = "#cdd6f4"
    EDITOR_GUTTER = "#151522"
    PUSH_BG = "#2563eb"
    PUSH_HOVER = "#1d4ed8"
    PUSH_PRESSED = "#1e40af"
    PUSH_TEXT = "#ffffff"

    @classmethod
    def qss(cls) -> str:
        return f"""
QMainWindow {{
    background-color: {cls.BG};
}}

QWidget {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 14px;
    color: {cls.TEXT};
}}

#leftPanel {{
    background-color: {cls.LEFT_BG};
    border-right: 1px solid {cls.LEFT_BORDER};
}}

#appTitle {{
    color: {cls.LEFT_ACCENT};
    font-size: 18px;
    font-weight: bold;
    padding: 20px 16px;
    letter-spacing: 1px;
}}

#navButton {{
    background-color: transparent;
    color: {cls.LEFT_TEXT};
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
}}

#navButton:hover {{
    background-color: {cls.LEFT_HOVER};
    color: {cls.LEFT_TEXT};
}}

#navButton:checked {{
    background-color: {cls.LEFT_ACTIVE};
    color: {cls.LEFT_TEXT};
    border-left: 3px solid {cls.LEFT_ACCENT};
    font-weight: bold;
}}

#rightPanel {{
    background-color: {cls.RIGHT_BG};
    color: {cls.TEXT_DARK};
}}

#rightPanel, #rightPanel > QWidget, #rightPanel QWidget {{
    background-color: {cls.RIGHT_BG};
}}

QScrollArea {{
    border: none;
    background-color: {cls.RIGHT_BG};
}}

#dayHeader {{
    color: {cls.TEXT_DARK};
    font-size: 22px;
    font-weight: bold;
    padding: 20px 24px 12px 24px;
    background-color: transparent;
}}

QScrollBar:vertical {{
    background: #f5f5f7;
    width: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background: #d0d0d5;
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {cls.ACCENT_DARK};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QSplitter::handle {{
    background-color: {cls.LEFT_BORDER};
    width: 2px;
}}

QSplitter::handle:hover {{
    background-color: {cls.LEFT_ACCENT};
}}

#editorArea {{
    background-color: {cls.EDITOR_BG};
    color: {cls.EDITOR_TEXT};
    border: 1px solid {cls.BORDER};
    border-radius: 8px;
    padding: 12px;
    font-family: "JetBrains Mono", "Menlo", monospace;
    font-size: 13px;
    selection-background-color: {cls.ACCENT_DARK};
}}

#outputArea {{
    background-color: {cls.EDITOR_BG};
    color: {cls.TEXT};
    border: 1px solid {cls.BORDER};
    border-radius: 8px;
    padding: 12px;
    font-family: "JetBrains Mono", "Menlo", monospace;
    font-size: 13px;
}}

#runButton {{
    background-color: {cls.ACCENT_DARK};
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
}}

#runButton:hover {{
    background-color: {cls.ACCENT};
    color: {cls.BG};
}}

#runButton:disabled {{
    background-color: #555;
    color: #999;
}}















#sectionHeader {{
    color: {cls.TEXT_DARK};
    font-size: 20px;
    font-weight: bold;
    padding: 16px 0 8px 0;
    background-color: transparent;
}}

#notesArea {{
    background-color: #ffffff;
    color: {cls.TEXT_DARK};
    border: 1px solid {cls.CARD_BORDER};
    border-radius: 8px;
    padding: 12px;
    font-family: "JetBrains Mono", "Menlo", monospace;
    font-size: 14px;
}}

QDialog, QMessageBox, QInputDialog {{
    background-color: #ffffff;
    color: #1e1e2e;
}}

QDialog QLabel, QMessageBox QLabel, QInputDialog QLabel {{
    color: #1e1e2e;
    background-color: transparent;
}}

QDialog QLineEdit, QInputDialog QLineEdit {{
    background-color: #ffffff;
    color: #1e1e2e;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: #00b377;
}}

QDialog QPushButton, QMessageBox QPushButton, QInputDialog QPushButton {{
    background-color: #00b377;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    min-width: 80px;
}}

QDialog QPushButton:hover, QMessageBox QPushButton:hover, QInputDialog QPushButton:hover {{
    background-color: #00ff88;
    color: #0a0a0f;
}}

#pushButton {{
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 15px;
    font-weight: bold;
}}

#pushButton:hover {{
    background-color: #1d4ed8;
}}

#pushButton:pressed {{
    background-color: #1e40af;
}}

#secondaryButton {{
    background-color: #00b377;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: bold;
}}

#secondaryButton:hover {{
    background-color: #00ff88;
    color: #0a0a0f;
}}

#dangerButton {{
    background-color: #d32f2f;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: bold;
}}

#dangerButton:hover {{
    background-color: #b71c1c;
}}

"""


class LightTheme(Theme):
    BG = "#ffffff"
    LEFT_BG = "#f5f5f7"
    LEFT_BORDER = "#e0e0e0"
    LEFT_HOVER = "#ebebeb"
    LEFT_ACTIVE = "#e0e0e0"
    LEFT_TEXT = "#1e1e2e"
    LEFT_ACCENT = "#732dcf"
    RIGHT_BG = "#ffffff"
    TEXT = "#1e1e2e"
    BORDER = "#e0e0e0"
    ACCENT = "#00b377"
    ACCENT_DARK = "#008f5e"
