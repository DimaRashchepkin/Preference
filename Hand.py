from Card import Card


class Hand:
    def __init__(self):
        self.cards = []
        self.__bribes = 0

    def put(self, card: Card):
        res = self.cards.pop(self.cards.index(card))
        return res

    def get(self, card: Card):
        self.cards.append(card)
        self.cards.sort()

    def getCards(self, cards: list[Card]):
        if len(cards) == 10:
            self.cards = cards
        self.cards.sort()

    @property
    def bribes(self):
        return self.__bribes

    @bribes.setter
    def bribes(self, value: int):
        self.__bribes = value
