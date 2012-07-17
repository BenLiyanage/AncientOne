import pygame
import tiledtmxloader
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


def PossibleMovesPath(board, tile_x, tile_y, movement_value,dirs=[]):
#returns a list of possible move positions, their cost and the best path there.  Note the cost may be redundant
    tilesize=32 
    baselayer=0
    fringelayer=1
    shadowlayer=2
    objectlayer=3
    overhanglayer=4
    collisionlayer=5
    characters=board.Characters()
    layers=board.getLayers()
    coll_layer=layers[collisionlayer]
    obj_layer=layers[objectlayer]
    map_tile_x = len(layers[collisionlayer].content2D[0])
    map_tile_y = len(layers[collisionlayer].content2D)
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
            isClear = coll_layer.content2D[tile_y+diry][tile_x + dirx] is None
            
            isFree=True #may be set to be true even though it is not because it doesn't matter if isClear is false
            if isClear:
                for actor in characters:
                    if actor.tile_x==tile_x + dirx and actor.tile_y==tile_y + diry:
                        isFree=False
                        break
                
            isEfficient=True
            
            #checks if there was a previously discovered more expensive path, which it will remove
            if isFree and isClear:
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
                       
            
            if isClear and isFree and isEfficient:
    
                tile_rects=tile_rects+PossibleMovesPath(board, tile_x + dirx, tile_y+diry, movement_value-1,dirs+[(dirx,diry)])


                
        return tile_rects
        
def PathList(board, tile_x, tile_y, movement_value):
    return cleanPathList(PossibleMovesPath(board, tile_x, tile_y, movement_value,[]))

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
    def PossibleMoves(self, tile_x, tile_y, movement_value):
    #returns a list of possible move positions
        tile_rects = [(tile_x,tile_y)]
        if movement_value==0:
           return tile_rects
        else:
            for (dirx,diry) in [(1,0), (-1,0), (0,1), (0,-1)]:
                look_tile=self._coll_layer.content2D[tile_y+diry][tile_x + dirx]

                if look_tile is None:
                    tile_rects.append((tile_x + dirx, tile_y+diry))
                    tile_rects=list(set(tile_rects+self.PossibleMoves(tile_x + dirx, tile_y+diry, movement_value-1)))
            return tile_rects

    #def PossibleMoves2(self, tile_x, tile_y, movement_value):
    #    #a simple way to do this we make a matrix, then just flip adjacent tiles with numbers in them
    #    tilearray=[][]
    #    for i
'''
