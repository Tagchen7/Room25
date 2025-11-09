import sys
import os
import pygame
import pygame.locals
from Game.GameLogic.game import GameState

# If the app is frozen by PyInstaller (or similar tools), resources are
# extracted to a temporary directory available as sys._MEIPASS. Change
# the current working directory there so relative paths and any code that
# depends on CWD continue to work. This is safe when running normally as
# well because getattr will return False.
if getattr(sys, 'frozen', False):
    base = getattr(sys, '_MEIPASS', None)
    if base:
        try:
            os.chdir(base)
        except Exception:
            # If chdir fails, continue - asset loading uses ASSETS_BASE which
            # is computed from _MEIPASS in the code.
            pass

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Room25 Helper')

game = GameState()

while True:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            game.handle_click(event.pos)
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_RETURN:
                print("Return (enter) pressed")
                game.key_pressed("return")
            elif event.key == pygame.locals.K_BACKSPACE:
                print("Backspace pressed")
                game.key_pressed("backspace")
            else:
                keychar = event.unicode
                print(f"{keychar} pressed")
                game.key_pressed(keychar)
                    
    DISPLAYSURF.fill("white")
    game.draw(DISPLAYSURF)
    pygame.display.update()