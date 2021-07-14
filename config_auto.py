#!/usr/bin/python
# -*- coding: utf8 -*-
#####################################################################################################################
##                                                                                                                 ##
##                                                 config_auto.py                                                  ##                                
##                                                                                                                 ##                                                                                      
#####################################################################################################################                                                                                                                          
##Auteur:   Laurent Nero                                                                                           ##                                  
##Version:      1                                                                                                  ##
##Date:     11/07/2021												   ##
#####################################################################################################################
##                                                 Description                                                     ##
#####################################################################################################################                                                                                                                 ##                                                               
##Ce script peut être utilisé pour la  conception, la configuration et l'administration de réseau informatique.    ##
##Les informations de configurations sont collectées puis envoyée sur les équipements (switch-routeur-serveur)     ##
##après initialisation de la connexion distante.                                                                   ##
#####################################################################################################################

#Importation des librairies et fonctions incluses, neccéssaires à l'exécution du script
from netmiko import (ConnectHandler, NetmikoTimeoutException) #Initialise les connexions en SSH aux appareil,
from paramiko.ssh_exception import SSHException               # et gere des messages d' erreur.  
from getpass import getpass             #Cache les mot de passe tapé sur l'interface de commande
import json                 #Crée des fichier JSON dont le contenu est exploitable par le script.
import logging              #Crée des log dans un format exploitable dans un fichier.
    
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
        logging.warning(error)      #Envoi de l'erreur dans le fichier de log.
        print('Valeur incorrecte...Indiquez un nombre entier.\nRetour à la 1ère Partie\n') #Affiche le message.    
        get_infos()         #Relance la fonction    
        
    for i in range(0,i):                #La boucle délimitée par la variable nbresw_answer enregistre les machines dans une liste.
        if int(nbresw_answer) > 1 and len(list_devices) >= 1  :  #Si il n'y a q'une machine, le message n'est pas affiché.
            print("\nEnregistrement informations de la machine suivante\n")

                      #Déclaration en variable global afin de pouvoir l'utiliser hors de la fonction. 
        device_name = input("""\nIndiquez le nom de la machine: >>>>>""")                   #Les des données néccessaire
        list_devices.append(device_name)       #Ajout du nom de l'appareil à chaque tour de boucle      # à la connexion distante des machines
        answer_ip = input("""\nIndiquez l\'addresse IP de l\'équipement sans son masque: >>>>>""")      # sont déclarées dans les variables,   
        answer_username = input("""\nIndiquez le nom de l\'utilisateur: >>>>>""")               #par l'intéractivité entre le script    
        print("""\nIndiquez le mot de passe pour la connexion SSH ainsi que celui du mode privilégié:""",)  #et l'utilisateur.
        answer_mdp = getpass() #Cache le mot de passe indiqué par l'utilisateur
        answer_mdp_enable = getpass() #Cache le mot de passe de la CLI de la machine distante   

        file_json = device_name + "_connexion.json"       #Variable distinguant les machines afin de creer leur fichier JSON de connexion. 
        device_dictionnary = device_name + "_dictionnary" #Variable distinguant les dictionnaires regroupant les données des machines.
    
        #Création du dictionnaire contenant les infos de connexion de chaque machine.
        device_dictionnary = {
        "host": answer_ip,
        "username": answer_username,
        "password": answer_mdp,
        "secret": answer_mdp_enable,
        "device_type": "cisco_ios",
        }
        try:
            net_connect = ConnectHandler(**device_dictionnary)  #Teste si la connexion en SSH est possible.
            all_device_dict.append(device_dictionnary)      #Ajoute le dictionnaire à la liste à chaque tour de boucle.    
            
            use_json(file_json, device_dictionnary)     #Enregistre le dictionnaire de la machine dans une fichier JSON.  
        except (NetmikoTimeoutException, SSHException, NameError, ValueError) as error:     #Récupération de l'erreur,
            logging.warning(error)                              #et envoi dans le fichier log.  
            print("Connexion impossible, vérifiez vos informations de connexion... Retour à l'enregistrement des informations.")
            get_infos()                     

        #Enregistrement du fichier JSON listant tous les appareils.         
        if int(nbresw_answer) == len(list_devices):     #Si le nombre machine à enregistrer = nombre d'objets de la liste de machine,
            try:                                        #Les tests suivants sont effectués:                                                             
                tf = open("list_devices.json", "r")     #-Ouverture (en mode lecture) de la liste des machines existantes.                                 
                device = json.load(tf)          #-Chargement de la liste dans la variable device.
                list_devices.extend(device)     #-Ajoute dans list_devices les machines de la liste devices.
                tf = open("list_devices.json", "w") #-Ouverture (en mode édition) de la liste des machines.
                json.dump(list_devices,tf)      #-Enregistrement de la liste modifiée dans le fichier JSON.
                tf.close()                      #-Fermeture du fichier 
            except (FileNotFoundError, NameError) as error:     #En cas d'erreurs:
                use_json("list_devices.json", list_devices)     #-Lancement de la fonction simple avec les paramètres définis.   
                logging.warning(error)              #-Envoi de l'erreur dans le fichier log

    for device_dictionnary in all_device_dict:     #Pour chaque dictionnaire de la liste:                                                     
        connexion(r_data = device_dictionnary)     #Lancement de la fonction pour afficher la conexion distante réalisée.
                    
def get_config():
                          ##Fonction permettant par l'intéractivité la collecte des commandes néccéssaires à  
                          ##la mise en place des configurations sur les machines distantes. L'utilisateur peut choisir 
                          ##aussi  de quitter le script  ou d'être redirigé vers la partie enregistrement.

     print ('\n########## 2ème partie:Configuration à mettre en place###########\nRecherche des machines enregistrées...\n')

     try:                                       #Les tests suivants sont effectués:
        tf = open("list_devices.json", "r")     #-Ouverture du fichier JSON contenant la liste des machines,
        devices = json.load(tf)                 #-Chargement du contenu du fichier dans une variable pour l'afficher.
        print("Récupération des machines et de leurs fichiers de connexion.\nLes machines enregistrées sont:", devices,"\n")
     except (FileNotFoundError, NameError) as error:    #En cas d'erreur:
        logging.warning(error)              #Redirection des erreurs possibles dans le fichier log, affichage d'un averissement.
        print("\nLes variables globales n'existent pas dans l'exécution actuelle du script...\nAucunes machines et fichiers de connexion enregistrés.\nRetour au menu précédent....")
        get_infos()
                                         
     try:                   #Test des instructions qui suivent.
        device_name = input('\nIndiquez le nom des machine à configurer séparé par un tiret\nExemple: switch1-switch3\nRéponse: >>>>>')
        device = device_name + "_connexion.json"            #Transformation du contenu de la variable device_name:
        device = device.replace('-', '_connexion.json-')    #-Modification de l'intérieur et de la finde la chaîne de caractère.
        device = device.split("-")                          #-Chande du type en liste pour récupéré le(s) fichier(s) de connexion.
        devices_config = []                       #Création d'une liste (vide) qui contiendra toutes les infos de connexion. 
        for device in device:                       #La boucle effectue les  instructions suivantes pour chaque objet de la liste:    
            tf = open(device, "r")          #-Ouverture des fichier de connexion des machines indiquées par l'utilisateur
            use_json(file_json = device, data =1)   #-Chargement dans la variable des infos de connexion.
            devices_config.append(r_data)           #-Ajout des donneés de connexions à la liste devices_config.   
     except (FileNotFoundError, NameError) as error:            #Redirections des erreurs dans le fichier log relancement de la fonction.
        logging.warning(error) 
        print('\nLe(s)équipement(s) est/sont incorect(s):(plusieurs raisons possibles)\n-Ils ne sont pas séparés par un tiret.\n-Ils ne font pas partie des équipements configuré\nRetour au menu des configurations...')
        get_config()
     
     global user_config          #Transformation en variable globale de la réponse de l'utilisateur au menu de configuration. 
     user_config = input("\n-Configuration de VlANS: Tapez 1\n-Configuration d\'interface: Tapez 2\n-Configuration par fichier: Tapez 3\n-Retour à l'enregistrement des équipements: Tapez 4\n>>>>> Réponse:")

     if user_config == "1":
        all_vl_cmd =[]              #Création d'une liste (vide) qui contiendra toutes les configurations de vlan
        try:

            nbr_config = input('\n-Nombre de vlan à configurer: >>>>>') 
            i = int(nbr_config)             #Changement du type de la variable en nombre entier

            for i in range(i):              #Récupération à chaque tour (tour en fonction de nbre_config) des données des variables vlan
                vlan_nbr = input('\nAjouter le numéro du VlAN: >>>>>>')
                vlan_name = input('\nIndiquez le nom du VlAN: >>>>>>')    
                vlan_ip = input('\nIndiquez, si néccessaire l\' addresse du VlAN avec son masque en annotation décimale: >>>>>')
       
                i = int(nbr_config)
                for i in range(0, i):   #Création à chaque tour d'une liste des commande.                 
                    model_vlan = ["vl ", "name ", "int vl ", "ip add ", "do wr"] #Création d'une liste de commandes basiques utilisées 
                                                                                 # pour créer un VLAN sur un switch CISCO.
                    model_vlan[0] = model_vlan[0] + vlan_nbr   #Création de la liste des configurations config_command, 
                    model_vlan[1] = model_vlan[1] + vlan_name  #en ajoutant les données des variable vlan,
                    model_vlan[2] = model_vlan[2] + vlan_nbr   #aux chaînes de caractère de la liste de commandes 
                    model_vlan[3] = model_vlan[3] + vlan_ip    #basique(model_vlan) en fonction de leurs emplacements dans la liste. 
                    config_command = model_vlan

<<<<<<< HEAD
                all_vl_cmd.append(config_command) #Chaque liste de commande est rajoutée à liste principale. 
                print("Récapitulatif des configurations à envoyer:\n", all_vl_cmd)
=======
                    all_vl_cmd.append(config_command) #Chaque liste de commande est rajoutée à liste principale. 
                    print("Récapitulatif des configurations à envoyer:\n", all_vl_cmd)
>>>>>>> 2b5c54b0cfbfcf564b47bd881758a600243860e3

            for device in devices_config:           #Pour chaque fichiers de connexion contenu dans la liste devices_config:
                connexion(r_data = device)          #-Lancement de la fonction de connexion SSH
                for config_command in all_vl_cmd:       #Pour chaque liste de commande contenu dans la liste all_vl_cmd:
                    send_config(config_command)         #-Lancement la fonction d'envoi de commande sur la(es) machine(s) distante(s).             
            print('Retour au menu principal')
            choice_menu()               
            
        except (ValueError) as error:
            logging.warning(error)      #Envoi de l'erreur dans le fichier de log.
            print('Valeur incorrecte...Indiquez un nombre entier.\nRetour au choix de configuration\n') #Affiche le message.    
            get_config()         #Relance la fonction        
                        
     elif user_config == "2":
        all_int_cmd = []                #Création d'une liste (vide) qui contiendra toutes les configurations d'interfaces
        try:
            nbr_rg = input('\nNombre de range ou d\'interfaces à configurer: >>>>>>')
            i = int(nbr_rg)                 #Changement du type de la variable en nombre entier

            for i in range(i):      #Récupération à chaque tour (tour en fonction de nbre_rg) des données des variables d'interfaces
                int_mod = input('\nIndiquez le mode de configuration:\nAccess tapez 1\nTrunk tapez 2\nRéponse: >>>>>>')            
                int_rg = input('\nIndiquez le type d\'interface, le numéro de l\'interface ou le range.\nExemple interface: gi0/1 ---- Exemple de range: fa0/1-24)\nRéponse: >>>>>> ')
                int_vl = input('\nIndiquez le(s) VlAN(s) autorisé(s) selon le mode défine (exemple mode access 3 mode trunk 4-8): >>>>>>\n')
                       
                i = int(nbr_rg)
                for i in range(0, i):       #Création à chaque tour d'une liste des commande.  
                   
                    model_access = ["int range ", "swit mod acc  ", "swit acc vl ", "do wr"]  #Création de deux liste de commandes basiques utilisées
                    model_trunk = ["int range ", "swi tr enc do  ", "switch mod tr", "swit tr all vl ", "do wr"] #pour configurer les différents modes  
                                                                 #des interfaces sur un switch CISCO.
                    if int_mod == "1":                             
                        model_access[0] = model_access[0] + int_rg      
                        model_access[2] = model_access[2] + int_vl                                                
                        config_command = model_access                #Selon le choix de l'utilisateur (variable int_mod):
                                                                     #-Création de la liste des configurations config_command, 
                    elif int_mod == "2":                             #-Ajout des données des variable interfaces,
                        model_trunk[0] = model_trunk[0] + int_rg     #aux chaînes de caractère de la liste de commande basique 
                        model_trunk[3] = model_trunk[3] + int_vl     #(model_access ou mode_trunk)en fonction de  leurs emplacements dans la liste
                        config_command = model_trunk
        
                    else:
                        print('Le mode de configuration choisi est incorecte...\nRetour au choix de configuration...')
                        get_config() 
                                    
<<<<<<< HEAD
                all_int_cmd.append(config_command)                  #Chaque liste de commande est rajoutée à liste principale 
                print("Récapitulatif des configurations à envoyer:\n", all_int_cmd)
=======
                    all_int_cmd.append(config_command)                  #Chaque liste de commande est rajoutée à liste principale 
                    print("Récapitulatif des configurations à envoyer:\n", all_int_cmd)
>>>>>>> 2b5c54b0cfbfcf564b47bd881758a600243860e3

            for device in devices_config:          #Pour chaque fichiers de connexion contenu dans la liste devices_config:
                connexion(r_data = device)         #-Lancement la fonction de connexion SSH.
                for config_command in all_int_cmd:          #Pour chaque liste de commande contenu dans la liste:   
                    send_config(config_command)             #Lancement de la fonction d'envoi de commande sur la(es) machine(s) distante(s).    
            
            print('Retour au menu principal')
            choice_menu()
        except (ValueError) as error:
            logging.warning(error)      #Envoi de l'erreur dans le fichier de log.
            print('Valeur incorrecte...Indiquez un nombre entier.\nRetour au choix de configuration\n') #Affiche le message.    
            get_config()         #Relance la fonction         

     elif user_config == "3":
        fichier_txt = input('\nIndiquez le fichier contenant la configuration à appliquer: >>>>')  #Nom du fichier contenant les commandes 
        for device in devices_config:           #Pour chaque fichiers de connexion contenu dans la liste devices_config:
            connexion(r_data = device)          #-Lancement la fonction de connexion SSH.
            send_config(config_command = fichier_txt)   #Lancement de la fonction d'envoi de commande sur la(es) machine(s) distante(s).
        print('Retour au menu principal')
        choice_menu()
           
     elif user_config == "4":
        print ('\nRetour au menu Enregistrement des machines... \n')
        get_infos()
     else:                      #Si la réponses utilsateur ne correspond à aucunes des possibilités:
        print('\nLa réponse ne fait pas partie des propositions.\nRetour au choix de configuration.') #Affichage de l'avertissement.
        get_config()                    #Retour au menu de configuration.
                
def use_json(file_json, data):      ##Fonction permettant la création, la lecture, l'écriture de fichiers au format
                                    ##JSON. Les types de données (entier-boléeen-string-ect...) et la forme sous laquelles
                                    ##elles sont insérées (dictionnaires-listes-ect...)sont utilisables partout dans le script
                                    ##Cette fonction dépend du module JSON qui doit être importé en amont."""
    global r_data               #Permet son utilisation dans toutes les fonctions
    try:                        #Test les instructions suivantes:
        tf = open(file_json, "r")               #-Lecture du fichier contenu de la variable file_json
        r_data = json.load(tf)              #-Chargement des données lues dans la variable globale r-data 
    except FileNotFoundError:           #En cas d'erreur des instructions précédentes:
        tf = open(file_json, "w")       #-Création du fichier contenu de la variable file_json.
        json.dump(data,tf)              #-Ecriture des données contenu dans la variable data, sur le fichier. 
        tf.close()                      #
        tf = open(file_json, "r")       #-Après fermeture du fichier, ouverture du fichier en mode (lecture)
                           
        r_data = json.load(tf)      #-Chargement des données lues dans la variable globale r-data 

def connexion(r_data):   
                            ##Fonction permettant la connexion en SSH aux machines pour lesquelles
                            ##les données neccessaires à la connexion ont été envoyées en paramètres.
                            ##Cette fonction dépend du module Netmiko qui doit être importé en amont.                      
    global net_connect
    try:            #Après Déclariation de la variable global net_connect test des instructions qui suivent.
        print('################ Connexion SSH en cours ################') 
        net_connect = ConnectHandler(**r_data)  #Déclaration de la variable exécutant une fonction du module Netmiko.
        print(net_connect.find_prompt())        #La variable globale r_data passée en paramètre permet la connexion SSH à la machine.
                                                #D'autres actions comme l'affichage du prompt ou l'envoi de commande sont possibles.
        print('-------------------- Connexion établie --------------------')
    except (NetmikoTimeoutException, SSHException, NameError) as error: #Les erreurs de connexions sont affichées ainsi qu'un message,
        logging.warning(error)                                          #avant le renvoi au menu principal.
        print("Connexion impossible:(plusieurs raisons possibles)\n-Vérifiez vos informations de connexion.\nConnexion trop longue à établir.\nRetour à l'enregistrement des informations.\n")
        choice_menu()
    
def send_config(config_command):        ##Fonction permettant l'envoi de configuration à la machine. Dépend du module Netmiko.
    try:                                #Test des instructions suivantes:
        net_connect.enable()                            #-Autorisation du mode privilège de la machine.
        net_connect.find_prompt()                       #-Affichage du prompt.
        if user_config == "1" or user_config == "2":            #Selon l'option choisi, utilisation de:
            output = net_connect.send_config_set(config_command)    #-La fonction de configuration par liste du module Netmiko.
        elif user_config == "3":
            output = net_connect.send_config_from_file(config_command)  #-La fonction de configuration par fichier texte du module Netmiko.
        print(output)                           #-Affichage des commandes envoyées.
        print('\n\n---------------- Configuration terminée -----------------\n \n')
    except (NetmikoTimeoutException, SSHException, NameError, FileNotFoundError) as error:   #Si erreurs de connexion, affichage d'un message,
        logging.warning(error)                                                               #avant le renvoi au menu de configuration.
        print ('Une erreur s\'est produite.Verifiez que le nom du fichier de configuration est correcte...\nVoir le fichier de log config_auto.py...')
    
def choice_menu():          ##Fonction permettant le choix entre les différentes actions à effectuer. 
    print ('\n\n#################### CONFIGURATION RESEAU ####################\n\n') 
    devices_exist = input("""Quelle est l\'action à effectuer?\nEnregistrer une machine: Tapez 1\nCongigurer une machine: Tapez 2\nQuitter le script: Tapez 3\nRéponse: >>>>>""")    
                                   #Enregistre le choix d'action à effectuer par le contenu de la variable.
    if devices_exist == "1":       #Exécute la fonction d'enregistrement,  
        get_infos()                #suivie de la fonction de configuration si la variable contient 1.
        get_config()

    elif devices_exist == "2":      #Exécute la fonction de configuration si la variable contient 2.    
        get_config()

    elif devices_exist == "3":      #Affiche le message et quitte le script si la variable contient 3.        
        print('\nFermeture du script\n-----------------------------\n')
      
    else :              #Renvoie au menu pricipal si aucun des choix précédents est indiqué.
        print('\nLa réponse ne fait pas partie des choix proposés... \nRetour au menu principal...\n\n\n')
        choice_menu()

def main(): 
                            ##Fonction principal exécutant le script et génère le fichier de log,
                            ##où sont contenu les informations sur les erreurs.
    logging.basicConfig(filename='config_auto.log', filemode='w', level=logging.WARNING,\
    format='%(asctime)s -- %(lineno)d -- %(funcName)s -- %(levelname)s -- %(message)s')

    try:                            #Test les instructions suivantes:
        choice_menu()               #-Lancement de la fonction.                 
    except (NameError, ModuleNotFoundError) as error:     #En cas d'erreur au lancement du script:         
        logging.warning(error)                            #-Redirection de l'erreur vers le fichier de log. 
        print ('\nModule(s) neccessaires non installés.') #-Affichage d'un message d'avertissement.
        print('\nVoir le fichier de log "config_auto_device.log".Pour installer le module manquant, exécuter la commande suivante: pip install "nom-du-module')

if __name__ == '__main__':          #Différencie l'exécution de l'import du script dans un autre script 
    main()                          #Execution du script.
