## Fichier log généré par le script

Au lancement du script, un fichier log est généré permettant de traiter les éventuelles erreurs rencontré avant et durant l'exécution.   
Les informations remontées dans les logs permettent un traitement rapide de l'erreur en indentifiant sa source ce qui rend sa résolution plus aisée.   

### Exemple d'une ligne du fichier log 

`2021-07-11 13:24:03,225 -- 249 -- send_config -- WARNING -- [Errno 2] No such file or directory: 'gggg'`  

**Information détaillée de cette ligne:**  
* **2021-07-11 13:24:03**: Heure et date à laquelle l'erreur s'est produit.  
* **225**: Identifiant de l'erreur.  
* **249**: Numero de la ligne dans le code où se situe l'erreur.  
* **send_config**: Fonction dans le code où se situe l'erreur.  
* **WARNING**: Niveau de criticité de l'erreur(ici le niveau est par défaut).  
* **[Errno 2] No such file or directory: 'gggg'**: Message d'erreur récupéré
