import pygame
from pygame.locals import *
import sprites
from sprites import AnimatedSprite, Actor

pygame.init()

screen = pygame.display.set_mode((800,600))
background = pygame.Surface([800,600])
background.fill([0,0,0]) #'''black background'''

PrincessImageSet = sprites.load_sliced_sprites(64,64,'princess.png')
PrincessSprite = Actor(PrincessImageSet[1], PrincessImageSet[0], PrincessImageSet[2], PrincessImageSet[3], 0, 0, 0, 0, 0)

Characters = pygame.sprite.RenderUpdates()
Characters.add(PrincessSprite)

clock = pygame.time.Clock()

while 1:

	for event in pygame.event.get():
		if event.type == QUIT: sys.exit(0)

		if not hasattr(event, 'key') or event.type!=KEYDOWN: continue
		if event.key == K_RIGHT: PrincessSprite.Move("Right")
		elif event.key == K_LEFT: PrincessSprite.Move("Left")
		elif event.key == K_UP: PrincessSprite.Move("Up")
		elif event.key == K_DOWN: PrincessSprite.Move("Down")
			
	clock.tick(30)
	time = pygame.time.get_ticks() 
	Characters.clear(screen, background)
	Characters.update(time)
	rectList = Characters.draw(screen)
	pygame.display.update(rectList)

#	PrincessSprite.update(time)
#	screen.blit(PrincessSprite.image, PrincessSprite.rect)
#	pygame.display.flip()

