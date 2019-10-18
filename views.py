from flask import Flask, render_template, request

from route_helper import simple_route

import random


app = Flask(__name__)

difficulty = 10

attempts = 0

answers = []

loss = False

@simple_route('/')
def hello(world: dict) -> str:
    """
    The welcome screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
    global difficulty
    global attempts
    global answers
    global loss
    difficulty = 10
    attempts = 0
    answers = []
    loss = False
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
    global attempts
    if monster_fight_decision == "Leave":
        return render_template('left_monster.html')
    elif monster_fight_decision == "Stay and fight!":
        return render_template('monster_fight.html', difficulty=difficulty, attempts_left=3, health_status=100)


@simple_route("/save/ending/")
def finish_game(world: dict, number_choice):
    global attempts
    global answers
    answers.append(random.randint(1, difficulty))
    if number_choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        return render_template('monster_fight.html', difficulty=difficulty, attempts_left=3-attempts,
                               health_status=(100-33.333*attempts), is_int="You must enter a number!")
    elif int(number_choice) == answers[0]:
        assistance = "Impressive. You conquered him all by yourself!"
        if difficulty == 3:
            assistance = "With Kyle on your side, the monster never stood a chance!"
        elif difficulty == 5:
            assistance = "The caffeine and sugar flowing through your veins led you to victory!"
        return render_template('monster_result.html', monster_choice="defeated", forest_monster_choice=assistance,
                               final_monster_fight="/static/monster_you_defeat.jpg")
    elif attempts < 2:
        attempts += 1
        print(answers[0])
        return render_template('monster_fight.html', difficulty=difficulty, attempts_left=3-attempts,
                               health_status=(100-33.333*attempts))
    elif attempts >= 2:
        assistance = "Without any help, you stood no chance against his peppers."
        if difficulty == 3:
            assistance = "How could you lose with Kyle on your side?"
        elif difficulty == 5:
            assistance = "Even full of sugar and caffeine, you could not prevail."
        return render_template('monster_result.html', monster_choice="were slain by", forest_monster_choice=assistance,
                               final_monster_fight="/static/defeated.jpg")






