import pygame
import webbrowser
import os
import sys
import subprocess
import shutil
from pyvidplayer2 import Video, VideoPlayer

def open_url(url):

    if sys.platform.startswith("linux"):
        if "microsoft" in os.uname().release.lower():
            for wsl_cmd in (["wslview", url], ["cmd.exe", "/c", "start", "", url]):
                if shutil.which(wsl_cmd[0]):
                    subprocess.Popen(wsl_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return
        for browser in ("firefox", "google-chrome", "chromium", "chromium-browser", "brave-browser", "microsoft-edge"):
            if shutil.which(browser):
                subprocess.Popen([browser, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return 
        try:
            if webbrowser.open(url, new=2):
                return
        except Exception:
            pass               

def run_country_select(win):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    current_size = win.get_size()

    v = Video("./media/video/mm-binary-stream.mp4", use_pygame_audio=True)
    player = VideoPlayer(v, (0, 0, *current_size), loop=True)

    ui_cs_original = pygame.image.load("./media/images/country-select-overlay.png").convert_alpha()
    ui_cs = pygame.transform.smoothscale(ui_cs_original, win.get_size())

    us_btn_original = pygame.image.load("./media/images/buttons/cs-buttons-us.png").convert_alpha()
    finland_btn_original = pygame.image.load("./media/images/buttons/cs-buttons-finland.png").convert_alpha()
    china_btn_original = pygame.image.load("./media/images/buttons/cs-buttons-china.png").convert_alpha()
    germany_btn_original = pygame.image.load("./media/images/buttons/cs-buttons-germany.png").convert_alpha()
    brazil_btn_original = pygame.image.load("./media/images/buttons/cs-buttons-brazil.png").convert_alpha()
    more_btn_original = pygame.image.load("./media/images/buttons/cs-buttons-more.png").convert_alpha()
    back_btn_original = pygame.image.load("./media/images/buttons/cs-buttons-back.png").convert_alpha()

    us_ratio = us_btn_original.get_width() / us_btn_original.get_height()
    finland_ratio = finland_btn_original.get_width() / finland_btn_original.get_height()
    china_ratio = china_btn_original.get_width() / china_btn_original.get_height()
    germany_ratio = germany_btn_original.get_width() / germany_btn_original.get_height()
    brazil_ratio = brazil_btn_original.get_width() / brazil_btn_original.get_height()
    more_ratio = more_btn_original.get_width() / more_btn_original.get_height()
    back_ratio = back_btn_original.get_width() / back_btn_original.get_height()

    def recalculate_ui(window_size):
        win_w, win_h = window_size
        ui_cs = pygame.transform.smoothscale(ui_cs_original, window_size)

        btn_h = int(win_h * 0.13)
        us_btn = pygame.transform.smoothscale(us_btn_original, (int(btn_h * us_ratio), btn_h))
        finland_btn = pygame.transform.smoothscale(finland_btn_original, (int(btn_h * finland_ratio), btn_h))
        china_btn = pygame.transform.smoothscale(china_btn_original, (int(btn_h * china_ratio), btn_h))
        germany_btn = pygame.transform.smoothscale(germany_btn_original, (int(btn_h * germany_ratio), btn_h))
        brazil_btn = pygame.transform.smoothscale(brazil_btn_original, (int(btn_h * brazil_ratio), btn_h))

        more_btn_h = int(win_h * 0.22)
        more_btn = pygame.transform.smoothscale(more_btn_original, (int(more_btn_h * more_ratio), more_btn_h))

        back_btn_h = int(win_h * 0.09)
        back_btn = pygame.transform.smoothscale(back_btn_original, (int(back_btn_h * back_ratio), back_btn_h))
         
        
        us_rect = us_btn.get_rect(center=(win_w // 2, int(win_h * 0.25)))
        finland_rect = finland_btn.get_rect(center=(win_w // 2, int(win_h * 0.40)))
        china_rect = china_btn.get_rect(center=(win_w // 2, int(win_h * 0.55)))
        germany_rect = germany_btn.get_rect(center=(win_w // 2, int(win_h * 0.70)))
        brazil_rect = brazil_btn.get_rect(center=(win_w // 2, int(win_h * 0.85)))
        more_rect = more_btn.get_rect(center=(win_w // 1.14, int(win_h * 0.85)))
        back_rect = back_btn.get_rect(center=(win_w // 8.14, int(win_h * 0.9)))
        return ui_cs, us_btn, us_rect, finland_btn, finland_rect, china_btn, china_rect, germany_btn, germany_rect, brazil_btn, brazil_rect, more_btn, more_rect, back_btn, back_rect
    
    ui_cs, us_btn, us_rect, finland_btn, finland_rect, china_btn, china_rect, germany_btn, germany_rect, brazil_btn, brazil_rect, more_btn, more_rect, back_btn, back_rect = recalculate_ui(current_size)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                player.close()
                return "EXIT"

            elif event.type == pygame.VIDEORESIZE:
                win = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                player.resize(event.size)
                ui_cs, us_btn, us_rect, finland_btn, finland_rect, china_btn, china_rect, germany_btn, germany_rect, brazil_btn, brazil_rect, more_btn, more_rect, back_btn, back_rect = recalculate_ui(event.size)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if more_rect.collidepoint(event.pos):
                        open_url("https://www.weber.edu/studyabroad/Short_Term_Programs.html")
                    elif back_rect.collidepoint(event.pos):
                        player.close()
                        return "MAIN_MENU"


        pygame.time.wait(16)

        player.update(events)
        player.draw(win)

        win.blit(ui_cs, (0, 0))
        win.blit(us_btn, us_rect)
        win.blit(finland_btn, finland_rect)
        win.blit(china_btn, china_rect)
        win.blit(germany_btn, germany_rect)
        win.blit(brazil_btn, brazil_rect)
        win.blit(more_btn, more_rect)
        win.blit(back_btn, back_rect)

        pygame.display.update()
