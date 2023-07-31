from ui_base import *
import sys

def main():
    app = QApplication(sys.argv)
    window = LaunchWindow()

    apply_stylesheet(app, theme='dark_cyan.xml')

    window.show()

    app.exec()


if __name__ == "__main__":
    main()