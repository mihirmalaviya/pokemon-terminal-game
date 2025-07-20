
from utils import align_text, remove_empty_lines, clear, center
from time import sleep
from pokemon_info import MOVES_INFO, type_colors, WILD_ANIMATION
from colorama import init, Style, Fore
import copy
from map import center, cclear
from time import sleep

from startup import *

init()

global sprite_cache
sprite_cache = {}


def get_pokemon_sprite(pokemon_name, back=False, white=False, small_factor=2):
	if pokemon_name in sprite_cache and not white:
		if not back:
			if "front" in sprite_cache[pokemon_name]:
				return sprite_cache[pokemon_name]["front"]
		else:
			if "back" in sprite_cache[pokemon_name]:
				return sprite_cache[pokemon_name]["back"]

	import requests
	from PIL import Image

	POKEMON_ART_COLOR_OFFSET = 100

	response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
	if response.status_code == 200:
		data = response.json()
		if not back:
			sprite_url = data['sprites']['front_default']
		else:
			sprite_url = data['sprites']['back_default']
		sprite_response = requests.get(sprite_url, stream=True)
		if sprite_response.status_code == 200:
			sprite_response.raw.decode_content = True
			img = Image.open(sprite_response.raw)

			# resize
			img = img.resize((96 // (1 * small_factor), 96 // (2 * small_factor)))

			img = img.convert('RGBA')

			ascii_chars = " @B%8&WM#*oahkbdpqwmZO=QLCJU(Xzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::
			                                                                                        1]

			if white:
				ascii_chars = " " * len(ascii_chars)

			ascii_art = ""
			for y in range(img.height):
				for x in range(img.width):
					r, g, b, a = img.getpixel((x, y))
					gray_value = ((r + g + b) // 3)

					ascii_char = ascii_chars[int(gray_value / 3.65714285714)]
					if a != 0:
						if white:
							r, g, b = 255, 255, 255

						fg_color = f"\033[38;2;{abs(r-POKEMON_ART_COLOR_OFFSET)};{abs(g-POKEMON_ART_COLOR_OFFSET)};{abs(b-POKEMON_ART_COLOR_OFFSET)}m"
						bg_color = f"\033[48;2;{r};{g};{b}m"
					else:
						bg_color = ""
						fg_color = ""
					ascii_art += f"{fg_color}{bg_color}{ascii_char}"
					if bg_color:
						ascii_art += '\033[0m'
				ascii_art += '\n'

			if pokemon_name not in sprite_cache:
				sprite_cache[pokemon_name] = {}
			if not back:
				sprite_cache[pokemon_name]["front"] = ascii_art
			else:
				sprite_cache[pokemon_name]["back"] = ascii_art

			return ascii_art

	return -1


def evolve_animation(old, new):
	old_img = center( # init
	 align_text(remove_empty_lines(str(get_pokemon_sprite(old, white=False)))))
	old_img_white = center(
	 align_text(remove_empty_lines(str(get_pokemon_sprite(old, white=True)))))
	new_img = center(
	 align_text(remove_empty_lines(str(get_pokemon_sprite(new, white=False)))))
	new_img_white = center(
	 align_text(remove_empty_lines(str(get_pokemon_sprite(new, white=True)))))

	SLEEPTIME = .5
	clear()
	print(old_img)
	sleep(SLEEPTIME * 3)
	for i in range(4): # animation in loop
		for j in range(4):
			clear()
			print(old_img_white)
			sleep(SLEEPTIME)
			clear()
			print(new_img_white)
			sleep(SLEEPTIME)
		SLEEPTIME /= 2
	SLEEPTIME = .5
	clear()
	print(new_img)
	sleep(SLEEPTIME * 4)


def display_move(move):
	info = MOVES_INFO[move] # move styles

	return (
	 f"\033[1m{type_colors[info['type']]}{move.capitalize():<11}{Style.RESET_ALL} \x1B[3m"
	 f"{type_colors[info['type']]}{info['type'] or 'N/A':<9}{Style.RESET_ALL}\x1B[3m "
	 f"POW {info['power'] or 'N/A':<5} "
	 f"ACC {info['accuracy'] or 'N/A'}{'%':<4} "
	 # f"PP {info['pp'] or 'N/A'}"
	 f"{Style.RESET_ALL}")


def deepcopy_pokemon_list(pokemons):
	p = []
	for pokemon in pokemons:
		poke = copy.deepcopy(base_pokemons[pokemon])
		p.append(poke)
	return p


def play_animation(animation=WILD_ANIMATION, centered=True):
	for i in animation:
		cclear()
		print(center(i))
		sleep(.05)
