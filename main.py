import colorama
from colorama import Fore, Style
from time import sleep
import random
import copy
import os
import platform

import termios
import fcntl

colorama.init()

from globals import *
from startup import *

from pokemon_info import *

from utils import *
from pokemon_utils import *

from pokemon import Pokemon
from player import Player
from npc import NPC

from pokemart import *
from grass import grass_spawn_rates_progression
from map import *
from battle import *

from bag import bag


# OCK.say("sup im dr ock")
player = Player(
    npcs["dr ock"].ask("whats ur name? "),
    money=5000,
    items={
        "pokeball": 20,
        "revive": 1,
        "potion": 5,
        # "master ball": 200,
        # "book": 5
    },
)
if godmode:
    player.money += 1000000000

npcs["dr ock"].say("cool my names dr ock")
npcs["dr ock"].ask("aight i got like 3 pokemon do you want one  ")
npcs["dr ock"].say("ok cool pick one")

starters = ""
for starter in ["bulbasaur", "charmander", "squirtle"]:
    starters += remove_empty_lines(get_pokemon_sprite(starter)) + "\n\n"

print(align_text(starters))

starter = copy.deepcopy(
    base_pokemons[
        ["bulbasaur", "charmander", "squirtle"][
            menu(["bulbasaur", "charmander", "squirtle"])
        ]
    ]
)

if godmode:
    starter.buff(100)
else:
    starter.buff(0.4)

player.pokemons.append(starter)
player.give_pokemon_exp(1000, silent=True)
player.pokemons[0].auto_learn()


npcs["dr ock"].say("alright, i also gave you some other items\n")
sleep(TURNDELAY)
# clear()
player.display_items()
sleep(TURNDELAY * 3)

battle_npc(player, npcs["dr ock"])


# while 1:
# 	actions = ["grass", "battle npc", "pokemart", "bag", "pokemons"]
# 	action = menu(actions)
# 	if action == 0:
# 		battle_wild(player, grass(grass_spawn_rates_progression[0]))
# 	elif action == 1:
# 		battle_npc(player, npcs[npc_names[menu(npc_names)]])
# 	elif action == 2:
# 		pokemart(player)
# 	elif action == 3:
# 		bag(player)
# 	elif action == 4:
# 		player.display_pokemon()

while 1:
    print("ok")
    event = map()
    if event == "w":
        battle_wild(
            player, grass(grass_spawn_rates_progression[grass_progression], player)
        )
    elif event in "ecaot":
        if event == "e":
            fight = npcs["gabe"]
        elif event == "c":
            fight = npcs["fly guy"]
        elif event == "a":
            fight = npcs["tyrone"]
        elif event == "o":
            fight = npcs["bob"]
        elif event == "t":
            fight = npcs["Keymer"]
        battle_npc(player, fight)
    elif event == "M":
        pokemart(player)
    elif event == "B":
        bag(player)
    elif event == "P":
        player.display_pokemon()
        input("exit? (anything)  ")
