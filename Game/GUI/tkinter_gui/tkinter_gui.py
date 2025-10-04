import tkinter as tk
from Game.GUI.gui_base import GUIBase

class TkinterGUI(GUIBase):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.title("Room 25")
        self.fullscreen = True
        self.root.attributes('-fullscreen', self.fullscreen)
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack()
        
        self.bind_keys()

    def run(self, update_callback, click_callback):
        self.click_callback = click_callback
        self.root.after(16, update_callback)
        self.root.mainloop()

    def bind_keys(self):
        self.root.bind("<F5>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("<Button-1>", self.on_click)

        self.root.bind("<arrow-up>", self.on_key("up"))
        self.root.bind("<arrow-down>", self.on_key("down"))
        self.root.bind("<arrow-left>", self.on_key("left"))
        self.root.bind("<arrow-right>", self.on_key("right"))

        selected_keys = ["a", "d", "w", "s", "1", "2", "3", "4", "5", "j", "k", "l", "i", "space", "enter"]
        for key in selected_keys:
            self.root.bind(key, self.on_key(key))

    def on_click(self, event):
        self.click_callback(event.x, event.y)

    def on_key(self, key):
        pass

    def update(self, draw_info_for_gui):
        self.draw_info_for_gui = draw_info_for_gui
        self.canvas.delete("all")
        self.draw_elements()

    def draw_elements(self):
        pass
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes('-fullscreen', self.fullscreen)