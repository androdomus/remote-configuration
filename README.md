# Configuration distante de support reseau
-------------------------------------------


## Description générale
Ce script a pour finalité la configuration distante et automatique d’équipement réseau (switches manageables-routeurs-serveurs).
Ce dernier pourrait être utile aux techniciens et administrateurs réseau. 

Des notions du résaux ainsi que la connaissance des commandes des équipements à configurer sont primordiales pour l'utilisation de ce script dans de bonnes conditions.
De nombreux équipements sont compatibles et configurable.  
[Machines compatibles](https://github.com/ktbyers/netmiko/blob/develop/PLATFORMS.md)

La mise en place de configuration sur plusieurs équipements en même temps est possible.
Il en résulte un gain de temps lors de tâches d'administration longues, répétitives et fastidieuses qui peuvent souvent être source d'erreurs.  

### Environnement de test
Ce script a été éxécuté uniquement dans un environnement virtualisé **GNS3**. La machine hôte est une machine virtuelle linux sous **Debian 10**. 
Les machines distantes à configurer sont des machines virtuelles de switch **Cisco**  sous l'ios *vios_l2-adventerprisek9-m.vmdk.SSA.152-4.0.55.E.*.



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
* Informations générales de l'infrastruture (Numero, nom et addresse ip des Vlan).  
* Informations matérielles sur les machines distantes (Nombre et type d'interface - Schéma de branchement - identification des liens en access et en trunk).  

### Prérequis Machine hôte (ordinateur hébergeant le script):
* Une connexion internet (neccessaire juste pour installer les librairies et les paquet néccéssaires).    
* Accès root.  
* SSH activé.  
* Paquet pip3. Utlilisez la commande `apt-get install pip3 python`
* Module Netmiko installé. Utlilisez la commande `pip install netmiko`. 

### Prérequis Machine distante (équipement réseau à configurer) 
* Accès SSH activé et configuré sur le switch. Voir la configuration [ici](https://github.com/androdomus/remote-configuration/blob/master/Pr%C3%A9requis%20switch.md#exemple-de-configuration-ssh-dun-switch-avant-de-pouvoir-ex%C3%A9cuter-le-script)   
* Communication fonctionnelle avec la machine hôte.  
* Vlan d'adminstration configuré pour pouvoir accédé à tous les switch. Voir la configuration [ici](https://github.com/androdomus/remote-configuration/blob/master/Pr%C3%A9requis%20switch.md#exemple-de-configuration-dacc%C3%A8s-vlan-dun-switch-avant-de-pouvoir-ex%C3%A9cuter-le-script)  



## Fonctionnement


### Les actions exécutées par le script
Lors de son exécution, l’utilisateur navigue avec ses réponses à travers les divers menus proposés.
Après avoir indiqué les informations de connexion de chaque élément à configurer, une connexion rapide en SSH est effectuée.

A la suite des connexions réussies et l'affichachage du prompt de chaque machine, les informations de connexions sont enregistrées.
L'utilisateur est guidé vers un deuxième menu, à travers lequel il donne les informations sur les configurations à mettre en place.

Les informations demandées peuvent être indiquées de manière répétées. Il est donc possible d'effectuer plusieurs configurations sur plusieurs équipements en même temps.
Chaque configuration est enregistrée,puis appliquée les unes à la suite des autres sur toutes les machines distantes.

Un autre mode de configuration est possible. Avant l'exécution de script l'utilisateur peut créer un fichier texte dans le **même dossier** que le script.A l'interieur de ce fichier texte les commandes peuvent être renseignées comme sur l'interface de commande de  l'appareil (**CLI**).
Lors de l'exécution du script, il faudra quand lui sera fait la demande, donner  **le nom complet du fichier texte** (nom-du-fichier.txt)
Voir un exemple [ici](https://github.com/androdomus/remote-configuration/blob/master/base_config.txt)

### Gestion des erreurs

Les réponses de l'utilisateur, non attendues et prévues lors de la conception du programme, sont interprété comme une **erreur**.
L'utilisateur est renvoyé au menu dans le quel il devra répéter sa réponse ou, le cas échéant à un autre menu ou il pourra résoudre son erreur. 
Si l'erreur concerne un module non installé, le script se ferme.
Le fichier de log nommé **auto_config.log** est généré et les informations sur les erreurs y sont indiqué afin de pouvoir les résoudre. 


## Lancement du script


Pour lancer le script déplacez vous dans le fichier où se trouve le script et lancez la commande suivante.  
`python3 autco_config.py`










