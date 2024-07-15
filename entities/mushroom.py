from gameObject import gameObject
class mushroom(gameObject):
    def __init__(self, x, y, direction):
        super().__init__(x, y, 1, 1)
        self.speed = 0.02 # speed of mushroom
        self.left = direction # going left