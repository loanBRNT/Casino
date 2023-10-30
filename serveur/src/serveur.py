#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  serveur.py
#  serveur version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#
# "no description"
#
import ingescape as igs
import casino


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Serveur(metaclass=Singleton):
    timerID = -1

    def __init__(self, valTimerInit):
        self._titleO = None
        self.roulette = casino.Casino(valTimerInit)

    # outputs
    @property
    def titleO(self):
        return self._titleO

    @titleO.setter
    def titleO(self, value):
        self._titleO = value
        if self._titleO is not None:
            igs.output_set_string("title", self._titleO)

    # services
    def Miser(self, sender_agent_name, sender_agent_uuid, montant, cible):
        print(sender_agent_name, " a misé ", montant, " sur ", cible)
        self.roulette.ajouterUneMise(sender_agent_name, montant, cible)

    def majTimerRoulette(self):
        t = self.roulette.majTimerRoulette()
        self.titleO = "Faites vos jeux : " + str(t)
        if t == 0:
            return True
        if t % 5 == 0:
            s = "Prochain lancé dans " + str(t) + " secondes"
            print(s)
            igs.service_call("Whiteboard", "chat", s, "")
        return False

    def checkWinner(self):
        gagnants = self.roulette.trouverGagnant()
        for g in gagnants:
            print(g.toString())
            igs.service_call("Whiteboard", "chat", g.toString(), "")


'''
- Comment fixer la position des éléments sur le whiteboard
- String ne s'update pas
'''