from enum import Enum

from Hand import Hand


class Player:
    def __init__(self):
        self.hand = Hand()
        self.cond = 0
