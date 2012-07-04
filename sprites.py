import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, images, x, y, fps = 10):
        pygame.sprite.Sprite.__init__(self)
        self._images = images

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0

        # Call update to set our first image.
        self.update(pygame.time.get_ticks())

	# Set some default values for use in calcuating positioning.
#	print x + ' ' +  y + ' ' +self.image.get_height() + ' ' +self.image.get_width()
	self.rect = pygame.Rect(x, y, self.image.get_height(), self.image.get_width())

    def update(self, t):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.

	#self.rect = pygame.Rect(x, y, self.image._width, self.image._height)

        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images): self._frame = 0
            self.image = self._images[self._frame]
            self._last_update = t


def load_sliced_sprites(w, h, filename):
    '''
    Specs :
    	Master can be any height.
    	Sprites frames width must be the same width
    	Master width must be len(frames)*frame.width
    Assuming you ressources directory is named "ressources"
    '''
    images = []
    '''PC way to create paths: os.path.join('ressources', filename)'''
    master_image = pygame.image.load(filename).convert_alpha()

    master_width, master_height = master_image.get_size()
    for i in xrange(int(master_width/w)):
    	images.append(master_image.subsurface((i*w,0,w,h)))
    return images

class Actor(AnimatedSprite):
	def __init__(self, MoveLeftImages, MoveUpImages, MoveDownImages):
		AnimatedSprite.__init(self, MoveDownImages, 50, 100)
		self._MoveLeftImages = MoveLeftImages
		self._MoveUpImages = MoveUpImages
		self._MoveDownImages = MoveDownImages
		self._MidAnimation = false

	def Move(self, direction):
		if (not self._MidAnimation)
			
		
