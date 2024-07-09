from PySide6.QtCore import QTimer, Slot, Signal
from PySide6.QtGui import QIcon, QFont, QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QInputDialog, QPushButton, QWidget, QProgressBar, \
    QLabel, QGridLayout, QMessageBox

import rc_resources
from Card import Card
from Condition import Condition
from Game import Game


class Preference(QMainWindow):
    __done = Signal()
    __chosen = []

    def __init__(self, data):
        super().__init__()
        self.setMinimumSize(1280, 720)
        self.setWindowTitle("Preference")
        self.setWindowIcon(QIcon(":/resources/icon.ico"))

        self.info = QLabel()
        self.info.setFont(QFont("Times", 18))
        self.info.setAlignment(Qt.AlignCenter)

        self.bribes = [QLabel(self), QLabel(self), QLabel(self)]
        for i in range(len(self.bribes)):
            self.bribes[i].setFont(QFont("Times", 18))
            self.bribes[i].setAlignment(Qt.AlignCenter)
        self.levels = [QLabel(self), QLabel(self), QLabel(self)]
        for i in range(len(self.levels)):
            self.levels[i].setFont(QFont("Times", 18))
            self.levels[i].setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start", self)
        self.start_button.setFixedSize(100, 40)
        self.start_button.clicked.connect(self.start)

        self.bet_button = QPushButton("Bet", self)
        self.bet_button.setFixedSize(100, 40)
        self.bet_button.clicked.connect(self.trading)
        self.bet_button.hide()

        deck = QPixmap(":/resources/Deck.png")
        self.deck = QLabel()
        self.deck.setPixmap(deck)

        self.layout = QGridLayout(self)
        self.resize(1600, 1024)
        debugLabel = QLabel(str(len(data)))
        debugLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(debugLabel, 11, 13, Qt.AlignCenter)

        self.layout.addWidget(self.info, 0, 4, 1, 6, Qt.AlignCenter)
        self.layout.addWidget(self.start_button, 1, 6, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.bet_button, 2, 6, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.bribes[0], 9, 6, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.bribes[1], 9, 2, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.bribes[2], 9, 10, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.levels[0], 8, 6, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.levels[1], 0, 0, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.levels[2], 0, 12, 1, 2, Qt.AlignCenter)
        self.central_widget = QWidget()
        self.central_widget.resize(self.size())
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setFormat("Distribution %p%")
        self.statusBar().addWidget(self.progress)
        self.progress.hide()

        self.bet_dialog = QInputDialog()
        self.bet_dialog.setCancelButtonText("Pass")

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.setSingleShot(True)
        self.game = Game(Condition(data))

    def resizeEvent(self, event):
        self.central_widget.resize(event.size())
        for i in range(14):
            self.layout.setColumnMinimumWidth(i, int(event.size().width() / 14))
        for i in range(12):
            self.layout.setRowMinimumHeight(i, int(event.size().height() / 12))
        return super(Preference, self).resizeEvent(event)

    def start(self):
        self.start_button.hide()
        self.game = Game(self.game.cond)
        self.deck.show()
        self.layout.addWidget(self.deck, 4, 6, 2, 2, Qt.AlignCenter)
        self.distribute()

    def distribute(self):
        self.info.setText("Distribution")
        self.progress.show()
        self.progress.setValue(0)
        self.game.distribution()
        self.timer.timeout.connect(self.distributeDone)
        self.timer.start()

    @Slot()
    def distributeDone(self):
        self.timer.timeout.disconnect(self.distributeDone)
        self.progress.setValue(100)
        self.timer.timeout.connect(self.showCards)
        self.timer.start()

    def showCards(self):
        self.timer.timeout.disconnect(self.showCards)
        self.bet_button.show()
        self.info.setText("Trading. Evaluate your cards and make a bet")
        self.deck.hide()
        for i in range(len(self.game.players)):
            for j in range(len(self.game.players[i].hand.cards)):
                card = self.game.players[i].hand.cards[j]
                if i == 0:
                    self.layout.addWidget(card, 10, j + 2, 2, 1, Qt.AlignCenter)
                elif i == 1:
                    card.rotate()
                    self.layout.addWidget(card, j + 1, 0, 1, 2, Qt.AlignCenter)
                else:
                    card.rotate()
                    self.layout.addWidget(card, j + 1, 12, 1, 2, Qt.AlignCenter)
        for i in range(len(self.game.table.extra)):
            card = self.game.table.extra[i]
            card.setJacket()
            self.layout.addWidget(card, 4, 6 + i, 2, 1, Qt.AlignCenter)

    def trading(self):
        min_bet = 0
        isDone = False
        bets = ['', '', '']
        while isDone is False:
            bets[0], min_bet = self.getBet("Player 1", min_bet, bets[0])
            bets[1], min_bet = self.getBet("Player 2", min_bet, bets[1])
            bets[2], min_bet = self.getBet("Player 3", min_bet, bets[2])
            isDone = self.game.trading(bets)

        self.bet_button.hide()
        if self.game.gameLevel == "Pass":
            for i in range(len(self.levels)):
                self.levels[i].setText("Passing")
            self.gameCycle(0, self.game.gameLevel)
        else:
            for j in range(len(self.game.table.extra)):
                card = self.game.table.extra[j]
                card.setCard()
                self.layout.replaceWidget(self.game.table.extra[j], card)
            self.chooseCards()

    def chooseCards(self):
        self.info.setText("Choose 2 cards to remove from your hand and table")
        for i in range(len(self.game.players[self.game.fp_id].hand.cards)):
            self.game.players[self.game.fp_id].hand.cards[i].blockSignals(False)
            self.game.players[self.game.fp_id].hand.cards[i].chosen.connect(self.twoChosenCards)
        for i in range(len(self.game.table.extra)):
            self.game.table.extra[i].blockSignals(False)
            self.game.table.extra[i].chosen.connect(self.twoChosenCards)
        self.__done.connect(self.gameOrder)

    @Slot()
    def gameOrder(self):
        self.__done.disconnect(self.gameOrder)
        for i in range(len(self.game.players[self.game.fp_id].hand.cards)):
            self.game.players[self.game.fp_id].hand.cards[i].blockSignals(True)
            self.game.players[self.game.fp_id].hand.cards[i].chosen.disconnect(self.twoChosenCards)
            self.game.players[self.game.fp_id].hand.cards[i].setFrameStyle(0)
        for i in range(len(self.game.table.extra)):
            self.game.table.extra[i].blockSignals(True)
            self.game.table.extra[i].chosen.disconnect(self.twoChosenCards)
            self.game.players[self.game.fp_id].hand.cards[i].setFrameStyle(0)

        prev = self.game.players[self.game.fp_id].hand.cards[:]
        for card in prev:
            card.hide()
            if card in self.__chosen:
                self.__chosen.pop(self.__chosen.index(card))
                self.game.table.toHeap(self.game.players[self.game.fp_id].hand.put(card))

        prevEx = self.game.table.extra[:]
        for card in prevEx:
            card.hide()
            if card in self.__chosen:
                self.__chosen.pop(self.__chosen.index(card))
                self.game.table.toHeap(self.game.table.extra.pop(self.game.table.extra.index(card)))

        for card in self.game.table.extra:
            self.game.players[self.game.fp_id].hand.get(card)
        self.game.table.extra.clear()

        for i in range(len(self.game.players[self.game.fp_id].hand.cards)):
            card = self.game.players[self.game.fp_id].hand.cards[i]
            card.show()
            if self.game.fp_id == 0:
                self.layout.addWidget(card, 10, i + 2, 2, 1, Qt.AlignCenter)
            elif self.game.fp_id == 1:
                card.rotate()
                self.layout.addWidget(card, i + 1, 0, 1, 2, Qt.AlignCenter)
            else:
                card.rotate()
                self.layout.addWidget(card, i + 1, 12, 1, 2, Qt.AlignCenter)

        gLevel = self.getBet("Player " + str(self.game.fp_id + 1), self.game.bets.index(self.game.gameLevel) - 1,
                             self.game.gameLevel)[0]
        if gLevel != "Pass":
            self.game.gameLevel = gLevel
        self.levels[self.game.fp_id].setText("Player " + str(self.game.fp_id + 1) + ": " + self.game.gameLevel)
        self.whists()

    @Slot(str, int)
    def twoChosenCards(self, suit, value):
        card = Card(suit, value)
        if card not in self.__chosen:
            self.__chosen.append(card)
        if len(self.__chosen) == 2:
            self.__done.emit()

    def whists(self):
        tmp = ["Pass", self.game.gameLevel, "Whist"]
        passed = True
        for i in range(len(self.game.players)):
            if self.game.players[i].cond != 1:
                whist = self.getWhist("Player " + str(i + 1))
                if whist == "Whist":
                    self.game.players[i].cond = 2
                    passed = False
                self.levels[i].setText("Player " + str(i + 1) + ": " + tmp[self.game.players[i].cond])
        if passed:
            self.condition(True)
        else:
            self.gameCycle(0, self.game.gameLevel)

    def gameCycle(self, turn: int, gLevel):
        if turn == 0:
            if gLevel == "Pass":
                self.info.setText("Passing. Try not to get bribes. First hand: Player " + str(self.game.cur_id + 1))
                for card in self.game.table.extra:
                    card.hide()
                    self.game.table.toHeap(card)
                self.game.table.extra.clear()
            else:
                self.info.setText(
                    "Drawing. Try to get maximum amount of bribes. First hand: Player " + str(self.game.cur_id + 1))
            self.turn()
            return

        for i in range(len(self.game.players)):
            player = self.game.players[i]
            for card in player.hand.cards[:]:
                if card in self.__chosen:
                    self.__chosen.pop(self.__chosen.index(card))
                    self.game.table.get(player.hand.put(card), (i + self.game.cur_id) % 3)
                    card.hide()
        win_id = (self.game.table.countBribe() + self.game.cur_id) % 3
        self.game.cur_id = win_id
        self.game.players[win_id].hand.bribes += 1
        for i in range(len(self.game.players)):
            self.bribes[i].setText("Bribes: " + str(self.game.players[i].hand.bribes))

        if turn == 10:
            self.info.setText("Game turn is over, you can see results")
            self.condition(False)
            return
        else:
            if gLevel == "Pass":
                self.info.setText("Passing. Try not to get bribes. First hand: Player " + str(self.game.cur_id + 1))
            else:
                self.info.setText(
                    "Drawing. Try to get maximum amount of bribes. First hand: Player " + str(self.game.cur_id + 1))
            self.turn()

    def turn(self):
        pid = (self.game.cur_id + len(self.__chosen)) % 3
        prev = (pid - 1) % 3

        for i in range(len(self.game.players[pid].hand.cards)):
            self.game.players[pid].hand.cards[i].blockSignals(False)
            self.game.players[pid].hand.cards[i].chosen.connect(self.threeChosenCards)
        if len(self.__chosen) != 0:
            for i in range(len(self.game.players[prev].hand.cards)):
                self.game.players[prev].hand.cards[i].blockSignals(True)
                self.game.players[prev].hand.cards[i].chosen.disconnect(self.threeChosenCards)
                self.game.players[prev].hand.cards[i].setFrameStyle(0)
            for card in self.game.players[prev].hand.cards:
                if card == self.__chosen[-1]:
                    if prev == 0:
                        self.layout.addWidget(card, 6, 6, 2, 2, Qt.AlignCenter)
                    elif prev == 1:
                        card.rotate()
                        self.layout.addWidget(card, 5, 3, 2, 2, Qt.AlignCenter)
                    else:
                        card.rotate()
                        self.layout.addWidget(card, 5, 9, 2, 2, Qt.AlignCenter)
        if len(self.__chosen) == 3:
            for i in range(len(self.game.players[pid].hand.cards)):
                self.game.players[pid].hand.cards[i].blockSignals(True)
                self.game.players[pid].hand.cards[i].chosen.disconnect(self.threeChosenCards)
                self.game.players[pid].hand.cards[i].setFrameStyle(0)
            self.gameCycle(10 - len(self.game.players[pid].hand.cards) + 1, self.game.gameLevel)
        return

    @Slot(str, int)
    def threeChosenCards(self, suit, value):
        card = Card(suit, value)
        if card not in self.__chosen:
            self.__chosen.append(card)
            self.turn()

    def condition(self, passed: bool):
        result = self.game.cond.result(self.game.players, self.game.gameLevel, passed)
        txt = ""
        for i in range(len(self.game.players)):
            txt += "Player " + str(i + 1) + ": " + str(result[i]) + "\n"
        msgBox = QMessageBox()
        msgBox.setText(txt)
        msgBox.exec()
        self.start_button.show()
        self.start_button.setText("Continue")
        self.info.setText("")
        for i in range(len(self.levels)):
            self.levels[i].setText("")
            self.bribes[i].setText("")

    def getBet(self, player: str, min_bet: int, bet: str):
        if bet == "Pass":
            return "Pass", min_bet
        bet = self.bet_dialog.getItem(self, player, "Choose your bet:",
                                      self.game.bets[min_bet + 1:], 0, False)
        if bet[1] is False:
            return "Pass", min_bet
        else:
            if self.game.bets.index(bet[0]) > min_bet:
                return bet[0], self.game.bets.index(bet[0])
            else:
                return bet[0], min_bet

    def getWhist(self, player):
        res = self.bet_dialog.getItem(self, player, "Choose game:",
                                      ["Whist", "Pass"], 0, False)
        if res[1] is False:
            return "Pass"
        else:
            return res[0]
