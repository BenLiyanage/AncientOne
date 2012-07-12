import pygame
import tiledtmxloader

class CollisionFinder(object):
    def __init__(self, characters, layers):
        self.tilesize=32 
        self.baselayer=0
        self.fringelayer=1
        self.shadowlayer=2
        self.objectlayer=3
        self.overhanglayer=4
        self.collisionlayer=5
        self._characters=characters
        self.layers=layers
        self._coll_layer=layers[self.collisionlayer]
        self._obj_layer=layers[self.objectlayer]
        

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

#this will be an improved(more efficient) possibleMoves that will also determine the best path.
    def PossibleMovesPath(self, tile_x, tile_y, movement_value,dirs=[]):
    #returns a list of possible move positions, their cost and the best path there.  Note the cost may be redundant
        tile_rects = [(tile_x,tile_y,movement_value,dirs)]#initial position costs nothing and you do not need to move to get there
        if movement_value==0:
            return tile_rects          
        else:

            for (dirx,diry) in [(1,0), (-1,0), (0,1), (0,-1)]:
                isClear = self._coll_layer.content2D[tile_y+diry][tile_x + dirx] is None
                isFree=True
                for actor in self._characters:
                    if actor.tile_x==tile_x + dirx and actor.tile_y==tile_y + diry:
                        isFree=False
                    #isFree =  self._obj_layer.content2D[tile_y+diry][tile_x + dirx] is None
                #print("from",(tile_x,tile_y),"look if",(dirx,diry), "isClear is:", isClear)
                isEfficient=True
                #checks if there was a previously discovered more expensive path, which it will remove
                for t in tile_rects:
                    #print("comparing:",tile_x+dirx, tile_y+diry,"to",t)
                    #print(t[0]==tile_x + dirx, t[1]==tile_y+diry, t[2]>movement_value)
                    if t[0]==tile_x + dirx and t[1]==tile_y+diry:
                        if t[2]>movement_value:
                            isEfficient=False
                        else:
                            #print("removing",t)
                            tile_rects.remove(t)
                        #print(t in tile_rects)
                #If it is clear and cheap then add it to the list
                if isClear and isFree and isEfficient:
                    #dirs.append((dirx,diry))
                    #if (tile_x + dirx, tile_y+diry,movement_value-1,dirs+[(dirx,diry)]) not in tile_rects:
                    #    tile_rects.append((tile_x + dirx, tile_y+diry,movement_value-1,dirs+[(dirx,diry)]))

                    #tile_rects=tile_rects+self.PossibleMovesPath(tile_x + dirx, tile_y+diry, movement_value-1,dirs+[(dirx,diry)])
                    tile_rects=cleanPathList(tile_rects+self.PossibleMovesPath(tile_x + dirx, tile_y+diry, movement_value-1,dirs+[(dirx,diry)]))

                    #currently the "+" above does not clean out less efficient paths,  we need to do this, the below code tries to do this but is too messy
                    #new_branch=self.PossibleMovesPath(tile_x + dirx, tile_y+diry, movement_value-1,dirs+[(dirx,diry)])
                    #print(new_branch)
                    #for b in new_branch:
                    #    for c in tile_rects:
                    #        if b[0]==c[0] and b[1]==c[1] and b[2]>c[2]:
                    #            tile_rects.remove(c)
                    #            tile_rects.append(b)
                    #        else:
                    #            tile_rects.append(b)
                    
            return tile_rects
        
    def PathList(self, tile_x, tile_y, movement_value):
        return cleanPathList(self.PossibleMovesPath(tile_x, tile_y, movement_value,[]))

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
    

