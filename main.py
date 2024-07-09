import sys

from PySide6.QtWidgets import QApplication

from Preference import Preference
import rc_resources


def main():
    app = QApplication()
    with open("stylesheet.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
    pref = Preference(sys.argv[1:])
    pref.show()
    app.exec()
    pref.game.cond.save("data.xml")


if __name__ == "__main__":
    main()
