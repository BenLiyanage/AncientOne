import pygame
from pygame.locals import *
import sprites
from sprites import AnimatedSprite, Actor
import ui
from ui import Menu, CharacterInfo

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

        font = pygame.font.Font('petme/PetMe128.ttf', 12)
        text = font.render("Hello There", 1, (250, 250, 250))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)

        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()
        
        menuItems = ['Attack','Wait','Special One', 'Special Two']
        myMenu = Menu("Action:", menuItems, font, 50, 50, 200, 200)
        tilesize=32
        PrincessImageSet = sprites.load_sliced_sprites(64,64,'images/princess.png')
        PrincessSprite = Actor((23-.5)*tilesize, (21-1)*tilesize,PrincessImageSet[1], PrincessImageSet[0], PrincessImageSet[2], PrincessImageSet[3], "Peach", 3, 2, 2, 6, 60)

        princessInfo = CharacterInfo(PrincessSprite, font, 600)
        # Event loop
        while 1:
                for event in pygame.event.get():
                        if event.type == QUIT:
                                return
                        action = myMenu.input(event)

                        if action is not None:
                                print action
                screen.blit(background, (0, 0))
                screen.blit(myMenu.surface, myMenu.rect)                
                screen.blit(princessInfo.surface, princessInfo.rect)
                pygame.display.flip()

if __name__ == '__main__': main()

