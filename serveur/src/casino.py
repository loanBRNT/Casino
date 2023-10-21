import random
import Mise
import time


class Casino:
    num = None  # Num sorti
    miseInGame = []
    timer = 0
    etat= "ATTENTE" #   ATTENTE | MISAGE | EN COURS

    histo = []  # Historique des derniers tirages
    lastWinner = {'pseudo': "XXX", 'gain': 0}  # Stocke les informations du dernier plus gros gagnant du coup
    bigWinner = {'pseudo': "XXX", 'gain': 0}  # Stocke les informations du plus gros gagnant de la session

    def __init__(self,valTimer):
        self.timer = valTimer

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
                gagnants.append(Mise)
        return gagnants

    def relancerPartie(self,valeur):
        self.etat = "MISAGE"
        self.timer = valeur

    def majTimerRoulette(self):
        self.timer -= 1
        return self.timer

    def lancerAnimationRoulette(self):
        self.etat = "EN COURS"
        time.sleep(3) #Peut etre remplacer avec un Thread apres
        return self.tirerUneCase()