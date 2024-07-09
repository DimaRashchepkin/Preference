from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QPixmap, QTransform, Qt
from PySide6.QtWidgets import QLabel

import rc_resources


class Card(QLabel):
    chosen = Signal(str, int)

    def __init__(self, suit: str, value: int):
        super().__init__()
        self.suit = suit
        self.value = value

        self.card = QPixmap(":resources/" + self.suit + " " + str(self.value) + ".png")
        self.jacket = QPixmap(":resources/Jacket.png")
        self.setPixmap(self.card)
        self.setAlignment(Qt.AlignCenter)
        self.blockSignals(True)

    def mouseDoubleClickEvent(self, event):
        if not self.signalsBlocked():
            self.setFrameStyle(3)
            self.chosen.emit(self.suit, self.value)

    def rotate(self):
        t = QTransform().rotate(+90)
        self.setPixmap(self.card.transformed(t))

    def setJacket(self):
        self.setPixmap(self.jacket)

    def setCard(self):
        self.setPixmap(self.card)

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Wrong type")
        return self.suit == other.suit and self.value == other.value

    def __ne__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Wrong type")
        return self.suit != other.suit or self.value != other.value

    def __lt__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Wrong type")
        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Wrong type")
        return self.value > other.value

    def __str__(self):
        return self.suit + " " + str(self.value)

    @property
    def suit(self):
        return self.__suit

    @suit.setter
    def suit(self, suit):
        if suit not in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            raise ValueError("Wrong value")
        else:
            self.__suit = suit

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value not in range(7, 15):
            raise ValueError("Wrong value")
        else:
            self.__value = value
