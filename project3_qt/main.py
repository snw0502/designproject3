from ui_base2 import *
import sys

def main():
    app = QApplication(sys.argv)
    window = AlgorithmVisualizer()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()