import pygame
import tiledtmxloader

class CollisionFinder(object):
    def __init__(self, layers):
        #pygame.sprite.RenderUpdates()=Characters
        #tiledtmxloader.helperspygame.SpriteLayer.__init__()=coll_layer

        self.baselayer=0
        self.fringelayer=1
        self.objectlayer=2
        self.overhanglayer=3
        self.collisionlayer=4
        self.layers=layers
        self._coll_layer=layers[self.collisionlayer]
        self._obj_layer=layers[self.objectlayer]
        
        #print(self._coll_layer.content2D[0][0].__class__)
    def PossibleMoves(self, tile_x, tile_y, movement_value):
    #returns a list of possible move positions
        tile_rects = [(tile_x,tile_y)]
        if movement_value==0:
           return tile_rects
        else:
            for (dirx,diry) in [(1,0), (-1,0), (0,1), (0,-1)]:
                look_tile=self._coll_layer.content2D[tile_y+diry][tile_x + dirx]
                #print("movement", movement_value)
                #print("checking",tile_x+dirx,tile_y + diry)
                #print("is it already in:", (tile_x + dirx, tile_y+diry) in tile_rects)
                #print( "is the space free:", look_tile is None)
                #print("List so far",tile_rects)
                #if (tile_x + dirx, tile_y+diry) not in tile_rects and look_tile is None:
                if look_tile is None:
                    #print("ADDING:",tile_x+dirx,tile_y + diry)
                    tile_rects.append((tile_x + dirx, tile_y+diry))
                    #tile_rects=tile_rects+self.PossibleMoves(tile_x + dirx, tile_y+diry, movement_value-1)
                    tile_rects=list(set(tile_rects+self.PossibleMoves(tile_x + dirx, tile_y+diry, movement_value-1)))
            return tile_rects

#this will be an improved(more efficient) possibleMoves that will also determine the best path.
    def PossibleMovesPath(self, tile_x, tile_y, movement_value):
    #returns a list of possible move positions, their cost and the best path there.  Note the cost may be redundant
        tile_rects = [(tile_x,tile_y)]#initial position costs nothing and you do not need to move to get there
        #print(self._coll_layer.content2D[0][0].__class__)
        if movement_value==0:
           return tile_rects
        else:
            for (dirx,diry) in [(1,0), (-1,0), (0,1), (0,-1)]:
                look_tile=self._coll_layer.content2D[tile_y+diry][tile_x + dirx]
                #print("movement", movement_value)
                #print("checking",tile_x+dirx,tile_y + diry)
                #print("is it already in:", (tile_x + dirx, tile_y+diry) in tile_rects)
                #print( "is the space free:", look_tile is None)
                #print("List so far",tile_rects)
                #if (tile_x + dirx, tile_y+diry) not in tile_rects and look_tile is None:
                if look_tile is None:
                    #print("ADDING:",tile_x+dirx,tile_y + diry)
                    tile_rects.append((tile_x + dirx, tile_y+diry))
                    #tile_rects=tile_rects+self.PossibleMoves(tile_x + dirx, tile_y+diry, movement_value-1)
                    tile_rects=list(set(tile_rects+self.PossibleMoves(tile_x + dirx, tile_y+diry, movement_value-1)))
            return tile_rects


    #makes a path
    #def pathlist

