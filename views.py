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


@app.route("/result", methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)


@simple_route("/save/name/")
def save_name(world: dict, monsters_name: str) -> str:
    """
    Update the name of the monster.

    :param world: The current world
    :param monsters_name:
    :return:
    """
    world['name'] = monsters_name

    return GAME_HEADER+"""You are in {where}, and you are nearby {monster_name}
    <br><br>
    <a href='/'>Return to the start</a>
    """.format(where=world['location'], monster_name=world['name'], monster_action_one=world['action'])


if __name__ == '__main__':
    app.run(debug=True)
