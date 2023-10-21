COULEUR = {'rouge':[1,3,5,7,9,12,14,16,18,
                     19,21,23,25,27,30,32,34,36],'vert':[0]}

class Mise:
    pseudo = None
    montant = 0
    regle = {'couleur':'None'}

    def __init__(self,pseudo,montant,regle):
        self.pseudo = pseudo
        self.montant = montant
        self.regle['couleur'] = regle


    def isWin(self,num):
        if self.regle['couleur'] != 'None':
            if num in COULEUR[self.regle['couleur']]:
                return True
        return False