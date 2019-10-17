from flask import Flask, render_template, request

from route_helper import simple_route

import random
app = Flask(__name__)

difficulty = 10


@simple_route('/')
def hello(world: dict) -> str:
    """
    The welcome screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
    global difficulty
    difficulty = 10
    return render_template('welcome.html')


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
    global difficulty
    if monster_decision == "Run away":
        return render_template('no_monster.html')
    elif monster_decision == "Find a Kyle to drink it for you":
        difficulty = 3
        return render_template('kyle.html')
    elif monster_decision == "Drink it":
        difficulty = 5
        return render_template('drink_monster.html')


@simple_route("/save/encounter/")
def save_fight(world: dict, monster_fight_decision: str) -> str:
    if monster_fight_decision == "Leave":
        return render_template('left_monster.html')
    elif monster_fight_decision == "Stay and fight!":
        return render_template('monster_fight.html', difficulty=difficulty)

@simple_route("/save/ending/")



