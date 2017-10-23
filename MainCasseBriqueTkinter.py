from upemtk import *
import time
from tkinter import *


def keypress_handler(event):
	print(event.keysym,' cliqué')
	if event.keysym=='Right':
		return(True,'droite')
	elif event.keysym == 'Left':
		return(True,'gauche')
	elif event.keysym=='Right':
		return(False,'immobile')
	elif event.keysym == 'Left':
		return(False,'immobile')



if __name__ == '__main__':
	largeurFen = 500
	hauteurFen = 500
	fenetrePrinc = Tk()
	canvasFen = Canvas(fenetrePrinc,width = largeurFen,height=hauteurFen)
	canvasFen.pack()
	#---le carré---
	hauteurRect = 30
	largeurRect = 60
	xRect = largeurFen//2
	yRect = hauteurFen-hauteurRect
	deplacerRect = (False,'immobile')

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
		canvasFen.delete('ball')
		canvasFen.delete('rect')
		canvasFen.create_rectangle(xRect,yRect,xRect+largeurRect,yRect+hauteurRect,\
			fill='black',tag='rect')
		canvasFen.create_oval(xBalle-rayonBalle,yBalle-rayonBalle,\
			xBalle+rayonBalle,yBalle +rayonBalle,fill='red',tag='ball')
		time.sleep(0.030)

		canvasFen.update()
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


		print(deplacerRect, 'deplacer')
		if deplacerRect[0] == True:
			
			fenetrePrinc.unbind('<KeyPress>')
			fenetrePrinc.unbind('<KeyRelease>')
			if deplacerRect[1] == 'droite':
				xRect += vitesseRect
			elif deplacerRect[1] == 'gauche':
				xRect -= vitesseRect


		else:
			fenetrePrinc.bind('<KeyPress>',keypress_handler)
			fenetrePrinc.bind('<KeyRelease>',keyrelease_handler)






		


	fenetrePrinc.mainloop()