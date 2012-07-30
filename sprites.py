# <Animated Sprites as well as individual character information is handled here.>
# Copyright (C) <2012>  <Phong Le and Benjamin Liyanage>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import random
import tiledtmxloader
#class AnimatedSprite(pygame.sprite.Sprite):
class AnimatedSprite(tiledtmxloader.helperspygame.SpriteLayer.Sprite):#PLE modification
	def __init__(self, images, x, y, fps = 20,tileoffset_x=0, tileoffset_y=0):             
		#pygame.sprite.Sprite.__init__(self)
                tiledtmxloader.helperspygame.SpriteLayer.Sprite.__init__(self,x,y)#PLE
		self._images = images
                self._DefaultImages = images
		# Track the time we started, and the time between updates.
		# Then we can figure out when we have to switch the image.
		self._start = pygame.time.get_ticks()
		self._delay = 1000 / fps
		self._lastImageRotation = 0
		self._imageRotationDelay = 1000 / fps
		self._lastAnimation = 0
		self._animationDelay = .001
		self._frame = 0
		self._MidAnimation = 0
		self._revertImageOnAnimationComplete = 0
		self._postAnimationAction = ""
		self.image = self._images[0]
		self._height = self.image.get_height()
		self._width = self.image.get_width()
		
		self._tilesize=32
		self.tile_x=int((x+self._tilesize/2-tileoffset_x) //self._tilesize)
                self.tile_y=int((y+self._tilesize-tileoffset_y) //self._tilesize)
                self._tileoffset_x=tileoffset_x
                self._tileoffset_y=tileoffset_y
		self.rect = pygame.Rect(x, y, self._height, self._width)
		self._destination = pygame.Rect(x, y, self._height, self._width)

		self._path=[]#this is a list of path instructions that the character must remember for multimove

		self.__g = {} # The groups the sprite is in. This is for http://www.pygame.org/docs/tut/SpriteIntro.html (added by PLE)

		#print "finished loading AnimatedSprite"

	def update(self, t):
		# Note that this doesn't work if it's been more that self._delay
		# time between calls to update(); we only update the image once
		# then, but it really should be updated twice.

		#self.rect = pygame.Rect(x, y, self.image._width, self.image._height)
                walkSpeed=2
		if t - self._lastAnimation > self._animationDelay:
			# handle movement adjustments
			if self.rect.top > self._destination.top:
				self.rect.move_ip(0,-walkSpeed)
			elif self.rect.top < self._destination.top:
				self.rect.move_ip(0,walkSpeed)

			if self.rect.left > self._destination.left:
				self.rect.move_ip(-walkSpeed, 0)
			elif self.rect.left < self._destination.left:
				self.rect.move_ip(walkSpeed, 0)

			if self.rect.left == self._destination.left and self.rect.top == self._destination.top:
				self._MidAnimation = 0
				
				#print("MidAnimation=0")

			self._lastAnimation = t

		if t - self._lastImageRotation > self._imageRotationDelay:
			self._frame += 1

		    	if self._frame >= len(self._images):
				if self._postAnimationAction == "revert" and self.Animating()==False:
                                        #if self.Animating()==False:
                                        self._postanimationAction =[]
					self._images = self._revertImageSet #maybe this should just be _DownImageSet 
				elif self._postAnimationAction == "dispose":
                                        #print("time to take out the trash!")
                                        #this tells the game board to remove the sprite                                        
					self._postAnimationAction = "remove"
					#print(self._postAnimationAction)
					
				self._frame = 0#-1
		    	self.image = self._images[self._frame]
		    	self._lastImageRotation = t
		    	#self._frame+=1

                if self._path !=[]and self._MidAnimation ==0:
                        self._path.reverse()#since pop() pulls the last element
                        nextmove=self._path.pop()
                        self._path.reverse()
                        self.Move(nextmove)
                
                        
                
		    	#Updates the tile coordinates (with the offset)
                self.tile_x=int((self.rect.x+self._tilesize/2-self._tileoffset_x) //self._tilesize)
                self.tile_y=int((self.rect.y+self._tilesize-self._tileoffset_y) //self._tilesize)	    	

	def setImageSet(self, imageSet, postAnimationAction):

		if postAnimationAction == 'revert':
			#self._revertImageSet = self._images
                        self._revertImageSet = self._DefaultImages
		
		self.image = imageSet[0]
		self._images = imageSet
		self._postAnimationAction = postAnimationAction
		self._frame = -1; #next update will force a redraw of the first frame


# Add and remove internal to be in any extension of the Sprite Class.  see http://www.pygame.org/docs/tut/SpriteIntro.html .(PLE)
        def add_internal(self, group):
                self.__g[group] = 0

        def remove_internal(self, group):
                del self.__g[group]




        def Animating(self):
                if self._path !=[] or self._MidAnimation ==1:
                        return True
                else:
                        return False

        def PostAnimationAction(self):
                return self._postAnimationAction

        



def load_sliced_sprites(w, h, filename):
	'''
	Specs :
	Master can be any height.
	Sprites frames width must be the same width
	Master width must be len(frames)*frame.width
	'''
	'''PC way to create paths: os.path.join('ressources', filename)'''
	master_image = pygame.image.load(filename).convert_alpha()
	master_width, master_height = master_image.get_size()
	#print master_height
	animationSet = []

	for y in xrange(int(master_height/h)):
		#print y
		images = []

		for x in xrange(int(master_width/w)):
			images.append(master_image.subsurface((x*w,y*h,w,h)))

		animationSet.append(images)
	return animationSet


class Actor(AnimatedSprite):
	def __init__(self, start_pos_x, start_pos_y, MoveUpImages, MoveLeftImages, MoveDownImages, MoveRightImages, \
                     DeathImages, AttackUpImages, AttackLeftImages, AttackDownImages, AttackRightImages, \
                     Name, Alignment ,Power, Defense, Speed, Movement, MaxHealth, Level=1, Experience=1,x=0,y=0):
		super(Actor, self).__init__(MoveDownImages, start_pos_x, start_pos_y, tileoffset_x=x, tileoffset_y=y)
                #super(tiledtmxloader.helperspygame.SpriteLayer.Sprite, self).__init__(MoveDownImages, 50,100)#Phong switched the order of the arguments cause tiledtmxloader didn't like it
		# Set Animations		
		self._MoveLeftImages = MoveLeftImages
		self._MoveUpImages = MoveUpImages
		self._MoveDownImages = MoveDownImages
		self._MoveRightImages = MoveRightImages
		self._DeathImages = DeathImages
                self._AttackLeftImages = AttackLeftImages
		self._AttackUpImages = AttackUpImages
		self._AttackDownImages = AttackDownImages
		self._AttackRightImages = AttackRightImages
		self._DefaultImages = MoveDownImages

		# Set Stats
                self._Name = Name
		self._Power = Power
		self._Defense = Defense
		self._Speed = Speed
		self._Movement = Movement
		self._Health = MaxHealth
		self._MaxHealth = MaxHealth
		self._Initiative = 0
		self._Experience = 0
		self._Level = 1
		self._LevelUp=False #Flags the level up UI in the main loop
		self._Actions = {}#this is the list passed to the UI
		self._Alignment= Alignment#'Friendly', 'Neutral', 'Hostile'

		self._WalkSound = pygame.mixer.Sound("sound/walk.wav")
                self._HitSound = pygame.mixer.Sound("sound/hit.wav")
		MOVE="Move"
                CANCEL="Cancel"
                WAIT="End Turn"
                self.RegisterAction(MOVE, "A character may move once per turn", self.MultiMove, self._MoveDownImages)
		self.RegisterAction(WAIT, "If you have not moved or taken an action, your next turn will come up sooner.", self.Wait, self._MoveDownImages)
		self.RegisterAction(CANCEL, "Cancels the current action", self.Wait, self._MoveDownImages)

        #RegisterAction is not completely used because attacks, special attacks in particular, are more easily handled through the TurnController.
	def RegisterAction(self, actionName, actionDescription, actionMethod, actionAnimation, actionSkillLevel=1):

		self._Actions[actionName] = [actionMethod, actionDescription, actionAnimation, actionSkillLevel]

	def LevelUpAction(self, actionName):
                self._Actions[actionName][3] +=1
                self._LevelUp=False
                #print(actionName," is now level ", self._Actions[actionName][3])
	def GetActionNames(self):
		return self._Actions.keys()
	def GetActions(self):
                return self._Actions
	
	def ActionLevel(self, actionName):
                return self._Actions[actionName][3]

	def PerformAction(self, actionName, actionParameters):
		# actionParameters will be passed to the actionMethod.
		self._Actions[actionName][0](actionParameters)
		self.SetImageSet(self._Actions[1], "revert")#???

	def StartTurn(self):
		self._Initiative = self._Initiative + self._Speed

        def Kill(self):
	#def Kill(self, AnimationLayer):
		self.setImageSet(self._DeathImages, "dispose")
		self._HitSound.play(loops=6)  ##REPLACE WITH A BETTER DEATH SOUND LATER
		self._HitSound.fadeout(1500)
		# TODO figure out if this is pass by value or pass by reference
		# this is needed for death animation so that we can remvoe it from the list
                 
		#self._AnimationLayer = AnimationLayer

		#if not self._MidAnimation:
		#	self._MidAnimation = 1;
                #        self._images = self._DeathImages
                print(self.Name(), 'has been killed!')
	def Wait(self):
		#Personal call:  
		#Making no offensive action lets you take your next action sooner, based on how fast you are.
		self._Initiative = self._Initiative + self._Speed
		#self._images = self._MoveDownImages 

	def Attack(self, target, attackPower, animate=True, sound=True): #the basic way one deals damage, this is how the AI deals damage
                dx, dy= self.tile_x-target.tile_x, self.tile_y-target.tile_y
                
                if  abs(dx)>abs(dy) and animate:
                        if dx<0:
                                self.setImageSet(self._AttackRightImages,"revert")
			else:
                                self.setImageSet(self._AttackLeftImages,"revert")
                elif  abs(dx)<=abs(dy) and animate:
                        if dy<=0:
                                self.setImageSet(self._AttackDownImages,"revert")
			else:
                                self.setImageSet(self._AttackUpImages,"revert")
                if sound:
                        self._HitSound.play(loops=1)
		damage = attackPower - target._Defense
		if damage <=0:
                        damage=1# you always deal at least one damage
                        
		experience = target.RecieveDamage(damage)#formula calcuated based on the level of the opponent and the damage
		#now we factor in the level of the attacker
		experience = int(experience*(1-.1*self.Level()))
		if experience<0: experience=1
		self.GetExperience(experience)

		print(self.Name(), 'has damaged', target.Name(),'for', damage, 'damage!')
		return damage

	def RecieveDamage(self, damage):
                damage=min(self._Health,damage) #this prevents extra xp from overkill
		self._Health = self._Health - damage

		experience = 10 + int(damage*(1+.1*self.Level()))#probably factor in level at some point
		if self._Health <= 0:
                        self.Kill()
                        experience +=self.Level()*5
		

		return experience#note this still needs to factor in the level of the attacker


	def GetExperience(self, newExperience):
		self._Experience = self._Experience + newExperience

		if self._Experience > 100:
			self._Experience = self._Experience % 100
			self._Level = self._Level + 1
			self._Power = self._Power + 1 + int(self._Power * .05)
			self._Defense = self._Defense + 1 + int(self._Defense * .05)
			self._Speed = self._Speed + 1 + int(self._Speed * .05)
			HealthBonus = 2 + int(self._MaxHealth * .05)
			self._MaxHealth = self._MaxHealth + HealthBonus
			self._Health = self._Health + int(HealthBonus/2)
			
			if self.Alignment()=='Friendly':
                                self._LevelUp=True
        def ForceLevel(self,level):#forces a player to have a given level.
                #print("forcelevel called to promote to level", level)
                if level-1>1:
                        for i in range(level-1):
                                self._Level = self._Level + 1
                                self._Power = self._Power + 1 + int(self._Power * .1)
                                self._Defense = self._Defense + 1 + int(self._Defense * .1)
                                self._Speed = self._Speed + 1 + int(self._Speed * .1)
                                HealthBonus =  5 + int(self._MaxHealth * .1)
                                self._MaxHealth = self._MaxHealth + HealthBonus
                                self._Health = self._Health + HealthBonus
                
        def Heal(self, target, healamount):

                target._Health +=healamount
                if target._Health > target._MaxHealth:
                        target._Health = target._MaxHealth
                print(target.Name(),"healed for", healamount)
                self.GetExperience(int(1.5*healamount)+4)

	def Move(self, direction):
		if not self._MidAnimation:
			self._MidAnimation = 1;
			self._WalkSound.play(loops=2)
			#print("MidAnimation =1")
				# TODO Need to accomodate for centering on the screen/not centering on the screen. PLE-made some adjustment in the gameboard to fix this
			if direction == "Left":
				self._images = self._MoveLeftImages
				self._destination.move_ip(-self._tilesize, 0)
			elif direction == "Up":
				self._images = self._MoveUpImages
				self._destination.move_ip(0, -self._tilesize)
			elif direction == "Down":
				self._images = self._MoveDownImages
				self._destination.move_ip(0, +self._tilesize)
			elif direction == "Right":
				self._images = self._MoveRightImages
				self._destination.move_ip(self._tilesize, 0)
			#self._MidAnimation = 1
	def MultiMove(self, newpath):
                self._path=newpath
        
                

	def Name(self):
                return self._Name
        def Alignment(self):
                return self._Alignment
	def Power(self):
		return self._Power
	def Defense(self):
		return self._Defense
	def Speed(self):
		return self._Speed
	def Movement(self):
		return self._Movement
	def Health(self):
		return self._Health
	def MaxHealth(self):
		return self._MaxHealth 
	def Initiative(self):
		return self._Initiative
	def Experience(self):
		return self._Experience
	def Level(self):
		return self._Level
	def LevelUp(self):
                return self._LevelUp






'''
	def update(self, t):
		AnimatedSprite.update(self, t)
'''
