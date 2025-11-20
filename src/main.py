import sys
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer
from ui.main_window import MainWindow, resource_path


def main():
    app = QApplication(sys.argv)
    
    # Set application icon (shows in taskbar)
    app.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
    
    # Create and display splash screen
    splash_pix = QPixmap(resource_path("assets/splash.png"))
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()
    
    # Create main window (but don't show yet)
    window = MainWindow()
    
    # Close splash and show main window after 2 seconds
    def show_main_window():
        splash.close()
        window.show()
    
    QTimer.singleShot(2000, show_main_window)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
