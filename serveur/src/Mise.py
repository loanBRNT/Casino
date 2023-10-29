COULEUR = {'rouge': [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
           'vert': [0],
           'noir': [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]}


class Mise:
    def toString(self):
        return self.pseudo + " a gagné " + str(self.montant)

    def __init__(self, pseudo, montant, regle):
        self.regle = {}
        self.pseudo = pseudo
        self.montant = montant
        print(regle)
        self.regle['couleur'] = regle

    def isWin(self, num):
        if self.regle['couleur'] != 'None':
            if num in COULEUR[self.regle['couleur']]:
                self.montant = self.montant * 2
                return True
        return False
