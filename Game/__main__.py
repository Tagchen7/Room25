# This is the main entry point of your application.
# It initializes the game logic and GUI components,
# starts the game loop, and handles any interactions between them.

from Game.GameLogic.game import Game

def main():
    """
    if len(sys.argv) > 1 and sys.argv[1] == "html":
        ## later ...
        # from Game.GUI.web_gui import web_gui as GUI
    else:
        from Game.GUI.tkinter_gui import tkinter_gui as GUI
    """
    from Game.GUI.tkinter_gui.tkinter_gui import TkinterGUI as GUI

    game_loop = Game(GUI)
    game_loop.run()

if __name__ == "__main__":
    main()