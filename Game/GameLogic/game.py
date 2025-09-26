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
        pass


class GameState:
    def __init__(self):
       pass

    def update(self):
        # Update game logic here
        return True
    
def draw_info_for_gui(game_state):        
    """
    Prepare information for GUI rendering.
    returns a list of all objects to be drawn, and the offset to center the view on
    """
    # x, y offset
    base_x = 500
    base_y = 500
    add_x = 50
    add_y = 100
    sel_y = 50
    info = {
        "color": {"background": "white",
                  "Stopper": "black",
                  "Border": "black"},
        "flask":{"offset" : {"base_x": base_x,
                              "base_y": base_y,
                              "add_x": add_x,
                              "add_y": add_y,
                              "sel_y": sel_y},
                "num_per_line": 5,
                "flasks" : game_state.flasks
                }
    }
    return info