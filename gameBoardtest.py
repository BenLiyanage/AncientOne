import sys
import os
#import array
import pygame

#import collision
#from collision import CollisionFinder, PopBestPath

#import ui
#from ui import Menu, CharacterInfo

from pygame.locals import*

import sprites
from sprites import AnimatedSprite, Actor

import tiledtmxloader #this reads .tmx files
import GameBoard
from GameBoard import Board

MAP="images/map01.tmx"

tileSize=32

def main():
    """
    Main method.
    """
    args = sys.argv[1:]
    if len(args) < 1:
        path_to_map = os.path.join("", MAP) #Loads the map path
        #print(("usage: python %s your_map.tmx\n\nUsing default map '%s'\n" % \
        #    (os.path.basename(__file__), path_to_map)))
    else:
        path_to_map = args[0]

    main_pygame(path_to_map)

def main_pygame(file_name):

    

    pygame.init()
    
    worldMap = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)
    assert worldMap.orientation == "orthogonal"
    screen_width = min(1024, worldMap.pixel_width)
    screen_height = min(768, worldMap.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))
    Characters = pygame.sprite.RenderUpdates()
    
    GameBoard = Board(worldMap, Characters, tileSize, screen)


        #CHARACTERS!
    #
    
    #Obligatory Female Supporting Character (with sassyness!)
    PrincessImageSet = sprites.load_sliced_sprites(64,64,'images/princess.png')
    PrincessSprite = Actor((23-.5)*tileSize, (21-1)*tileSize,PrincessImageSet[1], PrincessImageSet[0], PrincessImageSet[2], PrincessImageSet[3], "Peach", 30, 2, 2, 6, 60)
    Characters.add(PrincessSprite)
  
    #Bebop's Legacy
    PigImageSet = sprites.load_sliced_sprites(64, 64, 'images/pigman_walkcycle.png')
    PigSprite = Actor((24-.5)*tileSize, (21-1)*tileSize, PigImageSet[1], PigImageSet[0], PigImageSet[2], PigImageSet[3], "Bebop", 20, 2, 5, 5, 60)
    Characters.add(PigSprite)
    
    #Solider of Fortune
    SoldierImageSet = sprites.load_sliced_sprites(64, 64, 'images/base_assets/soldier.png')
    SoldierSprite = Actor((25-.5)*tileSize, (21-1)*tileSize, SoldierImageSet[1], SoldierImageSet[0], SoldierImageSet[2], SoldierImageSet[3], "Bald Cloud", 30, 4, 3, 3, 80)
    Characters.add(SoldierSprite)

    #www.whoisthemask.com
    MaskImageSet = sprites.load_sliced_sprites(64, 64, 'images/maskman.png')
    MaskSprite = Actor((26-.5)*tileSize, (21-1)*tileSize, MaskImageSet[1], MaskImageSet[0], MaskImageSet[2], MaskImageSet[3],"Tuxedo Mask" ,20, 2, 5, 5, 75)
    Characters.add(MaskSprite)

    #Skeletastic
    SkeletonImageSet = sprites.load_sliced_sprites(64, 64, 'images/skeleton.png')
    SkeletonSprite = Actor((27-.5)*tileSize, (21-1)*tileSize, SkeletonImageSet[1], SkeletonImageSet[0], SkeletonImageSet[2], SkeletonImageSet[3], "Jack" ,40, 3, 2, 6, 50)
    Characters.add(SkeletonSprite)

    
    

    # mainloop variables for gameplay
    frames_per_sec = 60.0
    clock = pygame.time.Clock()
    running = True
    grid=False #Debugging boolean to draw a grid

    CurrentActor = []
    TurnMode=[]

    ##The Main Game Loop 
    while running:
        clock.tick(frames_per_sec)
        time = pygame.time.get_ticks()
        

        
        
        #used these if you want to be able to hold down the mouse/keys
        pressedKeys=pygame.key.get_pressed() #actions that come from the keyboard This is for holding down
        pressedMouse = pygame.mouse.get_pressed() # mouse pressed event 3 booleans [button1, button2, button3]

        #Move the camera manually with "wasd"
        if pressedKeys[K_d]: GameBoard.MoveCamera(tileSize,0, relative=True) #right
        elif pressedKeys[K_a]: GameBoard.MoveCamera(-tileSize,0, relative=True)#left
        elif pressedKeys[K_w]: GameBoard.MoveCamera(0,-tileSize, relative=True) #up
        elif pressedKeys[K_s]: GameBoard.MoveCamera(0,tileSize, relative=True) #down
        

        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos() #mouse coordinates
        
        for event in pygame.event.get():
            if event.type == QUIT or event.type == pygame.QUIT or (pressedKeys[K_w] and pressedKeys[K_LMETA]):
                running = False
                pygame.quit()
                sys.exit()
            if not hasattr(event, 'key') or event.type!=KEYDOWN: continue
            
            #single keystroke type inputs
            if event.key ==K_RIGHT: pygame.mouse.set_pos([mouse_pos_x+tileSize, mouse_pos_y])
            elif event.key == K_LEFT: pygame.mouse.set_pos([mouse_pos_x-tileSize, mouse_pos_y])
            elif event.key == K_UP: pygame.mouse.set_pos([mouse_pos_x, mouse_pos_y-tileSize])
            elif event.key == K_DOWN: pygame.mouse.set_pos([mouse_pos_x, mouse_pos_y+tileSize])

            #Debug
            elif event.key==K_g: grid= not grid #DEBUG: this toggles the grid
            elif event.key == K_h: GameBoard.PanCamera(3*tileSize,3*tileSize, relative=True)
            elif event.key == K_j: 

            '''
            #Debugging Spawn a PigMan
            #Bebop's Brood
            elif event.key == K_1: 
                NewPigSprite = Actor((20-.5)*tileSize, (20-1)*tileSize, PigImageSet[1], PigImageSet[0], PigImageSet[2], PigImageSet[3],"Pig Spawn" ,2, 2, 5, 5, 60)
                Characters.add(NewPigSprite)                  
                sprite_layers[objectlayer].add_sprites(Characters)
            elif event.key == K_2:
                Characters.remove(NewPigSprite)
                sprite_layers[objectlayer].remove_sprite(NewPigSprite)
            '''

            

        Characters.update(time)  
        GameBoard.update(time)


        #DEBUGGING: Grid
        if grid:#on a press of "g" the grid will be toggled
            for i in range(GameBoard._tileWidth):#draw vertical lines
                pygame.draw.line(screen, (0,0,0), (i*tileSize,0),(i*tileSize,GameBoard._width))
            for j in range(GameBoard._tileHeight):#draw horizontal lines
                pygame.draw.line(screen, (20,0,20), (0,j*tileSize),(GameBoard._height,j*tileSize))

                
        pygame.display.flip()





if __name__ == '__main__':

    main()
