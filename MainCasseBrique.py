from upemtk import *
import time

def changer_direction():
	evenement = type_evenement(donne_evenement())
	if evenement == 'Touche':
		nomTouche = touche(evenement)
		if nomTouche == 'Right'
			direction = 'droite'
		elif nomTouche == 'Left':
			direction = 'gauche'
	return direction
def deplacer_rect(direction,rect,vitesse):
	if direction == 'droite':
		additionX = +vitesse
	elif direction =='gauche':
		additionX = -vitesse
	#pas fini

if __name__ == '__main__':
	largeurFen = 500
	hauteurFen = 500
	cree_fenetre(largeurFen,hauteurFen)
	#---le carré---
	hauteurRect = 30
	largeurRect = 60
	xRect = largeurFen//2
	yRect = hauteurFen-hauteurRect


	# vitesseRect = int(input('entrez une vitesse de rectangle :\
	# 	entre 1 et 10\n'))
	#---la balle---
	rayonBalle = 20
	xBalle = largeurFen//2
	yBalle = hauteurFen-rayonBalle-hauteurRect
	backXballe = False
	backYballe = False
	vitesseBalle = int(input('entrez une vitesse compris\
		entre 1 et 10\n'))
	
	
	while True:
		efface('ball')
		efface('rect')
		rectangle(xRect,yRect,xRect+largeurRect,yRect+hauteurRect,\
			remplissage='black',tag='rect')
		cercle(xBalle,yBalle,rayonBalle,\
			remplissage='red',tag='ball')
		time.sleep(0.030)

		mise_a_jour()
		#checking if the ball touches window edges
		if xBalle+rayonBalle >=largeurFen or xBalle-rayonBalle<=0:
			if backXballe:
				backXballe = False
			else:
				backXballe = True
		if yBalle+rayonBalle>=hauteurFen or yBalle-rayonBalle<=0:

			if backYballe:
				backYballe = False
			else:
				backYballe = True
		#moving the ball
		if backXballe:
			xBalle -= vitesseBalle
		else:
			xBalle += vitesseBalle
		if backYballe:
			# les additions/soustractions sont inversé par rapport à xBalle
			#car l'axe des y est inversé, il faut additioné pour monter
			yBalle += vitesseBalle
		else:
			yBalle -= vitesseBalle

		direction = changer_direction()








		


	fenetrePrinc.mainloop()
