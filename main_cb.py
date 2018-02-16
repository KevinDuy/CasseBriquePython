from upemtk import *
import random
import time
import sys
import string
from balle_et_raquette_cb import *
from briques_et_extensions_cb import *



def deplacer_rect_and_event_handler(xRect):
    """ renvoie la nouvelle position de la raquette afin de la deplacer """
    evenement = donne_evenement()
    type_ev = type_evenement(evenement)
    global largeurFen,hauteurFen,briques_lst,dimBriques,infos_niveau
    if type_ev == 'Deplacement':
        posX = clic_x(evenement)
        return posX-largeurRect//2
    if type_ev == 'Touche':
        nomTouche = touche(evenement)
        if nomTouche=='p':
            texte(largeurFen//2,hauteurFen//2," - Pause - \n tapez sur 's' pour sauvegarder \n'q' pour quitter",couleur='red',ancrage='center',taille=13,tag='pause')

            rien,nomTouche,typeEv = attente_clic_ou_touche()
            if nomTouche == 's':
                
                sauvegarder(briques_lst,dimBriques['largCase'],dimBriques['hautCase'], dimBriques['paddingTop'],dimBriques['briquesC'],dimBriques['briquesL'])
                print("partie sauvegardée")
                
                
            if nomTouche =='q':
                exit(0)
            
            efface('pause')
    return xRect

def collision_briques():
    global briques_lst,xBalle,yBalle,largCase,hautCase,largeurFen,hauteurFen,sensYballe,sensXballe,score
    collision = False
    
    # verififier si il y a collision sur une des briques
    if briques_lst and yBalle<briques_lst[-1]['y']+rayonBalle+50:

        #collision balle-briques pour les 4 côtés
        for i in range(len(briques_lst)):
            #pour chaque coté de la brique on verifie si il  y a collision
            brique = briques_lst[i]

            #haut
            sensYballe, collision = verif_collisions_haut(brique['x'], brique['y'], brique['x']+largCase, brique['y'], \
                sensYballe, xBalle, yBalle+rayonBalle, ancienYballe, collision)
            #bas
            sensYballe, collision = verif_collisions_bas(brique['x'], brique['y']+hautCase, brique['x']+largCase,\
                brique['y']+hautCase, sensYballe, xBalle, yBalle-rayonBalle, ancienYballe, collision)
            #gauche
            sensXballe, collision = verif_collisions_gauche(brique['x'], brique['y'], brique['x'], brique['y']+hautCase,\
                sensXballe, xBalle+rayonBalle, yBalle, ancienXballe, collision)
            #droite
            sensXballe, collision = verif_collisions_droite(brique['x']+largCase, brique['y'], brique['x']+largCase,\
                brique['y']+hautCase, sensXballe, xBalle-rayonBalle, yBalle, ancienXballe, collision)
            

            #----gestion de la vie et de la couleur----
            if collision :
                
                brique['vie'] -= 1
            
                if brique['vie'] <= 0:
                    score += 1
                    afficher_score(score)
                    briques_lst.pop(i)
                    efface('briques')

                    if brique['bonus_malus'] == 'bonus':
                        ensemble_bonus_malus.append({'xbm':brique['x']+largCase//2, 'ybm':brique['y']+hautCase, 'categ':'bonus'})
                    if brique['bonus_malus'] == 'malus':
                        ensemble_bonus_malus.append({'xbm':brique['x']+largCase//2, 'ybm':brique['y']+hautCase, 'categ':'malus'})

                dessiner_briques(briques_lst,largCase,hautCase)
                break
                #ici on se permet de le pop car la balle ne peut pas etre en collsion avec deux brique en meme temps
                #donc pas de probleme d'indice au niveau de la liste

def dessin(xBalle,yBalle,rayonBalle,xRect,yRect,largeurRect,hauteurRect):
    """dessine tout les elements affiché """
    efface('rect')
    efface('ball')
    
    cercle(xBalle,yBalle,rayonBalle,\
        remplissage='blue',tag='ball')
    rectangle(xRect,yRect,xRect+largeurRect,yRect+hauteurRect,\
        remplissage='black',tag='rect')
    mise_a_jour()

def deplacement_objets(sensXballe,sensYballe,xBalle,yBalle,vitesse,xRect):
    """gere le deplacement de la balle et de la raquette"""
    global largeurFen

    sensXballe,sensYballe = rebond_balle_fen(sensXballe,sensYballe,xBalle,yBalle,rayonBalle,largeurFen)
    xBalle,yBalle = deplacer_balle(xBalle,yBalle,vitesse,sensXballe,sensYballe)
    #deplacer raquette
    xRect = deplacer_rect_and_event_handler(xRect) #yRect ne change pas
    xRect = rebond_bord_raquette(xRect, largeurRect, largeurFen)
    return sensXballe,sensYballe,xBalle,yBalle,xRect

def collision_bm(ensemble_bonus_malus,xRect,yRect,largeurRect,hauteurRect):
    """ gere les collisions avec les briques contenant des malus ou des bonus """
    global hauteurFen,largeurFen
    efface('bonus_malus')
    for element in ensemble_bonus_malus:

        ancienYbm = element['ybm']
        ancienXbm = element['xbm']

        #si le bonus/malus se situe au dessus du bas de la fenetre on le dessine
        if element['ybm']<hauteurFen:
            if element['categ']=='bonus':
                dessiner_bonus(element['xbm'],element['ybm'],rayon_bm,'green')
            if element['categ']=='malus':
                dessiner_malus(element['xbm'],element['ybm'],rayon_bm,'red')
            element['ybm'] += vitesse/1.5

        #---gestion de collision entre le bonus/malus et la raquette---
        alpha = -1 #variable placebo qui permet de réutiliser les fonctions verif_collisions et remplacer le return de sensBalle
        collision_bm = False

        alpha, collision_bm = verif_collisions_haut(xRect, yRect, xRect+largeurRect, yRect, alpha, element['xbm'], element['ybm']+rayon_bm, ancienYbm, collision_bm)
        alpha,collision_bm = verif_collisions_gauche(xRect, yRect, xRect, yRect+hauteurRect, alpha, element['xbm']+rayon_bm, element['ybm'], ancienXbm, collision_bm)
        alpha,collision_bm= verif_collisions_droite(xRect+largeurRect, yRect, xRect+largeurRect, yRect+hauteurRect, alpha, element['xbm']-rayon_bm, \
            element['ybm'], ancienXbm, collision_bm)

        if collision_bm:
            if element['categ'] == 'bonus':

                #on limite la taille de la raquette
                if largeurRect<100:
                    largeurRect += 20
            else:
                if largeurRect>30:
                    largeurRect -= 20
            element['ybm'] = hauteurFen*2 #on la met hors de la fenetre pour ne plus la dessiner

def collision_balle_barre():
    """ gere la collision entre la balle et la barre """
    global xRect,yRect,xBalle,yBalle,rayonBalle,sensYballe,sensXballe,collision
    seuil_surete = 0.8
    if auto:
        xRect = xBalle-largeurRect/2
        sensYballe, collision = verif_collisions_haut(xRect, yRect, xRect+largeurRect, yRect, sensYballe, xBalle, yBalle+rayonBalle, ancienYballe, collision)

    elif xRect <= xBalle <= xRect+largeurRect and yBalle+rayonBalle >= yRect and ancienYballe < yRect:
        if xBalle > (xRect + largeurRect/2):
            sensXballe = (xBalle-xRect-largeurRect/2)*seuil_surete/(largeurRect/2)
            sensYballe = sensXballe-1
        else:
            sensXballe = ((xRect+largeurRect/2)-xBalle)*seuil_surete/(-largeurRect/2)
            sensYballe = -sensXballe-1

    if yRect <= yBalle <= yRect+hauteurRect and xBalle+rayonBalle > xRect and xBalle < xRect+largeurRect:
        if xBalle <= xRect+largeurRect//2 :
            sensXballe = ((xRect+largeurRect/2)-xBalle)*seuil_surete/(-largeurRect/2)
            sensYballe = -sensXballe-1
        elif xBalle >= xRect+largeurRect//2 :
            sensXballe = (xBalle-xRect-largeurRect/2)*seuil_surete/(largeurRect/2)
            sensYballe = sensXballe-1 

def perdu_gagner(yBalle,rayonBalle,briques_lst,score):
    """ verifie si la partie est terminé """
    global hauteurFen
    if yBalle-rayonBalle > hauteurFen :
        
        fin_de_jeu("Perdu !")
    elif not briques_lst:
        fin_de_jeu("Gagné !")
    else :
        return False
    
    return True
def fin_de_jeu(a_afficher):
    efface_tout()
    texte((largeurFen//2)-100, (hauteurFen//2)-150, a_afficher, taille=30)
    texte((largeurFen//2)-100, (hauteurFen//2)-80, "Score = "+str(score), taille=20)
    texte((largeurFen//2)-110, (hauteurFen//2)-20, "Highscores", taille=25)
    gestion_score(score)
    
    

def mode_auto():
    """ verifie si il y a un mode auto ou une vitesse rentréen argument """
    vitesse =3
    auto = False
    for argument in sys.argv[1:]:
        if argument == 'auto':
            auto = True

        #verification si l'argument est un digit
        elif argument in string.digits:
            argument = int(argument)
            if 0 < argument:
                vitesse = argument
        else:
            print("La vitesse de la balle doit être un entier compris entre 1 et 9.")
            print("Elle prend sa valeur par défault :", vitesse)
    return auto,vitesse

def afficher_score(score):
    """affiche le score sur l'écran """
    efface('score_actu')
    texte(0, largeurFen-30, "Score = "+str(score), taille=12, tag='score_actu')

def gestion_score(score):
    """gere les scores"""
    with open("Highscores.txt", 'r') as highscores:
        lst_score = highscores.readlines()
        for i, ligne in enumerate(lst_score):
            if score > int(ligne[3:-1]):
                lst_score.insert(i,'0. '+str(score)+'\n')
                del lst_score[-1]
                break

    with open("Highscores.txt", 'w') as modification:
        for i, ligne in enumerate(lst_score):
            ligne = str(i+1)+'. '+str(ligne[3:-1])+'\n'
            modification.write(ligne)
            texte((largeurFen//2)-50, (hauteurFen//2)+(i+1)*25, ligne, taille=20)
def charger_niveau():
    global largeurFen,hauteurFen
    niveau = select_niveau(hauteurFen,largeurFen)
    dimBriques = def_dimens_briques(largeurFen,hauteurFen,40,60,niveau[0],niveau[1])
    briques_lst=initialiser_briques(dimBriques['largCase'],dimBriques['hautCase'],dimBriques['paddingTop'],\
        dimBriques['briquesL'],dimBriques['briquesC'],niveau[2])

    dessiner_briques(briques_lst,dimBriques['largCase'],dimBriques['hautCase'])
    return dimBriques,briques_lst



if __name__ == '__main__':


    #---proprétés de la fenetre----
    largeurFen,hauteurFen  = 500,500
    cree_fenetre(largeurFen,hauteurFen)

    #---propriétés de la raquette---
    hauteurRect,largeurRect = 15,70
    xRect = (largeurFen//2)-largeurRect//2
    yRect = hauteurFen-hauteurRect

    #---propriétés de la balle---
    rayonBalle = 5
    xBalle = largeurFen//2
    yBalle = hauteurFen-rayonBalle-hauteurRect
    sensXballe ,sensYballe= 0.5, -0.5
    ancienYballe,ancienXballe = yBalle,xBalle

    vitesse = 3 # par default

    auto,vitesse = mode_auto()

    stop = False
    infos_niveau = charger_niveau()
    dimBriques= infos_niveau[0]
    largCase= dimBriques['largCase']
    hautCase=dimBriques['hautCase']

    briques_lst = infos_niveau[1]

    #----propriétés des bonus/malus----
    ensemble_bonus_malus = []
    rayon_bm = 7

    #----mode automatique + vitesse choisi-----

    #----initialisation du score-----
    score = 0
    afficher_score(score)
    texte(0,0,"'p' pour mettre en pause",taille=9)

    #boucle qui fait les changements pour chaque images
    while not stop:
        collision = False
        #------dessin des objets + rafraichissement -----
        dessin(xBalle,yBalle,rayonBalle,xRect,yRect,largeurRect,hauteurRect)
        time.sleep(0.01)
        #----verifier si perdu/gagner-----
        stop = perdu_gagner(yBalle,rayonBalle,briques_lst,score)
        
        #-----deplacement objets------
        #deplacer balle
        sensXballe,sensYballe,xBalle,yBalle,xRect=deplacement_objets(sensXballe,sensYballe,xBalle,yBalle,vitesse,xRect)
        #------gestion de collisions-------
        collision_briques()
        #-----dessin + gestion collisions des bonus/malus-----
        collision_bm(ensemble_bonus_malus,xRect,yRect,largeurRect,hauteurRect)
        #collision balle-barre
        collision_balle_barre()



        # variable  qui enregistre la position de la balle une image avant
        ancienYballe = yBalle
        ancienXballe = xBalle

      
    attente_touche()
    ferme_fenetre()