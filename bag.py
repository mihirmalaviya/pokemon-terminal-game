
from player import Player
from pokemon import Pokemon
from utils import *
from time import sleep
import random

def bag(player):
	player_items = []
	player_items_display = []
	for item, amount in player.items.items():
		if amount > 0:
			player_items.append(item)
			player_items_display.append(f"{amount}x {item.title()}")

	if player_items and input("use an item? (y/anything else) ").lower()=='y':
		print("\npick an item")
		player_item_choice = menu(player_items_display)

		if "ball" in player_items[player_item_choice]:
			print("you cant throw a ball unless you are in battle")
		elif "revive" in player_items[player_item_choice]:
			valid_pokemons = []
			valid_pokemons_display = []

			for i, pokemon in enumerate(player.pokemons):
				if pokemon.hp <= 0:
					valid_pokemons.append(pokemon)
					valid_pokemons_display.append(f"{pokemon.info_string()} ")

			if len(valid_pokemons) > 0:

				revive_percent = {
				 "revive": .5,
				 "max revive": 1,
				 "party revive": 2,
				}[player_items[player_item_choice]]

				if revive_percent < 2:
					print("\npick a pokemon to heal: ")

					recipient = valid_pokemons[menu(valid_pokemons_display)]
					recipient.heal(recipient.max_hp * revive_percent)
				else:
					for pokemon in player.pokemons:
						pokemon.hp = pokemon.max_hp
				print("revived successfully")

				add_to_dict(player.items, player_items[player_item_choice], -1)
				return 1

		elif "potion" in player_items[player_item_choice]:
			valid_pokemons = []
			valid_pokemons_display = []

			for i, pokemon in enumerate(player.pokemons):
				if pokemon.hp > 0 and pokemon.hp < pokemon.max_hp:
					valid_pokemons.append(pokemon)
					valid_pokemons_display.append(f"{pokemon.info_string()} ")

			if len(valid_pokemons) > 0:
				print("\npick a pokemon to heal: ")

				heal_amount = {
				 "potion": 25,
				 "super potion": 50,
				 "hyper potion": 150
				}[player_items[player_item_choice]]

				valid_pokemons[menu(valid_pokemons_display)].heal(heal_amount)
				print("healed successfully")

				add_to_dict(player.items, player_items[player_item_choice], -1)
				return 1

		elif "book" in player_items[player_item_choice]:
			pokemons_display, pokemons = [], []
			if player.pokemons:
				for pokemon in player.pokemons:
					if pokemon.hp>0:
						pokemons.append(pokemon)
						pokemons_display.append(f"{pokemon.info_string()} ")

			if not pokemons:
				print('all ur pokemon are dead lol')
				return
			print("use on: ")
			victim = pokemons[menu(pokemons_display)]
			# print(victim)

			if input("are you sure you want to use `book` (y/anything else)  ").lower() == 'y':
				add_to_dict(player.items, player_items[player_item_choice], -1)
				try:
					vel = float(input("pick a velocity (a float 1 to 10)"))
					if vel>1 and vel<10:
						pass
					else:
						print("i guess you cant follow directions... 10 it is")
						vel = float(10)
				except:
					print("i guess you cant follow directions... 10 it is")
					vel = float(10)

				if vel > 6.4:
					print("you throw the book at the pokemon and it dies from internal bleeding")
					sleep(1)
				else:
					# print(victim)
					gain = int(victim.exp * (random.random()+random.random()+.2))
					print(f"the book hits the pokemon at a perfect velocity and then the pokemon reads it and geains alot of life experience, giving it {gain} exp")
					victim.give_exp(gain)

		else:
			print("you cant use that")
