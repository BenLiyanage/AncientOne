import pygame
import tiledtmxloader
#class AnimatedSprite(pygame.sprite.Sprite):
class AnimatedSprite(tiledtmxloader.helperspygame.SpriteLayer.Sprite):#PLE modification
	def __init__(self, images, x, y, fps = 10):             
		#pygame.sprite.Sprite.__init__(self)
                tiledtmxloader.helperspygame.SpriteLayer.Sprite.__init__(self,x,y)#PLE
		self._images = images

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

		self.rect = pygame.Rect(x, y, self._height, self._width)
		self._destination = pygame.Rect(x, y, self._height, self._width)


		print "finished loading AnimatedSprite"

	def update(self, t):
		# Note that this doesn't work if it's been more that self._delay
		# time between calls to update(); we only update the image once
		# then, but it really should be updated twice.

		#self.rect = pygame.Rect(x, y, self.image._width, self.image._height)

		if t - self._lastAnimation > self._animationDelay:
			# handle movement adjustments
			if self.rect.top > self._destination.top:
				self.rect.move_ip(0,-1)
			elif self.rect.top < self._destination.top:
				self.rect.move_ip(0,1)

			if self.rect.left > self._destination.left:
				self.rect.move_ip(-1, 0)
			elif self.rect.left < self._destination.left:
				self.rect.move_ip(1, 0)

			if self.rect.left == self._destination.left and self.rect.top == self._destination.top:
				self._MidAnimation = 0 

			self._lastAnimation = t

		if t - self._lastImageRotation > self._imageRotationDelay:
			self._frame += 1

		    	if self._frame >= len(self._images): 
				if self._postAnimationAction == "revert":
					self._images = self._revertImageSet
				elif self._postAnimationAction == "dispose":
					# TODO
					# need to trigger some way to remove this object from the set of things to update

					# not sure if this will work.  I suspect that ._AnimationLayer is 
					# pass by value rather then pass by reference
					self._AnimationLayer.remove(self)

				self._frame = 0
		    	self.image = self._images[self._frame]
		    	self._lastImageRotation = t

	def setImageSet(self, imageSet, postAnimationAction):

		if postAnimationAction == 'revert':
			self._revertImageSet = self._images
		
		self.image = imageSet[0]
		self._images = imageSet
		self._postAnimationAction = postAnimationAction
		self._frame = -1; #next update will force a redraw of the first frame




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
	print master_height
	animationSet = []

	for y in xrange(int(master_height/h)):
		print y
		images = []

		for x in xrange(int(master_width/w)):
			images.append(master_image.subsurface((x*w,y*h,w,h)))

		animationSet.append(images)
	return animationSet


class Actor(AnimatedSprite):
	def __init__(self, start_pos_x, start_pos_y, MoveLeftImages, MoveUpImages, MoveDownImages, MoveRightImages, Power, Defense, Speed, Movement, MaxHealth, Level=1, Experience=1, DeathImages = []):
		super(Actor, self).__init__(MoveDownImages, start_pos_x, start_pos_y)
                #super(tiledtmxloader.helperspygame.SpriteLayer.Sprite, self).__init__(MoveDownImages, 50,100)#Phong switched the order of the arguments cause tiledtmxloader didn't like it
		# Set Animations		
		self._MoveLeftImages = MoveLeftImages
		self._MoveUpImages = MoveUpImages
		self._MoveDownImages = MoveDownImages
		self._MoveRightImages = MoveRightImages
		self._DeathImages = DeathImages

		# Set Stats
		self._Power = Power
		self._Defense = Defense
		self._Speed = Speed
		self._Movement = Movement
		self._Health = MaxHealth
		self._MaxHealth = MaxHealth
		self._Initiative = 0
		self._Actions = {}
		
		self.__g = {} # The groups the sprite is in. This is for http://www.pygame.org/docs/tut/SpriteIntro.html (added by PLE)
                self.tilesize=32
                
		self.RegisterAction("wait", "Take no action for the turn in order to take your next turn sooner.", self.Wait, self._MoveDownImages)

        
	def Move(self, direction):
		if not self._MidAnimation:
			self._MidAnimation = 1;
				# TODO Need to accomodate for centering on the screen/not centering on the screen
			if direction == "Left":
				self._images = self._MoveLeftImages
				self._destination.move_ip(-self.tilesize, 0)
			elif direction == "Up":
				self._images = self._MoveUpImages
				self._destination.move_ip(0, -self.tilesize)
			elif direction == "Down":
				self._images = self._MoveDownImages
				self._destination.move_ip(0, +self.tilesize)
			elif direction == "Right":
				self._images = self._MoveRightImages
				self._destination.move_ip(self.tilesize, 0)

	def RegisterAction(self, actionName, actionDescription, actionMethod, actionAnimation, actionSkillLevel=-1):

		self._Actions[actionName] = [actionMethod, actionDescription, actionAnimation, actionSkillLevel]

	def GetActions(self):
	
		return self._Actions.keys()

	def PerformAction(self, actionName, actionParameters):
		# actionParameters will be passed to the actionMethod.
		self._Actions[actionName][0](actionParameters)
		self.SetImageSet(self._Actions[1], "revert")

	def StartTurn(self):
		self._Initiative = self._Initiative + self._Speed

	def Kill(self, AnimationLayer):
		self.setImageSet(self, self._DeathImages, "dispose")
		# TODO figure out if this is pass by value or pass by reference
		# this is needed for death animation so that we can remvoe it from the list
		self._AnimationLayer = AnimationLayer

	def Wait(self):
		#Personal call:  
		#Making no offensive action lets you take your next action sooner, based on how fast you are.
		self._Initiative = self._Initiative + self._Speed

	def Attack(self, target):
		damage = self._Power - target._Defense
		experience = target.RecieveDamage(damage)
		self.GetExperience(experience)

	def RecieveDamage(self, damage):
		self._Health = self._Health - damage
		if self._Health <= 0:
			# TODO: Need to get AnimationLayer from somewhere
			self.Kill(self._AnimationLayer)
		experience = 10 + (damage * .1)
		return experience

	def GetExperience(newExperience):
		self._Experience = self._Experience + newExperience

		if self._Experience > 100:
			self._Experience = self._Experience % 100
			self._Level = self._Level + 1
			self._Power = self._Power + 1 + (self._Power * .1)
			self._Defense = self._Defense + 1 + (self._Defense * .1)
			self._Speed = self._Speed + 1 + (self._Speed * .1)
			HealthBonus = self._MaxHealth + 10 + (self._MaxHealth * .1)
			self._MaxHealth = self._MaxHealth + HealthBonus
			self._Health = self._Health + HealthBonus

# These need to be in any extension of the Sprite Class.  see http://www.pygame.org/docs/tut/SpriteIntro.html .(PLE)
        def add_internal(self, group):
                self.__g[group] = 0

        def remove_internal(self, group):
                del self.__g[group]

'''
	def update(self, t):
		AnimatedSprite.update(self, t)
'''
