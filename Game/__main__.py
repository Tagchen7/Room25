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
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            #print(pygame.mouse.get_pos())
            # check if an arrow was clicked
            for arrow in Game.grid.arrows:
                if arrow.rect.collidepoint(event.pos):
                    print(f"Clicked on arrow {arrow.direction}, {arrow.number}")
                    Game.grid.shift_rooms(arrow.direction, arrow.number)
            for room in Game.grid.rooms.values():
                if room.rect.collidepoint(event.pos):
                    print(f"Clicked on room {room.color}{room.number}")
                    
    DISPLAYSURF.fill("white")
    Game.grid.draw(DISPLAYSURF)
    pygame.display.update()