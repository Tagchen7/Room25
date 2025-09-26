import tkinter as tk
import importlib.resources
from PIL import Image, ImageTk, ImageOps
from Game.GUI.gui_base import GUIBase

class TkinterGUI(GUIBase):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.title("Flask Sorting")
        self.fullscreen = True
        self.root.attributes('-fullscreen', self.fullscreen)
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack()
        
        self.root.bind("<F5>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("<Button-1>", self.on_click)

        # map for selecting objects
        self.item_map = {}
        # Load Assets
        self.Flask_Assets = {}
        Flask_Asset_Names = ["Bottom_Border", "Bottom_Filling", "Middle_Border", "Middle_Filling", "Top_Border", "Top_Filling", "Stopper_Filling", "Stopper_Filling"]
        for name in Flask_Asset_Names:
            with importlib.resources.files("Assets").joinpath(f"{name}.png").open("rb") as img_file:
                original_img = Image.open(img_file)
                original_img.load()
                self.Flask_Assets[name] = ImageTk.PhotoImage(original_img)

    def run(self, update_callback, click_callback):
        self.click_callback = click_callback
        self.root.after(16, update_callback)
        self.root.mainloop()

    def on_click(self, event):
        self.click_callback(event.x, event.y)

    def update(self, draw_info_for_gui):
        self.draw_info_for_gui = draw_info_for_gui
        self.canvas.delete("all")
        self.canvas.configure(background=self.draw_info_for_gui.get("color").get("background"))
        self.draw_elements()

    def colorize_image(self, img, color):
        gray = img.convert("L")
        alpha = img.getchannel("A") if "A" in img.getbands() else None
        color_img = ImageOps.colorize(gray, black=color, white=color)
        if alpha:
            color_img.putalpha(alpha)
        return color_img

    def draw_elements(self):
        self.draw_flasks()

    def draw_flasks(self):
        info = self.draw_info_for_gui.get("flask")
        for i, flask in enumerate(info.get("flasks")):
            print(info.get("offset"))
            print(info.get("offset").get("add_x"))
            cx = info.get("offset").get("base_x") + info.get("offset").get("add_x") * (i % info.get("num_per_line"))
            cy = info.get("offset").get("base_y") + info.get("offset").get("add_y") * (i // info.get("num_per_line"))
            if flask.selected:
                cy += info.get("offset").get("sel_y")
            self.draw_flask(obj=flask, cx=cx, cy=cy)

    def draw_flask(self, obj, cx=0, cy=0):
        dy = 5 # offset between flask parts
        hitbox_item_ids = []
        for part_2 in ["Filling", "Border"]:
            for i, part_1 in enumerate(["Bottom", "Middle" * (obj.size - 2), "Top", "Stopper"]):
                color = self.draw_info_for_gui.get("color").get("background")
                if part_1 == "Stopper":
                    color = self.draw_info_for_gui.get("color").get("Stopper")
                elif part_2 == "Filling" and i < len(obj.contents):
                    color = obj.contents[i]
                if part_1 == "Stopper" and part_2 == "Border":
                    # there is no Asset for Stopper and Border -> Skip drawing it
                    continue
                img=self.Flask_Assets[f"{part_1}_{part_2}"]
                img = self.colorize_image(img=img, color=color)
                hitbox_item_ids.append(self.canvas.create_image(cx, cy+dy*i, image=img))

        return hitbox_item_ids
    
    def is_pixel_opaque(self, img, cx, cy, mouse_x, mouse_y):
        img_w, img_h = img.size
        rel_x = int(mouse_x - (cx - img_w // 2))
        rel_y = int(mouse_y - (cy - img_h // 2))
        if 0 <= rel_x < img_w and 0 <= rel_y < img_h:
            alpha = img.getchannel("A").getpixel((rel_x, rel_y))
            return alpha > 10  # Adjust threshold as needed
        return False
    
    def get_objects_at(self, x, y):
        # Check all overlapping items, topmost first
        overlapping = self.canvas.find_overlapping(x, y, x, y)
        obj_list = []
        for item_id in reversed(overlapping):
            # Order not important anymore, check all maps TODO: merge maps?
            selection_order = [self.item_map.get(item_id)]
            for info in selection_order:
                obj = self.get_object_from_info(info, x, y)
                if obj:
                    obj_list.append(obj)
        return obj_list
    
    def get_object_from_info(self, info, ex, ey):
        if info:
            obj, img, cx, cy = info
            if self.is_pixel_opaque(img, cx, cy, ex, ey):
                return obj
        return None
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes('-fullscreen', self.fullscreen)