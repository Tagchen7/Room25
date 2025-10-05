import sys
import pygame
import pygame.locals
from Game.GameLogic.game import GameState

pygame.init()

SCREEN_WIDTH = 900
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
            #print(pygame.mouse.get_pos())
            # check if an arrow was clicked
            game.before_any_click()
            for arrow in game.grid.arrows:
                if arrow.rect.collidepoint(event.pos):
                    print(f"Clicked on arrow {arrow.direction}, {arrow.number}")
                    game.grid.shift_rooms(arrow.direction, arrow.number)
            for room in game.grid.rooms.values():
                if room.rect.collidepoint(event.pos):
                    print(f"Clicked on room {room.color}{room.number}")
                    game.grid_room_clicked(room)
            for room in game.room_notes.all_rooms():
                if room.rect.collidepoint(event.pos):
                    print(f"Clicked on note room {room.color}{room.number}")
                    game.room_note_clicked(room)
            for note in game.color_notes.all_notes():
                if note.rect.collidepoint(event.pos):
                    print(f"Clicked on color note {note.color}")
                    game.color_note_clicked(note)
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_SPACE:
                print("Space pressed")
                game.space_pressed()
                    
    DISPLAYSURF.fill("white")
    game.draw(DISPLAYSURF)
    pygame.display.update()