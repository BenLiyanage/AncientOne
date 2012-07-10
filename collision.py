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
    #returns a list of possible moves.
        
        tile_rects = [[tile_x,tile_y]]
        #print(self._coll_layer.content2D[0][0].__class__)
        if movement_value==0:
           return tile_rects
        else:
            for diry in (-1 , 0,1):
                for dirx in (-1,0, 1):
                    #print("checking",tile_x+dirx,tile_y + diry)
                    if self._coll_layer.content2D[tile_y + diry][tile_x + dirx] is None and movement_value>0:
                        tile_rects.append([tile_x + dirx, tile_y + diry])
                        return tile_rects+self.PossibleMoves(tile_x + dirx, tile_y + diry, movement_value-1)
                    else:
                        return tile_rects

    #makes a path
    #def pathlist
