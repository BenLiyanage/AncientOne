import pygame
from pygame.locals import *

pygame.init()

FONTCOLOR = (10, 10, 10)
BACKGROUNDCOLOR = (250,250,250)
BLUE = (0,0,255)
RED  =( 255,0,0)
VIOLET = ( 130,0,255)

class InfoBox(object):
	def __init__(self, title, font, x, y, width, height):

		self._font = font

		self._title = title
		self._title = self._font.render(title, 0, RED)
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
		super(CharacterInfo,self).__init__(character._Name, font, 0, screenHeight-150, 300, 200)
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

	def __init__(self, title, menuItems, font, x, y, width, height,text="",ActionItems=[]):

                textwidth=width-40#max width of text
                textList=TextChunks(text,int(width/12),[])
                

		super(Menu,self).__init__(title, font, x, y, width, height+15*len(textList))

		self._x=x
		self._y=y
		self._width=width
		self._height=height
		self._ActionItems=ActionItems
		#print(ActionItems)
                self._indent = 40
		itemY = self._titlePosition.bottom + 10 
		itemX = self._titlePosition.left + self._indent

		
                for item in textList:
			textItem = {}
			textItem['name'] = item
			textItem['surface'] = self._font.render(item, 0, VIOLET)
			textItem['position'] = textItem['surface'].get_rect()
			textItem['position'].top = itemY
			textItem['position'].left = itemX
			itemY = textItem['position'].bottom + 5
			self.surface.blit(textItem['surface'], textItem['position'])
                
		self._currentMenuItem = 0

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

		self._menuY=itemY
		self._itemY=itemY
		self._itemX=itemX
		

	def setActive(self, itemNumber):
		self._menuItems[self._currentMenuItem]['surface'] = self._font.render(self._menuItems[self._currentMenuItem]['name'],0,FONTCOLOR, BACKGROUNDCOLOR)
		self.surface.blit(self._menuItems[self._currentMenuItem]['surface'], self._menuItems[self._currentMenuItem]['position'])

		self._menuItems[itemNumber]['surface'] = self._font.render(self._menuItems[itemNumber]['name'],0,BACKGROUNDCOLOR, FONTCOLOR)
		self.surface.blit(self._menuItems[itemNumber]['surface'], self._menuItems[itemNumber]['position'])

                if self._currentMenuItem != itemNumber:
                        self._BlipSound.play(loops=0)
                
		self._currentMenuItem = itemNumber

		

                #draws the description text.
                #eraserRect = pygame.rect(0,self._menuY,self._width, self._height-self._menuY)
		if self._ActionItems !=[]:
                        pygame.draw.rect(self.surface,BACKGROUNDCOLOR,(0,self._menuY,self._width, self._height-self._menuY+15))


                        
                        self._itemY=self._menuY
                        itemDescription = {}
                        itemDescriptionText = self._ActionItems[self._menuItems[itemNumber]['name']][1]
                        textList= TextChunks(itemDescriptionText,15,[])
                        #print(textList)
                        for item in textList:
                                #print(itemDescriptionText)
                                itemDescription['name'] = item
                                itemDescription['surface'] = self._font.render(item, 0, BLUE)
                                itemDescription['position'] = itemDescription['surface'].get_rect()
                                itemDescription['position'].top = self._itemY
                                itemDescription['position'].left = self._itemX
                                self._itemY = itemDescription['position'].bottom + 5
                                self.surface.blit(itemDescription['surface'], itemDescription['position'])
		

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
                WAIT="End Turn"
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

def TextChunks(l,n,list):#still recursive
        l=l.strip()
        if l==[]:
                return list
        elif len(l)<n:
                list.append(l[0:len(l)])
                return list
        else:

                k=PreviousWord(l,n)
                if k==n:
                    list.append(l[0:n])
                    return list+TextChunks(l[n:len(l)],n,[])
                else:
                    list.append(l[0:k])
                    return list+TextChunks(l[k:len(l)],n,[])
        
def PreviousWord(l,j): #returns the end of the first full word prior to the index. 
        #print("previous word list", l)
        if len(l)<j:
            return 0
        if j==0:
                return 0
        for i in range(j):
                #print("len of l",len(l))
                #print("j",j)
                #print("i",i)
                #print("j-i",j-i)
                if len(l) <=j-i:
                        return j-i
                elif l[j-i]==" ":
                        return j-i
                elif j>i and l[j-i]!=" " and l[j-i-1]==" ":
                        return j-i
        return 0
        
        
