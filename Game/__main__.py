import sys
import pygame
import pygame.locals
from Game.GameLogic.game import GameState

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

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
                    Game.grid_room_clicked(room)
            for room in Game.room_notes.all_rooms():
                if room.rect.collidepoint(event.pos):
                    print(f"Clicked on note room {room.color}{room.number}")
                    Game.room_note_clicked(room)
            for note in Game.color_notes.notes:
                if note.rect.collidepoint(event.pos):
                    print(f"Clicked on color note {note.color}")
                    Game.color_note_clicked(note.color)
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_SPACE:
                print("Space pressed")
                Game.space_pressed()
                    
    DISPLAYSURF.fill("white")
    Game.draw(DISPLAYSURF)
    pygame.display.update()