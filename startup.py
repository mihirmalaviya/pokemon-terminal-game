
import copy
from pokemon import Pokemon
from npc import NPC
from player import Player
from pokemon_info import POKEMON_INFO

npcs_info = {
 "dr ock": {
  "pokemon": ["pikachu"],
  "money": 1000,
  "exp": 900,
  "progress": 7000
 },
 "gabe": {
  "pokemon": ["mankey", "diglett"],
  "money": 2000,
  "exp": 5000,
  "progress": 22000
 },
 "fly guy": {
  "pokemon": sorted(["butterfree", "zubat", "pidgeotto"]), # sort here, this is important because i was too lazy to move zubat but the sort does it for me
  "money": 7500,
  "exp": 17000,
  "progress": 40000
 },
 "tyrone": {
  "pokemon": ["beedrill", "ekans", "arbok"],
  "money": 9000,
  "exp": 30000,
  "progress": 60000
 },
 "bob": {
  "pokemon": ["gyarados", "kabutops", "onix"],
  "money": 50000,
  "exp": 50000,
  "progress": 110000
 },
 "Keymer": {
  "pokemon": ["articuno", "zapdos", "moltres", "mew", "mewtwo"],
  "money": 70000,
  "exp": 80000,
  "progress": 99999999
 }
}

base_pokemons = {}

for name, info in POKEMON_INFO.items():
	base_pokemons[name] = Pokemon(name,
	                              info['base_health'],
	                              info['starting_moves'],
	                              info['types'],
	                              learned_moves=info['learned_moves'],
	                              evolution_chain=info['evolution_chain'],
	                              catch_rate=info["catch_rate"])



grass_progression = 0

npcs = {}

for name, info in npcs_info.items():
	copied_pokemon = []
	for pokemon in info["pokemon"]:
		p = copy.deepcopy(base_pokemons[pokemon])
		p.is_npc_pokemon=True
		copied_pokemon.append(p)

	n = NPC(name, copied_pokemon, money=info["money"])
	n.give_pokemon_exp(info['exp'])
	n.exp_difficulty_cap_add = info['progress']
	# for pokemon in n.pokemons:
	npcs[name] = n

npc_names = []
for name, _ in npcs.items():
	npc_names.append(name)
