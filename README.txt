----- Le casse_brique ------
Version 24.11
 
par Do Duy Kevin et Rémi Apruzzese
Le but dans une partie de Casse-Brique est de casser toutes les briques qui s’affichent sur l’écran.



-- prérequis --
les fichiers disponibles :
main_cb.py : contiens la boucle principale de rafraîchissement de chaque image du jeu et la gestion des directions.
balle_et_raquette.py : contiens toutes les fonctions permettant de gérer les déplacement,collisions,des rebonds sur la fenêtre
briques_et_extensions.py : contiens toutes les fonctions permettant de gérer l'utilisation des briques, leurs dessins et le dessin des bonus et des malus (1er rendu)
les fichiers txt : Highscore.txt pour enregistrer les scores, niveauX.txt pour chaque niveau et save.txt qui permet d'enregistrer la configuration
actuelle du joueur.

-- extensions/infos utilisateur--

Mode auto :

entrez le mot-clé 'auto' en ligne de commande en tant qu'argument
"python3 main_cb.py auto"

Régler la vitesse:

De même il suffit de rentrer un nombre compis entre 1 et 9 afin de changer la vitesse
"python3 main_cb.py auto 5 "

Selection de niveau :

Au début du jeu sélectionner un niveau en tapant sur les touches correspondantes

Pause:
Appuyez sur 'p' pour mettre en pause et puis 's' pour sauvegarder et 'q' pour quitter sans sauvegarder

Optimisations/extras :

Attributions de bonus ou malus aux briques : À chaque destruction on ajoute dans un ensemble le bonus/malus avec ses propriétés dans un dictionnaire, ensuite on dessine chacun de ces extras si il se situe au-dessus du bas de la fenêtre. S'il y a collision sur le cote gauche, droite ou haut de la raquette, on déplace les coordonnées de la brique hors de la fenêtre afin de ne plus le dessiner. Ici, on ne supprime (à l'aide de lst.pop() par ex. ) pas les extras dans l'ensemble qui sont utilisés étant donné qu'il y en a peu, l'impact sur la performance est négligeable.
Les bonus apparaissent comme des boules verte et les malus comme des boules rouges

-- fonctionnement --
Déplacements:

Les déplacement sur réalisé grâce à un rafraîchissement d'image régulier. Dans laquelle on efface et redessine les formes à chaque passage de boucle.
Nous avons opté pour un systeme continu, lorsque que l'on tape sur une touche afin de déplacer le rectangle, l'animation continue afin de rendre le jeu plus agréable et fluide. (Etant donné que la gestion par souris n'est pas mis en place pour le 1er rendu)

Collisions :

nous avons créé 4 fonctions gérant respectivement les 4 côtés d'un rectangle. Si les coordonnées de l'objet atteignent les coordonnées de la ligne de collision, soit la petite zone qui permet de détecter l'entrée de l'objet sur un côté du rectangle.

Rebond objet-fenetre :

On observe si les coordonnées de l'objet en question se situent hors de la fenêtre


-- problématiques --

performance :

la question de performance a été omniprésente durant la construction du programme. Dans la boucle de rafraîchissement, les dessins doivent se charger assez rapidement afin que l'animation soit fluide. Il a fallu bien effacer chaque dessin à chaque rafraîchissement, sinon les dessins se cumulaient et ralentissaient le programme. Afin d'optimiser cette performance nous avons décidé de dessiner le mur de briques avant et de ne redessiner les briques qu'à chaque collision. Nous avons également commencé a lancer les vérifications de collisions pour chaque brique uniquement si la balle atteignait une certaine limite (proche de la zone des briques) afin de ne pas vérifier les collisions même quand la balle se situe dans la zone où il n'y a pas de briques.
Le dessin des bonus/malus a été un problème lorsque nous voulions avoir un dessin de bonus/malus avec un texte. Nous nous sommes rapidement rendu compte qu'en rafraîchissant avec du texte (pour l'animation de descente des extras) le programme était fortement ralentit dût au dessin de texte qui est un long processus. Nous avons donc finalement opté pour des formes simples

gestion des collisions:

En ce qui concerne les collisions de la balle avec les bords de l'écran, nous avions commencé par utiliser 2 variables booléennes qui prenaient True ou False comme valeur. Elles servaient à dire si la balle allait dans le sens des + ou des - pour la position x et y. Nous avons continué d'utiliser cela pour la collision avec les briques et la raquette pour inverser la direction. Cependant, lors de l'ajout de la gestion de l'angle de la balle sur la raquette, elle est devenue obsolète, car l'angle lui-même est positif ou négatif. Nous l'avons remplacé par les 2 variables sensXballe et sensYballe qui vont de -1 à 1 avec toujours :
|sensXballe| + |sensYballe| = 1
Pour détecter la collision avec les briques ou la raquette, on a d'abord fait une unique fonction qui renvoie (l'inverse de) la direction de la balle concernée en fonction de son ancienne position pour chaque surface : gauche, droite, bas et haut. Mais une fois finalisée, elle était trop complexe. Nous avons donc décidé de la diviser en 4 pour chaque direction. Pour incrémenter le système d'angle, nous avons fait une fonction dédiée à la collision avec la raquette qui change le sens en X proportionnellement à la différence entre le point d'impact et le centre de la raquette. Lorsque le rayon de la balle est trop grand l'espacement entre les briques devient trop étroit pour la laisser passer et la balle à des risques de passer à travers les diagonales des briques avec un certain angle (même si cela reste très rare).
Pour le mode automatique, nous avons dû réutiliser la fonction de collision des briques vers le haut pour la raquette, car sinon elle renvoie la balle toujours dans la même direction (vers le haut, si la balle est placée au centre).

Lecture des niveaux:
il a fallut pouvoir lire chaque informations et les séparer, on a choisi de les retirer en tant que String pour chaque ligne, puis d'en tirer les infos tel que la présence de 'm' ou de 'b' pour les bonus et les malus.

Sauvegarde la configuration actuelle:
Après plusieurs tentatives d'algorithmes pour pouvoir enregistrer les vies et le nombres de briques, on a décidé de parcourir un indice qui correspond au nombre de briques total et on incrémente les coordonnées comme si on initialisait la liste de briques puis si la brique au coordonnées n'est pas présente dans la liste on écrit un '.' autrement on incrémente un deuxieme indice afin de parcourir la liste des briques présentes et on note sa vie.
