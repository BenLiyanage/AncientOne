import sys
import os
import array
import numpy
import pygame
import collision
from collision import CollisionFinder

from pygame.locals import*

import sprites
from sprites import AnimatedSprite, Actor

import tiledtmxloader #this reads .tmx files

#Variables (WARNING: Does not necessarily follow standard python etiquette
tilesize=32
#Layers, lower renders first
baselayer=0
fringelayer=1
objectlayer=2
overhanglayer=3
collisionlayer=4

MAP="images/map01.tmx"
#MAP = "images/smallmap.tmx" #small map for testing

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
    tilewidth = world_map.pixel_width/tilesize
    tileheight = world_map.pixel_height/tilesize
    #print("tilewidth:",tilewidth,"tileheight:", tileheight)

    # 2d array of the map where collisions
    
    #collisionarray = [[False for i in range(tileheight)] for j in range(tileheight)]

    pygame.init()

    #Fonts/size
    myfont = pygame.font.SysFont("Futura", 15)
    

    pygame.display.set_caption("tiledtmxloader - " + file_name + " - keys: arrows" )
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))
    #screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF, 32)

    #Bounds for the camera so it does not go off the map (in pixels)
    cam_world_pos_xmin=0
    cam_world_pos_ymin=0
    cam_world_pos_xmax=world_map.pixel_width-screen_width
    cam_world_pos_ymax=world_map.pixel_height-screen_height
    # initial camera position
    cam_world_pos_x = 0
    cam_world_pos_y = 0
    
    # load the map resources there are several layers, for things the sprite is
    #above, behind and including one for collision
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)

    # load the cursorbox
    cursorbox= pygame.image.load("images/alpha_box.png")

    # prepare map rendering
    assert world_map.orientation == "orthogonal"

    # renderer
    renderer = tiledtmxloader.helperspygame.RendererPygame()


    # set initial cam position and size
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height, "topleft")

    # retrieve the layers
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    # Checks if there is a special "Object Layer" which we will not use.
    sprite_layers = [layer for layer in sprite_layers if not layer.is_object_group]

    # create hero sprite (temporary until AnimatedSprite is up
    hero_pos_tile_x=14
    hero_pos_tile_y=10
    hero_pos_x = hero_pos_tile_x*tilesize+tilesize/2
    hero_pos_y = hero_pos_tile_y*tilesize+tilesize
    hero = create_hero(hero_pos_x, hero_pos_y)#creates a "hero" at the associated position.
    #adds hero to the right layer
    sprite_layers[objectlayer].add_sprite(hero) #possibly wrong layer


    #Loads images and creates Actors
    Characters = pygame.sprite.RenderUpdates()
    #Obligatory Female Supporting Character (with sassyness!)
    PrincessImageSet = sprites.load_sliced_sprites(64,64,'images/princess.png')
    PrincessSprite = Actor(320+16,320,PrincessImageSet[1], PrincessImageSet[0], PrincessImageSet[2], PrincessImageSet[3], 0, 0, 0, 0, 0)
    Characters.add(PrincessSprite)

    #Bebop's Legacy
    PigImageSet = sprites.load_sliced_sprites(64, 64, 'images/pigman_walkcycle.png')
    PigSprite = Actor(352+16,320,PigImageSet[1], PigImageSet[0], PigImageSet[2], PigImageSet[3], 0, 0, 0, 0, 0)
    Characters.add(PigSprite)
    
    sprite_layers[objectlayer].add_sprites(Characters)


    Collider= CollisionFinder(sprite_layers)
    print(Collider.PossibleMoves(3,3,2))

    # variables for the main loop
    frames_per_sec = 60.0# was 60.0
    clock = pygame.time.Clock()
    running = True
    grid = False #variable controling the gridlines
    keypressed = "No Key Pressed"

    # mainloop
    while running:
        clock.tick(frames_per_sec)
        time = pygame.time.get_ticks()
        disable_inputs=False#Disable mouse+keyboard except for hitting escape
        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
            #elif event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_ESCAPE:#shuts down when you hit escape
            #        running = False
            disable_inputs=False

            if not hasattr(event, 'key') or event.type!=KEYDOWN: continue
            if disable_inputs: continue
            #print(event.key)#Debugging

            #Camera Movement
            if event.key == K_d: cam_world_pos_x +=tilesize #right
            elif event.key == K_a: cam_world_pos_x -=tilesize#left
            elif event.key == K_w: cam_world_pos_y -=tilesize#up
            elif event.key == K_s: cam_world_pos_y +=tilesize#down
          
            #Hero Movement
            #elif event.key == K_RIGHT: hero_pos_tile_x +=1
            if event.key == K_RIGHT:
                hero_pos_tile_x, hero_pos_tile_y = check_collision(sprite_layers[collisionlayer], hero_pos_tile_x, hero_pos_tile_y,hero_pos_tile_x+1,hero_pos_tile_y)
                PrincessSprite.Move("Right")
            #elif event.key == K_LEFT: hero_pos_tile_x -=1
            elif event.key == K_LEFT: 
                hero_pos_tile_x, hero_pos_tile_y = check_collision(sprite_layers[collisionlayer], hero_pos_tile_x, hero_pos_tile_y,hero_pos_tile_x-1,hero_pos_tile_y)
                PrincessSprite.Move("Left")
            #elif event.key == K_UP: hero_pos_tile_y -=1
            elif event.key == K_UP:
                hero_pos_tile_x, hero_pos_tile_y = check_collision(sprite_layers[collisionlayer], hero_pos_tile_x, hero_pos_tile_y,hero_pos_tile_x,hero_pos_tile_y-1)
                PrincessSprite.Move("Up")
            #elif event.key == K_DOWN: hero_pos_tile_y +=1
            elif event.key == K_DOWN:
                hero_pos_tile_x, hero_pos_tile_y = check_collision(sprite_layers[collisionlayer], hero_pos_tile_x, hero_pos_tile_y,hero_pos_tile_x,hero_pos_tile_y+1)
                PrincessSprite.Move("Down")
            
            #Take this out later this is strictly for debugging purposes
            
            elif event.key ==K_g: grid= not grid #this toggles the grid
            #updates hero location
            hero_pos_x = hero_pos_tile_x*tilesize+tilesize/2
            hero_pos_y = hero_pos_tile_y*tilesize+tilesize
            hero.rect.midbottom = (hero_pos_x, hero_pos_y)

            ##END KEYLOGGING
            
        #Reading Mouse movements to help with screen scrolling
        #We may need to slow this down.  It is based on the game clock speed
        mouse_pos_x,mouse_pos_y=pygame.mouse.get_pos()
        '''
        if mouse_pos_x<tilesize: cam_world_pos_x -=tilesize
        if mouse_pos_y<tilesize: cam_world_pos_y -=tilesize
        if mouse_pos_x>screen_width-tilesize: cam_world_pos_x +=tilesize
        if mouse_pos_y>screen_height-tilesize: cam_world_pos_y +=tilesize
        '''        
            
        #checks if the camera has gone off the board and moves it back
        if cam_world_pos_x<cam_world_pos_xmin: cam_world_pos_x=cam_world_pos_xmin
        if cam_world_pos_y<cam_world_pos_ymin: cam_world_pos_y=cam_world_pos_ymin
        if cam_world_pos_x>cam_world_pos_xmax: cam_world_pos_x=cam_world_pos_xmax
        if cam_world_pos_y>cam_world_pos_ymax: cam_world_pos_y=cam_world_pos_ymax
            
            
            
         
    # Reading the Mouse
        #mouse_pos_x,mouse_pos_y=pygame.mouse.get_pos()
        x_tile=tilesize*(mouse_pos_x//tilesize)
        y_tile=tilesize*(mouse_pos_y//tilesize)
        
        
    # Text (Mostly for Debugging)
        label =myfont.render(" 'Working Title: Ancient Juan' ",1,(0,255,255))
        coordinates = myfont.render("Mouse Coordinates:("+str(mouse_pos_x)+","+str(mouse_pos_y)+")",1, (255,255,255))
        tilecoordinates = myfont.render("Tile Coordinates:("+str(int(mouse_pos_x/tilesize))+","+str(int(mouse_pos_y/tilesize))+")",1, (255,255,255))
        gameclock = myfont.render("Game clock:"+str(time),1,(0,255,0))


        #RENDERING PHASE (Make sure you are adding the right element to the right layer)
        # adjust camera to position according to the keypresses "wasd"
        renderer.set_camera_position(cam_world_pos_x, \
                                     cam_world_pos_y, "topleft")

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


        #Grid
        if grid:#on a press of "g" the grid will be toggled
            for i in range(tilewidth):#draw vertical lines
                pygame.draw.line(screen, (0,0,0), (i*tilesize,0),(i*tilesize,world_map.pixel_width))
            for j in range(tileheight):#draw horizontal lines
                pygame.draw.line(screen, (20,0,20), (0,j*tilesize),(world_map.pixel_height,j*tilesize))
    

        #Text
        screen.blit(label, (32,0))
        screen.blit(coordinates, (32,32))
        screen.blit(tilecoordinates, (32,64))
        screen.blit(gameclock,(32,96))

        #cursorbox
        screen.blit(cursorbox, (x_tile,y_tile))


        

        #Draw stuff
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
    

#this is a much more simple collision checker since were are in a fairly discrete world
#this will check if your destination is correct, not just direction
#we may want to change this if we want an animation of walking into a wall(in place)
#WARNING THE X AND Y COORDINATES ARE SWITCHED ON "content2D" it sux not to know that ahead of time
def check_collision(coll_layer, start_tile_x, start_tile_y, end_tile_x,end_tile_y):
    if coll_layer.content2D[end_tile_y][end_tile_x] is not None:
        #print("Collision at:", start_tile_x, start_tile_y, "with",end_tile_x,end_tile_y)
        return start_tile_x, start_tile_y
    
    else: return end_tile_x, end_tile_y
       

#  ------------------
def neighbor(coll_layer, tile_x, tile_y): #makes a list of neighbors to a tile by checking the collision layer
    tile_rects = []#neighbors
    for diry in (-1, 0 , 1):#remove "0" if you want to remove the origin
        for dirx in (-1, 0, 1):
            if coll_layer.content2D[tile_y + diry][tile_x + dirx] is not None:
                tile_rects.append(tile_x + dirx, tile_y + diry)
    return tile_rects


#  -----------------------------------------------------------------------------
#def path(coll_layer, start_tile_x, start_tile_y, end_tile_x,end_tile_y):# find a path between the start and the end.
# if this is lagging we can implement A*, note that since our heuristic is not monotone this is not necessarily the best.
 #   closedset=[]
    #hypot(x_0-x_1,y_0-y_1)
  #  openset=[(start_tile_x, start_tile_y)]
 #   path[start_tile_x, start_tile_y)]#the path so far
 #   def g_score(x)=0 #cost from start
 #   f_score

#  -----------------------------------------------------------------------------

if __name__ == '__main__':

    main()





