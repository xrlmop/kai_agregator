import os
import sys
import shutil

from PyQt6.QtWidgets import (
    QApplication, QStyleFactory, QMainWindow, QStackedWidget
)

from ui.main_window import MainWindow
from ui.license_view import LicenseView
from ui.theme import Theme
from core.license import has_valid_user_license


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def ensure_project_structure():
    folders = ["ui", "data", "core", "ai", "notes"]
    for folder in folders:
        os.makedirs(os.path.join(PROJECT_ROOT, folder), exist_ok=True)
    for folder in ["ui", "data", "core", "ai"]:
        init_file = os.path.join(PROJECT_ROOT, folder, "__init__.py")
        if not os.path.exists(init_file) or os.path.getsize(init_file) > 0:
            open(init_file, "w").close()


def check_environment():
    missing = []
    if shutil.which("gcc") is None:
        missing.append("gcc  →  xcode-select --install")
    try:
        import PyQt6  # noqa
    except ImportError:
        missing.append("PyQt6  →  pip install PyQt6")
    if missing:
        print("Чего-то не хватает:")
        for m in missing:
            print("   -", m)
        print()
        return False
    return True


class AppRoot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KAI Aggregator")
        self.resize(1100, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.license_view = LicenseView()
        self.license_view.activated.connect(self.open_main)
        self.stack.addWidget(self.license_view)

        self.main_widget = None

        if has_valid_user_license().get("valid"):
            self.open_main()
        else:
            self.stack.setCurrentWidget(self.license_view)

    def open_main(self):
        if self.main_widget is None:
            self.main_widget = MainWindow()
            self.stack.addWidget(self.main_widget)
        self.stack.setCurrentWidget(self.main_widget)


def main():
    ensure_project_structure()
    check_environment()

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setStyleSheet(Theme.qss())

    window = AppRoot()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
