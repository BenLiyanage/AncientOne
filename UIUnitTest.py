import pygame
from pygame.locals import *
import sprites
from sprites import AnimatedSprite, Actor
import ui
from ui import Menu

pygame.init()

def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('Basic Pygame program')

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	# Display some text

	font = pygame.font.Font(None, 36)
	text = font.render("Hello There", 1, (250, 250, 250))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)

	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	menuItems = ['Attack','Wait','Special One', 'Special Two']
	myMenu = Menu("Action:", menuItems, font, 50, 50, 200, 200)


	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			action = myMenu.input(event)

			if action is not None:
				print action
		screen.blit(background, (0, 0))
		screen.blit(myMenu._menuBackground, myMenu.rect)		
		pygame.display.flip()

if __name__ == '__main__': main()

