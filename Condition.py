import xml.etree.ElementTree as et

from Player import Player


class Condition:
    def __init__(self, data):
        self.__data = {0: [0, [0, 0, 0], 0], 1: [0, [0, 0, 0], 0], 2: [0, [0, 0, 0], 0]}
        if len(data) == 15:
            for i in range(3):
                self.__data[i][0] = int(data[i * 5])
                self.__data[i][1] = [int(data[i * 5 + 1]), int(data[i * 5 + 2]), int(data[i * 5 + 3])]
                self.__data[i][2] = int(data[i * 5 + 4])
        self.__coefs = {"6": [2, 4], "7": [4, 2], "8": [6, 1], "9": [8, 1], "10": [10, 0], "MIN": [10, 10]}
        self.__result = [0, 0, 0]

    def __table(self, players: list[Player], gLevel: str):
        if gLevel == "Pass":
            for i in range(len(players)):
                self.__data[i][2] += players[i].hand.bribes * 2
        elif gLevel == "MIN":
            order = gLevel.split()[0]
            for i in range(len(players)):
                if players[i].cond == 1:
                    if players[i].hand.bribes == 0:
                        self.__data[i][0] += self.__coefs[order][0]
                    else:
                        self.__data[i][2] += players[i].hand.bribes * self.__coefs[order][0]
        else:
            whisters = []
            order = gLevel.split()[0]
            fp = -1
            for i in range(len(players)):
                if players[i].cond == 1:
                    fp = i
                    if players[i].hand.bribes >= int(order):
                        self.__data[i][0] += self.__coefs[order][0]
                    else:
                        self.__data[i][2] += (int(order) - players[i].hand.bribes) * self.__coefs[order][0]
                elif players[i].cond == 2:
                    whisters.append([players[i], i])
            if len(whisters) == 1:
                if whisters[0][0].hand.bribes >= self.__coefs[order][1]:
                    self.__data[whisters[0][1]][1][fp] += whisters[0][0].hand.bribes * self.__coefs[order][0]
                else:
                    self.__data[whisters[0][1]][2] += (self.__coefs[order][1] - whisters[0][0].hand.bribes) * \
                                                      self.__coefs[order][0]
            elif len(whisters) == 2:
                if whisters[0][0].hand.bribes + whisters[1][0].hand.bribes >= self.__coefs[order][1]:
                    for i in range(2):
                        self.__data[whisters[i][1]][1][fp] += whisters[i][0].hand.bribes * self.__coefs[order][0]
                else:
                    for i in range(2):
                        if whisters[i][0].hand.bribes >= int(self.__coefs[order][1] / 2):
                            self.__data[whisters[i][1]][1][fp] += whisters[i][0].hand.bribes * self.__coefs[order][0]
                        else:
                            self.__data[whisters[i][1]][2] += (int(self.__coefs[order][1] / 2) - whisters[i][
                                0].hand.bribes) * self.__coefs[order][0]

    def __passed(self, players: list[Player], gLevel: str):
        order = gLevel.split()[0]
        for i in range(len(players)):
            if players[i].cond == 1:
                self.__data[i][0] += self.__coefs[order][0]

    def result(self, players: list[Player], gLevel: str, passed: bool):
        if passed:
            self.__passed(players, gLevel)
        else:
            self.__table(players, gLevel)

        for i in range(len(self.__data)):
            self.__result[i] += self.__data[i][0] * 10  # Очки за пулю
            self.__result[i] += sum(self.__data[i][1])  # Очки за висты
            self.__result[i] -= self.__data[i][2] * 2  # Штраф за гору
            for j in range(len(self.__data)):
                if i != j:
                    self.__result[i] += self.__data[j][2]  # Очки за чужую гору
                    self.__result[i] -= self.__data[j][1][i]  # Штраф за чужие висты
                    self.__result[i] -= int(self.__data[j][0] / 2) * 10  # Штраф за чужую пулю
        return self.__result

    def save(self, file: str):
        players = ["First", "Second", "Third"]
        base = et.Element("data", {"points": str(self.__result[0])})
        for i in range(len(self.data)):
            el = et.SubElement(base, players[i])
            sub1 = et.SubElement(el, "Bullet")
            sub1.text = str(self.data[i][0])
            sub2 = et.SubElement(el, "Whists")
            for j in range(3):
                sub = et.SubElement(sub2, players[j])
                sub.text = str(self.data[i][1][j])
            sub3 = et.SubElement(el, "Mount")
            sub3.text = str(self.data[i][2])
        tree = et.ElementTree(base)
        tree.write(file)

    @property
    def data(self):
        return self.__data
