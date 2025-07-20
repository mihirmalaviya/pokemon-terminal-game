
from colorama import init, Fore
from time import sleep
import os
import platform

from globals import *

init()

def progress_bar(size, health, max_health, color=Fore.LIGHTBLUE_EX):
	filled_blocks = int((health / max_health) * size)
	empty_blocks = size - filled_blocks

	bar = (color + '#') * filled_blocks + (Fore.YELLOW + ':') * empty_blocks

	return bar + Fore.RESET

def clear():
	operating_system = platform.system()

	if operating_system == 'Windows':
		os.system('cls')
	else:
		os.system('clear')


def printd(text, end="\n"):
	for i in text:
		print(i, end="", flush=True)  # flush needed or else it is choppy
		sleep(TYPEDELAY)
	print("", end=end)


def inputd(text):
	printd(text, end="")
	return input()


def menu(options):
	for i, option in enumerate(options):
		print(f"{i + 1}\t{option}")

	while True:  # error trap
		try:
			choice = int(input()) - 1
			if 0 <= choice < len(options):
				return choice
			else:
				print("invalid choice, please enter a valid option")
		except ValueError:
			print("invalid input, please enter a number corresponding to an option")


def add_to_dict(dictionary, key, value):
	if key in dictionary:
		dictionary[key] += value
	else:
		dictionary[key] = value

def align_text(text, push=1):
  # split into lines
  lines = text.split('\n')

  # find min spaces
  min_spaces = 999
  for line in lines:
    if line.strip() != '':
      spaces = len(line) - len(line.lstrip())
      min_spaces = min(min_spaces, spaces)

  # slice each line
  aligned_lines = []
  for line in lines:
    if line.strip() == '':
      aligned_lines.append(line)
    else:
      aligned_lines.append(line[min_spaces:])

  # join back
  aligned_text = ('\n'+(' '*push))+('\n'+(' '*push)).join(aligned_lines)

  return aligned_text

def remove_empty_lines(text):
	lines = text.split('\n')
	while lines and not lines[0].strip():
		lines.pop(0)
	while lines and not lines[-1].strip():
		lines.pop()
	return '\n'.join(lines)


def center(text, offset = (0,0)):
  terminal_cols, terminal_rows = get_terminal_size()

  text_width = len(text.split("\n")[0])-(offset[0]*2)
  text_height = len(text.split("\n"))-(offset[1]*2)


  text=("\n"+" "*((terminal_cols//2)-(text_width-(text_width//2))))+("\n"+" "*((terminal_cols//2)-(text_width-(text_width//2)))).join(text.split("\n"))

  text = "\n"*((terminal_rows//2)-(text_height-(text_height//2))) + text
  return text


def get_terminal_size():
  terminal_size = os.get_terminal_size()
  return terminal_size.columns, terminal_size.lines
