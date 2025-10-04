import sys
import pygame
import pygame.locals
from Game.GameLogic.game import GameState

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Room25 Helper')

Game = GameState()

while True:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.fill("white")
    Game.grid.draw(DISPLAYSURF)
    pygame.display.update()