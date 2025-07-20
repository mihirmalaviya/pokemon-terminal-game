from pokemon_info import POKEMON_INFO
import random
import copy
from pokemon import Pokemon
from player import Player
from time import sleep
from utils import *
from startup import *

grass_spawn_rates_progression = []
grass_spawn_rates = {}  # hardcoded rates
for name, info in POKEMON_INFO.items():
    if info["catch_rate"] >= 200:
        grass_spawn_rates[name] = int(
            1000 / (info["catch_rate"] * 2 + info["base_health"])
        )
grass_spawn_rates_progression.append(grass_spawn_rates)

grass_spawn_rates = {}
for name, info in POKEMON_INFO.items():
    if info["catch_rate"] >= 160:
        grass_spawn_rates[name] = int(
            1000 / (info["catch_rate"] * 2 + info["base_health"])
        )
grass_spawn_rates_progression.append(grass_spawn_rates)

grass_spawn_rates = {}
for name, info in POKEMON_INFO.items():
    if info["catch_rate"] >= 100 and info["catch_rate"] <= 200:
        grass_spawn_rates[name] = int(
            1000 / (info["catch_rate"] * 2 + info["base_health"])
        )
grass_spawn_rates_progression.append(grass_spawn_rates)

grass_spawn_rates = {}
for name, info in POKEMON_INFO.items():
    if info["catch_rate"] >= 70 and info["catch_rate"] <= 135:
        grass_spawn_rates[name] = int(
            1000 / (info["catch_rate"] * 2 + info["base_health"])
        )
grass_spawn_rates_progression.append(grass_spawn_rates)

grass_spawn_rates = {}
for name, info in POKEMON_INFO.items():
    if info["catch_rate"] >= 20 and info["catch_rate"] <= 100:
        grass_spawn_rates[name] = int(
            1000 / (info["catch_rate"] * 2 + info["base_health"])
        )
grass_spawn_rates_progression.append(grass_spawn_rates)

grass_spawn_rates = {}
for name, info in POKEMON_INFO.items():
    if info["catch_rate"] >= 1 and info["catch_rate"] <= 40:
        grass_spawn_rates[name] = int(
            1000 / (info["catch_rate"] * 2 + info["base_health"])
        )
grass_spawn_rates_progression.append(grass_spawn_rates)


def grass(grass_spawn_rates, player):
    total_spawn_rate = sum(grass_spawn_rates.values())
    rand_num = random.randint(
        1, total_spawn_rate * 6
    )  # 1 in 6 chance of getting a pokemon

    cumulative_spawn_rate = 0
    for pokemon, rate in grass_spawn_rates.items():
        cumulative_spawn_rate += rate
        if rand_num <= cumulative_spawn_rate:
            pokemon = copy.deepcopy(base_pokemons[pokemon])

            exp_amount = abs(player.exp_sum() / len(player.pokemons) - 20)

            if exp_amount > player.exp_difficulty_cap:
                exp_amount = player.exp_difficulty_cap + random.randint(-300, 800)

            pokemon.give_exp(exp_amount, silent=True)
            pokemon.auto_evolve()
            pokemon.auto_learn()
            print(center(f"a wild {pokemon.name.upper()} appeared!"))
            sleep(0.5)
            return pokemon

    # print("no pokemon in grass")
    return None
