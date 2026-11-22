import pygame
from pyvidplayer2 import Video, VideoPlayer

def run_main_menu(win):
    current_size = win.get_size()

    # Load in Window and background video
    v = Video("./media/video/mm-binary-stream.mp4", use_pygame_audio=True)
    player = VideoPlayer(v, (0, 0, *current_size), loop=True)

    # Load in UI over background video
    ui_mm_original = pygame.image.load("./media/images/mm-overlay.png").convert_alpha()

    # Load in Start and Exit Buttons over UI
    start_btn_original = pygame.image.load("./media/images/buttons/mm-buttons-start.png").convert_alpha()
    exit_btn_original = pygame.image.load("./media/images/buttons/mm-buttons-exit.png").convert_alpha()

    start_ratio = start_btn_original.get_width() / start_btn_original.get_height()
    exit_ratio = exit_btn_original.get_width() / exit_btn_original.get_height()

    def recalculate_ui(window_size):
        win_w, win_h = window_size
        ui_mm = pygame.transform.smoothscale(ui_mm_original, window_size)

        btn_h = int(win_h * 0.10)
        start_btn = pygame.transform.smoothscale(start_btn_original, (int(btn_h * start_ratio), btn_h))
        exit_btn = pygame.transform.smoothscale(exit_btn_original, (int(btn_h * exit_ratio), btn_h))

        start_rect = start_btn.get_rect(center=(win_w // 2, int(win_h * 0.65)))
        exit_rect = exit_btn.get_rect(center=(win_w // 2, int(win_h * 0.78)))
        return ui_mm, start_btn, start_rect, exit_btn, exit_rect

    ui_mm, start_btn, start_rect, exit_btn, exit_rect = recalculate_ui(current_size)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                player.close()
                return "EXIT"

            elif event.type == pygame.VIDEORESIZE:
                win = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                player.resize(event.size)
                ui_mm, start_btn, start_rect, exit_btn, exit_rect = recalculate_ui(event.size)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_rect.collidepoint(event.pos):
                        player.close()
                        return "COUNTRY_SELECT"

                    elif exit_rect.collidepoint(event.pos):
                        player.close()
                        return "EXIT"

        pygame.time.wait(16)

        # Change mouse if button is hovered over
        mouse_pos = pygame.mouse.get_pos()

        if start_rect.collidepoint(mouse_pos) or exit_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
        player.update(events)
        player.draw(win)

        win.blit(ui_mm, (0,0))
        win.blit(start_btn, start_rect)
        win.blit(exit_btn, exit_rect)

        pygame.display.update()