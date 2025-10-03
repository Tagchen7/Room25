# Contains the main game logic, including game initialization, game loop, collision detection, etc.
from Game.GameLogic import entity
import random

from Game.GameLogic.utils import get_random_colors

class Game:
    def __init__(self, GUI):
        self.game_state = GameState()
        self.gui = GUI()

    def run(self):
        self.gui.run(update_callback=self.loop, click_callback=self.handle_click)

    def update(self):
        self.game_state.update()
        self.gui.update(draw_info_for_gui(self.game_state))
    
    def loop(self):
        self.update()
        self.gui.root.after(1000, self.loop)
    
    def handle_click(self, x, y):
        self.game_state.handle_click(x, y)
        self.gui.update(draw_info_for_gui(self.game_state))


class GameState:
    def __init__(self):
       self.grid = entity.Grid()
       self.players = 4
       self.state = None
       
    def update(self):
        # Update game logic here
        pass

    def handle_click(self, x, y):
        if self.state == None:
            pass
            
    
def draw_info_for_gui(game_state):        
    """
    Prepare information for GUI rendering.
    returns a list of all objects to be drawn, and the offset to center the view on
    """
    return game_state.grid