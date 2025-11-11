# Contains utility functions used in game logic, such as calculations or helper functions.

import random
import math

def get_random_colors(n):
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]
    #rand_color = random.choices(range(256), k=3) maybe later?
    return random.sample(colors, n)

def edit_filename(filename):
    filename = filename.split("/")[-1]
    filename = filename.split("\\")[-1]
    filename = filename.split(".")[0]
    return filename
