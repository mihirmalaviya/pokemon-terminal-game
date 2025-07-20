from pokemon_info import *
import random
from time import sleep
from utils import *
from pokemon_utils import *
from pokemon import Pokemon
from player import Player
from npc import NPC
from grass import *

from globals import *


def calculate_damage(move, attacker, defender):  # damage calc
    move_damage = MOVES_INFO[move]["power"]
    move_accuracy = MOVES_INFO[move]["accuracy"]
    if move_accuracy:
        if random.randint(1, 100) >= move_accuracy:
            print("move missed")
            return 0

    if MOVES_INFO[move]["buffs"]["defense"]:
        attacker.defense += MOVES_INFO[move]["buffs"]["defense"] * 0.1

    if MOVES_INFO[move]["buffs"]["attack"]:
        attacker.attack += MOVES_INFO[move]["buffs"]["attack"] * 0.1

    effectiveness = calculate_effectiveness(MOVES_INFO[move]["type"], defender.types)

    if effectiveness > 2:  # type effectiveness
        print(f"it was {Fore.GREEN}super effective{Style.RESET_ALL}")
    if effectiveness > 1:
        print(f"it was {Fore.LIGHTGREEN_EX}effective{Style.RESET_ALL}")
    if effectiveness == 0:
        print(f"it was{Fore.RED} useless lol{Style.RESET_ALL}")
    if effectiveness < 1:
        print(f"it was {Fore.LIGHTRED_EX}ineffective{Style.RESET_ALL}")

    if move_damage:
        damage = (attacker.attack / defender.defense) * move_damage * effectiveness
        critical = 1

        if random.randint(1, 8) == 1:
            critical = 1.8
            print(f"its a {Fore.YELLOW}critical{Fore.RESET} hit!")

        return damage * critical
    return 0


def perform_move(move, attacker, defender):
    print(
        f"\n{attacker.name.upper()} used {type_colors[MOVES_INFO[move]['type']] + move.upper() + Fore.RESET}!"
    )
    damage = calculate_damage(move, attacker, defender)
    defender.hp -= damage

    if damage:
        print(
            f"{defender.name.upper()} took {Fore.LIGHTRED_EX}{(damage):.2f}{Fore.RESET} damage."
        )


def player_turn(player_pokemon, npc_pokemon, player):
    sleep(TURNDELAY)
    clear()
    print(f"\n{player.name.upper()}, it's your turn.")
    print(
        f"\n{align_text(remove_empty_lines(get_pokemon_sprite(npc_pokemon.name)), push=17)}\n"
    )
    npc_pokemon.display_info()
    print(
        f"\n{align_text(remove_empty_lines(get_pokemon_sprite(player_pokemon.name, back=True)))}\n"
    )
    player_pokemon.display_info()

    battling = True
    while battling:
        print("\npick an action")
        action = menu(["MOVE", "ITEM", "SWITCH", "RUN", "SKIP"])

        if action == 0:  # move
            print("\npick a move:")
            display_moves = []

            for move in player_pokemon.moves:
                display_moves.append(display_move(move))
            # print(display_moves)

            move_index = menu(display_moves)
            selected_move = player_pokemon.moves[move_index]
            perform_move(selected_move, player_pokemon, npc_pokemon)
            break
        if action == 1:  # items
            player_items = []
            player_items_display = []
            for item, amount in player.items.items():
                if amount > 0:
                    player_items.append(item)
                    player_items_display.append(f"{amount}x {item.title()}")

            if player_items:
                print("\npick an item")
                player_item_choice = menu(player_items_display)

                if "ball" in player_items[player_item_choice]:
                    add_to_dict(player.items, player_items[player_item_choice], -1)
                    caught = catch_pokemon(
                        player, npc_pokemon, player_items[player_item_choice]
                    )

                    if caught == -1:
                        add_to_dict(player.items, player_items[player_item_choice], 1)
                        return 1

                    if caught:
                        return 0
                    return 1
                elif "revive" in player_items[player_item_choice]:
                    add_to_dict(player.items, player_items[player_item_choice], -1)
                    valid_pokemons = []
                    valid_pokemons_display = []

                    for i, pokemon in enumerate(player.pokemons):
                        # if i == 0: pass
                        if pokemon.hp <= 0:
                            valid_pokemons.append(pokemon)
                            valid_pokemons_display.append(f"{pokemon.info_string()} ")

                    if len(valid_pokemons) > 0:
                        revive_percent = {
                            "revive": 0.5,
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
                        return 1

                elif "potion" in player_items[player_item_choice]:
                    add_to_dict(player.items, player_items[player_item_choice], -1)
                    valid_pokemons = []
                    valid_pokemons_display = []

                    for i, pokemon in enumerate(player.pokemons):
                        # if i == 0: pass
                        if pokemon.hp > 0 and pokemon.hp < pokemon.max_hp:
                            valid_pokemons.append(pokemon)
                            valid_pokemons_display.append(f"{pokemon.info_string()} ")

                    if len(valid_pokemons) > 0:
                        print("\npick a pokemon to heal: ")

                        heal_amount = {
                            "potion": 25,
                            "super potion": 50,
                            "hyper potion": 150,
                        }[player_items[player_item_choice]]

                        valid_pokemons[menu(valid_pokemons_display)].heal(heal_amount)
                        print("healed successfully")
                        return 1

        if action == 2:
            if player.get_alive_pokemon() > 1:
                valid_pokemons = []
                valid_pokemons_display = []

                for i, pokemon in enumerate(player.pokemons):
                    if i == 0:
                        pass
                    if pokemon.hp > 0:
                        valid_pokemons.append(pokemon)
                        valid_pokemons_display.append(f"{pokemon.info_string()} ")

                if len(valid_pokemons) > 1:
                    print("\npick a pokemon to switch to: ")

                    player.switch_pokemon(valid_pokemons[menu(valid_pokemons_display)])
                    return 1
                else:
                    print("all your other pokemon are dead lol")

            else:
                print("you only have one pokemon")
        if action == 3:
            print("you cant run >:-)")
            return 1
        if action == 4:
            return 1
    return 1


def npc_turn(player_pokemon, npc_pokemon):
    print(f"\n{npc_pokemon.name.upper()} is attacking!")
    move_index = random.randint(0, len(npc_pokemon.moves) - 1)
    selected_move = npc_pokemon.moves[move_index]
    perform_move(selected_move, npc_pokemon, player_pokemon)
    sleep(TURNDELAY)


def battle_npc(player, npc, repeat=False):
    if not npc.beat:
        if not repeat:
            npc.heal_all_pokemon()
        sleep(TURNDELAY)
        clear()
        # print(f"--{npc.name.upper()}--")
        player_pokemon = player.pokemons[0]
        npc_pokemon = npc.pokemons[0]

        for pokemon in [player_pokemon, npc_pokemon]:
            pokemon.attack = pokemon.base_attack
            pokemon.defense = pokemon.base_defense

        if player_pokemon.hp > 0 and not repeat:
            print(center(f"\n{player.name.upper()} VS {npc.name.upper()}"))  # names
            sleep(2)

        while player_pokemon.hp > 0 and npc_pokemon.hp > 0:
            player_turn(player_pokemon, npc_pokemon, player)
            if npc_pokemon.hp <= 0:
                break

            player_pokemon = player.pokemons[0]

            npc_turn(player_pokemon, npc_pokemon)

        if player_pokemon.hp <= 0:
            print(
                f"{Fore.LIGHTRED_EX}{player_pokemon.name.upper()} fainted.{Fore.RESET}\n"
            )
            if player.get_alive_pokemon() > 1:
                valid_pokemons = []
                valid_pokemons_display = []

                for i, pokemon in enumerate(player.pokemons):
                    if pokemon.hp > 0:
                        valid_pokemons.append(pokemon)
                        valid_pokemons_display.append(f"{pokemon.info_string()} ")

                if len(valid_pokemons) > 0:
                    print("\npick a pokemon to switch to: ")

                    player.switch_pokemon(valid_pokemons[menu(valid_pokemons_display)])
                    battle_npc(player, npc, repeat=True)
                else:
                    if npc.name != "dr ock":
                        clear()
                        print(center(f"{npc.name.upper()}:  you shall not pass >:-)"))
                        sleep(TURNDELAY)
                        player_position[0] -= 1
            else:
                if npc.name != "dr ock":
                    clear()
                    print(
                        center(f"{npc.name.upper()}:  you shall not pass >:-)")
                    )  # pervent skipping
                    sleep(TURNDELAY)
                    player_position[0] -= 1
        elif npc_pokemon.hp <= 0:
            print(
                f"{Fore.LIGHTRED_EX}{npc_pokemon.name.upper()} fainted.{Fore.RESET}\n"
            )

            if npc.get_alive_pokemon():
                idx = -1
                for i, pokemon in enumerate(npc.pokemons):
                    if pokemon.hp > 0:
                        idx = i
                if idx != -1:
                    temp = npc.pokemons[0]
                    npc.pokemons[0] = npc.pokemons[idx]
                    npc.pokemons[idx] = temp

                    # print (npc.get_alive_pokemon())
                    # npc.display_pokemon()

                    npc.say(f"go {npc.pokemons[0].name.title()}!")
                    sleep(2)

                    battle_npc(player, npc, repeat=True)

            else:
                npc.beat = True
                player.give_pokemon_exp(npc.exp_sum() / (len(player.pokemons) * 3))
                player.money += npc.money

                print(
                    f"you gained Ƀ{npc.money} now you have Ƀ{player.money}"
                )  # show money
                sleep(2)

                player.exp_difficulty_cap += npc.exp_difficulty_cap_add
                player_position[0] += 1
                global grass_progression
                grass_progression += 1

            player_position[0] -= 2


def battle_wild(player, wild):
    if wild:
        # sleep(TURNDELAY)
        play_animation()  # animation
        sleep(0.1)
        clear()
        player_pokemon = player.pokemons[0]

        for pokemon in [player_pokemon, wild]:  # reset buffs
            pokemon.attack = pokemon.base_attack
            pokemon.defense = pokemon.base_defense

        print(f"\n{player.name.upper()} VS {wild.name.upper()}")
        sleep(2)

        not_caught = 1
        while player_pokemon.hp > 0 and wild.hp > 0 and not_caught:
            not_caught = player_turn(player_pokemon, wild, player)

            if not_caught:
                if wild.hp <= 0:
                    break

                player_pokemon = player.pokemons[0]

                npc_turn(player_pokemon, wild)

        if not not_caught:
            pass

        if player_pokemon.hp <= 0:  # dead
            print(
                f"{Fore.LIGHTRED_EX}{player_pokemon.name.upper()} fainted.{Fore.RESET}\n"
            )

            if player.get_alive_pokemon() > 1:
                valid_pokemons = []
                valid_pokemons_display = []

                for i, pokemon in enumerate(player.pokemons):
                    if pokemon.hp > 0:
                        valid_pokemons.append(pokemon)
                        valid_pokemons_display.append(f"{pokemon.info_string()} ")

                if len(valid_pokemons) > 0:
                    print("\npick a pokemon to switch to: ")  # pick

                    player.switch_pokemon(valid_pokemons[menu(valid_pokemons_display)])
                    battle_wild(player, wild)

        elif wild.hp <= 0:
            print(f"{Fore.LIGHTRED_EX}{wild.name.upper()} fainted.{Fore.RESET}\n")
            sleep(1)
            if godmode:
                player.give_pokemon_exp(wild.exp // (len(player.pokemons) * 0.01))
            player.give_pokemon_exp(wild.exp // (len(player.pokemons) * 3))

            money_gain = random.randint(500, int(2000 + (player.money / 5)))
            player.money += money_gain

            print(f"you gained Ƀ{money_gain} now you have Ƀ{player.money}")
            sleep(2)


def catch_pokemon(player, pokemon, ball):
    if not pokemon.is_npc_pokemon:
        ball_catch_rates = {  # rates dict
            "pokeball": 0.3,
            "great ball": 0.4,
            "ultra ball": 0.7,
            "master ball": 1,
        }
        print(f"{ball.title()} thrown!")
        sleep(1)

        catch_rate = ball_catch_rates[ball]

        chance_to_catch = POKEMON_INFO[pokemon.name]["catch_rate"] / 600 + catch_rate

        if random.random() < chance_to_catch:  # caught
            clear()
            for _ in range(2):
                print(Fore.LIGHTGREEN_EX + center("Beep!"))
                sleep(1)
                clear()
                sleep(0.1)
            print(Fore.LIGHTGREEN_EX + center("Beep! :)") + Style.RESET_ALL)
            sleep(1)
            clear()
            sleep(0.1)
            print(center(f"you caught {pokemon.name}!"))
            sleep(2)
            player.pokemons.append(copy.deepcopy(pokemon))
            return 1
        else:  # no caught
            clear()
            for _ in range(2):
                print(Fore.LIGHTGREEN_EX + center("Beep!"))
                sleep(1)
                clear()
                sleep(0.1)
            print(Fore.RED + center("Bloop! :(") + Style.RESET_ALL)
            sleep(1)
            clear()
            sleep(0.1)
            # print(center(f"{pokemon.name} broke free!"))
            # sleep(2)
            return 0
    else:
        print("the npc doesnt consent")
        return -1
