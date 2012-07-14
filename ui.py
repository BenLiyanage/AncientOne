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
			action = myMenu.input(event)

			if action is not None:
				print action
		screen.blit(background, (0, 0))
		screen.blit(myMenu._menuBackground, myMenu.rect)		
		pygame.display.flip()


class InfoBox(object):
	def __init__(self):
		self._title = "placeholder"

class CharacterInfo(object):
	def __init__(self, character):
		self._background = pygame.Surface((100, 200))
		self._background.convert()
		self._background.fill((250,250,250))

class Menu(object):

	def __init__(self, title, menuItems, font, x, y, width, height):

		self._font = font
		self._title = self._font.render(title, 0, (10, 10, 10))
		self._titlePosition = self._title.get_rect()
		self._titlePosition.top = 0
		self._titlePosition.left = 0
		self._currentMenuItem = 0

		self._menuBackground = pygame.Surface((width, height))
		self._menuBackground = self._menuBackground.convert()
		self._menuBackground.fill((250,250,250))
		self._menuBackground.blit(self._title, self._titlePosition)

		self.rect = self._menuBackground.get_rect()
		self.rect.top = x
		self.rect.left = y

		self._indent = 40
		itemY = self._titlePosition.bottom + 10
		itemX = self._titlePosition.left + self._indent

		self._menuItems = []
		for item in menuItems:
			menuItem = {}
			menuItem['name'] = item
			menuItem['surface'] = self._font.render(item, 0, (10,10,10))			
			menuItem['position'] = menuItem['surface'].get_rect()
			menuItem['position'].top = itemY
			menuItem['position'].left = itemX
			itemY = menuItem['position'].bottom + 5
			self._menuBackground.blit(menuItem['surface'], menuItem['position'])		
			self._menuItems.append(menuItem)

	def setActive(self, itemNumber):
		self._menuItems[self._currentMenuItem]['surface'] = self._font.render(self._menuItems[self._currentMenuItem]['name'],0,(10,10,10), (250, 250, 250))
		self._menuBackground.blit(self._menuItems[self._currentMenuItem]['surface'], self._menuItems[self._currentMenuItem]['position'])

		self._menuItems[itemNumber]['surface'] = self._font.render(self._menuItems[itemNumber]['name'],0,(250,250,250), (10,10,10))
		self._menuBackground.blit(self._menuItems[itemNumber]['surface'], self._menuItems[itemNumber]['position'])

		self._currentMenuItem = itemNumber

	def input(self, event):
		itemNumber = self._currentMenuItem
		if (event.type==KEYDOWN):
			if (event.key == K_DOWN):
				if (self._currentMenuItem == len(self._menuItems)-1):
					itemNumber = 0
				else:
					itemNumber = self._currentMenuItem + 1
			elif (event.key == K_UP):
				if (self._currentMenuItem == 0):
					itemNumber = len(self._menuItems) - 1
				else:
					itemNumber = self._currentMenuItem - 1
			elif (event.key == K_RETURN):
				return self._menuItems[self._currentMenuItem]['name']

			self.setActive(itemNumber)
		elif (event.type == MOUSEMOTION):
			itemNumber = self.mouseOverItem()

			if itemNumber is not None:
				self.setActive(itemNumber)

		elif (event.type == MOUSEBUTTONUP):
			itemNumber = self.mouseOverItem()
			if itemNumber is not None:
				return self._menuItems[itemNumber]['name']

	def mouseOverItem(self):
		x,y=pygame.mouse.get_pos()
		for itemNumber in range(len(self._menuItems)):
			if self._menuItems[itemNumber]['position'].collidepoint(x - self.rect.left, y - self.rect.top):
				return itemNumber			


if __name__ == '__main__': main()


