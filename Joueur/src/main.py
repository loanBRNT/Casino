#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Joueur version 1.0
#  Created by Ingenuity i/o on 2023/11/06
#
# "no description"
#

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys
import pygame
import io
import base64
import os
from Joueur import *
port = 5670
agent_name = "Joueur"
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
        assert isinstance(agent_object, Joueur)
        # add code here if needed
    except:
        print(traceback.format_exc())


def on_freeze_callback(is_frozen, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Joueur)
        # add code here if needed
    except:
        print(traceback.format_exc())

# services
def Mise_effectuee_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Joueur)
        succes = tuple_args[0]
        agent_object.Mise_effectuee(sender_agent_name, sender_agent_uuid, succes)
    except:
        print(traceback.format_exc())


def Gain_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Joueur)
        sommeGagnee = tuple_args[0]
        agent_object.Gain(sender_agent_name, sender_agent_uuid, sommeGagnee)
    except:
        print(traceback.format_exc())


def snapshotResult_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Joueur)
        image =arguments[0]
        agent_object.snapshotResult(sender_agent_name, sender_agent_uuid, image)
    except:
        print(traceback.format_exc())

def select_zone(position):

    x,y=position
    if y <window_height-image_height+6 or x>image_width:
        return None
    else:
        if y<window_height-image_height+225 and x <80: # cas du zero
                return 0
        if y < window_height - image_height + 225:
            if x>680:
                y = y - (window_height - image_height + 6)
                if (y // 75) == 0:
                    return "tier1"
                elif (y // 75) == 1:
                    return "tier2"
                else:
                    return "tier3"

            else:
                x=x-80
                colonne= x//50
                y=y-(window_height-image_height+6)
                ligne= y//75 +1
                ligne=abs(ligne-3)+1
                return str(ligne+3*colonne)

        elif y<window_height-image_height+275:
            #cas des tiers colonnes
            if x < 80 or x > 680:
                return None
            else:
                x=x-80
                if(x//200)==0:
                    return "1-12"
                elif(x//200)==1:
                   return "13-24"
                else:
                    return "25-36"
        else:
             #cas des pairs
            if x<80 or x > 680 :
                return None
            else:
                x=x-80
                if(x//100)==0:
                    return "1-18"
                elif(x//100)==1:
                    return "pair"
                elif (x // 100) == 2:
                    return "rouge"
                elif (x // 100) == 3:
                    return "noir"
                elif (x // 100) == 4:
                    return "impair"
                else:
                    return "19-36"

def select_montant_mise(position):
    x,y=position
    y = y - (window_height - image_height + 6)
    if (y // 75) == 0:
        print("mise 5")
    elif (y // 75) == 1:
        print("mise 25")
    elif (y//75)==2:
        print("mise 50")
    else:
        print("mise 100")





if __name__ == "__main__":
    window_height=920
    window_width=1080


    #creation fenetre
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    image_height=334
    image_width=736
    image = pygame.image.load('../../tapis_roulette.png')
    w=image_width+10
    h=window_height-image_height
    screen.blit(image, (0,window_height-image_height))
    list_image=os.listdir("../../jetons")
    list_image.sort()
    for image in list_image:
        pygame.draw.rect(screen,(0,0,0),(w,h,75,75))
        image_path= os.path.join("../../jetons/",image)
        image_jeton = pygame.image.load(image_path)
        screen.blit(image_jeton, (w,h))
        h = h + image_jeton.get_height()+5

    clock = pygame.time.Clock()
    running = True
    dt = 0

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
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(device))
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

    agent = Joueur()

    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.observe_freeze(on_freeze_callback, agent)

    igs.service_init("Mise_effectuee", Mise_effectuee_callback, agent)
    igs.service_arg_add("Mise_effectuee", "succes", igs.BOOL_T)
    igs.service_init("Gain", Gain_callback, agent)
    igs.service_arg_add("Gain", "sommeGagnee", igs.DOUBLE_T)
    igs.service_init("snapshotResult", snapshotResult_callback,agent)
    igs.service_arg_add("snapshotResult", "base64Png", igs.DATA_T)

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
        while (not is_interrupted) and igs.is_started():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        prev_mouse_pos = pygame.mouse.get_pos()
                        x,y=prev_mouse_pos
                        #si click tapis de mise
                        if( y >window_height-image_height+6 and x<image_width):
                            value=select_zone(prev_mouse_pos)
                            #on envoie au serveur la mise
                            igs.service_call("serveur", "Miser", (5.0,value), "")

                        if( y >window_height-image_height+6 and x>image_width and x<image_width+80):
                            select_montant_mise(prev_mouse_pos)
                # fill the screen with a color to wipe away anything from last frame
            igs.service_call("Whiteboard","snapshot",(),"")
            if agent.current_image==None :
                NoImage=True
                # print("Pas d'image du whiteboard")
            else:
                output = io.BytesIO(base64.b64decode(agent.current_image))
                image = pygame.image.load(output)

                screen.blit(image, (0, 0))

            #

            pygame.display.flip()
            time.sleep(0.02)

            # flip() the display to put your work on screen


            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            #dt = clock.tick(60) / 1000


    if igs.is_started():
        igs.stop()
