import sys
import os
import array
import pygame
import collision
from collision import CollisionFinder, PopBestPath

import ui
from ui import Menu, CharacterInfo

from pygame.locals import*

import sprites
from sprites import AnimatedSprite, Actor

import tiledtmxloader #this reads .tmx files

#Variables (WARNING: Does not necessarily follow standard python etiquette)
tilesize=32
#Layers, lower renders first
baselayer=0 # the ground
fringelayer=1 #grass etc
shadowlayer=2 # mostly to render below Actors but above the ground
objectlayer=3 #where the Actors (Characters) go
overhanglayer=4 # things that render over the characters
collisionlayer=5 #in the release version this will be invisible, (Red Blocks)

initiative_threshold = 50# When someone's initiative is above this cutoff their turn is up.  We just need this to be much bigger than anyone's speed.

global cam_world_pos_xmin, cam_world_pos_xmax, cam_world_pos_ymin, cam_world_pos_ymax, cam_world_pos_x, cam_world_pos_y


MAP="images/map01.tmx"
#MAP = "images/citysample.tmx" #small map for testing

#  -----------------------------------------------------------------------------

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

    

#  -----------------------------------------------------------------------------def main(): 

def main_pygame(file_name):

    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)

    screen_tile_width = screen_width // tilesize
    screen_tile_height = screen_height // tilesize
    tilewidth = world_map.pixel_width // tilesize
    tileheight = world_map.pixel_height // tilesize
    #print("tilewidth:",tilewidth,"tileheight:", tileheight)

    #Bounds for the camera so it does not go off the map (in pixels)  Note the camera coordinate is always the top left so plan accordingly
    cam_world_pos_xmin= 0
    cam_world_pos_ymin= 0
    cam_world_pos_xmax=world_map.pixel_width-screen_width
    cam_world_pos_ymax=world_map.pixel_height-screen_height
    
    # initial camera position
    cam_world_pos_x = 16*tilesize
    cam_world_pos_y = 13*tilesize


    pygame.init()

    #Set the Global Font
    #myfont = pygame.font.SysFont("Futura", 15)
    myfont = pygame.font.Font("petme/PetMe128.ttf", 10)
    #pygame.display.set_caption("tiledtmxloader - " + file_name + " - keys: arrows" )
    pygame.display.set_caption("Ancient Juan")

    screen = pygame.display.set_mode((screen_width, screen_height))
    #screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF, 32)#do we need double Buffering?

    # load the map resources there are several layers, for things the sprite is
    #above, behind and including one for collision
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # load the cursorbox
    cursorbox= pygame.image.load("images/alpha_box.png")
    ActiveShadowTile = pygame.image.load("images/ActiveShadow.png")
    

    # prepare map rendering
    assert world_map.orientation == "orthogonal"
    renderer = tiledtmxloader.helperspygame.RendererPygame()

    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)
    # Checks if there is a special "Object Layer" which we will not use.
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]
    #print(sprite_layers.__class__)

    #Characters contains all the dynamic sprites
    Characters = pygame.sprite.RenderUpdates()

    
    #UI sprite container
    #UImenu = pygame.sprite.RenderUpdates()
    menuItems = ["Attack", "Move" ,"Wait","Special One", "Special Two"]
    myMenu = Menu("Action:", menuItems, myfont, 50, 150, 200, 200)
	
    #CHARACTERS!
    #
    
    #Obligatory Female Supporting Character (with sassyness!)
    PrincessImageSet = sprites.load_sliced_sprites(64,64,'images/princess.png')
    PrincessSprite = Actor((23-.5)*tilesize, (21-1)*tilesize,PrincessImageSet[1], PrincessImageSet[0], PrincessImageSet[2], PrincessImageSet[3], "Peach", 30, 2, 2, 6, 60)
    Characters.add(PrincessSprite)

    #Bebop's Legacy
    PigImageSet = sprites.load_sliced_sprites(64, 64, 'images/pigman_walkcycle.png')
    PigSprite = Actor((24-.5)*tilesize, (21-1)*tilesize, PigImageSet[1], PigImageSet[0], PigImageSet[2], PigImageSet[3], "Bebop", 20, 2, 5, 5, 60)
    Characters.add(PigSprite)
    
    #Solider of Fortune
    SoldierImageSet = sprites.load_sliced_sprites(64, 64, 'images/base_assets/soldier.png')
    SoldierSprite = Actor((25-.5)*tilesize, (21-1)*tilesize, SoldierImageSet[1], SoldierImageSet[0], SoldierImageSet[2], SoldierImageSet[3], "Bald Cloud", 30, 4, 3, 3, 80)
    Characters.add(SoldierSprite)

    #www.whoisthemask.com
    MaskImageSet = sprites.load_sliced_sprites(64, 64, 'images/maskman.png')
    MaskSprite = Actor((26-.5)*tilesize, (21-1)*tilesize, MaskImageSet[1], MaskImageSet[0], MaskImageSet[2], MaskImageSet[3],"Tuxedo Mask" ,20, 2, 5, 5, 75)
    Characters.add(MaskSprite)

    #Skeletastic
    SkeletonImageSet = sprites.load_sliced_sprites(64, 64, 'images/skeleton.png')
    SkeletonSprite = Actor((27-.5)*tilesize, (21-1)*tilesize, SkeletonImageSet[1], SkeletonImageSet[0], SkeletonImageSet[2], SkeletonImageSet[3], "Jack" ,40, 3, 2, 6, 50)
    Characters.add(SkeletonSprite)
    
    sprite_layers[objectlayer].add_sprites(Characters)
    

    # mainloop variables
    frames_per_sec = 60.0# was 60.0
    clock = pygame.time.Clock()
    running = True
    grid = False #variable controling the gridlines
    keypressed = "No Key Pressed"

    ##Turn Variables. These are variables used when it is someone's turn.
    CurrentSprite=[] #this is a basic way to track whose turn it is.
    CanAttack=False
    CanMove=False
    AttackMode=False
    MoveMode=False

    #these are mostly so you do not mess with the game while it is animating.
    EnableKeyboard=True
    EnableMouse=True
    GameTimerOn=True

    ##The Main Game Loop 
    while running:

        #Part 1: These are things that should always happen regardless of what is going on in the game
        clock.tick(frames_per_sec)
        time = pygame.time.get_ticks()

        #updates the mouse position
        mouse_pos_x,mouse_pos_y=pygame.mouse.get_pos()
        tile_x, tile_y = (mouse_pos_x+cam_world_pos_x)//tilesize, (mouse_pos_y+cam_world_pos_y)//tilesize
         
        # Text (Mostly for Debugging)
        label =myfont.render(" 'Working Title: Ancient Juan' ",1,(0,255,255))
        coordinates = myfont.render("Mouse Coordinates:("+str(mouse_pos_x)+","+str(mouse_pos_y)+")",1, (255,255,255))
        tilecoordinates = myfont.render("Tile Coordinates:("+str(tile_x)+","+str(tile_y)+")",1, (255,255,255))
        cameracoords = myfont.render("Camera Coordinates:("+str(cam_world_pos_x)+","+str(cam_world_pos_y)+")",1,(0,0,0))
        controlsdescription = myfont.render("z/x/c = Attack/Move/Wait",1,(0,255,0))


        '''
        for actor in Characters:
            if actor._MidAnimation==1:
                #print("We are in the Middle of Animation")
                EnableKeyboard=False
                EnableMouse=False
                GameTimerOn=False
            elif actor._MidAnimation==0:
                EnableKeyboard=True
                EnableMouse=True
                if CurrentSprite==[]:
                    GameTimerOn=True
        '''

        #Part 2 If an animation is occuring none of this should happen
        # event handling
        
        ##Game Turns
        # We will bring up the next
        if GameTimerOn and (CurrentSprite==[] or CurrentSprite._MidAnimation==0):
            NextTurn(Characters)
        for actor in Characters:
            
            if actor._Initiative>initiative_threshold and GameTimerOn==True:
                
                print("Found Someone!  Its",actor._Name,"'s turn!") 
                #print(actor, actor._Initiative)
                actor._Initiative=0  #resets initiative to 0 after moving.  we could decrement this based on how far you walk later.
                GameTimerOn=False#stop looking for whose turn it is
                CurrentSprite=actor
                cam_world_pos_x, cam_world_pos_y = CameraFocus(cam_world_pos_x, cam_world_pos_y, int(CurrentSprite.tile_x-screen_tile_width/2)*tilesize, \
                    (CurrentSprite.tile_y-screen_tile_height/2)*tilesize, 4, cam_world_pos_xmin, cam_world_pos_ymin, cam_world_pos_xmax, cam_world_pos_ymax, sprite_layers, renderer, screen, clock, frames_per_sec)
                CanMove=True
                CanAttack=True
                #Collider= CollisionFinder(Characters, sprite_layers)
                #moves=Collider.Path                                  
                EnableMouse=True
                
                
                ActiveShadowTileBox=ActiveShadowTile.get_rect()  
                ActiveShadowTileBox.midbottom=(CurrentSprite.tile_x*tilesize+tilesize/2,CurrentSprite.tile_y*tilesize+tilesize)#again we need to translate 
                sprite_layers[shadowlayer].add_sprite(tiledtmxloader.helperspygame.SpriteLayer.Sprite(ActiveShadowTile, ActiveShadowTileBox))

                CurrentSpriteInfo = CharacterInfo(CurrentSprite, myfont, screen_height)
                


                

        ##Events include Mouse and Keyboard actions

        for event in pygame.event.get():
            pressedkeys=pygame.key.get_pressed() #actions that come from the keyboard
            action = myMenu.input(event) #actions that come from the menu
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.QUIT:
                running = False

            pygame.display.update()
            if not hasattr(event, 'key') or event.type!=KEYDOWN: continue
            #if EnableKeyboard: continue
            #print(event.key)#Debugging

            if pressedkeys[K_w] and pressedkeys[K_LMETA]:
                pygame.quit()
                sys.exit()
            #Camera Movement using "wasd"'
            if EnableKeyboard:
                if event.key == K_d: cam_world_pos_x +=tilesize #right
                elif event.key == K_a: cam_world_pos_x -=tilesize#left
                elif event.key == K_w: cam_world_pos_y -=tilesize#up
                elif event.key == K_s: cam_world_pos_y +=tilesize#down

                elif (pressedkeys[K_z] or action=="Attack") and CanAttack and AttackMode==False and MoveMode==False:#attack
                    print("Entering Attack Mode")
                    AttackMode=True #now we will wait for mouse imput on who to attack # we also need a way to cancel the attack

                elif (pressedkeys[K_x] or action=="Move") and CanMove and MoveMode==False and AttackMode==False:#move
                    print("Entering Move Mode")
                    MoveMode=True
                    Collider= CollisionFinder(Characters, sprite_layers)
                    moves=Collider.PathList(CurrentSprite.tile_x,actor.tile_y,CurrentSprite._Movement)
                    DrawPossibleMoves(moves,shadowlayer,sprite_layers)
                    
                elif pressedkeys[K_c] or action=="Wait":#skipturn/wait
                    ClearLayer(shadowlayer,sprite_layers) 
                    CurrentSprite._Initiative=0# or something smaller
                    GameTimerOn=True
                    CanAttack=True
                    CanMove=False
                    AttackMode=False
                    MoveMode=False
                    CurrentSprite=[]

                elif pressedkeys==K_v: #cancel action
                    pass

                    
                #Debugging Spawn a PigMan
                #Bebop's Brood
                elif event.key == K_1: 
                    NewPigSprite = Actor((20-.5)*tilesize, (20-1)*tilesize, PigImageSet[1], PigImageSet[0], PigImageSet[2], PigImageSet[3],"Pig Spawn" ,2, 2, 5, 5, 60)
                    Characters.add(NewPigSprite)                  
                    sprite_layers[objectlayer].add_sprites(Characters)
                elif event.key == K_2:
                    Characters.remove(NewPigSprite)
                    sprite_layers[objectlayer].remove_sprite(NewPigSprite)

            #Debugging. If you need to take manual control of a sprite here is how you do it
     

            if event.key == K_RIGHT:
                pygame.mouse.set_pos([mouse_pos_x+tilesize, mouse_pos_y])
            elif event.key == K_LEFT:
                pygame.mouse.set_pos([mouse_pos_x-tilesize, mouse_pos_y])
            elif event.key == K_UP:
                pygame.mouse.set_pos([mouse_pos_x, mouse_pos_y-tilesize])
            elif event.key == K_DOWN:
                pygame.mouse.set_pos([mouse_pos_x, mouse_pos_y+tilesize])

            
            #Take this out later this is strictly for debugging purposes            
            if event.key ==K_g: grid= not grid #this toggles the grid


            #if pressedkeys[K_RETURN]:
            #    print("Enter Hit")      

        ##Mostly Actor stuff
        
        if (pygame.mouse.get_pressed()[0] and EnableMouse) or (pressedkeys[K_RETURN]):
            #print("Mouse button 1 is pressed at:",tile_x, tile_y)

            if CurrentSprite !=[] and CurrentSprite.tile_x==tile_x and CurrentSprite.tile_y==tile_y: #clicked on CurrentSprite
                pass
                #do something else like maybe a menu screen
            elif AttackMode:
                print("Attacking Someone!")
                for actor in Characters:
                    if actor.tile_x==tile_x and actor.tile_y==tile_y and actor != CurrentSprite:
                        print(CurrentSprite._Name, "is attacking", actor._Name)
                        CurrentSprite.Attack(actor)
                        Characters.update(time)#updates experience
                        AttackMode=False
                        CanAttack=False
            elif MoveMode:
                #look to see if you are away from the path
                path = PopBestPath(tile_x, tile_y, moves)
                if path== []:#no path found then erase path and start over
                    pass
                else: #The player has clicked on a shaded tile, Now we move the Actor

                    ClearLayer(shadowlayer,sprite_layers)
                    EnableMouse=False#this is a bit redundant and possibly dangerous
                    #print("startmove")
                    MultiMove(path, Characters, CurrentSprite, sprite_layers, renderer, screen, clock, frames_per_sec)
                    #print("endmove")

                    ActiveShadowTileBox=ActiveShadowTile.get_rect()  
                    ActiveShadowTileBox.midbottom=(tile_x*tilesize+tilesize/2,tile_y*tilesize+tilesize)#again we need to translate 
                    sprite_layers[shadowlayer].add_sprite(tiledtmxloader.helperspygame.SpriteLayer.Sprite(ActiveShadowTile, ActiveShadowTileBox))
                    
                    MoveMode=False
                    CanMove=False
                    EnableMouse=True
            else: #not clicking on a move or place or anything
                 pass
     



        #Part 4: RENDERING PHASE (Make sure you are adding the right element to the right layer)
        # adjust camera to position according to the keypresses "wasd"

        #checks if the camera has gone off the board and moves it back
        if cam_world_pos_x<cam_world_pos_xmin: cam_world_pos_x=cam_world_pos_xmin
        if cam_world_pos_y<cam_world_pos_ymin: cam_world_pos_y=cam_world_pos_ymin
        if cam_world_pos_x>cam_world_pos_xmax: cam_world_pos_x=cam_world_pos_xmax
        if cam_world_pos_y>cam_world_pos_ymax: cam_world_pos_y=cam_world_pos_ymax

        #Focus on active character
        #if CurrentSprite !=[]:
        #    CameraFocus(mouse_pos_x, mouse_pos_y, (CurrentSprite.tile_x)*tilesize, (CurrentSprite.tile_y)*tilesize, 10, sprite_layers, renderer, screen, clock, frames_per_sec)
        #else:
        renderer.set_camera_position(cam_world_pos_x, cam_world_pos_y, "topleft")



        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0, 0, 0))

        # render the map
        for sprite_layer in sprite_layers:
            if sprite_layer.is_object_group:
                # we dont draw the object group layers
                # you should filter them out if not needed
                continue
            else:
                Characters.update(time)
                renderer.render_layer(screen, sprite_layer)


        #DEBUGGING: Grid
        if grid:#on a press of "g" the grid will be toggled
            for i in range(tilewidth):#draw vertical lines
                pygame.draw.line(screen, (0,0,0), (i*tilesize,0),(i*tilesize,world_map.pixel_width))
            for j in range(tileheight):#draw horizontal lines
                pygame.draw.line(screen, (20,0,20), (0,j*tilesize),(world_map.pixel_height,j*tilesize))
    

        #DEBUGGING: Text
        screen.blit(label, (32,0))
        screen.blit(coordinates, (32,32))
        screen.blit(tilecoordinates, (32,64))
        screen.blit(cameracoords,(32,96))
        
        if CurrentSprite !=[]:
            screen.blit(CurrentSpriteInfo.surface, CurrentSpriteInfo.rect)

        #cursorbox
        screen.blit(cursorbox, (tilesize*(tile_x)-cam_world_pos_x,tilesize*(tile_y)-cam_world_pos_y))


        #Draw stuff
        #print("camera at:",cam_world_pos_x,cam_world_pos_x)
        screen.blit(myMenu.surface, myMenu.rect)
        

        pygame.display.flip()


#both of these will need to be reworked
#  -----------------------------------------------------------------------------

def create_hero(start_pos_x, start_pos_y):
    """
    Creates the hero sprite.
    """
    image = pygame.Surface((25, 45), pygame.SRCALPHA)
    image.fill((255, 0, 0, 200))
    rect = image.get_rect()
    rect.midbottom = (start_pos_x, start_pos_y)
    return tiledtmxloader.helperspygame.SpriteLayer.Sprite(image, rect)

#  ------------------
#note used (yet)
def CameraFocus(start_x, start_y, end_x, end_y, speed, cam_world_pos_xmin, cam_world_pos_ymin, cam_world_pos_xmax, cam_world_pos_ymax, sprite_layers, renderer, screen, clock, frames_per_sec): #moves the camera slowly from one place to another, frames is how many steps
    #print("CameraFocus called to move a camera from",start_x, start_y, "to", end_x, end_y)

    if end_x<cam_world_pos_xmin: end_x=cam_world_pos_xmin
    if end_y<cam_world_pos_ymin: end_y=cam_world_pos_ymin
    if end_x>cam_world_pos_xmax: end_x=cam_world_pos_xmax
    if end_y>cam_world_pos_ymax: end_y=cam_world_pos_ymax

    
    dx=0
    dy=0
    #records for posterity the original camera positions
    #dx, dy = int((end_x-start_x)/steps), int((end_y-start_y)/steps)
    #print(dx, dy)
    
    if end_x>start_x:
        dx=speed
    else:
        dx=-speed
    
    if end_y>start_y:
        dy=speed
    else:
        dy=-speed
    
    #dist= sqrt((dx)**2+(dy)**2)
    
    cam_world_pos_x, cam_world_pos_y = start_x, start_y
    while abs(cam_world_pos_x-end_x) > 0 or abs(cam_world_pos_y-end_y) > 0:
        
    #for i in range(steps-2):
        if abs(cam_world_pos_x-end_x) >= abs(dx):
            cam_world_pos_x += dx
        if abs(cam_world_pos_y-end_y) >= abs(dy):
            cam_world_pos_y += dy
        #print("camera at:",cam_world_pos_x,cam_world_pos_x)
        
        clock.tick(frames_per_sec)
        time = pygame.time.get_ticks()
        for sprite_layer in sprite_layers:
            renderer.render_layer(screen, sprite_layer)
        renderer.set_camera_position(cam_world_pos_x, \
                                     cam_world_pos_y, "topleft")
        pygame.display.flip()
        
    #one last camera assignment just to make sure
    
    cam_world_pos_x = end_x
    cam_world_pos_y = end_y
    print("camera at:",cam_world_pos_x,cam_world_pos_x)
    clock.tick(frames_per_sec)
    time = pygame.time.get_ticks()
    for sprite_layer in sprite_layers:
        renderer.render_layer(screen, sprite_layer)
    renderer.set_camera_position(cam_world_pos_x, \
                                 cam_world_pos_y, "topleft")
    
    #needs to remind the world this is where we are
    return end_x, end_y


#  -----------------------------------------------------------------------------
def DrawPossibleMoves(moves, layer,sprite_layers):
    for i in range(len(moves)):
        BoxImage=pygame.image.load("images/alpha_box.png")
        BoxRect=BoxImage.get_rect()  
        BoxRect.midbottom=(moves[i][0]*tilesize+tilesize/2,moves[i][1]*tilesize+tilesize)#again we need to translate 
        sprite_layers[layer].add_sprite(tiledtmxloader.helperspygame.SpriteLayer.Sprite(BoxImage, BoxRect))
    
#  -----------------------------------------------------------------------------

def ClearLayer(old_layer, sprite_layers):#Clears out an entire layer of the map.  This is primarily used for special effects that only last momentarily.
    sprite_layers[old_layer].sprites=[]

    
#  -----------------------------------------------------------------------------

def NextTurn(Characters):
    #increments the initiative of each character by speed.  If you have above 100 speed, your turn is up.
    for actor in Characters:
        actor._Initiative+=actor._Speed




def MultiMove(path, Characters, CurrentSprite, sprite_layers, renderer, screen, clock, frames_per_sec):

    path.reverse()#since pop() pulls the last element
    nextmove=path.pop()
                    
    #print("popped", nextmove)
    CurrentSprite.Move(nextmove)
    
    while path != []:   
        while CurrentSprite._MidAnimation==1:
            clock.tick(frames_per_sec)
            time = pygame.time.get_ticks()
            Characters.update(time)                            
            for sprite_layer in sprite_layers:
                renderer.render_layer(screen, sprite_layer)
            pygame.display.flip()
            
        nextmove=path.pop()     
        CurrentSprite.Move(nextmove)
        
    #this last loop is to make sure the character is done moving before the next turn begins
    while CurrentSprite._MidAnimation==1:
        clock.tick(frames_per_sec)
        time = pygame.time.get_ticks()
        Characters.update(time)
        for sprite_layer in sprite_layers:
            renderer.render_layer(screen, sprite_layer)
        pygame.display.flip()

    #this sets the characters animation to looking down
    CurrentSprite._images = CurrentSprite._MoveDownImages
     
#  -----------------------------------------------------------------------------
    
#  -----------------------------------------------------------------------------

if __name__ == '__main__':

    main()



    



