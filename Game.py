from Condition import Condition
from Player import Player
from Table import Table


class Game:
    def __init__(self, condition: Condition):
        self.table = Table()
        self.players = [Player(), Player(), Player()]
        self.cond = condition
        self.bets = ["Pass", "6 spades", "6 clubs", "6 diamonds", "6 hearts", "6 NT",
                     "7 spades", "7 clubs", "7 diamonds", "7 hearts", "7 NT",
                     "8 spades", "8 clubs", "8 diamonds", "8 hearts", "8 NT",
                     "9 spades", "9 clubs", "9 diamonds", "9 hearts", "9 NT",
                     "10 spades", "10 clubs", "10 diamonds", "10 hearts", "10 NT",
                     "MIN"]
        self.gameLevel = ""
        self.fp_id = -1
        self.cur_id = -1

    def distribution(self):
        cards = self.table.distribution()
        self.players[0].hand.getCards(cards[0])
        self.players[1].hand.getCards(cards[1])
        self.players[2].hand.getCards(cards[2])

    def trading(self, bets: list[str]):
        ids = [self.bets.index(bets[0]), self.bets.index(bets[1]), self.bets.index(bets[2])]
        cnt = 0
        for x in ids:
            if x == 0:
                cnt += 1

        if cnt == 3:
            self.gameLevel = "Pass"
            self.fp_id = 0
            self.cur_id = 0
            return True
        if cnt == 2:
            for i in range(len(ids)):
                if ids[i] != 0:
                    self.gameLevel = bets[i]
                    self.players[i].cond = 1
                    self.fp_id = i
                    self.cur_id = i
                    return True
        else:
            return False
