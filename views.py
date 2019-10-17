from flask import Flask, render_template, request

from route_helper import simple_route

app = Flask(__name__)

GAME_HEADER = """
<h1>Welcome to adventure quest!</h1>
<p>At any time you can <a href='/reset/'>reset</a> your game.</p>
"""


@simple_route('/')
def hello(world: dict) -> str:
    """
    The welcome screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
    return render_template('welcome.html')

'''
ENCOUNTER_MONSTER_LAIR = """
<!-- Curly braces let us inject values into the string -->
You are in {}. You found a monster!<br>

<!-- Image taken from site that generates random Corgi pictures-->
<img src="http://placecorgi.com/260/180" /><br>
    
What is its name?

<!-- Form allows you to have more text entry -->    
<form action="/save/name/">
    <input type="text" name="player"><br>
    <input type="submit" value="Submit"><br>
</form>
"""
ENCOUNTER_MONSTER_FOREST = """
You are in the forest now. You found a Monster!<br>

<img src="/static/Forest.jpg" width="400" height="200"/><br>

What would you like to do with it?

<!-- Form allows you to have more text entry -->    
<form action="/save/action/">
    <select name="action">
        <option value="drink">Drink it</option>
        <option value="run">Run away</option>
        <option value="kyle">Find a Kyle to drink it for you</option>        
    <input type="submit" value="Submit"><br>
</form>

"""
'''
@simple_route('/goto')
def open_doo(world: dict, where: str) -> str:
    """
    Update the player location and encounter a monster, prompting the player
    to give them a name.

    :param world: The current world
    :param where: The new location to move to
    :return: The HTML to show the player
    """
    values = request.values


@simple_route('/goto/<where>/')
def open_door(world: dict, where: str) -> str:
    """
    Update the player location and encounter a monster, prompting the player
    to give them a name.

    :param world: The current world
    :param where: The new location to move to
    :return: The HTML to show the player
    """
    world['location'] = where
    if where == "forest":
        return render_template('forest.html')
    elif where == "lair":
        return render_template('lair.html')


@simple_route("/save/result/")
def save_name(world: dict, monster_decision: str) -> str:
    """
    Update the name of the monster.

    :param monster_decision:
    :param world: The current world
    :return:
    """
    world['action'] = monster_decision
    if world['action'] == "Run away":
        return render_template('no_monster.html')


@simple_route("/save/encounter/")
def save_fight(world: dict, monster_fight_decision: str) -> str:
    world['fight_status'] = monster_fight_decision
    if world['fight_status'] == "Leave":
        return render_template('left_monster.html')

