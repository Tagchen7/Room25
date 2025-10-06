import sys
import pygame
import pygame.locals
from Game.GameLogic.game import GameState

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
            if event.key == pygame.locals.K_SPACE:
                print("Space pressed")
                game.space_pressed()
            if event.key == pygame.locals.K_DOWN:
                pass
            if event.key == pygame.locals.K_0:
                game.number_pressed(0)
                    
    DISPLAYSURF.fill("white")
    game.draw(DISPLAYSURF)
    pygame.display.update()