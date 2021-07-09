# remote-configuration
## Configuration distante d'une machine par un script semi-intéractif

### Description générale
Le script Remote_config_device est un script qui a pour finalité la configuration distante et automatique d’équipement réseau ( Switch manageable-Routeurs-Serveur).
Ce dernier pourrait être utile  destination aux techniciens réseaux et administrateur réseau. 
Des notions du résaux ainsi que la connaissance des commandes des équipements à configurer sont primordiaux pour l'utilisation de ce script dans de bonnes conditions.  De nombreux équipements sont compatibles voir lien Netmiko

L'avantage avec l'exécution de ce script est la mise en place de configuration sur plusieurs équipement en même temps.
Il en résulte un gain de temps lors de  tâche d'administration longues répétitives et fastidieuses qui peuvent souvent être source d'erreurs.  

### Environnement de test
Ce script a été éxécuté uniquement dans un environnement virtualisé GNS3 sur une VM linux (Debian 10) mais pourra être lancé sur d’autres systèmes d’exploitation dans le futur.
Les machines distantes configurées après l’exécution du script sont des VM de switch 3745


### Fonctionnement
Avant de se lancer, pur que le script s'exécute correctement, vérifiez que vous disposez de tous les éléments neccessaires à la configuration des machines.
##### Informations de connexion en SSH sur la machine distante:  
* Un nom évocateur (pour pouvoir différencier les machines si vous configurez plusieurs machines en mêême temps)  
* L'addresse IP de la machine sans son masque
* L'identifiant de connexion SSH.  
* Le mot de passe pour la connexion SSH.  
* Le mode de passe du mode privilège sur la machine distante.  

##### Elements néccessaires pour la configuration du réseau:
* Commandes de configuration de la machine distante.  
* Informations générales de l'infrastruture (Numero, nom et addresse ip des Vlan).  
* Informations matérielle sur les machines distantes (Nombre et type d'interface - Schéma de branchement - identification des lien en access et en trunk).  

#### Les actions exécutées par le script
Lors de son exécution, l’utilisateur navigue avec ses réponses à travers les divers menus proposés.
Après avoir indiqué les informations de connexion de chaque élément à configurer, une connexion rapide en SSH est effectuée.
Après une connexion réussie sur toutes les machines, l'utilisateur est averti, et les informations de connexions sont enregistrées.
L'utilisateur peut à présent indiquer les configuration à mettre en place.
Ces dernières peuvent être uniques ou sous forme de suite pour effectuer plusieurs configurations sur plusieurs équipements en même temps.
Chaque configuration est enregistrée,puis appliquée les unes à la suite des autres sur toutes les machines distantes.

### Prérequis Machine hôte (ordinateur hébergeant le script):
* Une connexion internet (neccessaire juste pour installer les librairies et les paquet néccéssaires).    
* Accès root.  
* SSH activé.  
* Paquet pip3 installé avec la commande. Utlilisé la commande `apt-get install pip3 python`
* Module Netmiko installé avec la commande. Utlilisé la commande `pip install netmiko`. 

### Prérequis Machine distante (équipement réseau à configurer) 
* Accès SSH activé et configuré sur le switch.  
* Communication fonctionnelle avec la machine hôte.  
* Vlan d'adminstration configuré pour pouvoir accédé à tous les switch.  

Exemple de configuration SSH d'un switch avant de pouvoir exécuter le script

#enable secret motdepasse
#username cisco secret cisco
#ip domain-name cisco
#line vty 0 4			mode config terminaux virtuels (5 ici)
#password motdepasse	mot de passe connexion telnet ou SSH
#login	local			activer authentification (local utiliser pour les user mdp precedement créer
#crypto key generate RSA	               Géneration de clé ssh de «360 à 2048
#ip ssh version 2

Exemple de configuration d'accès Vlan d'un switch avant de pouvoir exécuter le script

#d'un switch avant de pouvoir exécuter le script









