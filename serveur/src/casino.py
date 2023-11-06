import random
import Mise
import time


class Casino:
    num = None  # Num sorti
    miseInGame = []
    timer = 0
    etat = "ATTENTE"  # ATTENTE | MISAGE | EN COURS

    histo = []  # Historique des derniers tirages
    lastWinner = {'pseudo': "XXX", 'gain': 0}  # Stocke les informations du dernier plus gros gagnant du coup
    bigWinner = {'pseudo': "XXX", 'gain': 0}  # Stocke les informations du plus gros gagnant de la session

    def __init__(self, valTimer):
        self.timer = valTimer

    def getStringLastWinner(self):
        return "Dernier Gagnant : " + self.lastWinner['pseudo'] + " - " + str(self.lastWinner['gain'])

    def getStringBigWinner(self):
        return "Meilleur Gagnant : " + self.bigWinner['pseudo'] + " - " + str(self.bigWinner['gain'])

    def tirerUneCase(self):
        self.num = random.randint(0, 36)
        self.histo.append(self.num)
        return self.num

    def ajouterUneMise(self, pseudo, montant, regle):
        mise = Mise.Mise(pseudo, montant, regle)
        self.miseInGame.append(mise)

    def trouverGagnant(self):
        gagnants = []
        for mise in self.miseInGame:
            if mise.isWin(self.num):

                if self.lastWinner['gain'] < mise.montant:
                    self.lastWinner['gain'] = mise.montant
                    self.lastWinner['pseudo'] = mise.pseudo

                if self.bigWinner['gain'] < mise.montant:
                    self.bigWinner['gain'] = mise.montant
                    self.bigWinner['pseudo'] = mise.pseudo

                gagnants.append(mise)
        return gagnants

    def relancerPartie(self, valeur):
        self.etat = "MISAGE"
        self.timer = valeur
        self.lastWinner = {'pseudo': "XXX", 'gain': 0}
        self.miseInGame.clear()

    def majTimerRoulette(self):
        self.timer -= 1
        return self.timer

    def lancerAnimationRoulette(self):
        self.etat = "EN COURS"
        time.sleep(3)  # Peut-être remplacer avec un Thread apres
        return self.tirerUneCase()
