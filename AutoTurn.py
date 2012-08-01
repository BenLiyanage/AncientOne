# <This is the file contains functions that dictate NPC actions.>
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
import sprites
import random
from sprites import AnimatedSprite, Actor
import GameBoard
from GameBoard import Board
import collision
from collision import PopBestPath, PathList, MovesArray, TracePath, CollisionArray

#import TurnController
#from TurnController import Turn



            
def PortalAI(Turn):#this is how the portal thinks
    #should modify so that if the portal is deserted it spawns a stronger enemy
    #print('PortalAI called to control', Turn.CurrentSprite().Name())
    SpawnRadius=15#this is how far it looks for bad guys
    AttackRadius=3
    SpawnThreshold=6# if too many of the same alignment are nearby the portal will not spawn a badguy
    AllyCount=0#how many allies are neaby
    AdjacentCount=0
    HostileNearby=False
    targetOpponent=[]
    coinflip=random.randint(0,1) 
    #first check if the surrounding spaces are occupied
    for actor in Turn.Characters():
        if actorDist(actor, Turn.CurrentSprite())==1:
            AdjacentCount+=1
        if actor.Alignment()==Turn.CurrentSprite().Alignment() and actorDist(actor, Turn.CurrentSprite())<SpawnRadius:
           AllyCount+=1
        elif actor.Alignment()!= Turn.CurrentSprite().Alignment() and actorDist(actor, Turn.CurrentSprite())<AttackRadius: #these are the non allies
            HostileNearby=True
            targetOpponent=actor
        elif actorDist(actor, Turn.CurrentSprite())<SpawnRadius: #these are the non allies
            HostileNearby=True
    if targetOpponent !=[] and coinflip:
        print("target for tentacle:", targetOpponent.Name())
        Turn.addQueue('Tentacle',targetOpponent,[])
        
    elif AdjacentCount<4 and AllyCount<SpawnThreshold and HostileNearby:
        Turn.CurrentSprite().GetExperience(10-int(Turn.CurrentSprite().Level()/2))
        #First find a free tile, then spawn a baddie in it
        tile_x=Turn.CurrentSprite().tile_x
        tile_y=Turn.CurrentSprite().tile_y
        PortalLevel=Turn.CurrentSprite().Level()
        if Turn.Board().getTile(tile_x+1,tile_y, tiled=True)[0]=="Clear":
            Turn.SpawnRandomEnemy(tile_x+1,tile_y, PortalLevel)
            PortalMusic =pygame.mixer.Sound("sound/portal.wav")
            PortalMusic.play(loops=0)
        elif Turn.Board().getTile(tile_x-1,tile_y, tiled=True)[0]=="Clear":
            Turn.SpawnRandomEnemy(tile_x-1,tile_y,PortalLevel)
            PortalMusic =pygame.mixer.Sound("sound/portal.wav")
            PortalMusic.play(loops=0)
        elif Turn.Board().getTile(tile_x,tile_y+1, tiled=True)[0]=="Clear":
            Turn.SpawnRandomEnemy(tile_x,tile_y+1,PortalLevel)
            PortalMusic =pygame.mixer.Sound("sound/portal.wav")
            PortalMusic.play(loops=0)
        elif Turn.Board().getTile(tile_x,tile_y-1, tiled=True)[0]=="Clear":
            Turn.SpawnRandomEnemy(tile_x,tile_y-1, PortalLevel)
            PortalMusic =pygame.mixer.Sound("sound/portal.wav")
            PortalMusic.play(loops=0)
        else:
            print('Something crazy must have happened with the PortalAI')
    else:
        Turn.CurrentSprite().GetExperience(10-int(Turn.CurrentSprite().Level()/2))



    Turn.addQueue('Wait',[],[])

def TurnAI(Turn, minRange=1, maxRange=1):
    #Check all of your allies and opponents, figure out which can be moved to and attacked.
    #if you begin with a target in range, take the shot then move toward the nearest ally, if no ally is near, move away from enemies that are too close (<2) if possible
    #if you begin with no targets in range, figure out if you can move an attack, if you can, do so, if not , move toward the nearest ally, if no ally is near, stay put.

    #print('RangedAI called to control', Turn.CurrentSprite().Name())
    #def __init__(Turn, board):
        #super(Turn, Turn).__init__(Turn, board)

    #first we find a potential target/ally
    distanceThreshold= 2*(Turn.CurrentSprite().Movement()+Turn.CurrentSprite().Level())+20
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

    
    
    #(removed for new pathfinding) Turn._moves = PathList(Turn._board, Turn._currentSprite.tile_x,Turn._currentSprite.tile_y, Turn._currentSprite._Movement)
    movePoint={} #the point (as defined in collision.py) that the character will move toward
    moveDistance=0
    retreatPoint={}
    retreatDistance={}#the retreats are simply moving toward an ally
    boundarySet= [{'x':Turn.CurrentSprite().tile_x,'y':Turn.CurrentSprite().tile_y, 'cost':0, 'previous_x':Turn.CurrentSprite().tile_x,'previous_y':Turn.CurrentSprite().tile_y }]
    Turn._moves= MovesArray(CollisionArray(Turn._board), boundarySet,[],Turn.CurrentSprite()._Movement,0)
    #Find the cheapest to get to ally and opponent, also find out if you can attack.
    for actor in Turn.Characters():
        #ally
        if actor.Alignment() == Turn.CurrentSprite().Alignment() and actor !=Turn.CurrentSprite():
            if allyDist==0: #this means you have no closest ally 
                closeAlly=actor
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
                
            #if no target can be hit without moving, then find the closest actor you can walk to:

        for point in Turn._moves:
            if movePoint=={}: movePoint=point
            if retreatPoint=={}: retreatPoint=point
            currentMoveDistance = dist(actor.tile_x, actor.tile_y, point['x'], point['y'])
            if actor == Turn.CurrentSprite():
                continue
            
            if AttackFirst==False and actor.Alignment() != Turn.CurrentSprite().Alignment() and minRange<= moveDistance and maxRange <=moveDistance: #if you can move within range
                targetOpponent=actor
                MovePoint=point
                moveDistance=currentMoveDistance
                NoAttack=False
                targetOpponent=actor
                    
                
            
            elif NoAttack and actor.Alignment() != Turn.CurrentSprite().Alignment() and currentMoveDistance<moveDistance: #if you cant attack then move closer
                currentMovePoint=point
                moveDistance=currentMoveDistance
            elif actor.Alignment() == Turn.CurrentSprite().Alignment() and retreatDistance> currentMoveDistance:
                retreatPoint=point
                retreatDistance=currentMoveDistance
                
                            
                        
    '''    
            elif targetDist > actorDist(Turn.CurrentSprite(), actor):
                targetOpponent=actor
                targetDist = actorDist(Turn.CurrentSprite(), actor)


    
    for move in Turn._moves:

        if currentMove=={}:
            currentMove=move
       
        
        currentMoveOpponentDist = dist(currentMove['x'], currentMove['y'], targetOpponent.tile_x, targetOpponent.tile_y)
        newMoveOpponentDist = dist(move['x'], move['y'], targetOpponent.tile_x, targetOpponent.tile_y)
        if closeAlly !=[]:
            currentMoveAllyDist = dist(currentMove['x'], currentMove['y'], closeAlly.tile_x, closeAlly.tile_y)
            newMoveAllyDist = dist(move['x'], move['y'], closeAlly.tile_x, closeAlly.tile_y)
        else:
            currentMoveAllyDist=0
            newMoveAllyDist=0

        

        
        if AttackFirst and newMoveOpponentDist<=maxRange and newMoveAllyDist <= currentMoveAllyDist:
            currentMove=move
            
        if AttackFirst==False:
            if NoAttack==False  and newMoveOpponentDist<=maxRange and newMoveOpponentDist >=minRange and newMoveOpponentDist>=currentMoveOpponentDist:
                currentMove=move
            elif newMoveOpponentDist<=maxRange and newMoveOpponentDist >=minRange:
                currentMove=move
                NoAttack=False
            # if you cannot attack that round, walk toward the closest/cheapest opponent within distanceThreshold

                currentMove=move
    '''
    #These next variables cuts off the movement generated to only provide the number of directions
    #equal to the characters movement
    targetMoveFull=TracePath(Turn._moves, targetOpponent.tile_x,targetOpponent.tile_y)
    if len(targetMoveFull)>=Turn.CurrentSprite().Movement():
        targetMove=targetMoveFull
    else:
        targetMove=targetMoveFull[len(targetMoveFull)-Turn.CurrentSprite().Movement():len(targetMoveFull)]

    retreatMoveFull=TracePath(Turn._moves, retreatPoint['x'],retreatPoint['y'])
    print("Full AutoTurn action", targetMoveFull, "will be cut down to", Turn.CurrentSprite().Movement())
    print("AutoTurn wants",Turn.CurrentSprite().Name(), "to ", targetMove)
    if len(retreatMoveFull)>=Turn.CurrentSprite().Movement():
        retreatMove=retreatMoveFull
    else:
        retreatMove=targetMoveFull[len(retreatMoveFull)-Turn.CurrentSprite().Movement():len(retreatMoveFull)]    

    #now we add to the queue
    if targetDist==0:#No good guys on the board
        Turn.addQueue('Wait', targetOpponent, targetMove)
        
    elif AttackFirst:# and attackType != "Ranged"
        Turn.addQueue('Attack', targetOpponent, retreatMove)
        Turn.addQueue('Move', targetOpponent, retreatMove)
        Turn.addQueue('Wait', targetOpponent, retreatMove)
        
    elif AttackFirst==False and NoAttack==False:

        Turn.addQueue('Move', targetOpponent, targetMove)
        Turn.addQueue("Attack", targetOpponent, targetMove)
        Turn.addQueue('Wait', targetOpponent, targetMove)

    elif NoAttack and targetDist < 2*Turn.CurrentSprite().Movement():
        Turn.addQueue('Move', targetOpponent, targetMove)
        Turn.addQueue('Wait', targetOpponent, targetMove)
    elif NoAttack and targetDist > 2*Turn.CurrentSprite().Movement():
        Turn.addQueue('Move', targetOpponent, retreatMove)
        Turn.addQueue('Wait', targetOpponent, targetMove)
    else:
        #this means you are far from everyone
        Turn.addQueue('Wait', targetOpponent, targetMove)                  
  


def actorDist(actor0, actor1):
    return abs(actor1.tile_x - actor0.tile_x) + abs(actor1.tile_y - actor0.tile_y)

def dist(x0,y0,x1,y1):
    return abs(x1-x0)+abs(y1-y0)
