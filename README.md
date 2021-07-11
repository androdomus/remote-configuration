# Configuration distante de support reseau
-------------------------------------------


## Description générale
Ce script a pour finalité la configuration distante et automatique d’équipements réseaux (switches manageables-routeurs-serveurs).  
Il s'appuie principalement sur le module **Netmiko** qui permet la connexion et l'envoi de commande aux machines distantes.  
Voir le projet Netmiko [ici](https://github.com/ktbyers/netmiko).

Les données sont d'abord récoltées par le mode semi-intéractif du script, puis modélisées en configuration basique à envoyer aux machines correspondantes.  
A destination de toutes personnes souhaitant faire de la conception, configuration et administration de réseaux, l'utilisation de ce script neccessite d'avoir quelques notions en informatique et de connaître les commandes des équipements à configurer.  
De nombreux équipements sont compatibles et configurables.([Machines compatibles](https://github.com/ktbyers/netmiko/blob/develop/PLATFORMS.md))

La mise en place de configuration sur plusieurs équipements en même temps est possible. Avec l'utilisation des variables il n'est pas néccéssaire de "coder en dur" les configurations à l'intérieur du script.  
Il en résulte un gain de temps lors de tâches d'administration longues, répétitives et fastidieuses qui sont souvent source d'erreurs.  

### Environnement de test
Développé en **Python version 3.9**, ce script a été éxécuté uniquement dans un environnement virtualisé **GNS3**. La machine hôte est une machine virtuelle linux sous **Debian 10**. 
Les machines distantes à configurer sont des machines virtuelles de switch **Cisco** de couche 3  sous l'ios *vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E.*.

--------------------------------------------------------------

## Prérequis

Pour que le script s'exécute correctement, vérifiez que vous disposez de tous les éléments neccessaires à la configuration des machines.

### Informations de connexion en SSH sur la machine distante:  
* Un nom évocateur (pour pouvoir différencier les machines, si vous configurez plusieurs machines en même temps).  
* L'addresse IP de la machine sans son masque.
* L'identifiant de connexion SSH.  
* Le mot de passe pour la connexion SSH.  
* Le mot de passe du mode privilège sur la machine distante.  

### Elements néccessaires pour la configuration du réseau:
* Commandes de configuration de la machine distante.  
* Informations générales de l'infrastruture (numero, nom et addresse ip des Vlan-schéma de l'infrastructure-plan d'addressage ip-informations détaillées du branchement des connectiques réseau).  
* Informations matérielles sur les machines distantes (modèle et marque des équipement réseau-nombre et type d'interface-identification des liens en access et en trunk).  

### Prérequis Machine hôte (ordinateur hébergeant le script):
* Une connexion Internet (neccessaire juste pour les mises à jour, la récupération du projet et l'installation des librairies et paquets néccéssaires).    
* Accès root.  
* SSH activé.  
* Paquet pip3. Utlilisez la commande `apt-get install python3-pip`.
* Module Netmiko installé. Utlilisez la commande `pip install netmiko`. 

### Prérequis Machine distante (équipement réseau à configurer) 
* Accès SSH activé et configuré sur le switch. Voir la configuration [ici](https://github.com/androdomus/remote-configuration/blob/master/Pr%C3%A9requis%20switch.md#exemple-de-configuration-ssh-dun-switch-avant-de-pouvoir-ex%C3%A9cuter-le-script)   
* Communication fonctionnelle avec la machine hôte.  
* Vlan d'adminstration configuré pour pouvoir accédé à tous les switch. Voir la configuration [ici](https://github.com/androdomus/remote-configuration/blob/master/Pr%C3%A9requis%20switch.md#exemple-de-configuration-dacc%C3%A8s-vlan-dun-switch-avant-de-pouvoir-ex%C3%A9cuter-le-script)  


----------------------------------------------------------------

## Fonctionnement


### Les actions exécutées par le script
Lors de son exécution, l’utilisateur navigue avec ses réponses à travers les divers menus proposés.
Après avoir indiqué les informations de connexion de chaque élément à configurer, une connexion rapide en SSH est effectuée.

A la suite des connexions réussies et l'affichage du prompt de chaque machine, les informations de connexions sont enregistrées.
L'utilisateur est guidé vers un deuxième menu, à travers lequel il donne les informations sur les configurations à mettre en place.

Les informations demandées peuvent être indiquées de manière répétées. Il est alors possible d'effectuer plusieurs configurations sur plusieurs équipements en même temps.
Chaque configuration est enregistrée,puis appliquée les unes à la suite des autres sur toutes les machines distantes.

Il existe un autre mode de configuration. Avant l'exécution du script, l'utilisateur crée un fichier texte dans le **même dossier** que le script.A l'interieur de ce fichier texte, il indique la configuration à envoyer comme il le ferait  sur l'interface de commande de  l'appareil (**CLI**).  
Lors de l'exécution du script, il faudra quand lui sera fait la demande, donner  **le nom complet du fichier texte** (nom-du-fichier.txt).  
Voir un exemple [ici](https://github.com/androdomus/remote-configuration/blob/master/base_config.txt) d'un fichier texte de configuration.

### Gestion des erreurs

Les réponses de l'utilisateur, non attendues et prévues lors de la conception du programme, sont interprétées comme des **erreurs**.  
L'utilisateur est renvoyé au menu dans lequel il devra répéter sa réponse ou, le cas échéant à un autre menu où il pourra résoudre son erreur. 
Si l'erreur concerne un module non installé, le script se ferme.
Le fichier de log nommé **auto_config.log** est généré et les informations sur les erreurs y sont indiqué afin de pouvoir les résoudre.   
Voir la composition d'une ligne dans le fichier log [ici](https://github.com/androdomus/remote-configuration/new/master#fichier-log-g%C3%A9n%C3%A9r%C3%A9-par-le-script)

-----------------------------------------------------------------

## Lancement du script

Copiez le code de la branche **master** du projet https://github.com/androdomus/remote-configuration.git  

Vérifiez la présence du gestionnaire de paquet pour les librairies Python.  
`apt-get install python3-pip`

Installez le module Netmiko  
`pip install netmiko`

Pour lancer le script déplacez vous dans le fichier **remote-configuration** et lancez la commande suivante.  
`python3 auto_config.py`










