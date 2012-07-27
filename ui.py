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
		super(CharacterInfo,self).__init__(character._Name, font, 0, screenHeight-150, 300, 150)
		self._toolTips = []

		# Print Stats in columns

		# First Column
		xOffset = 10
		yOffset = self._titlePosition.bottom+15
                yOffset = self.AddTip("Health: " +str(character.Health())+"/"+str(character.MaxHealth()), "", xOffset, yOffset)+5
		yOffset = self.AddTip("Level: " + str(character.Level()), "", xOffset, yOffset) + 5
		yOffset = self.AddTip("Power: " + str(character.Power()), "", xOffset, yOffset) + 5
		self.AddTip("Speed: " + str(character.Speed()), "", xOffset, yOffset)

		# Second Column
		xOffset = 125
		yOffset = self._titlePosition.bottom+30

		yOffset = self.AddTip("Experience: " + str(int(character.Experience())), "", xOffset, yOffset) + 5
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

		self._BlipSound = pygame.mixer.Sound("sound/blip.wav")

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

                if self._currentMenuItem != itemNumber:
                        self._BlipSound.play(loops=0)
                
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
			print(itemNumber)
		elif (event.type == MOUSEMOTION):
			itemNumber = self.mouseOverItem()

			if itemNumber is not None:
				self.setActive(itemNumber)

		elif (event.type == MOUSEBUTTONUP):
                        
			itemNumber = self.mouseOverItem()
                        #itemNumber = self._currentMenuItem
			if itemNumber is not None:
                                #print('From UI',self._menuItems[itemNumber]['name'])
				return self._menuItems[itemNumber]['name']

	def mouseOverItem(self):
		x,y=pygame.mouse.get_pos()
		for itemNumber in range(len(self._menuItems)):
			if self._menuItems[itemNumber]['position'].collidepoint(x - self.rect.left, y - self.rect.top):
				return itemNumber			


class LevelUpScreen(Menu):
	def __init__(self, actor, title, font, x, y ,width, height):
                MOVE="Move"
                CANCEL="Cancel"
                WAIT="Wait"
                CLOSE="Close Window"
                self._menuItems = actor.GetActions()
                self._menuItems.remove(MOVE)
                self._menuItems.remove(CANCEL)
                self._menuItems.remove(WAIT)
                #self._menuItems.append(CLOSE)

                super(LevelUpScreen,self).__init__(title,self._menuItems ,font, x, y, width, height)
                
                
                self._text="Choose a skill to improve"
                self._text = font.render(self._text, 0, FONTCOLOR)
		self._textPosition = self._text.get_rect()
		self._textPosition.top = 15*len(self._menuItems)+20
		self._textPosition.left = 0
                self.surface.blit(self._text,self._textPosition )
                
                #displays different special attacks, you pick which to level up
                
                #once selected, you need to pass an action called "Next"
		print "stub"
