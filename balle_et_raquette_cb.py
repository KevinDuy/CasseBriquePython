from upemtk import *

def rebond_bord_raquette(xRect, largeurRect, largeurFen):
    """Bloque la raquette si elle touche le bord de l'écran"""
    if xRect < 0 :
        xRect = 0
    if xRect+largeurRect > largeurFen :
        xRect = largeurFen-largeurRect
    return xRect

def rebond_balle_fen(sensXballe,sensYballe,xBalle,yBalle,rayonBalle,largeurFen):
    """Verifie si la balle touche la fenetre et change la direction de deplacement"""
    if xBalle+rayonBalle >=largeurFen or xBalle-rayonBalle<=0:
        sensXballe = -sensXballe
    
    if yBalle-rayonBalle<=0:
        sensYballe = -sensYballe
    return sensXballe,sensYballe

def deplacer_rect(direction,xRect,vitesse):
    """ renvoie la nouvelle position de la raquette afin de la deplacer """
    if direction == 'droite':
        xRect += vitesse*0.6
    elif direction == 'gauche':
        xRect -= vitesse*0.6
    return xRect

def deplacer_balle(xBalle,yBalle,vitesse,sensXballe,sensYballe):
    """ renvoie la nouvelle position de la balle afin de la deplacer """
    xBalle += vitesse*sensXballe

    yBalle += vitesse*sensYballe

    return xBalle,yBalle


def verif_collisions_droite(xRect1, yRect1, xRect2, yRect2, sensBalle, xBalle, yBalle, ancienPosBalle, collision):
    """verifie la collision entre la balle et un rectangle (qui peut etre la petite ligne qui avec laquelle il y a collision d'un coté de la raquette par ex. ) 
    provenant de la droite sur le côté droit du rectangle, retourne la direction de la balle et un boolean collision"""

    if xRect1 == xRect2 and yRect1<=yBalle<=yRect2:
        #venant de droite 
        if xBalle <= xRect1 and ancienPosBalle > xRect1:
            sensBalle = -sensBalle
            collision = True
    return sensBalle,collision

def verif_collisions_gauche(xRect1, yRect1, xRect2, yRect2, sensBalle, xBalle, yBalle, ancienPosBalle, collision):
    """verifie la collision entre la balle et un rectangle (qui peut etre la petite zone d'un coté de la raquette par ex. ) 
    provenant de la gauche sur le côté gauche du rectangle, retourne la direction de la balle et un boolean collision"""

    if xRect1 == xRect2 and yRect1<=yBalle<=yRect2:
        #venant de gauche
        if xBalle >= xRect1 and ancienPosBalle < xRect1:
            sensBalle = -sensBalle
            collision = True
    return sensBalle,collision

def verif_collisions_haut(xRect1, yRect1, xRect2, yRect2, sensBalle, xBalle, yBalle, ancienPosBalle, collision):
    """verifie la collision entre la balle et un rectangle (qui peut etre la petite zone d'un coté de la raquette par ex. ) 
    provenant du haut sur le côté haut du rectangle, retourne la direction de la balle et un boolean collision"""

    if yRect1 == yRect2 and xRect1<=xBalle<=xRect2:
        #venant du haut
        if yBalle >= yRect1 and ancienPosBalle < yRect1:
            sensBalle = -sensBalle
            collision = True
    return sensBalle,collision

def verif_collisions_bas(xRect1, yRect1, xRect2, yRect2, sensBalle, xBalle, yBalle, ancienPosBalle, collision):
    """verifie la collision entre la balle et un rectangle (qui peut etre la petite zone d'un coté de la raquette par ex. ) 
    provenant du bas sur le côté bas du rectangle, retourne la direction de la balle et un boolean collision"""

    if yRect1 == yRect2 and xRect1<=xBalle<=xRect2:
        if yBalle <= yRect1 and ancienPosBalle > yRect1:
            sensBalle = -sensBalle
            collision = True
    return sensBalle,collision


if __name__ == '__main__':
    pass