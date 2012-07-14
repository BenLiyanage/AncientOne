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

		screen.blit(background, (0, 0))
		screen.blit(myMenu._menuBackground, myMenu.rect)
		pygame.display.flip()


class Menu(object):

	def __init__(self, title, menuItems, font, x, y, width, height):

		self._font = font
		self._title = self._font.render(title, 0, (10, 10, 10))
		self._titlePosition = self._title.get_rect()
		self._titlePosition.top = 0
		self._titlePosition.left = 0
		self._menuItems = menuItems
		self._currentMenuItem = 0

		self._menuBackground = pygame.Surface((width, height))
		self._menuBackground = self._menuBackground.convert()
		self._menuBackground.fill((250,250,250))
		self._menuBackground.blit(self._title, self._titlePosition)

		self.rect = self._menuBackground.get_rect()
		self.rect.top = x
		self.rect.left = y
		
		itemY = self._titlePosition.bottom + 10
		itemX = self._titlePosition.left + 40

		for item in self._menuItems:
			print item
			itemText = self._font.render(item, 0, (10,10,10))			
			itemPosition = itemText.get_rect()
			itemPosition.top = itemY
			itemPosition.left = itemX
			itemY = itemPosition.bottom + 5
			self._menuBackground.blit(itemText, itemPosition)		
		


if __name__ == '__main__': main()


