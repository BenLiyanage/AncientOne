#these are all the special attacks mode are in two parts.
#The player enters a mode, i.e. "AOEmode" for an AOE attack, then
#the player 


#def VampiricStrike(actor,target):# a special attack that also heals you.

#def Heal(actor, target):#heals a certain target

#def PassiveHeal(actor):


    
    
#def WhirlWind(actor):#attacks all players (hostile or friendly) in adjacent spa


#def Cripple(actor): decreases initiative.

#def Spawn(actor):


def AOEMode(self, specialtype):# right now this is an AOE attack
    if self._canAttack:
        self._mode=SPECIAL
        specialRange=4
        self._board.HighlightArea(self._currentSprite.tile_x, self._currentSprite.tile_y, specialRange,'images/blue_box.png')            
        self.Board().ChangeCursor("images/area01.png", -1, -1)

def AOEAttack(self,tile_x,tile_y, attacktype):
    board_x, board_y =tile_x+self.Board()._camTile_x, tile_y+self.Board()._camTile_y
    if dist(self.CurrentSprite().tile_x,self.CurrentSprite().tile_y, board_x,board_y)<=4:
        self._board.ClearLayer(self._board._shadowLayer)
        #print(tile_x+self.Board()._camTile_x,tile_y+self.Board()._camTile_y)
        self.Board().ChangeCursor("images/blue_box.png", 0, 0)
        for actor in self.Characters():
            print(actor.tile_x,actor.tile_y)
            if dist(actor.tile_x, actor.tile_y, board_x, board_y) <=1:
                self._currentSprite.Attack(actor)#should change this to something else later
                print(self._currentSprite._Name, "attacked", actor._Name)
        self._canAttack=False
        self._mode=[]
    else:
        print("Target Tile is out of Range.")

    

    

