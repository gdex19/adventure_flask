from flask import Flask, render_template, request

from route_helper import simple_route

import random


app = Flask(__name__)


@simple_route('/')
def hello(world: dict) -> str:
    """
    The start screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
    return render_template('welcome.html')


@simple_route('/goto/<where>/')
def open_door(world: dict, where: str) -> str:
    """
    Update the player location and prompt them with a decision.

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
    Receives decision about Monster, changes difficulty and loads appropriate page.

    :param monster_decision: the choice that the player makes with Monster.
    :param world: The current world
    :return: html page as result of decision
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
    """
    Loads appropriate page with variables on the if necessary.

    :param monster_fight_decision: the choice that the player against blue monster.
    :param world: The current world
    :return: html page as result of decision with variables.
    """
    if monster_fight_decision == "Leave":
        return render_template('left_monster.html')
    elif monster_fight_decision == "Stay and fight!":
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3, health_status=100)


def change_prompt(number_choice: str, world: dict):
    """
        Puts a correction in the input box if type is wrong

        :param number_choice: player's input in box
        :param world: The current world
        :return: a number relating to an html page on finish_game
        """
    if not str.isdigit(number_choice.replace(".", "").replace("-", "").replace("^", "")):
        world['correction'] = "You must enter a number!"
        return 1
    elif float(number_choice) != int(float(number_choice)):
        world['correction'] = "Enter a whole number!"
        return 2
    elif int(float(number_choice)) not in range(1, world['difficulty'] + 1):
        world['correction'] = "Keep the number between 1 and {}!".format(world['difficulty'])
        return 3
    else:
        return 0


def win_lose(number: int, number_choice: str, world: dict):
    """
        Changes strings on final page with respect to difficulty and determines win and loss.

        :param number: the number returned by change_prompt
        :param number_choice: player's input in box
        :param world: The current world
        :return: a number relating to the appropriate html page to load.
        """
    if number in [1, 2, 3]:
        return number
    elif int(float(number_choice)) == world['answers'][0]:
        world['result'] = "defeated"
        if world['difficulty'] == 3:
            world['assistance'] = "With Kyle on your side, the monster never stood a chance!"
        elif world['difficulty'] == 5:
            world['assistance'] = "The caffeine and sugar flowing through your veins led you to victory!"
        else:
            world['assistance'] = "Impressive. You conquered him all by yourself!"
        return 4
    elif world['attempts'] < 2:
        world['attempts'] += 1
        return 5
    elif world['attempts'] >= 2:
        world['result'] = "were slain by"
        if world['difficulty'] == 3:
            world['assistance'] = "How could you lose with Kyle on your side?"
        elif world['difficulty'] == 5:
            world['assistance'] = "Even full of sugar and caffeine, you could not prevail."
        else:
            world['assistance'] = "Without any help, you stood no chance against his peppers."
        return 6


@simple_route("/save/ending/")
def finish_game(world: dict, number_choice):
    """
    Finishes game with a final page (or guessing page) with variables from world and sets "answer" to guessing game.

    :param number_choice: player's input in box
    :param world: The current world
    :return: html page as result of number returned by win_lose
    """
    world['answers'].append(random.randint(1, world['difficulty']))
    result = win_lose(change_prompt(number_choice, world), number_choice, world)
    if result == 1:
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3-world['attempts'],
                               health_status=round(100-33.333*world['attempts']), is_int=world['correction'])
    elif result == 2:
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3-world['attempts'],
                               health_status=round(100-33.333*world['attempts']),
                               is_int=world['correction'])
    elif result == 3:
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3-world['attempts'],
                               health_status=round(100-33.333*world['attempts']),
                               is_int=world['correction'])
    elif result == 4:
        return render_template('monster_result.html', monster_choice=world['result'],
                               forest_monster_choice=world['assistance'],
                               final_monster_fight="/static/monster_you_defeat.jpg")
    elif result == 5:
        return render_template('monster_fight.html', difficulty=world['difficulty'], attempts_left=3-world['attempts'],
                               health_status=round(100-33.333*world['attempts']))
    elif result == 6:
        return render_template('monster_result.html', monster_choice=world['result'],
                               forest_monster_choice=world['assistance'], final_monster_fight="/static/defeated.jpg")