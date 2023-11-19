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
        if regle == "rouge" or regle == "noir":
            self.regle['couleur'] = regle
        elif regle == "pair" or regle == "impair":
            self.regle['parite'] = regle
        elif regle == "1-12" or regle == "13-24" or regle == "25-36":
            self.regle['tranche'] = regle
        elif regle =="tier1" or regle =="tier2" or regle =="tier3":
            self.regle['tier'] = regle
        else:
            self.regle['numero'] = regle

    def isWin(self, num):
        if 'couleur' in self.regle:
            if num in COULEUR[self.regle['couleur']]:
                self.montant = self.montant * 2
                return True
        elif 'parite' in self.regle:
            if num % 2 == 0 and self.regle['parite'] == "pair":
                self.montant = self.montant * 2
                return True
            elif num % 2 != 0 and self.regle['parite'] == "impair":
                self.montant = self.montant * 2
                return True
        elif 'tranche' in self.regle:
            if num < 13 and self.regle['tranche'] == "1-12":
                self.montant = self.montant * 3
                return True
            elif 12 < num < 25 and self.regle['tranche'] == "13-24":
                self.montant = self.montant * 3
                return True
            elif 24 < num and self.regle['tranche'] == "25-36":
                self.montant = self.montant * 3
                return True
        elif 'tier' in self.regle:
            if num % 3 == 0 and self.regle['tier'] == "tier1":
                self.montant = self.montant * 3
                return True
            if (num+1) % 3 == 0 and self.regle['tier'] == "tier2":
                self.montant = self.montant * 3
                return True
            if (num+2) % 3 == 0 and self.regle['tier'] == "tier3":
                self.montant = self.montant * 3
                return True
        elif 'numero' in self.regle:
            try:
                if num == int(self.regle['numero']):
                    self.montant = self.montant * 36
                    return True
            finally:
                return False
        return False
