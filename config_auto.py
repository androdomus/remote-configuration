##Ce programme a pour finalité  l'automatisation des tâches répétitives###
### effectué lors de la configuration d'un équipement réseau

# -*- coding: utf8 -*-

#Chargement des librairies neccéssaire à l'exécution du script
from netmiko import (ConnectHandler, NetmikoTimeoutException) #Permet la connexion en SSH aux appareil
from paramiko.ssh_exception import SSHException
from getpass import getpass
import json #Permet le chargement lal lecture et l'écriture de donnée à l'intérieur et à l'extérieur du script
import logging

print ('\n\n####################SCRIPT PARAMETRAGE RESEAU#################\n\n') 

logging.basicConfig(filename='config_auto_device.log', filemode='w', level=logging.WARNING,\
format='%(asctime)s -- %(lineno)d -- %(funcName)s -- %(levelname)s -- %(message)s')
    
def get_infos():
                    ##Fonction permettant par l'intéractivité la collecte de données néccéssaires à 
                    ##la connexion en SSH sur les machines. Les données sont ensuite placées dans des variables
                    ##sous forme de chaînes de caractère, de listes ou de dictionnaire utilisables hors du script.
                    
    global list_devices     #Declaration en variable global afin de pouvoir les utiliser hors de la fonction 
    global all_device_dict
    try:                    #Test l'existence des variables 
        list_devices        #Vérifie si la liste des appareils existe
        all_device_dict     #Vérifie si la liste des informations des appareils existe
    except NameError:       #Gestion de l'erreur afin de pouvoir poursuivre le script   
        list_devices = []   #Création des variables si la fonction n'a pas été encore exécutée
        all_device_dict = []

    print('\n########### 1ère Partie Enregistrement des informations de connexion ###########\n')
      
    nbresw_answer = input("\nCombien de machines à enregistrer? >>>>>")
    
    try:
        i = int(nbresw_answer)          #Test si la réponse déclarée en variable est un chiffre.
    except (ValueError) as error:
        logging.warning(error) 		#Envoi de l'erreur dans le fichier de log.
        print('Valeur incorrecte...Indiquez un nombre entier.\nRetour au menu d\'Enregistrement\n') #Affiche le message.    
        get_infos()			#Relance la fonction 	
        
    for i in range(0,i):                #La boucle délimitée par la variable nbresw_answer enregistre les machines dans une liste.
        if int(nbresw_answer) > 1 and len(list_devices) >= 1  :  #Si il n'y a q'une machine, le message n'est pas affiché.
            print("\nEnregistrement informations de la machine suivante\n")

        global device_name               #Déclaration en variable global afin de pouvoir l'utiliser hors de la fonction. 
        device_name = input("""\nIndiquez le nom de la machine: >>>>>""") 				    #Les des données néccessaire
        list_devices.append(device_name)       #Ajout du nom de l'appareil à chaque tour de boucle	    # à la connexion distante des machines
        answer_ip = input("""\nIndiquez l\'addresse IP de l\'équipement sans son masque: >>>>>""")	    # sont déclarées dans les variables,   
        answer_username = input("""\nIndiquez le nom de l\'utilisateur: >>>>>""")			    #par l'intéractivité entre le script	
        print("""\nIndiquez le mot de passe pour la connexion SSH ainsi que celui du mode privilégié:""",)  #et l'utilisateur.
        answer_mdp = getpass() #Cache le mot de passe indiqué par l'utilisateur
	
        file_json = device_name + "_connexion.json"       #Variable distinguant les machines afin de creer leur fichier JSON de connexion. 
        device_dictionnary = device_name + "_dictionnary" #Variable distinguant les dictionnaires regroupant les données des machines.
    
        #Création du dictionnaire contenant les infos de connexion de chaque machine.
        device_dictionnary = {
        "host": answer_ip,
        "username": answer_username,
        "password": getpass(),
        "secret": answer_mdp,
        "device_type": "cisco_ios",
        }
        try:
            net_connect = ConnectHandler(**device_dictionnary)  #Teste si la connexion en SSH est possible.
            all_device_dict.append(device_dictionnary) 		#Ajoute le dictionnaire à la liste à chaque tour de boucle.    
            
            use_json(file_json, device_dictionnary)		#Enregistre le dictionnaire de la machine dans une fichier JSON.  
        except (NetmikoTimeoutException, SSHException, NameError, ValueError) as error:		#Récupération de l'erreur,
            logging.warning(error)								#et envoi dans le fichier log.	
            print("Connexion impossible, vérifiez vos informations de connexion... Retour à l'enregistrement des informations.")
            get_infos()						

        #Enregistrement du fichier JSON listant tous les appareils.         
        if int(nbresw_answer) == len(list_devices): 	#Si le nombre machine à enregistrer = nombre d'objets de la liste de machine,
            try:                                    	#Les tests suivants sont effectués: 		                                                    
                tf = open("list_devices.json", "r")     #-Ouverture (en mode lecture) de la liste des machines existantes.                                 
                device = json.load(tf)			#-Chargement de la liste dans la variable device.
                list_devices.extend(device)		#-Ajoute dans list_devices les machines de la liste devices.
                tf = open("list_devices.json", "w")	#-Ouverture (en mode édition) de la liste des machines.
                json.dump(list_devices,tf) 		#-Enregistrement de la liste modifiée dans le fichier JSON.
                tf.close()                		#-Fermeture du fichier 
            except (FileNotFoundError, NameError) as error: 	#En cas d'erreurs:
                use_json("list_devices.json", list_devices) 	#-Lancement de la fonction simple avec les paramètres définis.   
                logging.warning(error)				#-Envoi de l'erreur dans le fichier log

    for device_dictionnary in all_device_dict:     #Pour chaque dictionnaire de la liste:                                                     
        connexion(r_data = device_dictionnary) 	   #Lancement de la fonction pour afficher la conexion distante réalisée.
                    
def get_config():
                          ##Fonction permettant par l'intéractivité la collecte des commandes néccéssaires à  
                          ##la mise en place des configurations sur les machines distantes. L'utilisateur peut choisir 
                          ##aussi  de quitter le script  ou d'être redirigé vers la partie enregistrement.

     print ('\n########## 2ème partie:Configuration à mettre en place###########\nRecherche des machines enregistrées...\n')

     try:                                       #Les tests suivants sont effectués:
        tf = open("list_devices.json", "r")     #-Ouverture du fichier JSON contenant la liste des machines,
        devices = json.load(tf)                 #-Chargement du contenu du fichier dans une variable pour l'afficher.
        print("Récupération des machines et de leurs fichiers de connexion.\nLes machines enregistrées sont:", devices,"\n")
     except (FileNotFoundError, NameError) as error:  	#En cas d'erreur:
        logging.warning(error) 				#Redirection des erreurs possibles dans le fichier log, affichage d'un averissement.
        print("\nLes variables globales n'existent pas dans l'exécution actuelle du script...\nAucunes machines et fichiers de connexion enregistrés.\nRetour au menu précédent....")
        get_infos()
                                    
     global  device_name
     try:
        device_name = input('\nIndiquez le nom des machine à configurer séparé par un tiret\nExemple: switch1-switch3\nRéponse: >>>>>')
        device = device.split("-")  
        devices_config = []                       #Création d'une liste contenant toutes les infos de connexion 
        for device in device:                     #La boucle lance la fonction et permet d'ouvrir des fichier de connexion   
            tf = open(device, "r") 
            use_json(file_json = device, data =1) #des machines indiquées par l'utilisateur. A chaque tour de boucle,
            devices_config.append(r_data)         #les donneés de connexions sont ajoutées à la liste principale devices_config.   
     except (FileNotFoundError, NameError) as error:
        logging.warning(error) 
        print('\nLe(s)équipement(s) est/sont incorect(s):(plusieurs raisons possibles)\n-Ils ne sont pas séparés par un tiret.\n-Ils ne font pas partie des équipements configuré\nRetour au menu des configurations...')
        get_config()
     
     global user_config
     user_config = input("\n-Configuration de VlANS: Tapez 1\n-Configuration d\'interface: Tapez 2\n-Configuration par fichier: Tapez 3\n-Retour à l'enregistrement des équipements: Tapez 4\n>>>>> Réponse:")

     if user_config == "1":
        all_vl_cmd =[]   #Création en variable d'une liste vide de toutes les configurations de vlan
        nbr_config = input('\n-Nombre de vlan à configurer: >>>>>')
        i = int(nbr_config) 

        for i in range(i):  #Boucle récupérant à chaque tour les données des variables vlan
            vlan_nbr = input('\nAjouter le numéro du VlAN: >>>>>>')
            vlan_name = input('\nIndiquez le nom du VlAN: >>>>>>')    
            vlan_ip = input('\nIndiquez l\' addresse du VlAN avec son masque en annotation décimale: >>>>>')
       
            i = len(nbr_config)
            for i in range(0, i):  #La boucle crée à chaque tour une liste des commande                 
                model_vlan = ["vl ", "name ", "int vl ", "ip add ", "do wr"]
                             
                model_vlan[0] = model_vlan[0] + vlan_nbr  #Création de la liste des configurations config_command, 
                model_vlan[1] = model_vlan[1] + vlan_name  #en ajoutant les données des variable vlan,
                model_vlan[2] = model_vlan[2] + vlan_nbr   # aux chaînes de caractère de la list de configuration 
                model_vlan[3] = model_vlan[3] + vlan_ip    #basique(model_vlan) et selon leurs emplacements dans la liste. 
                config_command = model_vlan

                all_vl_cmd.append(config_command) #Chaque liste de commande est rajoutée à liste principale 
                print(all_vl_cmd)

        for device in devices_config:           #Pour chaque fichiers de connexion contenu dans la liste,
            connexion(r_data = device)          #lance la fonction de connexion SSH
            for config_command in all_vl_cmd:   #et pour chaque liste de commande contenu dans la liste
                    send_config(config_command) #lance la fonction d'envoi de commande sur la machine.             
        print('Retour au menu principal')
        choice_menu()
                        
     elif user_config == "2":
        all_int_cmd = []
        nbr_rg = input('\nNombre de range à configurer: >>>>>>')
        i = int(nbr_rg) 

        for i in range(i):
            int_mod = input('\nIndiquez le mode du range:\nAccess tapez 1\nTrunk tapez 2\nRéponse: >>>>>>')            
            int_rg = input('\nIndiquez le type d\'interface, son  l\'interface ou le range (exemple fa0/1-24 - gi0/1,): >>>>>> ')
            int_vl = input('\nIndiquez le(s) VlAN(s) autorisé(s) selon le mode défine (exemple mode access 3 mode trunk 4-8): >>>>>>\n')
                   
            i = len(nbr_rg)
            for i in range(0, i): #La boucle crée à chaque tour une liste des commande  
               
                model_access = ["int range ", "swit mod acc  ", "swit acc vl ", "do wr"]
                model_trunk = ["int range ", "swi tr enc do  ", "switch mod tr", "swit tr all vl ", "do wr"]
        
                if int_mod == "1":                             
                    model_access[0] = model_access[0] + int_rg      
                    model_access[2] = model_access[2] + int_vl                                                
                    config_command = model_access                   #Selon le choix de l'utilisateur (variable int_mod)
                                                                    #Création de la liste des configurations config_command, 
                elif int_mod == "2":                                #en ajoutant les données des variable interfaces,
                    model_trunk[0] = model_trunk[0] + int_rg        #aux chaînes de caractère de la list de configuration basique 
                    model_trunk[3] = model_trunk[3] + int_vl        #(model_access ou mode_trunk) et selon leurs emplacements dans la liste
                    config_command = model_trunk
                     
                all_int_cmd.append(config_command)                     #Chaque liste de commande est rajoutée à liste principale 
                print(all_int_cmd)

        for device in devices_config:                   #Pour chaque fichiers de connexion contenu dans la liste,
            connexion(r_data = device)                  #lance la fonction de connexion SSH
            for config_command in all_int_cmd:          #et pour chaque liste de commande contenu dans la liste   
                send_config(config_command)             #lance la fonction d'envoi de commande sur la machine.    
        print('Retour au menu principal')
        choice_menu()

     elif user_config == "3":
        fichier_txt = input('\nIndiquez le fichier contenant la configuration à appliquer: >>>>')
        for device in devices_config:
            connexion(r_data = device)
            send_config(config_command = fichier_txt)
        print('Retour au menu principal')
        choice_menu()
           
     elif user_config == "4":
        print ('\nRetour au menu Enregistrement des machines... \n')
        get_infos()
     else:
        print('\nLa réponse ne fait pas partie des proposition.\nRetour au menu des configurations.')
        get_config()
                
def use_json(file_json, data):      ##Fonction permettant la création, la lecture, l'écriture de fichiers au format
                                    ##JSON. Les types de données (entier-boléeen-string-ect...) et la forme sous laquelles
                                    ##elles sont insérées (dictionnaires-listes-ect...)sont utilisables partout dans le script
                                    ##Cette fonction dépend du module JSON qui doit être importé en amont."""
    global r_data
    try:
        tf = open(file_json, "r")       #Test l'ouvertue d'un fichier dont le nom est le contenu de la variable file_json
        r_data = json.load(tf)
    except FileNotFoundError:           #Poursuit le script malgré l'erreur en créeant le fichier dont le nom est le contenu
        tf = open(file_json, "w")       #dans la variable.
        json.dump(data,tf)              #Les données contenu dans la variable data sont écrite sur le fichier. 
        tf.close()                      #
        tf = open(file_json, "r")       #Après fermeture du fichier ce dernier est ouvert en lecture pour chargé les données
                           #dans une variable qui est déclarée en globale pour être utilisé hors de la fonction.
        r_data = json.load(tf)

def connexion(r_data):   
                            ##Fonction permettant la connexion en SSH aux machines pour lesquelles
                            ##les données neccessaires à la connexion ont été envoyées en paramètre.
                            ##Cette fonction dépend du module Netmiko qui doit re importé en amont                      
    global net_connect
    try:            #Après Déclariation de la variable global net_connect test des instructions de la fonction.
        print('################ Connexion SSH en cours ################') 
        net_connect = ConnectHandler(**r_data)  #Déclaration de la variable dont le contenu est une fonction du module Netmiko 
        print(net_connect.find_prompt())        #permettant via un dictionnaire passé en paramètre la connexion SSH à la machine,
                                                #ainsi que d'autres actions comme l'affichage du prompt ou l'envoi de commande.
        print('-------------------- Connexion établie --------------------')
    except (NetmikoTimeoutException, SSHException, NameError) as error: #Les erreurs de connexions sont affichées ainsi qu'un message,
        logging.warning(error)                                                    #avant le renvoi au menu principal.
        print("Connexion impossible:(plusieurs raisons possibles)\n-Vérifiez vos informations de connexion.\nConnexion trop longue à établir.\nRetour à l'enregistrement des informations.\n")
        choice_menu()
    
def send_config(config_command):        ##Fonction permettant l'envoi de configuration à la machine.
    try:
        net_connect.enable()           #Autorise le mode privilège de la machine.
        net_connect.find_prompt()      #Affiche le prompt.
        if user_config == "1" or user_config == "2":
            output = net_connect.send_config_set(config_command)
        elif user_config == "3":
            output = net_connect.send_config_from_file(config_command)
        print(output)
        print('\n\n---------------- Configuration terminée -----------------\n \n')
    except (NetmikoTimeoutException, SSHException, NameError, FileNotFoundError) as error:   #Les erreurs de connexions sont affichées ainsi qu'un message,
        logging.warning(error)                                                       #avant le renvoi au menu de configuration.
        print ('Une erreur s\'est produite. Vérifiez le fichier log ligne...Retour au menu de Configuration...')
    
def choice_menu():          ##Fonction permettant le choix entre les différentes actions à effectuer. 
    
    devices_exist = input("""Quelle est l\'action à effectuer?\n
    Enregistrement un nouvel appareil: Tapez 1 
    Congiguration d'un appareil connu: Tapez 2
    Quitter le script: Tapez 3
    Réponse: >>>>>""")
                                   #Enregistre le choix d'action à effectuer par le contenu de la variable.
    if devices_exist == "1":        #Exécute la fonction d'enregistrement suivie de la 
        get_infos()                 #fonction de configuration si la variable contient 1.
        get_config()

    elif devices_exist == "2":      #Exécute la fonction de configuration si la variable contient 2.    
        get_config()

    elif devices_exist == "3":      #Affiche le message et quitte le script si la variable contient 3.        
        print('\nFermeture du script\n-----------------------------\n')
      
    else :
        print('\nLa réponse ne fait pas partie des choix proposés... \nRetour au menu principal...\n\n\n')
        choice_menu()    
try:
    choice_menu()      #Exécute le script via cette fonction.                 
except (NameError, ModuleNotFoundError) as error:
    logging.warning(error)  #avant le renvoi au menu de configuration.
    print ('\nModule(s) neccessaires non installés.\nVoir le fichier de log "config_auto_device.log".')
    print('Pour installer le module manquant, exécuter la commande suivante: pip install "nom-du-module')
