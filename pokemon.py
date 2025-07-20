from colorama import init, Fore, Back, Style
import random
from utils import progress_bar, align_text, remove_empty_lines, menu
from pokemon_info import *
from pokemon_utils import *
from time import sleep


class Pokemon:
    def __init__(
        self,
        name,
        base_hp,
        moves,
        types,
        evolution_chain=[],
        learned_moves=[],
        catch_rate=50,
        level=0,
        npc=False,
    ):
        # self.root_name = name
        self.name = name
        self.types = types
        self.base_hp = base_hp
        self.max_hp = base_hp
        self.hp = base_hp
        self.exp = (self.hp * 2) * (level**1.5)
        self.level = level
        self.moves = moves
        self.is_npc_pokemon = npc

        if len(moves) > 4:
            self.moves = []
            for i in range(4):
                self.moves.append(moves[i])

        self.learned_moves = learned_moves
        self.catch_rate = catch_rate
        self.evolution_chain = evolution_chain

        self.gender = random.randint(0, 1)

        self.base_attack = 1 + (random.random() - 0.5) / 4
        self.base_defense = 2 + (random.random() - 0.5) / 4

        self.attack = self.base_attack
        self.defense = self.base_defense

        self.forgotten_moves = []

    def buff(self, factor):
        self.base_defense += 0.7 * factor
        self.base_attack += 0.1 * factor
        self.attack = self.base_attack
        self.defense = self.base_defense

    def give_exp(self, amount, silent=False):
        self.exp += amount
        self.update_stats(silent=silent)

    def heal(self, amount):
        if self.hp < 0:
            self.hp = 0
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def auto_evolve(self):
        for name, level, evolution in self.evolution_chain:
            if name and level and evolution:
                if evolution in POKEMON_NAMES:
                    if self.name == name:
                        if self.level >= level:
                            self.name = evolution
                            self.learned_moves = POKEMON_INFO[self.name][
                                "learned_moves"
                            ]

    def auto_learn(self):
        if self.learned_moves:
            i = 0
            learned_moves = self.learned_moves
            for move, level in learned_moves:
                if not (move in self.forgotten_moves or move in self.moves):
                    if self.level >= level:
                        self.forgotten_moves.append(self.learned_moves.pop(i))
                        if len(self.moves) < 4:
                            self.moves.append(move)
                        else:
                            # print("which move will u get rid of?")
                            self.moves[random.randint(0, 3)] = move
                i += 1

    def evolve(self):
        current_exp = self.exp

        for name, level, evolution in self.evolution_chain:
            if name and level and evolution:
                if evolution in POKEMON_NAMES:
                    if name == self.name:
                        next_level_exp = (self.base_hp * 2) * ((level) ** 1.5)
                        self.give_exp(next_level_exp - current_exp)
                        self.auto_learn()
                        self.auto_evolve()
                        self.auto_learn()

    def update_stats(self, silent=False):
        new_level = int((self.exp / (self.base_hp * 2)) ** (2 / 3))

        if new_level > self.level:
            self.level = new_level
            self.max_hp = self.base_hp * (1 + (self.level / 10))
            self.hp = self.max_hp

            if not silent:
                print(
                    f"{self.name.upper()} leveled up to {Fore.LIGHTBLUE_EX}LVL {self.level}{Fore.RESET}! It has been healed, and its stats have been upgraded."
                )
                sleep(2)

                if self.learned_moves:
                    # print(self.learned_moves)
                    i = 0
                    learned_moves = self.learned_moves
                    for move, level in learned_moves:
                        if not (move in self.forgotten_moves or move in self.moves):
                            if self.level >= level:
                                self.forgotten_moves.append(self.learned_moves.pop(i))
                                permission = input(
                                    f"\n{self.name.upper()} wants to learn {move.capitalize()}, will you let it?\n{display_move(move)}\n(y/anything else)  "
                                )
                                if permission.lower() == "y":
                                    if len(self.moves) < 4:
                                        self.moves.append(move)
                                    else:
                                        print("which move will u get rid of?")
                                        moves_displays = []

                                        for move in self.moves:
                                            moves_displays.append(display_move(move))

                                        self.moves[menu(moves_displays)] = move
                        i += 1

                for name, level, evolution in self.evolution_chain:
                    if name and level and evolution:
                        if evolution in POKEMON_NAMES:
                            if self.name == name:
                                if self.level >= level:
                                    permission = input(
                                        f"congrats! {self.name.upper()} wants to evolve to {evolution.upper()}, will you let it? (y/anything else) "
                                    )
                                    if permission.lower() == "y":
                                        evolve_animation(self.name, evolution)
                                        print(
                                            f"{self.name.upper()} evolved into {evolution.upper()}!!!"
                                        )
                                        self.name = evolution
                                        self.learned_moves = POKEMON_INFO[self.name][
                                            "learned_moves"
                                        ]
                                        self.update_stats(silent=silent)
            else:
                self.auto_learn()
                # self.auto_learn()

    def display_info(self):
        self.display_name()
        self.display_hp()
        self.display_exp()

    def display_name(self):
        print(f"LVL {self.level + 1} {self.name.upper()}", end=Fore.RESET + " \x1b[3m")
        for i, type in enumerate(self.types):
            print(type_colors[type] + self.types[i], end=Fore.RESET + " ")
        print(Style.RESET_ALL)

    def display_hp(self):
        progress = progress_bar(16, self.hp, self.max_hp, color=Fore.RED)
        print(f"HP {int(self.hp)}/{int(self.max_hp)} [{progress}]{Style.RESET_ALL}")

    def display_exp(self):
        exp_progress = progress_bar(
            16,
            self.exp - ((self.base_hp * 2) * (self.level**1.5)),
            (self.base_hp * 2) * ((self.level + 1) ** 1.5),
            color=Fore.LIGHTBLUE_EX,
        )
        print(
            f"EXP {int(self.exp - ((self.base_hp * 2) * ((self.level) ** 1.5)))}/{int((self.base_hp * 2) * ((self.level + 1) ** 1.5))} [{exp_progress}]{Style.RESET_ALL}"
        )

    def info_string(self):
        info = self.name_string() + " "
        info += self.hp_string() + " "
        info += self.exp_string() + " "
        return info

    def name_string(self):
        name_info = f"LVL {self.level + 1} {self.name.upper()} \x1b[3m"
        for i, type in enumerate(self.types):
            name_info += type_colors[type] + self.types[i] + " "
        name_info += Style.RESET_ALL
        return name_info

    def hp_string(self):
        return f"HP {int(self.hp)}/{int(self.max_hp)} [{progress_bar(16, self.hp, self.max_hp, color=Fore.RED)}]{Style.RESET_ALL}"

    def exp_string(self):
        exp_progress = progress_bar(
            16,
            self.exp - ((self.base_hp * 2) * (self.level**1.5)),
            (self.base_hp * 2) * ((self.level + 1) ** 1.5),
            color=Fore.LIGHTBLUE_EX,
        )
        return f"EXP {int(self.exp - ((self.base_hp * 2) * ((self.level) ** 1.5)))}/{int((self.base_hp * 2) * ((self.level + 1) ** 1.5))} [{exp_progress}]{Style.RESET_ALL}"
