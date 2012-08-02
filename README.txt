=========================
Defeat of the Ancient One
=========================

Defeat of the Ancient One is our attempt at a tactical RPG as an entry to the 2012 Liberated Pixel Cup <http://lpc.opengameart.org/>.  As you can plainly see only part of the map is populated with enemies.

Github Repository
-----------------
https://github.com/BenLiyanage/AncientOne

Controls
--------
W - Camera pan up
A - Camera pan left
S - Camera pan down
D - Camera pan right

X - Enter move mode (when appropriate)
C - End turn (when appropriate)
V - Cancel action (when appropriate)
"+" - background volume up
"-" - background volume down

Up/Down arrows - scroll through and highlight actions.
Enter - select highlighted action.
Escape - pause/ unpause the game.



Building and running
--------------------
This game was programming with python, which will be necessary to build the game.

A copy of the tiledtmxloader module has been included, along with the appropriate licensing information.  This was used to load in the .tmx map.

the module pygame is also required to run the game.  Installation information can be found at <http://www.pygame.org/news.html>

Through the console or terminal, first navigate to the AncientOne folder, then enter:
 > Python -O AncientOne.py

That's it!

Other Game Notes:
-----------------
Defeat the portals quickly, for the longer you wait, the stronger they and the enemies who cross over become!!

Attacks:
Archie:
	Ranged: A ranged attack with a minimum range of 3 tiles and a maximum of 7.
	Cripple: A ranged attack that deals less damage, but delays the turn of the target.  The effect increase with each level.  Again the Cripple attack has a minimum range of 3 and maximum of 7.

Buster:
	Attack:  A slash attack against an adjacent target.
	Whirlwind:  A wild attack against all target within two tiles.  This does less damage than the standard attack.

Terra:
	Heal: heal all allies under within one tile of the target tile.
	Fire Lion: Terra conjures a fiery lion that damages all targets within one tile of the target tile.  Friendly fire is possible.

Attack