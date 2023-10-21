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
    def __init__(self, valTimerInit):
        # inputs
        self.testI = None

        # outputs
        self._gainO = None

        self.roulette = casino.Casino(valTimerInit)

    # outputs
    @property
    def gainO(self):
        return self._gainO

    @gainO.setter
    def gainO(self, value):
        self._gainO = value
        if self._gainO is not None:
            igs.output_set_int("gain", self._gainO)

    # services
    def Miser(self, sender_agent_name, sender_agent_uuid, montant, couleur):
        print(sender_agent_name, " a misé ", montant, " sur ", couleur)
        self.roulette.ajouterUneMise(sender_agent_name,montant, couleur)


