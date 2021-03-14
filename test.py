import playsound
import os
from Monsters.Imps import Imp
from PlayerManager.Player import Warrior
from Game.Game import *
os.system("python3 screen_resize.py")

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
curses.curs_set(0)
war = Warrior("Lunk")
impy = Imp()
init_colors()
playsound.playsound("Victorious.mp3", False)
display_intro_screen(screen)
screen.clear()
display_scene_1(screen, war, impy)
screen.refresh()

curses.curs_set(1)
curses.echo()
curses.nocbreak()
screen.keypad(False)

curses.endwin()
