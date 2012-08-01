# <This controls most of the art and the gameboard drawing.>
# Copyright (C) <2012>  <Phong Le and Benjamin Liyanage>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

import pygame



import sprites
from sprites import AnimatedSprite, Actor

import tiledtmxloader #this reads .tmx files


class Board(object):
#class Board(tiledtmxloader.helperspygame):
    def __init__(self, worldMap, characters, tileSize, screen):

        
        #Layers, lower renders first
        self._baseLayer=0 # the ground
        self._fringeLayer=1 #grass etc
        self._shadowLayer=2 # mostly to render below Actors but above the ground
        self._objectLayer=3 #where the Actors (Characters) go
        self._overhangLayer=4 # things that render over the characters
        self._collisionLayer=5 #in the release version this will be invisible, (Red Blocks)
        self._particleLayer=6
        self._characters = characters
        self._particles = pygame.sprite.RenderUpdates()#this is for particle effects for attacks that render above the board
        self._screen =screen
        self._tileSize = tileSize

        #Variables
        self._worldMap = worldMap

        self._screenWidth = min(1024, self._worldMap.pixel_width)
        self._screenHeight = min(768, self._worldMap.pixel_height)
        self._width = self._worldMap.pixel_width
        self._height = self._worldMap.pixel_height
        self._tileHeight = self._height // tileSize
        self._tileWidth = self._width // tileSize
        self._camPos_x = 0;#16*tilesize
        self._camPos_y = 0;#3*tilesize
        self._camTile_x = self._camPos_x // self._tileSize
        self._camTile_y = self._camPos_y // self._tileSize
        self._screenTileOffset_x=-int((self._screenWidth/2) // tileSize)
        self._screenTileOffset_y=-int((self._screenHeight/2) // tileSize)
        self._cursorTileOffset_x=0 #the cursorTileOffset is for AOE templates centering
        self._cursorTileOffset_y=0

        self._camDest_x = 0
        self._camDest_y = 0
        self._camMin_x = 0
        self._camMin_y = 0
        self._camMax_x = self._width - self._screenWidth
        self._camMax_y = self._height - self._screenHeight 
        self._midAnimation = 0
        

        
        self._resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
        self._resources.load(self._worldMap)
        
        self._renderer = tiledtmxloader.helperspygame.RendererPygame()

        

        self._renderer.set_camera_position_and_size(self._camPos_x, self._camPos_y, \
                                        self._screenWidth, self._screenHeight, "topleft")
        
        self.sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(self._resources)
        self.sprite_layers = [layer for layer in self.sprite_layers if not layer.is_object_group]

        self.sprite_layers[self._objectLayer].add_sprites(self._characters)

        #different hover cursors indicate different things to see.Maybe add an ally enemy etc later.
        self._cursorBox= pygame.image.load("images/alpha_box.png")
        self._activeBox = pygame.image.load("images/ActiveShadow.png")
        #self._activeBox = pygame.image.load("images/ActiveShadow.png")
        
        
        #self.sprite_layers[self._objectLayer].add_sprite(self._Cursor)

        
        

        #Renders the layers to the screen
        for sprite_layer in self.sprite_layers:
            self._renderer.render_layer(self._screen, sprite_layer)


        #print(self.sprite_layers[self._collisionLayer].content2D)

    def update(self, t):#might need (self,t) later
                # render the map

        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos() #mouse coordinates
        tile_x, tile_y = mouse_pos_x// self._tileSize, mouse_pos_y // self._tileSize

        #removes dead characters: We will probably have to check for animation later.
        for actor in self._characters:
            #if actor.Health()<=0 and actor._MidAnimation==0:
                #Right now we are just removing the character, we may do something different later.
            if actor.PostAnimationAction()=="remove":# and actor.Animating()==False and actor._frame >= len(actor._images):
                print(" GameBoard Removing", actor.Name(),"from the board.")
                self._characters.remove(actor)
        for particle in self._particles:
            if particle.PostAnimationAction()=="remove":
                self._particles.remove(particle)
                self.ClearLayer(self._particleLayer)#both this an removing the individual particle might be overkill
        
        self.ClearLayer(self._objectLayer)
        #self.sprite_layers[self._particleLayer].add_sprite(self._particles)
        self.sprite_layers[self._objectLayer].add_sprites(self._characters)
        
        self._characters.update(pygame.time.get_ticks())
        self._particles.update(pygame.time.get_ticks())
        for sprite_layer in self.sprite_layers:
            if sprite_layer.is_object_group:
                # we dont draw the object group layers
                # you should filter them out if not needed
                continue
            else:
                self._renderer.render_layer(self._screen, sprite_layer)

        #draws a cursor
        
        self._screen.blit(self._cursorBox,((tile_x+self._cursorTileOffset_x)*self._tileSize, (tile_y+self._cursorTileOffset_y)*self._tileSize))

        
 

        #maybe update the camera if necessary
        self.CameraUpdate()
        
        self._camTile_x = self._camPos_x // self._tileSize
        self._camTile_y = self._camPos_y // self._tileSize
        
        self._renderer.set_camera_position(self._camPos_x, self._camPos_y, "topleft")
    def camTile(self):
        return self._camTile_x, self._camTile_y

    def Characters(self):
        return self._characters

    def HighlightTile(self, tile_x, tile_y, imagepath):
        BoxImage=pygame.image.load(imagepath)
        BoxRect=BoxImage.get_rect()  
        BoxRect.midbottom=(tile_x*self._tileSize+self._tileSize/2,tile_y*self._tileSize+self._tileSize)#again we need to translate 
        self.sprite_layers[self._shadowLayer].add_sprite(tiledtmxloader.helperspygame.SpriteLayer.Sprite(BoxImage, BoxRect))


    

    def HighlightArea(self, tile_x,tile_y, minRange, maxRange,imagepath): #highlights an entire area with a max and min radius
        '''
        for i in range(-maxRange,maxRange):
            for j in range(maxRange-abs(i)):
                
                self.HighlightTile(tile_x+i, tile_y+j, imagepath)
                if j != 0:
                    self.HighlightTile(tile_x+i, tile_y-j, imagepath)
        '''
        #print("highlight area called")
        for i in range(-maxRange,maxRange):
            upper = maxRange-abs(i)
            lower = max(0, minRange-abs(i))
            for j in range(lower, upper):             
                self.HighlightTile(tile_x+i, tile_y+j, imagepath)
                if j != 0:
                    self.HighlightTile(tile_x+i, tile_y-j, imagepath)

    def ChangeCursor(self,cursorpath,tileOffset_x, tileOffset_y):
        self._cursorTileOffset_x, self._cursorTileOffset_y = tileOffset_x, tileOffset_y
        self._cursorBox= pygame.image.load(cursorpath)


    def MoveCamera(self, x, y, relative=False): #like panning but moves directly
        #Note if relative = True it will
        if relative:
            self._camPos_x = self._camPos_x +x
            self._camPos_y = self._camPos_y +y
        else:
            self._camPos_x =x
            self._camPos_y =y

        if self._camPos_x < self._camMin_x: self._camPos_x = self._camMin_x
        if self._camPos_x > self._camMax_x: self._camPos_x = self._camMax_x
        if self._camPos_y < self._camMin_y: self._camPos_y = self._camMin_y
        if self._camPos_y > self._camMax_y: self._camPos_y = self._camMax_y
        self._camDest_x = self._camPos_x
        self._camDest_y= self._camPos_y

    def PanCamera(self, x,y, relative= False):#sets a destination for the camera to pan toward.
        if relative:
            self._camDest_x, self._camDest_y = self._camPos_x+x, self._camPos_y+y
        else:
            self._camDest_x, self._camDest_y = x,y
            
        if self._camDest_x < self._camMin_x: self._camDest_x = self._camMin_x
        if self._camDest_x > self._camMax_x: self._camDest_x = self._camMax_x
        if self._camDest_y < self._camMin_y: self._camDest_y = self._camMin_y
        if self._camDest_y > self._camMax_y: self._camDest_y = self._camMax_y
    def CameraUpdate(self, speed=8, relative=False):# this is a helper function that is called whenever the camera needs to pan toward a location.
        dx, dy=0,0
        if self._camDest_x>self._camPos_x:
            dx=speed
        else:
            dx=-speed
        
        if self._camDest_y>self._camPos_y:
            dy=speed
        else:
            dy=-speed

        if abs(self._camPos_x  - self._camDest_x) > abs(dx):
            self._camPos_x +=dx
        else:
            self._camPos_x = self._camDest_x

        if abs(self._camPos_y  - self._camDest_y) > abs(dy):
            self._camPos_y +=dy
        else:
            self._camPos_y = self._camDest_y

        if self._camPos_x < self._camMin_x: self._camPos_x = self._camMin_x
        if self._camPos_x > self._camMax_x: self._camPos_x = self._camMax_x
        if self._camPos_y < self._camMin_y: self._camPos_y = self._camMin_y
        if self._camPos_y > self._camMax_y: self._camPos_y = self._camMax_y
    def Animating(self):
        if self._camPos_x != self._camDest_x or self._camPos_y != self._camDest_y:
            return True
        else: return False
        
    def ClearLayer(self, layer): #to clear the shadow layer after a players turn is over.
        self.sprite_layers[layer].sprites=[]
    def getLayers(self):
        return self.sprite_layers
    def Characters(self):
        return self._characters

    def DrawPossibleMoves(self, moves):
        #print(moves)
        for i in range(len(moves)):
            #print("Gameboard is drawing on",moves[i]) 
            BoxImage=pygame.image.load("images/alpha_box.png")
            BoxRect=BoxImage.get_rect()  
            #BoxRect.midbottom=(moves[i]['x']*self._tileSize+self._tileSize/2,moves[i]['y']*self._tileSize+self._tileSize)#again we need to translate
            BoxRect.midbottom=(moves[i][0]*self._tileSize+self._tileSize/2,moves[i][1]*self._tileSize+self._tileSize)#again we need to translate 
            self.sprite_layers[self._shadowLayer].add_sprite(tiledtmxloader.helperspygame.SpriteLayer.Sprite(BoxImage, BoxRect))

    def getTile(self, mouse_pos_x,mouse_pos_y, tiled=False):# returns a tuple
        if tiled:
            tile_x, tile_y = mouse_pos_x, mouse_pos_y
        else:
            tile_x, tile_y = (mouse_pos_x + self._camPos_x)// self._tileSize, (mouse_pos_y+ self._camPos_y) // self._tileSize
        for actor in self._characters:
            if (actor.tile_x, actor.tile_y) == (tile_x, tile_y):
                return ("Actor", actor, (tile_x, tile_y))
        if self.sprite_layers[self._collisionLayer].content2D[tile_y][tile_x] is  not None: #remember it reverses coordinates
            return ("Collision",0, (tile_x, tile_y))
        else:
            return ("Clear",0, (tile_x, tile_y))

    
    def AnimatedParticleEffect(self, w, h, path, boardTile_x, boardTile_y):
        ParticleImages = sprites.load_sliced_sprites(w, h, path)
        Particle = AnimatedSprite(ParticleImages[0],boardTile_x*self._tileSize-w/2, boardTile_y*self._tileSize-h/2)
        Particle._postAnimationAction="dispose"#only plays once then kills!
        self.sprite_layers[self._particleLayer].add_sprite(Particle)
    
        self._particles.add(Particle)
        
    def ObjectLayer(self):
        return self._objectLayer

    def CollisionLayer(self):
        return self._collisionLayer
    '''
      
    def drawActiveShadow() #draws the active shadow tile on the shadow layer under the active character.

    def moveCharacter()

    def collisions():#exports a 2d array of collision information.  It might be useful.

    def pauseBoard(): #everything will stop ticking, including walk animations and such.

    '''

        
    

        
