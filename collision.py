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
    def PossibleMovesPath(self, tile_x, tile_y, movement_value,dirs=[]):
    #returns a list of possible move positions, their cost and the best path there.  Note the cost may be redundant
        tile_rects = [(tile_x,tile_y,movement_value,dirs)]#initial position costs nothing and you do not need to move to get there
        if movement_value==0:
            return tile_rects          
        else:

            for (dirx,diry) in [(1,0), (-1,0), (0,1), (0,-1)]:
                isClear = self._coll_layer.content2D[tile_y+diry][tile_x + dirx] is None
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
                if isClear and isEfficient:
                    #dirs.append((dirx,diry))
                    #if (tile_x + dirx, tile_y+diry,movement_value-1,dirs+[(dirx,diry)]) not in tile_rects:
                    #    tile_rects.append((tile_x + dirx, tile_y+diry,movement_value-1,dirs+[(dirx,diry)]))

                    tile_rects=tile_rects+self.PossibleMovesPath(tile_x + dirx, tile_y+diry, movement_value-1,dirs+[(dirx,diry)])

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
            
    
#def popBestPath(x,y,path_list): returns a list of directions that is the best way to get to x,y from a list.

#def combinePathLists(list1, list2):
    #the function combines two pathlists whose entries look like #(endx,endy,cost,directionslist)
    #this looks through both lists and finds the entries that are most efficient pathways
#    newlist=[]
    

    
    
            
            

    #makes a path
    #def pathlist

