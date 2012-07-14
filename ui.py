import pygame
from pygame.locals import *

pygame.init()

FONTCOLOR = (10, 10, 10)
BACKGROUNDCOLOR = (250,250,250)

class InfoBox(object):
	def __init__(self, title, font, x, y, width, height):

		self._font = font

		self._title = title
		self._title = self._font.render(title, 0, FONTCOLOR)
		self._titlePosition = self._title.get_rect()
		self._titlePosition.top = 0
		self._titlePosition.left = 0

		self.surface = pygame.Surface((width, height))
		self.surface.convert()
		self.surface.fill(BACKGROUNDCOLOR)
		self.surface.blit(self._title, self._titlePosition)

		self.rect = self.surface.get_rect()
		self.rect.top = y
		self.rect.left = x

class CharacterInfo(InfoBox):
	def __init__(self, character, font, screenHeight):
		super(CharacterInfo,self).__init__(character._Name, font, 0, screenHeight-100, 300, 150)
		self._toolTips = []

		# Print Stats in columns

		# First Column
		xOffset = 10
		yOffset = self._titlePosition.bottom+10

		yOffset = self.AddTip("Level: " + str(character.Level()), "", xOffset, yOffset) + 5
		yOffset = self.AddTip("Power: " + str(character.Power()), "", xOffset, yOffset) + 5
		self.AddTip("Speed: " + str(character.Speed()), "", xOffset, yOffset)

		# Second Column
		xOffset = 125
		yOffset = self._titlePosition.bottom+10

		yOffset = self.AddTip("Experience: " + str(character.Experience()), "", xOffset, yOffset) + 5
		yOffset = self.AddTip("Defense: " + str(character.Defense()), "", xOffset, yOffset) + 5
		self.AddTip("Movement: " + str(character.Movement()), "", xOffset, yOffset)

	def AddTip(self, label, description, x, y):
		tip = {}
		tip['surface'] = self._font.render(label, 0, FONTCOLOR)
		tip['rect'] = tip['surface'].get_rect()
		tip['rect'].top = y
		tip['rect'].left = x
		tip['description'] = description
		self._toolTips.append(tip)

		self.surface.blit(tip['surface'],tip['rect'])

		return tip['rect'].bottom

class Menu(InfoBox):

	def __init__(self, title, menuItems, font, x, y, width, height):

		super(Menu,self).__init__(title, font, x, y, width, height)

		self._currentMenuItem = 0

		self._indent = 40
		itemY = self._titlePosition.bottom + 10
		itemX = self._titlePosition.left + self._indent

		self._menuItems = []
		for item in menuItems:
			menuItem = {}
			menuItem['name'] = item
			menuItem['surface'] = self._font.render(item, 0, FONTCOLOR)
			menuItem['position'] = menuItem['surface'].get_rect()
			menuItem['position'].top = itemY
			menuItem['position'].left = itemX
			itemY = menuItem['position'].bottom + 5
			self.surface.blit(menuItem['surface'], menuItem['position'])		
			self._menuItems.append(menuItem)

	def setActive(self, itemNumber):
		self._menuItems[self._currentMenuItem]['surface'] = self._font.render(self._menuItems[self._currentMenuItem]['name'],0,FONTCOLOR, BACKGROUNDCOLOR)
		self.surface.blit(self._menuItems[self._currentMenuItem]['surface'], self._menuItems[self._currentMenuItem]['position'])

		self._menuItems[itemNumber]['surface'] = self._font.render(self._menuItems[itemNumber]['name'],0,BACKGROUNDCOLOR, FONTCOLOR)
		self.surface.blit(self._menuItems[itemNumber]['surface'], self._menuItems[itemNumber]['position'])

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

