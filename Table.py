import random

from Card import Card


class Table:
    def __init__(self):
        self.__cards = {0: None, 1: None, 2: None}
        self.__heap = []
        self.extra = []
        for x in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for i in range(7, 15):
                self.__heap.append(Card(x, i))

    def countBribe(self):
        maxCard = self.__cards[0]
        winner = 0
        for i in range(1, 3):
            if self.__cards[i].suit == maxCard.suit:
                if self.__cards[i].value > maxCard.value:
                    maxCard = self.__cards[i]
                    winner = i
        for i in range(3):
            self.__heap.append(self.__cards[i])
            self.__cards[i] = None
        return winner

    def get(self, card: Card, player: int):
        if player not in range(3):
            raise ValueError("Wrong value")
        self.__cards[player] = card

    def toHeap(self, card: Card):
        self.__heap.append(card)

    def distribution(self):
        res = [[], [], []]
        for i in range(10):
            for j in range(3):
                card = self.__heap.pop(random.randint(0, len(self.__heap) - 1))
                res[j].append(card)
        ln = len(self.__heap)
        for i in range(ln):
            self.extra.append(self.__heap.pop(0))
        return res

    def isFull(self):
        for card in self.__cards:
            if self.__cards[card] is None:
                return False
        return True

    def isEmpty(self):
        for card in self.__cards:
            if self.__cards[card] is not None:
                return False
        return True
