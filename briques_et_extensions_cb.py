from upemtk import *
import random

import string
def def_dimens_briques(largeurFen,hauteurFen,paddingTop,paddingBot,nbrL=4,nbrCol=6):
    nbrL=int(nbrL)
    nbrCol=int(nbrCol)

    largCase = (largeurFen)/nbrCol
    hautCase = (hauteurFen-paddingTop-paddingBot)//nbrCol
    return {'largCase':largCase,'hautCase':hautCase,'paddingTop':paddingTop,'briquesL':nbrL,'briquesC':nbrCol}

def initialiser_briques(largCase,hautCase,paddingTop,nbrBriquesLigne,nbrDeBriqueColonne,liste_vies_briques=None):
    """retourne une liste contenant les propriétés des briques sous formes de dictionnaire """
    briques_lst = []
    bm = None
    x,y  = 0,paddingTop
    k=0
    #on créer une liste avec les coordonnées des briques et leurs points de vie
    for i in range(nbrBriquesLigne):
        #pour chaque ligne il faut remettre X à la position initiale et incrémentez Y
        for j in range(nbrDeBriqueColonne):
            
            # definition aléatoire d'un bonus/malus sur une brique
            if liste_vies_briques:
                element = liste_vies_briques[k]
                
                if element not in string.digits:
                    if element == '.':
                        x += largCase
                        k+=1
                        continue
                    if 'm' in element:
                        bm = 'malus'
                        element=element.strip('m')
                    elif 'b' in element:
                        bm = 'bonus'
                        element=element.strip('b')

                vie = int(element)
            else:
                nbr_aléatoire = random.randint(0,9)
                
                if  nbr_aléatoire == 3:
                    bm = 'malus'
                elif nbr_aléatoire<3:
                    bm = 'bonus'
                vie = random.randint(1,3)

            briques_lst.append({'x':x,'y':y, 'vie':vie,'bonus_malus':bm})

            # pour chaque brique sur la meme ligne on incrémente X 
            x += largCase
            k+=1
        x = 0
        y += hautCase

    return briques_lst


def dessiner_briques(briques_lst,largCase,hautCase):
    couleurs_vies = {1:'yellow', 2:'orange', 3:'red'}
    for brique in briques_lst:
            rectangle(brique['x'],brique['y'],brique['x']+largCase,brique['y']+hautCase\
              ,remplissage=couleurs_vies[brique['vie']], tag = 'briques')

def dessiner_malus(xcentre,ycentre,rayon,couleur):
    """dessine la forme du malus (on utilise une fonction annexe de celle provenant de upemtk car on peut 
    ajouter du contenu par la suite)"""

    cercle(xcentre, ycentre, rayon, remplissage=couleur, tag='bonus_malus')

def dessiner_bonus(xcentre,ycentre,rayon,couleur):
    """dessine la forme du bonus"""

    cercle(xcentre, ycentre, rayon, remplissage=couleur, tag='bonus_malus')

def lire_fichier_niveau(nomFichier):
    """ charge un fichier niveau """
    print('chargement de niveau')
    fichier = open(nomFichier,'r')
    nbrBriques_largeur=(fichier.readline()).strip()
    nbrBriques_hauteur=(fichier.readline()).strip()
    briques =[]
    fichier.readline() #ligne vide
    while True:
        ligne=fichier.readline()
        if not ligne: 
            break
        briques+=ligne.split()
    return nbrBriques_hauteur,nbrBriques_largeur,briques
    
def sauvegarder(briques_lst,largCase,hautCase,paddtop,nbrBriques_largeur,nbrBriques_hauteur):
    """sauvegarde le configuration actuelle dans un fichier save.txt """
    ligne = ''
    ttes_lignes = []
    fichier = open("niveaux/save.txt",'w')
    ibriques_lst = 0
    k = 0
    xdep = 0
    ydep = paddtop
    for i in range(nbrBriques_hauteur):
        for j in range(nbrBriques_largeur):
            # b = briques_lst[ibriques_lst]
            # print(xdep,ydep,b['x'],b['y'],ibriques_lst,nbrBriques_largeur,nbrBriques_hauteur)
            # print(ibriques_lst,k , briques_lst[ibriques_lst],xdep,ydep,ibriques_lst>=len(briques_lst) and (int(xdep) == int(briques_lst[ibriques_lst]['x']) and int(ydep)==int(briques_lst[ibriques_lst]['y'])))
            if ibriques_lst<len(briques_lst) and (int(xdep) == int(briques_lst[ibriques_lst]['x']) and int(ydep)==int(briques_lst[ibriques_lst]['y'])):
                #on tronque avec le int()
                ligne+= str(briques_lst[ibriques_lst]['vie'])+' '
                ibriques_lst +=1
            else:
                ligne+='. '

            xdep += largCase
            k+=1

        ttes_lignes.append(ligne)
        ligne=''
        xdep = 0
        ydep += hautCase

    fichier.write(str(nbrBriques_largeur)+'\n')
    fichier.write(str(nbrBriques_hauteur)+'\n')
    fichier.write('\n')
    for lig in ttes_lignes:
        fichier.write(lig+'\n')
    fichier.close()
    
    return
def select_niveau(hauteurFen,largeurFen):

    texte(largeurFen//2,hauteurFen//2,"Choisissez un niveau \na.niveau 1 \nb.niveau 2 \nc.niveau 3\nd.niveau 4 \ne.niveau 5\nf.lancer la sauvegarde\nq.quitter",couleur='red',ancrage='center',taille=13)


    type_ev = None
    nomTouche = None
    while type_ev !='Touche' or (nomTouche not in ('a','b','c')):
        rien,nomTouche,type_ev = attente_clic_ou_touche()
        if nomTouche == 'a':
            niveau = lire_fichier_niveau("niveaux/niveau1.txt")
            efface_tout()
            return niveau
        elif nomTouche == 'b':
            niveau = lire_fichier_niveau("niveaux/niveau2.txt")
            efface_tout()
            return niveau
        elif nomTouche == 'c':
            niveau = lire_fichier_niveau("niveaux/niveau3.txt")
            efface_tout()
            return niveau
        elif nomTouche == 'd':
            niveau = lire_fichier_niveau("niveaux/niveau4.txt")
            efface_tout()
            return niveau
        elif nomTouche == 'e':
            niveau = lire_fichier_niveau("niveaux/niveau5.txt")
            efface_tout()
            return niveau
        elif nomTouche == 'f':
            niveau =lire_fichier_niveau("niveaux/save.txt")
            efface_tout()
            return niveau
        elif nomTouche =='q':
            exit(0)

    

    

if __name__ == '__main__':
    pass