import pygame
from pygame.locals import *
import sprites
from sprites import AnimatedSprite

pygame.init()

screen = pygame.display.set_mode((800,600))
background = pygame.Surface([800,600])
background.fill([0,0,0]) #'''black background'''

PrincessImages = sprites.load_sliced_sprites(64,64,'princess-front.png')
PrincessSprite = AnimatedSprite(PrincessImages, 50, 100)

Characters = pygame.sprite.RenderUpdates()
Characters.add(PrincessSprite)

clock = pygame.time.Clock()

while 1:

	for event in pygame.event.get():
		if event.type == QUIT: sys.exit(0)

		if not hasattr(event, 'key') or event.type!=KEYDOWN: continue
		if event.key == K_RIGHT: PrincessSprite.rect.move_ip(5, 0)
		elif event.key == K_LEFT: PrincessSprite.rect.move_ip(-5, 0)
		elif event.key == K_UP: PrincessSprite.rect.move_ip(0, -5)
		elif event.key == K_DOWN: PrincessSprite.rect.move_ip(0, 5)
			
	clock.tick(30)
	time = pygame.time.get_ticks() 
	Characters.clear(screen, background)
	Characters.update(time)
	rectList = Characters.draw(screen)
	pygame.display.update(rectList)
#	PrincessSprite.update(time)
#	screen.blit(PrincessSprite.image, PrincessSprite.rect)
#	pygame.display.flip()

