#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  serveur version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#
# "no description"
#

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys
import base64

from serveur import *

global id_textLastGagnant, id_textBigGagnant, id_roulette

port = 5670
agent_name = "serveur"
device = None
verbose = False
is_interrupted = False

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")


def return_iop_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"


def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"


def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Serveur)
        # add code here if needed
    except:
        print(traceback.format_exc())


def on_freeze_callback(is_frozen, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Serveur)
        # add code here if needed
    except:
        print(traceback.format_exc())


# services
def Miser_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Serveur)
        montant = tuple_args[0]
        cible = tuple_args[1]
        agent_object.Miser(sender_agent_name, sender_agent_uuid, montant, cible)
        s = sender_agent_name + "/" + sender_agent_uuid + " a misé " + str(montant) + " sur " + str(cible)
        igs.service_call("Whiteboard", "chat", s, "")
        igs.service_call(sender_agent_uuid, "Mise_effectuee", True, "")
    except:
        print(traceback.format_exc())


def Element_Create_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        global id_textLastGagnant, id_roulette, id_textBigGagnant
        agent_object = my_data
        assert isinstance(agent_object, Serveur)
        '''
        id = tuple_args[0]
        if id_roulette == -1:
            id_roulette = id
        elif id_textLastGagnant == -1:
            id_textLastGagnant = id
        elif id_textBigGagnant == -1:
            id_textBigGagnant = id
        '''
    except:
        print(traceback.format_exc())


if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.definition_set_version("1.0")
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(
                device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = Serveur(20)

    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.observe_freeze(on_freeze_callback, agent)

    igs.output_create("title", igs.STRING_T, None)

    igs.service_init("Miser", Miser_callback, agent)
    igs.service_init("elementCreated", Element_Create_callback, agent)
    igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)
    igs.service_arg_add("Miser", "montant", igs.DOUBLE_T)
    igs.service_arg_add("Miser", "cible", igs.STRING_T)

    igs.start_with_device(device, port)
    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)

    if interactive_loop:
        print_usage_help()
        while True:
            command = input()
            if command == "/quit":
                break
            elif command == "/help":
                print_usage_help()
    else:
        t = 1
        # while (not is_interrupted) and igs.is_started() and agent.roulette.etat == "ATTENTE":

        id_textLastGagnant, id_textBigGagnant, id_roulette = 1, 2, -1

        while (not is_interrupted) and igs.is_started():
            time.sleep(1)
            if agent.roulette.etat == "ATTENTE":
                igs.service_call("Whiteboard", "clear", None, "")


                with open('../../wheel.png', 'rb') as image_file:
                    # Lire l'image et la convertir en base64
                    encoded_string = base64.b64encode(image_file.read()).decode()

                arg = ('https://raw.githubusercontent.com/loanBRNT/Casino/main/wheel.png', 200.0, 200.0)
                id_roulette = igs.service_call("Whiteboard", "addImageFromUrl", arg, "")

                if id_roulette == -1:
                    continue

                arg = (agent.roulette.getStringLastWinner(), 0.0, 10.0, "black")
                igs.service_call("Whiteboard", "addText", arg, "")

                arg = (agent.roulette.getStringBigWinner(), 0.0, 50.0, "black")
                igs.service_call("Whiteboard", "addText", arg, "")

                # arg = (id_roulette, "width",400 )
                # igs.service_call("Whiteboard","setDoubleProperty", arg, "")

                # arg = (id_roulette, "height", 400)
                # igs.service_call("Whiteboard", "setDoubleProperty", arg, "")

                agent.roulette.etat = "MISAGE"
                agent.titleO = "Faites vos jeux"

            if agent.roulette.etat == "MISAGE":
                if agent.majTimerRoulette():
                    agent.titleO = "Les jeux sont faits"
                    n = agent.roulette.lancerAnimationRoulette()
                    agent.titleO = "Le numéro gagnant est " + str(n) + " !"
                    igs.service_call("Whiteboard", "chat", "Le numéro gagnant est le " + str(n), "")
                    agent.checkWinner()
                    time.sleep(3)
                    agent.titleO = "Faites vos jeux"
                    agent.relancerPartie(20, id_textLastGagnant, id_textBigGagnant)
                    igs.service_call("Whiteboard","snapshot",(),"")

    if igs.is_started():
        igs.stop()
