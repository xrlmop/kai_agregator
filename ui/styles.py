DARK_QSS = """
QMainWindow {
    background-color: #0a0a0f;
}

QWidget {
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 14px;
    color: #cdd6f4;
}

#leftPanel {
    background-color: #151522;
    border-right: 1px solid #313244;
}

#appTitle {
    color: #00ff88;
    font-size: 18px;
    font-weight: bold;
    padding: 20px 16px;
    letter-spacing: 1px;
}

#navButton {
    background-color: transparent;
    color: #cdd6f4;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
}

#navButton:hover {
    background-color: #1e1e2e;
    color: #00ff88;
}

#navButton:checked {
    background-color: #1e1e2e;
    color: #00ff88;
    border-left: 3px solid #00ff88;
}

#rightPanel {
    background-color: #ffffff;
    color: #1e1e2e;
}

#rightPanel > QWidget {
    background-color: #ffffff;
}

QScrollArea {
    border: none;
    background-color: #ffffff;
}

QScrollArea > QWidget > QWidget {
    background-color: #ffffff;
}

#dayHeader {
    color: #1e1e2e;
    font-size: 22px;
    font-weight: bold;
    padding: 20px 24px 12px 24px;
    background-color: transparent;
}

#lessonCard {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
}

#lessonCard:hover {
    border: 1px solid #00b377;
    background-color: #f5fffb;
}

#cardTitle {
    color: #1e1e2e;
    font-size: 16px;
    font-weight: bold;
    background-color: transparent;
}

#cardMeta {
    color: #6c7086;
    font-size: 13px;
    background-color: transparent;
}

#cardRoom {
    color: #00b377;
    font-size: 13px;
    background-color: transparent;
}

QScrollBar:vertical {
    background: #f5f5f7;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #d0d0d5;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #00b377;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QSplitter::handle {
    background-color: #313244;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #00ff88;
}
"""