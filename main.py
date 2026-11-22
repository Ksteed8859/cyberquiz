import os
import pygame
from pyvidplayer2 import Video
from main_menu import run_main_menu
from country_selection import run_country_select

os.environ["SDL_AUDIODRIVER"] = "dummy"
pygame.init()

temp_v = Video("./media/video/mm-binary-stream.mp4", use_pygame_audio=True)
initial_size = temp_v.current_size
temp_v.close()

win = pygame.display.set_mode(initial_size, pygame.RESIZABLE)
pygame.display.set_caption("CyberQuiz - WSU Study Abroad Opportunity Scholarship Project")

current_screen = "MAIN_MENU"

while True:
    if current_screen == "MAIN_MENU":
        current_screen = run_main_menu(win)
    elif current_screen == "COUNTRY_SELECT":
        current_screen = run_country_select(win)

    elif current_screen == "EXIT" or current_screen is None:
        break

pygame.quit()