# Contains definitions for game entities like Player, Enemy, Projectile, etc.

class Room:
    size = 5
    
    def __init__(self, x, y):
        # Center = (0, 0)
        self.corner = (abs(x) == 2 or abs(y) == 2) and x != 0 and y != 0
        self.x = x
        self.y = y
        self.color = " "
        self.number = 0
        if x == 0 and y == 0:
            self.color = "B"
            self.number = 1

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, var):
        self._x = (self.size + var) % self.size

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, var):
        self._y = (self.size + var) % self.size

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, text):
        self._color = str(text)[0].capitalize()

    def __repr__(self) -> str:
        if self.number > 0:
            return f"{self.color}{self.number}"
        return self.color