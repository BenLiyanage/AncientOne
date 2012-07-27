import pygame
import sprites
from sprites import AnimatedSprite, Actor
import GameBoard
from GameBoard import Board
import collision
from collision import PopBestPath, PathList

#import TurnController
#from TurnController import Turn



#need a formula balancing distance with hp. (smarter AI

#we need to know if a bad guy can walk then kill, some kind of "inrange" sort of boolean

#this should run their turn for them

'''
if you can move and kill, do so,
if you can attack without moving, attack then move away
if no opponent is in range, then move toward the nearest ally,
if no one is near then do nothing.
'''

##this is really an extension of Turn
def TurnAI(Turn): #determines what you are going to do on your turn
    print('TurnAI called to control', Turn.CurrentSprite().Name())
    #def __init__(Turn, board):
        #super(Turn, Turn).__init__(Turn, board)

    #first we find a potential target/ally
    distanceThreshold= 2*Turn.CurrentSprite().Movement()+Turn.CurrentSprite().Level()
    closeAlly=[]
    allyDist = 0
    closeOpponent=[]
    opponentDist = 0

    Turn._moves = PathList(Turn._board, Turn._currentSprite.tile_x,Turn._currentSprite.tile_y, Turn._currentSprite._Movement)
    closeOpponentMove=[] #shortest move to get to the closeOpponent
    closeAllyMove=[] #shortest move to get to closeAlly


    #Find the closest ally and opponent
    for actor in Turn.Characters():
        if actor.Alignment() == Turn.CurrentSprite().Alignment() and actor !=Turn.CurrentSprite():
            if allyDist==0: #this means you have no closest ally 
                closeAlly=actor
                allyDist = actorDist(Turn.CurrentSprite(), actor)
                allyDist = actorDist(Turn.CurrentSprite(), actor)
            elif allyDist > actorDist(Turn.CurrentSprite(), actor):
                closeAlly=actor
                allyDist = actorDist(Turn.CurrentSprite(), actor)
        if actor.Alignment() != Turn.CurrentSprite().Alignment():
            if opponentDist==0: #this means you have no closest ally 
                closeOpponent=actor
                opponentDist = actorDist(Turn.CurrentSprite(), actor)
            #elif #same distance but more damaged?
            elif opponentDist > actorDist(Turn.CurrentSprite(), actor):
                closeOpponent=actor
                opponentDist = actorDist(Turn.CurrentSprite(), actor)

    #finds the best move toward the closest opponent and ally
    #this will have to change for ranged attacks.
    
    for move in Turn._moves:

        if closeOpponentMove==[]:
            closeOpponentMove=move
        if closeAllyMove==[]:
            closeAllyMove=move
        #print(move)
        #print(closeOpponent.Name())
        if closeOpponent != [] and (dist(move[0], move[1], closeOpponent.tile_x, closeOpponent.tile_y)==1 or \
            dist(move[0], move[1], closeOpponent.tile_x, closeOpponent.tile_y) < dist(closeOpponentMove[0], closeOpponentMove[1], closeOpponent.tile_x, closeOpponent.tile_y)):
            closeOpponentMove=move
        if closeAlly !=[] and (dist(move[0], move[1], closeAlly.tile_x, closeAlly.tile_y) < dist(closeAllyMove[0], closeAllyMove[1], closeAlly.tile_x, closeAlly.tile_y)):
            closeAllyMove=move           
       #if attacktype =="Ranged": check that the distance for the new move is more than one but less than the range of the attack

    if opponentDist==0:
        Turn.addQueue('Wait', closeOpponent, closeOpponentMove)
    
    elif opponentDist==1:# and attackType != "Ranged"
        Turn.addQueue('Attack', closeOpponent, closeOpponentMove)
        Turn.addQueue('Move', closeOpponent, closeAllyMove)
        Turn.addQueue('Wait', closeOpponent, closeAllyMove)

    elif opponentDist < Turn.CurrentSprite().Movement()+1 and dist(closeOpponent.tile_x, closeOpponent.tile_y, closeOpponentMove[0], closeOpponentMove[1])==1:
        Turn.addQueue('Move', closeOpponent, closeOpponentMove)
        Turn.addQueue("Attack", closeOpponent, closeOpponentMove)
        Turn.addQueue('Wait', closeOpponent, closeOpponentMove)
        #move toward the opponent, then attack
    elif opponentDist >= Turn.CurrentSprite().Movement()+1 and opponentDist < distanceThreshold:
        Turn.addQueue('Move', closeOpponent, closeOpponentMove)
        Turn.addQueue('Wait', closeOpponent, closeOpponentMove)
    elif opponentDist >= Turn.CurrentSprite().Movement()+1 and allyDist < 2*distanceThreshold:
        print('here?')
        Turn.addQueue('Move', closeOpponent, closeAllyMove)
        Turn.addQueue('Wait', closeOpponent, closeOpponentMove)
    else: # opponentDist > currentSprite.Movement and allyDist > 2*distanceThreshold:
        #Turn.addQueue('Move', closeOpponent, closeAllyMove)
 
        Turn.addQueue('Wait', closeOpponent, closeOpponentMove)                  
  
    #print('Closest Opponent', closeOpponent.Name())
    #print('Closest Ally', closeAlly.Name())
    print(Turn.Queue())
            
def PortalAI(Turn):#this is how the portal thinks
    print('PortalAI called to control', Turn.CurrentSprite().Name())
    SpawnRadius=15#this is how far it looks for bad guys
    SpawnThreshold=6# if too many of the same alignment are nearby the portal will not spawn a badguy
    AllyCount=0#how many allies are neaby
    AdjacentCount=0
    #first check if the surrounding spaces are occupied
    for actor in Turn.Characters():
        if actorDist(actor, Turn.CurrentSprite())==1:
            AdjacentCount+=1
        if actor.Alignment()==Turn.CurrentSprite().Alignment() and actorDist(actor, Turn.CurrentSprite())<SpawnRadius:
           AllyCount+=1
    if AdjacentCount<4 and AllyCount<SpawnThreshold:
        #First find a free tile, then spawn a baddie in it
        tile_x=Turn.CurrentSprite().tile_x
        tile_y=Turn.CurrentSprite().tile_y
        if Turn.Board().getTile(tile_x+1,tile_y, tiled=True)[0]=="Clear":
            Turn.SpawnSkeleton(tile_x+1,tile_y)
        elif Turn.Board().getTile(tile_x-1,tile_y, tiled=True)[0]=="Clear":
            Turn.SpawnSkeleton(tile_x-1,tile_y)
        elif Turn.Board().getTile(tile_x,tile_y+1, tiled=True)[0]=="Clear":
            Turn.SpawnSkeleton(tile_x,tile_y+1)
        elif Turn.Board().getTile(tile_x,tile_y-1, tiled=True)[0]=="Clear":
            Turn.SpawnSkeleton(tile_x,tile_y-1)
        else:
            print('Something crazy must have happened with the PortalAI')

    Turn.addQueue('Wait',[],[])

#def AIAttack(Turn): 

#def AIMove(Turn)

def actorDist(actor0, actor1):
    return abs(actor1.tile_x - actor0.tile_x) + abs(actor1.tile_y - actor0.tile_y)

def dist(x0,y0,x1,y1):
    return abs(x1-x0)+abs(y1-y0)
