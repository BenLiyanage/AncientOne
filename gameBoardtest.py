import sys
import os
#import array
import pygame

import collision
from collision import PopBestPath, PathList

import ui
from ui import Menu, CharacterInfo, LevelUpScreen

from pygame.locals import*

import sprites
from sprites import AnimatedSprite, Actor

import tiledtmxloader #this reads .tmx files
import GameBoard
from GameBoard import Board

import TurnController
from TurnController import Turn

import AutoTurn
from AutoTurn import TurnAI

MAP="images/map02.tmx"
STARTGAME="Start Game"

#alignments
FRIENDLY='Friendly'
HOSTILE='Hostile'
NEUTRAL = 'Neutral'

#other forms of attack

ATTACK="Attack"
WHIRLWIND="Whirlwind"
CRIPPLESTRIKE="Cripple"
RANGED="Ranged"
SPECIAL="Special"
HEAL="Heal"
AOE="Fire Lion"
MOVE="Move"
CANCEL="Cancel"
WAIT="End Turn"

#Special Modes
LEVELUP = 'Level Up'

actionList=[ATTACK, WHIRLWIND, CRIPPLESTRIKE, RANGED,SPECIAL,AOE, HEAL, MOVE,CANCEL]

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

    print(" x/c/v = move/wait/cancel, wasd=camera movement, '+/-' control the volume of the background music")


    myfont = pygame.font.Font("petme/PetMe128.ttf", 10)


    
    worldMap = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)
    assert worldMap.orientation == "orthogonal"
    screen_width = min(1024, worldMap.pixel_width)
    screen_height = min(768, worldMap.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))
    Characters = pygame.sprite.RenderUpdates()
    
    GameBoard = Board(worldMap, Characters, tileSize, screen)
    pygame.display.set_caption("Ancient Juan")


    #UI sprite container
    #UImenu = pygame.sprite.RenderUpdates()
    menuItems = ["Attack", "Move" ,"Wait", "Cancel"]#thse will be changed later
    myMenu = Menu("Action:", menuItems, myfont, 50, 150, 200, 200)
  

    #CHARACTERS!

    DeathImageSet=sprites.load_sliced_sprites(64,64,'images/skeleton_death.png')
    

    KnightDeathImageSet = sprites.load_sliced_sprites(64, 64, 'images/knight/knight_death.png')
    KnightImageSet = sprites.load_sliced_sprites(64, 64, 'images/knight/knight_walk.png')
    KnightAttackImageSet = sprites.load_sliced_sprites(64, 64, 'images/knight/knight_attack.png')
    KnightSprite = Actor((14-.5)*tileSize, (4-1)*tileSize, KnightImageSet[0], KnightImageSet[1], KnightImageSet[2], KnightImageSet[3], \
        KnightDeathImageSet[0], KnightAttackImageSet[0], KnightAttackImageSet[1], KnightAttackImageSet[2], KnightAttackImageSet[3], \
        "Buster", FRIENDLY ,10, 5, 5, 6, 16)
    #KnightSprite.RegisterAction(AOEAttack, 'The character conjures Feline Flames!', [],[])
    KnightSprite.RegisterAction(ATTACK, 'The character makes a powerful slash against adjacent target.',[],[])
    KnightSprite.RegisterAction(WHIRLWIND, 'the character spins in a flurry hitting all enemies up to two tiles away.', [],[])
    Characters.add(KnightSprite)
    

    ArcherDeathImageSet=sprites.load_sliced_sprites(64,64,'images/archer/archer_death.png')    
    ArcherImageSet = sprites.load_sliced_sprites(64, 64, 'images/archer/archer_walk.png')
    ArcherAttackImageSet = sprites.load_sliced_sprites(64, 64, 'images/archer/archer_attack.png')
    ArcherSprite = Actor((15-.5)*tileSize, (4-1)*tileSize, ArcherImageSet[0], ArcherImageSet[1], ArcherImageSet[2], ArcherImageSet[3], \
        DeathImageSet[0], ArcherAttackImageSet[0], ArcherAttackImageSet[1], ArcherAttackImageSet[2], ArcherAttackImageSet[3], \
        "Archie", FRIENDLY ,6, 4, 5, 5, 13)
    #ArcherSprite.RegisterAction(ATTACK, 'The character hits an adjacent target with the butt of his pistol',[],[])
    ArcherSprite.RegisterAction(RANGED, 'The character fires and arrow!', [],[])
    ArcherSprite.RegisterAction(CRIPPLESTRIKE, 'The character aims for a sensitive area, postponing the targets next turn.', [],[])
    Characters.add(ArcherSprite)
    
    ForestMageDeathImageSet=sprites.load_sliced_sprites(64,64,'images/forestmage/forestmage_death.png')
    ForestMageImageSet = sprites.load_sliced_sprites(64, 64, 'images/forestmage/forestmage_walk.png')
    ForestMageAttackImageSet = sprites.load_sliced_sprites(64, 64, 'images/forestmage/forestmage_spell.png')
    ForestMageSprite = Actor((16-.5)*tileSize, (4-1)*tileSize, ForestMageImageSet[0], ForestMageImageSet[1], ForestMageImageSet[2], ForestMageImageSet[3], \
        ForestMageDeathImageSet[0], ForestMageAttackImageSet[0], ForestMageAttackImageSet[1], ForestMageAttackImageSet[2], ForestMageAttackImageSet[3], \
        "Terra", FRIENDLY ,5, 3, 4, 5, 11)
    #MageSprite.RegisterAction(ATTACK, 'The character hits an adjacent target with the butt of his pistol',[],[])
    ForestMageSprite.RegisterAction(AOE, 'The character conjures Feline Flames!', [],[])
    ForestMageSprite.RegisterAction(HEAL, 'Restores the healt of yourself or an ally.', [], [])
    Characters.add(ForestMageSprite)
    
    

    # mainloop variables for gameplay
    frames_per_sec = 60.0
    clock = pygame.time.Clock()
    running = True
    paused=True #start the game paused
    grid=False #Debugging boolean to draw a grid
    startGame=True

    #Game Turns Controller
    PlayTurn=Turn(GameBoard)
    mode=PlayTurn.Mode()#used to detect when the mode changes for updating purposes

    #the Bad gusys
    PlayTurn.SpawnSkeleton(16,9)
    PlayTurn.SpawnSkeleton(22,13)
    PlayTurn.SpawnSkeleton(21,12)
    PlayTurn.SpawnMage(15,16)

    PlayTurn.SpawnPig(12,19)
    PlayTurn.SpawnPig(13,18)
  
  
    PlayTurn.SpawnPortal(2,6)
    PlayTurn.SpawnPortal(25,22)
    PlayTurn.SpawnPortal(12,41, level=2)
    PlayTurn.SpawnPortal(42,32, level=2)
    PlayTurn.SpawnPortal(64,8, level=3)
    PlayTurn.SpawnPortal(65,38, level=3)# eventually this will be the ancient one
    
    
    #Picks the first character
    CurrentSprite=PlayTurn.Next()
    CurrentSpriteInfo = CharacterInfo(PlayTurn.CurrentSprite(), myfont, screen_height)
    #LevelUpWindow = LevelUpScreen(CurrentSprite, CurrentSprite.Name()+'has gained a level!', myfont, 100,100,100,100)#they do not really level up, this just initialized the object
    myMenu = Menu("Turn:"+PlayTurn.CurrentSprite().Name(), PlayTurn.CurrentSprite().GetActionNames(), myfont, 50, 150, 200, 200, ActionItems = PlayTurn.CurrentSprite().GetActions())
    
    StartWindow = Menu("Defeat of the Ancient One", [STARTGAME], myfont, 100,100, 600,160, \
                       text="ARCHIE, BUSTER and TERRA have been following a disturbance in arcane energies to the edge of a deep fissure in the earth."+ \
                       "Just beyond the fissure they find what appears to be a green portal.  Before they can investigate they are ambushed by dark agents!"+\
                        " Control the players using the mouse. WASD keys move the camera.  + and - control the volume of the background music.")
    
    #Music
    BGvolume=.00#.05 #this is a number between 0 and 1
    BackgroundMusic =pygame.mixer.Sound("sound/wandering_around.wav")
    BackgroundMusic.play(loops=-1)
    BackgroundMusic.set_volume(BGvolume)
    LevelUpMusic = pygame.mixer.Sound("sound/levelup.wav")


    ##The Main Game Loop 
    while running:
        clock.tick(frames_per_sec)
        time = pygame.time.get_ticks()




        
        
        #checks for levelups,
        if PlayTurn.Mode()==LEVELUP and paused==False:# we are between turns

            if PlayTurn.CurrentSprite().LevelUp():#this is redundant
                print 'levelup!'
                paused=True
                LevelUpMusic.play(loops=0)
                CurrentSpriteInfo = CharacterInfo(PlayTurn.CurrentSprite(), myfont, screen_height)
                LevelUpWindow = LevelUpScreen(PlayTurn.CurrentSprite(), PlayTurn.CurrentSprite().Name()+' has gained a level!', myfont, 100,100,300,200)
                continue
                    

        #update the UI
        if (CurrentSprite != PlayTurn.CurrentSprite() or mode != PlayTurn.Mode() ) and PlayTurn.CurrentSprite !=[] and paused==False:
            CurrentSprite = PlayTurn.CurrentSprite()
            mode= PlayTurn.Mode()
            myMenu = Menu("Turn:"+PlayTurn.CurrentSprite().Name(), PlayTurn.CurrentActions(), myfont, 50, 150, 200, 200, ActionItems = PlayTurn.CurrentSprite().GetActions()) #CurrentActions is a list removing unavailable actions
            CurrentSpriteInfo = CharacterInfo(PlayTurn.CurrentSprite(), myfont, screen_height)
        #Move the camera manually with "wasd"


        #used these if you want to be able to hold down the mouse/keys
        pressedKeys=pygame.key.get_pressed() #actions that come from the keyboard This is for holding down
        pressedMouse = pygame.mouse.get_pressed() # mouse pressed event 3 booleans [button1, button2, button3]

        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos() #mouse coordinates
        tile_x, tile_y = mouse_pos_x// tileSize, mouse_pos_y // tileSize #note the board translates coordinates depending on the location of the camera
        for event in pygame.event.get():       
 
            if event.type == QUIT or event.type == pygame.QUIT or (pressedKeys[K_w] and pressedKeys[K_LMETA]):
                running = False
                pygame.quit()
                sys.exit()
                
            if PlayTurn.Mode()==LEVELUP and paused:
                action = LevelUpWindow.input(event)
            elif startGame and paused:
                action = StartWindow.input(event)
            else:
                action = myMenu.input(event) #actions that come from the menu
            
                
            if not (hasattr(event, 'key') or event.type==KEYDOWN or hasattr(event, 'button') or event.type==MOUSEBUTTONUP): continue
            #print(action)
            
            #UI or turn events
            if (action == STARTGAME):
                print("Let's Start the Game!!", action)
                paused=False
                startGame=True
            elif PlayTurn.CurrentSprite().Alignment() == HOSTILE:#if it is the enemy turn then turn off the inputs
                pass

                
            elif (action == MOVE or pressedKeys[K_x]) and PlayTurn.Mode()==[]:
                PlayTurn.MoveMode()

            elif (action == WAIT or pressedKeys[K_c]): #note right now this overrides whatever mode you were in, a back button might be nice 
                PlayTurn.EndTurn()
            elif(action == CANCEL or pressedKeys[K_v]):
                PlayTurn.CancelMode()
            elif (action in actionList or pressedKeys[K_z]) and PlayTurn.Mode()==[]:#right now it brings up a target list
                print("Entering Mode", action)
                PlayTurn.ActionMode(action)


            #the level up parts
            elif (action in actionList) and PlayTurn.Mode()==LEVELUP:
                CurrentSprite.LevelUpAction(action)
                PlayTurn._currentSprite=[]
                PlayTurn._mode=[]
                PlayTurn.Next()
                paused=False


            '''
            #single keystroke type inputs
            if event.key ==K_RIGHT: pygame.mouse.set_pos([mouse_pos_x+tileSize, mouse_pos_y])
            elif event.key == K_LEFT: pygame.mouse.set_pos([mouse_pos_x-tileSize, mouse_pos_y])
            elif event.key == K_UP: pygame.mouse.set_pos([mouse_pos_x, mouse_pos_y-tileSize])
            elif event.key == K_DOWN: pygame.mouse.set_pos([mouse_pos_x, mouse_pos_y+tileSize])
            '''
            #Debug
            if pressedKeys[K_g]: grid= not grid #DEBUG: this toggles the grid
            
        if pressedKeys[K_d]: GameBoard.MoveCamera(tileSize,0, relative=True) #right
        elif pressedKeys[K_a]: GameBoard.MoveCamera(-tileSize,0, relative=True)#left
        elif pressedKeys[K_w]: GameBoard.MoveCamera(0,-tileSize, relative=True) #up
        elif pressedKeys[K_s]: GameBoard.MoveCamera(0,tileSize, relative=True) #down

        elif pressedKeys[K_PLUS] or pressedKeys[K_EQUALS]:
            if BGvolume<1:
                BGvolume+=.05
        elif pressedKeys[K_MINUS] or pressedKeys[K_UNDERSCORE]:
            if BGvolume>0:
                BGvolume-=.05
        BackgroundMusic.set_volume(BGvolume)

        
        if pressedMouse[0]:
            print(GameBoard.getTile(mouse_pos_x, mouse_pos_y))
            #Seed what you clicked on and what turn mode you are in, then determins what to do
            if (PlayTurn.Mode()==ATTACK or PlayTurn.Mode()==RANGED or PlayTurn.Mode()==CRIPPLESTRIKE) and GameBoard.getTile(mouse_pos_x, mouse_pos_y)[0]=="Actor":
                PlayTurn.Attack(GameBoard.getTile(mouse_pos_x, mouse_pos_y)[1])
                CurrentSpriteInfo = CharacterInfo(PlayTurn.CurrentSprite(), myfont, screen_height)
                
            elif PlayTurn.Mode()==MOVE: #asks the game controller if the CurrentSprite can move there
                PlayTurn.Move(GameBoard.getTile(mouse_pos_x, mouse_pos_y)[2][0],GameBoard.getTile(mouse_pos_x, mouse_pos_y)[2][1] )
            elif PlayTurn.Mode()==AOE:
                PlayTurn.AOEAttack(tile_x, tile_y)
                CurrentSpriteInfo = CharacterInfo(PlayTurn.CurrentSprite(), myfont, screen_height)
            elif PlayTurn.Mode()==HEAL and GameBoard.getTile(mouse_pos_x, mouse_pos_y)[0]=="Actor":
                #print("heal called")
                PlayTurn.HealAction(GameBoard.getTile(mouse_pos_x, mouse_pos_y)[1])
                CurrentSpriteInfo = CharacterInfo(PlayTurn.CurrentSprite(), myfont, screen_height)

                
                    
                    
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
        if GameBoard.Animating() or paused:
            #print('Gameboard is animating or paused! Please be patient!', GameBoard.Animating(), paused)
            pass
        else:
            PlayTurn.update(time)


        #DEBUGGING: Grid
        if grid:#on a press of "g" the grid will be toggled
            for i in range(GameBoard._tileWidth):#draw vertical lines
                pygame.draw.line(screen, (0,0,0), (i*tileSize,0),(i*tileSize,GameBoard._width))
            for j in range(GameBoard._tileHeight):#draw horizontal lines
                pygame.draw.line(screen, (20,0,20), (0,j*tileSize),(GameBoard._height,j*tileSize))

        #moves the menu to the right if the camera is to the far left.
        if GameBoard.camTile()[0] < (myMenu.rect[0]+myMenu.rect[2])// tileSize:
            myMenu.rect[0]=screen_width-myMenu.rect[2]-50
            CurrentSpriteInfo.rect[0]=screen_width-CurrentSpriteInfo.rect[2]
        else:
            myMenu.rect[0]=50
            CurrentSpriteInfo.rect[0]=0
        if PlayTurn.CurrentSprite().Alignment()==FRIENDLY and paused==False:
            screen.blit(myMenu.surface, myMenu.rect)
        elif paused and PlayTurn.Mode()==LEVELUP:
            #print("Level up window for", CurrentSprite.Name())
            screen.blit(LevelUpWindow.surface, LevelUpWindow.rect)
        


        if GameBoard.getTile(mouse_pos_x, mouse_pos_y)[0]=="Actor" and paused==False:
                actor = GameBoard.getTile(mouse_pos_x, mouse_pos_y)[1]
                HoverWindow = CharacterInfo(actor, myfont, screen_height-150)
                screen.blit(HoverWindow.surface, HoverWindow.rect)
        screen.blit(CurrentSpriteInfo.surface, CurrentSpriteInfo.rect)


        if paused and startGame:
            screen.blit(StartWindow.surface, StartWindow.rect)

        pygame.display.flip()

#  -----------------------------------------------------------------------------


    


#  -----------------------------------------------------------------------------
#  -----------------------------------------------------------------------------
if __name__ == '__main__':

    main()
