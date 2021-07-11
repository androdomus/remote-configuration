## Prérequis des machines à configurer
--------------------------------------------------------------------------------------------------------------------------------------------------
Avant de lancer le script les commandes suivantes sont néccessaires pour pouvoir établier la communication (ping) et initialiser la connexion SSH.

Il existe différent moyen d'établir la communication avec les équipements réseau, tout dépend de la conception de votre réseau.

Dans l'environnement de test crée pour concevoir ce script, afin de faciliter l'accès au divers switchs (branché directement ou distant), des **sous-interfaces** ont été créées sur la machine hôte.  
Chaque sous interfaces permet la communication avec le vlan dédié sur chaque switch.
Les interfaces des switch sont en mode **trunk** afin d'autoriser les Vlans correspondants.


#### Exemple de configuration SSH d'un switch avant de pouvoir exécuter le script

```
switch_test(config)#hostname  
switch_test(config)#username cisco secret cisco  
switch_test(config)#ip domain-name cisco  
switch_test(config)#enable secret motdepasse  
switch_test(config)#crypto key generate RSA  
switch_test(config)#ip ssh version 2  
switch_test(config)#line vty 0 4  	
switch_test(config-line)#transport input ssh  
switch_test(config-line)#transport output ssh  
switch_test(config-line)#password motdepasse	
switch_test(config-line)#login local 
```      


#### Exemple de configuration d'accès Vlan d'un switch avant de pouvoir exécuter le script

  
```
switch_test(config)#vlan 99  
switch_test(config-vlan)#name Administration  
switch_test(config-vlan)#int vlan 99   
switch_test(config-if)#ip add 10.0.1.1 255.255.255.0  
switch_test(config-if)#no sh
switch_test(config-if)#exit  
switch_test(config-if)#int gi3/3  
switch_test(config-if)#sw  trunk encapsulation dot1q  
switch_test(config-if)#sw mode trunk all vl 99-110  
switch_test(config-if)#do wr
```
