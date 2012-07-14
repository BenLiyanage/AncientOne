import pygame
from pygame.locals import *

pygame.init()

def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('Basic Pygame program')

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	# Display some text

	font = pygame.font.Font(None, 36)
	text = font.render("Hello There", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)

	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()

	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(background, (0, 0))
		pygame.display.flip()


class Menu(object)

	def __init__(self, title, menuItems, x, y, width, height):

		self._title = title
		self._menuItems = menuItems
		self._currentMenuItem = 0

if __name__ == '__main__': main()


