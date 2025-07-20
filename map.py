import sys
import termios
import fcntl
import os
import platform
import random
import time


from colorama import init, Fore, Back, Style

init()

global IS_TERMINAL_SET
IS_TERMINAL_SET = False

from globals import *

# RAW_MAP = ("w"*64+"\n")*10+("p"*64+"\n")*1+("w"*64+"\n")*10

RAW_MAP = """
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X.../----\......../--------\..........&..............................................................................................................X
X../______\....../___PKMT___\.........&..............................................................................................................X
X.ww|H**H|ww....ww|HHHmmHHH|ww...rrr..XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X...............................rrrrr....@........rrr.......bbbbbbbb.....wwwwwwwwwwwww............bbbbbbbbbbbbbbb....@...............................X
X........................................e.......rrrrr....bbbbbbrrrbbb..wwwwwwwwwwwwwww..........bbbbbbbbbbbbbbbbb...o...............................X
X........................................e...............bbbbbbrrrrrbbbbwwwwwwwwwwwwwww..........bbbbbbbbbbbbbbbb....o.......rrr.....................X
X........................................e...............bbbbbbbbbbbbbbbbwwwwwwwwwwwwww...........a.bbbbbbbbbb.......o......rrrrr....................X
X..rrr...................................e.....wwww......bbbbbbbbbbbbbbbbwwwwwwwwwwwww............a..rrr.............o.................tttttt........X
X.rrrrr..................................e.....wwww.......bbbbrrbbbbbbbbbbbbrrrbbb................a.rrrrr............o.................tttttt..@.....X
X.................................rrr....e..................bbbbbbbbb..bbbbbbbbbbbbb..............a..................o.................tttttt........X
X................................rrrrr...e..................c....wwwwwwwwwww....bbbbb.............a..................o....rrr........................X
X........................................e..................c...wwwwwwwwwwwww..bbbbb.wwwwww.......a..................r...rrrrr.......................X
X.....wwwwwwwwwwwwwwwwwwwwwwwwww.........e..................c....wwwwwwwwwww.bbbbb..wwwwwwww......a....wwwwww..rrr...&.........................rrr...X
X...wwwwwwwwwwwwwwwwwwwwwwwwwwwww........e..................c.......bbbrrbbbbbbb.....wwwwww.......a...wwwwwwwwrrrrr..&........................rrrrr..X
X..wwwwwwwbbbbbbbbbbbwwwwwwwwwwwww.......e.......rrr........c.....bbbbbbbbbbb.....................a..................&......wwwwwwwwwwwwww...........X
X.wwwwwwwbbbbbbbbbbbbbwwwwwwwwwwwww......e......rrrrr.......c....bbbbwwwwwwwwwwwwwwww.............a..................&.....wwwwwwwwwwwwwwww..........X
X..wwwwwwwbbbbbbbbbbbwwwwwwwwwwwww......rrr.................c.....bbwwwwwwwwwwwwwwwwww............a....rrr...........&....wwwwwwwwwwwwwwwwww.........X
X...wwwwwwwwwwwwwwwwwwwwwwwwwwwww.....rrrrrr................c......bbwwwwwwwwwwwwwwwww............a...rrrrr..........&.....wwwwwwwwwwwwwwww..........X
X....wwwwwwwwwwwwwwwwwwwwwwwwwww.......rrrr.rr..............c........wwwwwwwwwwwwwwww.............a..................&......wwwwwwwwwwwwww...........X
X.....wwwwwwwwwwwwwwwwwwwwwwww.......rrrrrrrr...............@.........wwwwwwwwwwwwww..............@..................&...............................X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

"""

REPLACEMENTS = {
 'w': 'WWw',
 'p': '3688&%o',
 '.': ".,:;'",
 'b': "~^vy",
 'e': ",:;'",
 'c': ",:;'",
 'a': ",:;'",
 'o': ",:;'",
 't': ",:;'",
 'm': "*"
}

MAP = ""

for line in RAW_MAP.split("\n"):
	for char in line:
		if char in REPLACEMENTS:
			MAP += REPLACEMENTS[char][random.randint(0, len(REPLACEMENTS[char]) - 1)]
		else:
			MAP += char
	MAP += "\n"

# print(MAP)

PLAYER_FG = Fore.LIGHTBLUE_EX
PLAYER_BG = Back.RED

# player_position = [5, 5]


def colorize(text, colors):
	new_text = ''
	lines = text.splitlines()
	for line in lines:
		line = line.rstrip()  # remove trailing whitespace
		if not line:  # skip empty lines
			new_text += "\n"
			continue
		for char in line:
			if char.isspace():  # skip whitespace chars
				new_text += char
				continue
			for key, value in colors.items():
				if char in key:
					new_text += value + char + Style.RESET_ALL
					break
			else:
				new_text += char
		new_text += "\n"

	return new_text


def center(text, offset=(0, 0)):
	terminal_cols, terminal_rows = get_terminal_size()

	text_width = len(text.split("\n")[0]) - (offset[0] * 2)
	text_height = len(text.split("\n")) - (offset[1] * 2)

	text = ("\n" + " " *
	        ((terminal_cols // 2) -
	         (text_width - (text_width // 2)))) + ("\n" + " " * (
	          (terminal_cols // 2) - (text_width -
	                                  (text_width // 2)))).join(text.split("\n"))

	text = "\n" * ((terminal_rows // 2) - (text_height -
	                                       (text_height // 2))) + text
	return text


def get_terminal_size():
	terminal_size = os.get_terminal_size()
	return terminal_size.columns, terminal_size.lines


def cclear():
	operating_system = platform.system()

	if operating_system == 'Windows':
		os.system('cls')
	else:
		os.system('clear')


def get_coord(text, coord):
	text = text.split('\n')

	if coord[1] < 0 or coord[0] < 0:
		return 0

	try:
		return text[coord[1]][coord[0]]
	except:
		return 0


def slice_map(map_string,
              middle,
              view=[30, 12],
              character=[
               Back.LIGHTBLACK_EX + '@' + Style.RESET_ALL,
               Back.LIGHTBLACK_EX + 'M' + Style.RESET_ALL
              ]):
	map_lines = map_string.split("\n")

	# row_count = len(map_lines)
	# col_count = len(map_lines[0])

	middle_row = middle[1]
	middle_col = middle[0]

	slice_ = ""
	for y in range(view[1]):
		for x in range(view[0]):
			position = [y + middle_row - view[1] // 2, x + middle_col - view[0] // 2]

			if [x, y + 1] == [view[0] // 2, view[1] // 2]:
				slice_ += character[0]
			elif [x, y] == [view[0] // 2, view[1] // 2]:
				slice_ += character[1]
			else:

				try:
					if position[0] < 0 or position[1] < 0:
						slice_ += "R"
					else:
						slice_ += map_lines[position[0]][position[1]]
				except:
					slice_ += "R"
		slice_ += "\n"

	return colorize(
	 center(slice_), {
	  '~^vy': Back.BLUE,
	  '/\\_+-': Back.RED,
	  '@': Back.RED,
	  'wW': Back.GREEN,
	  '3688&%o': Fore.WHITE + Back.YELLOW,
	  'R': Fore.BLACK + Back.LIGHTBLACK_EX,
	  ".,:;'": Fore.BLACK + Back.YELLOW,
	  "X": Back.RED,
	  "r": Back.LIGHTBLACK_EX,
	  "&": Back.LIGHTBLACK_EX,
	  "*": Back.LIGHTWHITE_EX,
	  "H|": Back.LIGHTGREEN_EX
	 })


old_term = termios.tcgetattr(0)
new_term = termios.tcgetattr(0)
old_flags = None


def set_terminal():
	'''set terminal settings'''
	global IS_TERMINAL_SET
	IS_TERMINAL_SET = True
	new_term[3] = new_term[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(0, termios.TCSANOW, new_term)

	# stdin mode
	global old_flags
	old_flags = fcntl.fcntl(0, fcntl.F_GETFL)
	fcntl.fcntl(0, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)


def reset_terminal():
	'''restore terminal settings'''
	global IS_TERMINAL_SET
	IS_TERMINAL_SET = False
	termios.tcsetattr(0, termios.TCSANOW, old_term)
	fcntl.fcntl(0, fcntl.F_SETFL, old_flags)


def tinput(text):
	reset_terminal()
	cclear()
	x = input(center(text))
	set_terminal()
	return x


def next_char():
	'''intercept and read 1 char'''
	if IS_TERMINAL_SET == False:
		set_terminal()
		char = sys.stdin.read(1)
		reset_terminal()
		return char

	return sys.stdin.read(1)


lastmap = slice_map(MAP,
                    player_position,
                    character=[
                     PLAYER_FG + PLAYER_BG + '@' + Style.RESET_ALL,
                     PLAYER_FG + PLAYER_BG + 'M' + Style.RESET_ALL
                    ])


def map():
	global lastmap
	BLOCKED = "X&b@/\\_|rPHm"
	cclear()
	print(lastmap)
	set_terminal()
	player_standing = '.'
	try:
		while True:
			try:
				char = next_char()
				if char == 'w':
					player_position[1] -= 1
					go = get_coord(RAW_MAP, player_position)
					if not go or str(go) in BLOCKED:
						player_position[1] += 1
						if go == "m":
							return "M"
					else:
						cclear()
						lastmap = slice_map(MAP,
						                    player_position,
						                    character=[
						                     PLAYER_FG + PLAYER_BG + 'O' + Style.RESET_ALL,
						                     PLAYER_FG + PLAYER_BG + 'M' + Style.RESET_ALL
						                    ])
						print(lastmap)
						# print("up")
						player_standing = get_coord(RAW_MAP, player_position)
					# print(go)

				elif char == 's':
					player_position[1] += 1
					go = get_coord(RAW_MAP, player_position)
					if not go or str(go) in BLOCKED:
						player_position[1] -= 1
						if go == "m":
							return "M"
					else:
						cclear()
						lastmap = slice_map(MAP,
						                    player_position,
						                    character=[
						                     PLAYER_FG + PLAYER_BG + '@' + Style.RESET_ALL,
						                     PLAYER_FG + PLAYER_BG + 'M' + Style.RESET_ALL
						                    ])
						print(lastmap)
						# print("down")
						player_standing = get_coord(RAW_MAP, player_position)
					# print(tinput("hi?	"))
				if char == 'a':
					player_position[0] -= 1
					go = get_coord(RAW_MAP, player_position)
					if not go or str(go) in BLOCKED:
						player_position[0] += 1
						if go == "m":
							return "M"
					else:
						player_standing = get_coord(RAW_MAP, player_position)
						cclear()
						lastmap = slice_map(MAP,
						                    player_position,
						                    character=[
						                     PLAYER_FG + PLAYER_BG + 'D' + Style.RESET_ALL,
						                     PLAYER_FG + PLAYER_BG + 'X' + Style.RESET_ALL
						                    ])
						print(lastmap)
						# print("left")
				elif char == 'd':
					player_position[0] += 1
					go = get_coord(RAW_MAP, player_position)
					if not go or str(go) in BLOCKED:
						player_position[0] -= 1
						if go == "m":
							return "M"
					else:
						cclear()
						lastmap = slice_map(MAP,
						                    player_position,
						                    character=[
						                     PLAYER_FG + PLAYER_BG + 'C' + Style.RESET_ALL,
						                     PLAYER_FG + PLAYER_BG + 'X' + Style.RESET_ALL
						                    ])
						print(lastmap)
						# print("right")
						player_standing = get_coord(RAW_MAP, player_position)
				# if char == 'x':
				# 	print("stop")
				# 	break
				if char == 'b':
					return "B"
				if char == 'p':
					return "P"

				if player_standing in "wecaot":
					reset_terminal()
					cclear()
					return player_standing

			except IOError:
				pass

	except KeyboardInterrupt:
		pass

	finally:
		reset_terminal()


# map()
