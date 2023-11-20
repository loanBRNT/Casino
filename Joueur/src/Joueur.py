#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Joueur.py
#  Joueur version 1.0
#  Created by Ingenuity i/o on 2023/11/06
#
# "no description"
#

from tkinter import *
from tkinter import ttk


import ingescape as igs


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Joueur(metaclass=Singleton):



    def __init__(self):
        self.cagnotte=20
        self.current_image=None


    # services
    def Mise_effectuee(self, sender_agent_name, sender_agent_uuid, succes):
        print("chokbar")
        pass



    def Gain(self, sender_agent_name, sender_agent_uuid, sommeGagnee):
        self.cagnotte+=sommeGagnee
        pass

    def snapshotResult(self, sender_agent_name, sender_agent_uuid, image):
        self.current_image=image
        pass






