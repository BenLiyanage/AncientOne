# <This file contains the algorithms for pathfinding for the sprites.>
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

import pygame
import tiledtmxloader
import copy
from copy import deepcopy
'''
class CollisionFinder(object):
    def __init__(self, board):
        self.tilesize=32 
        self.baselayer=0
        self.fringelayer=1
        self.shadowlayer=2
        self.objectlayer=3
        self.overhanglayer=4
        self.collisionlayer=5
        self._characters=board.getCharacters()
        self.layers=board.getLayers()
        self._coll_layer=layers[self.collisionlayer]
        self._obj_layer=layers[self.objectlayer]
        self._map_tile_x = len(self.layers[self.collisionlayer].content2D[0])
        self._map_tile_y = len(layers[self.collisionlayer].content2D)
'''        


def PossibleMovesPath(Collisions, tile_x, tile_y, movement_value,dirs=[]):
#returns a list of possible move positions, their cost and the best path there.  Note the cost may be redundant

    map_tile_x = len(Collisions[0])
    map_tile_y = len(Collisions)
    tile_rects = [(tile_x,tile_y,movement_value,dirs)]#initial position costs nothing and you do not need to move to get there
    if movement_value==0:
        return tile_rects          
    else:
        lookset=[(1,0), (-1,0), (0,1), (0,-1)]
        if dirs != []:
            i=len(dirs)
            lookset.remove((-dirs[i-1][0],-dirs[i-1][1])) #takes out the last place you visited (since it is always better)
        
        for (dirx,diry) in lookset: #[(1,0), (-1,0), (0,1), (0,-1)]:
            #If one of isClear, isFree, isEfficient does not hold then we shouldn't check the others.
            isClear = Collisions[tile_y+diry][tile_x + dirx] is None
                
            isEfficient=True
            
            #checks if there was a previously discovered more expensive path, which it will remove
            if isClear:
                for t in tile_rects:
                    #print("comparing:",tile_x+dirx, tile_y+diry,"to",t)
                    #print(t[0]==tile_x + dirx, t[1]==tile_y+diry, t[2]>movement_value)
                    if t[0]==tile_x + dirx and t[1]==tile_y+diry:
                        if t[2]>movement_value:
                            isEfficient=False
                            break
                        else:
                            #removing is likely not very important since we will clean the list later.
                            #print("removing",t)
                            tile_rects.remove(t)
                        #print(t in tile_rects)
                       
            
            if isClear and isEfficient:
    
                tile_rects=tile_rects+PossibleMovesPath(Collisions, tile_x + dirx, tile_y+diry, movement_value-1,dirs+[(dirx,diry)])

                
        return tile_rects #these are the moves each possible move looks like a string of these (tile_x,tile_y,movement_value,dirs)
        
def PathList(board, tile_x, tile_y, movement_value):

    Collisions = CollisionArray(board)
    
    
    return cleanPathList(PossibleMovesPath(Collisions, tile_x, tile_y, movement_value,[]))

def cleanPathList(path_list):#removes bad entries from a list
    new_list=[]
    old_length=len(path_list)
    for j in range(old_length):
        best_path_index=j
        for k in range(old_length):
            if path_list[best_path_index][0]==path_list[k][0] and path_list[best_path_index][1]==path_list[k][1] and path_list[best_path_index][2]<=path_list[k][2]:
                best_path_index=k
        if path_list[best_path_index] not in new_list:
            new_list.append(path_list[best_path_index])
        #print new_list
    return new_list
            
    
def PopBestPath(x,y,path_list): #returns a list of directions that is the best way to get to x,y from a list.
    #first find it
    path=[]
    for i in path_list:
        if x==i[0] and y==i[1]:
            path=i[3]
    #return path
    #then turn it into "(1,0), (-1,0), (0,1), (0,-1)" -> ("Right","Left", "Down", "Up")    
    if path !=[]:
        for n, j in enumerate(path):
            if j==(1,0):
                path[n]="Right"
            elif j==(-1,0):
                path[n]="Left"
            elif j==(0,1):
                path[n]="Down"
            elif j==(0,-1):
                path[n]="Up"
            else:
                print("Error in PopBestPath list translation. Found a ",j,"at", n)
    return path
    
'''
def SmarterMoves(board,tile_x,tile_y, depth):
    #returns and array of all the possible moves you can get to,(possibly with the nearest ally/enemy labeled)
    #depth is how far it will search,  this it sort of how many steps it can think ahead,  this should be somewhow based on the level and movement value of the actor
    #possibly depth=2*(movement+level)

    collisionlayer=board.collisionLayer()
    characters=board.Characters()
    layers=board.getLayers()
    coll_layer=layers[collisionlayer]
    map_tile_x = len(layers[collisionlayer].content2D[0])#number of tiles the map is across
    map_tile_y = len(layers[collisionlayer].content2D)
    
    costMap={}
    xdepth_min = max(0,tile_x-depth)
    xdepth_max = min(map_tile_x, tile_x+depth)
    ydepth_min = max(0,tile_y-depth)
    ydepth_max = min(map_tile_y, tile_y+depth)

    #first we initialize the array of values.  
    for i in range(xdepth_min, xdepth_max):
        for j in range(ydepth_min,y_depthmax):
            costMap[i][j]=[i,j,None]#the x and y coordinates, along with a 'None' value meaning that it has not been visited.
'''

def CollisionArray(board,depth=0):

    collisionlayer=board.CollisionLayer()
    characters=board.Characters()
    layers=board.getLayers()
    coll_layer=deepcopy(layers[collisionlayer].content2D)#makes a copy
    #map_tile_x = len(layers[collisionlayer].content2D[0])#number of tiles the map is across
    #map_tile_y = len(layers[collisionlayer].content2D)
    

    for actor in characters:
        coll_layer[actor.tile_y][actor.tile_x]=actor.Name()
    #print coll_layer[15][4]
    return coll_layer
            

