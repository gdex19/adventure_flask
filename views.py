from flask import Flask, render_template, request

from route_helper import simple_route

import random


app = Flask(__name__)


@simple_route('/')
def hello(world: dict) -> str:
    """
    The welcome screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
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
    if monster_decision == "Run away":
        return render_template('no_monster.html')
    elif monster_decision == "Find a Kyle to drink it for you":
        world['difficulty'] = 3
        return render_template('kyle.html')
    elif monster_decision == "Drink it":
        world['difficulty'] = 5
        return render_template('drink_monster.html')


@simple_route("/save/encounter/")
def save_fight(world: dict, monster_fight_decision: str) -> str:
    if monster_fight_decision == "Leave":
        return render_template('left_monster.html')
    elif monster_fight_decision == "Stay and fight!":
        print(world['difficulty'])
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3, health_status=100)


@simple_route("/save/ending/")
def finish_game(world: dict, number_choice):
    world['answers'].append(random.randint(1, world['difficulty']))
    result = win_lose(change_prompt(number_choice, world), number_choice, world)
    print(result)
    if result == 1:
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3-world['attempts'],
                               health_status=round(100-33.333*world['attempts']), is_int=world['correction'])
    if result == 2:
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3-world['attempts'],
                               health_status=round(100-33.333*world['attempts']),
                               is_int=world['correction'])
    if result == 3:
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3-world['attempts'],
                               health_status=round(100-33.333*world['attempts']),
                               is_int=world['correction'])
    if result == 4:
        return render_template('monster_result.html', monster_choice=world['result'],
                               forest_monster_choice=world['assistance'],
                               final_monster_fight="/static/monster_you_defeat.jpg")
    if result == 5:
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3-world['attempts'],
                               health_status=round(100-33.333*world['attempts']))
    if result == 6:
        return render_template('monster_result.html', monster_choice=world['result'],
                               forest_monster_choice=world['assistance'], final_monster_fight="/static/defeated.jpg")


def change_prompt(guess: str, values: dict):
    if not str.isdigit(guess.replace(".", "").replace("-", "").replace("^", "")):
        values['correction'] = "You must enter a number!"
        return 1
    elif float(guess) != int(float(guess)):
        values['correction'] = "Enter a whole number!"
        return 2
    elif int(float(guess)) not in range(1, values['difficulty'] + 1):
        values['correction'] = "Keep the number between 1 and {}!".format(values['difficulty'])
        return 3
    else:
        return 0


def win_lose(number: int, guess: str, values: dict):
    if number in [1, 2, 3]:
        return number
    elif int(float(guess)) == values['answers'][0]:
        values['result'] = "defeated"
        if values['difficulty'] == 3:
            values['assistance'] = "With Kyle on your side, the monster never stood a chance!"
        elif values['difficulty'] == 5:
            values['assistance'] = "The caffeine and sugar flowing through your veins led you to victory!"
        else:
            values['assistance'] = "Impressive. You conquered him all by yourself!"
        return 4
    elif values['attempts'] < 2:
        values['attempts'] += 1
        return 5
    elif values['attempts'] >= 2:
        values['result'] = "were slain by"
        if values['difficulty'] == 3:
            values['assistance'] = "How could you lose with Kyle on your side?"
        elif values['difficulty'] == 5:
            values['assistance'] = "Even full of sugar and caffeine, you could not prevail."
        else:
            values['assistance'] = "Without any help, you stood no chance against his peppers."
        return 6







