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
    SpawnRadius=30#this is how far it looks for bad guys
    AttackRadius=3
    SpawnThreshold=8# if too many of the same alignment are nearby the portal will not spawn a badguy
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

    print('TurnAI called to control', Turn.CurrentSprite().Name(), 'at', Turn.CurrentSprite().tile_x, Turn.CurrentSprite().tile_y)
    #def __init__(Turn, board):
        #super(Turn, Turn).__init__(Turn, board)

    #first we find a potential target/ally
    #distanceThreshold= min(2*(Turn.CurrentSprite().Movement()+Turn.CurrentSprite().Level())+10,40)
    distanceThreshold=35
    closeAlly=[]
    allyDist = 0
    targetOpponent=[]
    targetDist = 0
    moveAlly=[]
    moveAllyDist=0
    moveAllyPoint={}
    moveOpponent=[]
    moveOpponentDist=0
    moveOpponentPoint={}
    AttackFirst=False #check to see if you should move then attack or vice versa
    NoAttack=True #checks to see if you can attack at all this round
    Ranged=False # are you a ranged attacker?

    if minRange<1: minRange=1
    if minRange>maxRange: maxRange=minRange
    if maxRange>1:
        Ranged=True
    
    boundarySet= [{'x':Turn.CurrentSprite().tile_x,'y':Turn.CurrentSprite().tile_y, 'cost':0, 'previous_x':Turn.CurrentSprite().tile_x,'previous_y':Turn.CurrentSprite().tile_y }]
    Turn._moves= MovesArray(CollisionArray(Turn._board), boundarySet,[],distanceThreshold,0)
    #Find the cheapest to get to ally and opponent, also find out if you can attack.
    for actor in Turn.Characters():
        #ally
        if actor ==Turn.CurrentSprite():
            pass
        elif actor.Alignment() == Turn.CurrentSprite().Alignment() and actor !=Turn.CurrentSprite():
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
        #find the ally and opponent where it would be cheapest to walk to.
        for point in Turn._moves:
            if moveOpponentPoint=={}: moveOpponentPoint=point
            if moveAllyPoint=={}: moveAllyPoint=point
            
            currentMoveDist = dist(actor.tile_x, actor.tile_y, point['x'], point['y'])
            if actor == Turn.CurrentSprite():
                pass 
            elif actor.Alignment() != Turn.CurrentSprite().Alignment():
                if moveOpponent==[]:
                    moveOpponent=actor
                    moveOpponentDist=currentMoveDist
                    moveOpponentPoint=point
                if minRange<= currentMoveDist and maxRange >=currentMoveDist and point['cost']<= Turn.CurrentSprite().Movement(): #if you can move within stiking range this turn
                    #if you have not targeted anyone yet, target this person
                    if NoAttack==True:
                        #print("Moving to", point," will allow me to attack", actor.Name(), "since my range is", maxRange, "and the target will be ", currentMoveDist,"away")
                        NoAttack=False
                        moveOpponent=actor
                        moveOpponentPoint=point
                        moveOpponentDist=currentMoveDist
                        print("AutoTurn targeting:", actor.Name())
                    elif AttackFirst and actor.Health()<=targetOpponent.Health():
                        #If you can move and attack someone weaker than the person you can attack without moving then do that.
                        AttackFirst=False 
                        moveOpponent=actor
                        moveOpponentPoint=point
                        moveDist=currentMoveDist
                    elif actor.Health()<moveOpponent.Health():
                        #if you are already moving you should find the weakest target you can move and attack
                        #print("Switching target from,", moveOpponent.Name(),"to", actor.Name())
                        #print("Point was", moveOpponentPoint, "but now is", point)
                        #print("Moving to", point," will allow me to attack", actor.Name(), "since my range is", maxRange, "and the target will be ", currentMoveDist,"away")
                        moveOpponent=actor
                        moveOpponentPoint=point
                        moveOpponentDist=currentMoveDist
                    NoAttack=False
                elif NoAttack and minRange<= currentMoveDist and maxRange >=currentMoveDist:#this means you can eventually move to the target
                    #No one to attack? just move closer to an opponent
                    movetOpponent=actor
                    moveOpponentPoint=point
                    moveOpponentDist=currentMoveDist
                    
            elif actor.Alignment() == Turn.CurrentSprite().Alignment():
                if moveAlly == []:
                    moveAlly=actor
                    moveAllyDist=currentMoveDist
                    moveAllyPoint=point
                elif moveAllyDist> currentMoveDist and point['cost']<moveAllyPoint['cost']:
                    moveAlly=actor
                    moveAllyDist=currentMoveDist
                    moveAllyPoint=point
                
    #print("After all that thinking, I've decided to move to", moveOpponentPoint, "to attack", moveOpponent.Name())  
    #These next variables cuts off the movement generated to only provide the number of directions
    #equal to the characters movement
    

    
    #print("AutoTurn opponentMove:", opponentMove)
    #print("AutoTurn allyMove:", allyMove)
    #now we add to the queue
    if targetDist==0:#No good guys on the board
        Turn.addQueue('Wait', [], [])
        
    elif AttackFirst:# and attackType != "Ranged"
        #print("Attack then move")
        allyMove=TracePath(Turn._moves, moveAllyPoint['x'],moveAllyPoint['y'], movement = Turn.CurrentSprite().Movement())
        Turn.addQueue('Attack', targetOpponent, [])
        Turn.addQueue('Move', [], allyMove)
        Turn.addQueue('Wait', [], [])
        
    elif AttackFirst==False and NoAttack==False:
        #print("move then attack")
        opponentMove=TracePath(Turn._moves, moveOpponentPoint['x'], moveOpponentPoint['y'], movement = Turn.CurrentSprite().Movement())
        #print("AutoTurn move:", opponentMove)
        Turn.addQueue('Move', [], opponentMove)
        Turn.addQueue("Attack", moveOpponent, [])
        Turn.addQueue('Wait', [], [])

    elif NoAttack:# and targetDist <= 3*Turn.CurrentSprite().Movement():
        #print("just move to target")
        opponentMove=TracePath(Turn._moves, moveOpponentPoint['x'], moveOpponentPoint['y'], movement = Turn.CurrentSprite().Movement())
        Turn.addQueue('Move', [], opponentMove)
        Turn.addQueue('Wait', [], [])
        '''    
    elif NoAttack and targetDist > 3*Turn.CurrentSprite().Movement():
        #print("just move to ally")     
        Turn.addQueue('Move', [], allyMove)
        Turn.addQueue('Wait', [], [])
        '''
    else:
        #print("just wait")
        #this means you are far from everyone
        Turn.addQueue('Wait', [], [])                  
  


def actorDist(actor0, actor1):
    return abs(actor1.tile_x - actor0.tile_x) + abs(actor1.tile_y - actor0.tile_y)

def dist(x0,y0,x1,y1):
    return abs(x1-x0)+abs(y1-y0)
