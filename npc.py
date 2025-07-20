from utils import printd, inputd


class NPC:
    def __init__(
        self, name, pokemons, money=100, dialogue={}, exp_difficulty_cap_add=10000
    ):
        self.exp_difficulty_cap_add = exp_difficulty_cap_add
        self.name = name
        self.pokemons = pokemons
        self.money = money
        self.dialogue = dialogue
        self.beat = False

    def say(self, text):
        print(self.name.upper() + ":", end="  ")
        printd(text)

    def ask(self, text):
        print(self.name.upper() + ":", end="  ")
        return inputd(text)

    def give_pokemon_exp(self, amount):
        for pokemon in self.pokemons:
            pokemon.give_exp(amount, silent=True)

    def exp_sum(self):
        total = 0
        for pokemon in self.pokemons:
            total += pokemon.exp
        return int(total)

    def display_info(self):
        print(f"{self.name.title()} {self.money:.2f}Ƀ")
        self.display_pokemon()

    def display_pokemon(self):
        if self.pokemons:
            print(f"{self.name.title()}'s pokemon: ")
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

    def heal_all_pokemon(self):
        for pokemon in self.pokemons:
            pokemon.hp = pokemon.max_hp
