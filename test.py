import pygame
import AnimatedSprite

pygame.init()

sprite = AnimatedSprite()


while pygame.event.poll().type != KEYDOWN: pygame.time.delay(10)
