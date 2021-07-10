### Prérequis des machines à configurer


Avant de lancer le script les commandes suivantes sont néccessaires pour pouvoir établier la communication (ping) et initialiser la connexion SSH.

#### Exemple de configuration SSH d'un switch avant de pouvoir exécuter le script

```
switch_test#hostname  
switch_test#username cisco secret cisco  
switch_test#ip domain-name cisco  
switch_test#enable secret motdepasse  
switch_test#crypto key generate RSA  
switch_test#ip ssh version 2  
switch_test#line vty 0 4  	
switch_test#transport input ssh  
switch_test#transport output ssh  
switch_test#password motdepasse	
switch_test#login local 
```

#### Exemple de configuration d'accès Vlan d'un switch avant de pouvoir exécuter le script
Sur chaque switch à configurer dédier un vlan à l'accès en SSH  

```
switch_test#vlan 99  
switch_testname Administration  
switch_test#int vlan 99   
switch_test#ip add 10.0.1.1 255.255.255.0  
switch_test#no sh  
switch_test#int gi3/3  
switch_testswitch_test#sw  trunk encapsulation dot1q  
switch_test#sw mode trunk all vl 99-110  
switch_test#do wr
```
