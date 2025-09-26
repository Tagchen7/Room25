# gui interface, everything the gamelogic needs is prepared here
# gui is a derived class from this

class GUIBase:
    def __init__(self):
        self.game_state = None

    def run(self, update_callback, click_callback):
        raise NotImplementedError

    def update(self, draw_info_for_gui):
        raise NotImplementedError

    def handle_click(self, x, y):
        raise NotImplementedError