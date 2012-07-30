import pygame
import sprites
from sprites import AnimatedSprite, Actor
import GameBoard
from GameBoard import Board
import collision
from collision import PopBestPath, PathList

#import TurnController
#from TurnController import Turn



            
def PortalAI(Turn):#this is how the portal thinks
    #should modify so that if the portal is deserted it spawns a stronger enemy
    #print('PortalAI called to control', Turn.CurrentSprite().Name())
    SpawnRadius=15#this is how far it looks for bad guys
    SpawnThreshold=6# if too many of the same alignment are nearby the portal will not spawn a badguy
    AllyCount=0#how many allies are neaby
    AdjacentCount=0
    HostileNearby=False
    #first check if the surrounding spaces are occupied
    for actor in Turn.Characters():
        if actorDist(actor, Turn.CurrentSprite())==1:
            AdjacentCount+=1
        if actor.Alignment()==Turn.CurrentSprite().Alignment() and actorDist(actor, Turn.CurrentSprite())<SpawnRadius:
           AllyCount+=1
        elif actorDist(actor, Turn.CurrentSprite())<SpawnRadius: #these are the non allies
            HostileNearby=True
    if AdjacentCount<4 and AllyCount<SpawnThreshold and HostileNearby:
        #First find a free tile, then spawn a baddie in it
        tile_x=Turn.CurrentSprite().tile_x
        tile_y=Turn.CurrentSprite().tile_y
        PortalLevel=Turn.CurrentSprite().Level()
        if Turn.Board().getTile(tile_x+1,tile_y, tiled=True)[0]=="Clear":
            Turn.SpawnSkeleton(tile_x+1,tile_y, level=PortalLevel)
            PortalMusic =pygame.mixer.Sound("sound/portal.wav")
            PortalMusic.play(loops=0)
        elif Turn.Board().getTile(tile_x-1,tile_y, tiled=True)[0]=="Clear":
            Turn.SpawnSkeleton(tile_x-1,tile_ylevel=PortalLevel)
            PortalMusic =pygame.mixer.Sound("sound/portal.wav")
            PortalMusic.play(loops=0)
        elif Turn.Board().getTile(tile_x,tile_y+1, tiled=True)[0]=="Clear":
            Turn.SpawnSkeleton(tile_x,tile_y+1,level=PortalLevel)
            PortalMusic =pygame.mixer.Sound("sound/portal.wav")
            PortalMusic.play(loops=0)
        elif Turn.Board().getTile(tile_x,tile_y-1, tiled=True)[0]=="Clear":
            Turn.SpawnSkeleton(tile_x,tile_y-1, level=PortalLevel)
            PortalMusic =pygame.mixer.Sound("sound/portal.wav")
            PortalMusic.play(loops=0)
        else:
            print('Something crazy must have happened with the PortalAI')
    else:
        Turn.CurrentSprite().GetExperience(10+int(Turn.CurrentSprite().Level()/2))



    Turn.addQueue('Wait',[],[])

def TurnAI(Turn, minRange=1, maxRange=1):
    #Check all of your allies and opponents, figure out which can be moved to and attacked.
    #if you begin with a target in range, take the shot then move toward the nearest ally, if no ally is near, move away from enemies that are too close (<2) if possible
    #if you begin with no targets in range, figure out if you can move an attack, if you can, do so, if not , move toward the nearest ally, if no ally is near, stay put.

    print('RangedAI called to control', Turn.CurrentSprite().Name())
    #def __init__(Turn, board):
        #super(Turn, Turn).__init__(Turn, board)

    #first we find a potential target/ally
    distanceThreshold= 2*(Turn.CurrentSprite().Movement()+Turn.CurrentSprite().Level())
    closeAlly=[]
    allyDist = 0
    targetOpponent=[]
    targetDist = 0
    AttackFirst=False #check to see if you should move then attack or vice versa
    NoAttack=True
    Ranged=False

    if minRange<1: minRange=1
    if minRange>maxRange: maxRange=minRange
    if maxRange>1:
        Ranged=True
        
        

    Turn._moves = PathList(Turn._board, Turn._currentSprite.tile_x,Turn._currentSprite.tile_y, Turn._currentSprite._Movement)
    currentMove=[] #shortest move to get to the closeOpponent


    #Find the closest ally and opponent
    for actor in Turn.Characters():
        #ally
        if actor.Alignment() == Turn.CurrentSprite().Alignment() and actor !=Turn.CurrentSprite():
            if allyDist==0: #this means you have no closest ally 
                closeAlly=actor
                allyDist = actorDist(Turn.CurrentSprite(), actor)
                allyDist = actorDist(Turn.CurrentSprite(), actor)
            elif allyDist > actorDist(Turn.CurrentSprite(), actor):
                closeAlly=actor
                allyDist = actorDist(Turn.CurrentSprite(), actor)

        #opponent      
        if actor.Alignment() != Turn.CurrentSprite().Alignment():
            if targetDist==0: #this means you have no closest ally 
                targetOpponent=actor
                targetDist = actorDist(Turn.CurrentSprite(), actor)

            #if the target can be hit without moving and has fewer hp than the current target
            elif minRange <= actorDist(Turn.CurrentSprite(), actor) and maxRange >= actorDist(Turn.CurrentSprite(), actor) and actor.Health()< targetOpponent.Health(): 
                targetOpponent=actor
                targetDist = actorDist(Turn.CurrentSprite(), actor)
                AttackFirst=True
                NoAttack=False
                
            #if no target can be hit without moving, then find the nearest opponent    
            elif targetDist > actorDist(Turn.CurrentSprite(), actor):
                targetOpponent=actor
                targetDist = actorDist(Turn.CurrentSprite(), actor)

    #finds the best move toward the closest opponent and ally


    for move in Turn._moves:

        if currentMove==[]:
            currentMove=move
            
        currentMoveOpponentDist = dist(currentMove[0], currentMove[1], targetOpponent.tile_x, targetOpponent.tile_y)
        newMoveOpponentDist = dist(move[0], move[1], targetOpponent.tile_x, targetOpponent.tile_y)
        if closeAlly !=[]:
            currentMoveAllyDist = dist(currentMove[0], currentMove[1], closeAlly.tile_x, closeAlly.tile_y)
            newMoveAllyDist = dist(move[0], move[1], closeAlly.tile_x, closeAlly.tile_y)
        else:
            currentMoveallyDist=0
            newMoveAllyDist=0
            
        #print(move)
        #print(closeOpponent.Name())
        #find the best move
        #If you are a ranged and can attack then move, then you attack them move as far as you can while still staying in range.

        
        if AttackFirst and newMoveOpponentDist<=maxRange and newMoveAllyDist <= currentMoveAllyDist:
            currentMove=move
            
        if AttackFirst==False:
            if NoAttack==False  and newMoveOpponentDist<=maxRange and newMoveOpponentDist >=minRange and newMoveOpponentDist>=currentMoveOpponentDist:
                currentMove=move
            elif newMoveOpponentDist<=maxRange and newMoveOpponentDist >=minRange:
                currentMove=move
                NoAttack=False
            elif NoAttack and newMoveOpponentDist <= currentMoveOpponentDist:
                currentMove=move
                
       #if attacktype =="Ranged": check that the distance for the new move is more than one but less than the range of the attack
    if targetDist==0:#this means there is no opponents so just hang out, this should actually never happen except in testing.
        Turn.addQueue('Wait', targetOpponent, currentMove)
        
    elif AttackFirst:# and attackType != "Ranged"
        Turn.addQueue('Attack', targetOpponent, currentMove)
        Turn.addQueue('Move', targetOpponent, currentMove)
        Turn.addQueue('Wait', targetOpponent, currentMove)
        
    elif AttackFirst==False and NoAttack==False:

        Turn.addQueue('Move', targetOpponent, currentMove)
        Turn.addQueue("Attack", targetOpponent, currentMove)
        Turn.addQueue('Wait', targetOpponent, currentMove)
        #move toward the opponent, then attack
    elif NoAttack and targetDist < distanceThreshold:
        Turn.addQueue('Move', targetOpponent, currentMove)
        Turn.addQueue('Wait', targetOpponent, currentMove)
    else:
        #this means you are far from everyone
        Turn.addQueue('Wait', targetOpponent, currentMove)                  
  
    #print(Turn.Queue())


#def AIAttack(Turn): 

#def AIMove(Turn)

def actorDist(actor0, actor1):
    return abs(actor1.tile_x - actor0.tile_x) + abs(actor1.tile_y - actor0.tile_y)

def dist(x0,y0,x1,y1):
    return abs(x1-x0)+abs(y1-y0)
