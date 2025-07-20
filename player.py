

class Player:

	def __init__(self, name, pokemons=[], items={}, money=0, exp_difficulty_cap=5000):

		self.exp_difficulty_cap = exp_difficulty_cap

		self.name = name
		self.pokemons = pokemons
		self.items = items
		self.money = money

	def give_pokemon_exp(self, amount, silent=False):
		for pokemon in self.pokemons:
			pokemon.give_exp(amount, silent=silent)

	def exp_sum(self):
		total = 0
		for pokemon in self.pokemons:
			total += pokemon.exp
		return int(total)

	def display_info(self):
		print(f"{self.name} Ƀ{self.money:.2f}")
		self.display_items()
		self.display_pokemon()

	def display_items(self):
		print(f"{self.name}'s pouch: ")
		if self.items:
			for item, amount in self.items.items():
				if amount > 0:
					print(f"\t {amount}x {item.title()}")
		else:
			print("empty")

	def display_pokemon(self):
		if self.pokemons:
			print(f"{self.name}'s pokemon: ")
			for pokemon in self.pokemons:
				pokemon.display_info()
		else:
			print("empty")

	def get_alive_pokemon(self):
		alive_pokemon = 0
		for pokemon in self.pokemons:
			if pokemon.hp > 0:
				alive_pokemon += 1
		return alive_pokemon

	def switch_pokemon(self, pokemon):
		temp = self.pokemons[0]


		for i in range(len(self.pokemons)):
			if self.pokemons[i] is pokemon:
				self.pokemons[i] = temp

		self.pokemons[0] = pokemon
