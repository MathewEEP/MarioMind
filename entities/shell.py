from gameObject import gameObject
class shell(gameObject):
    def __init__(self, x, y, left):
        super().__init__(x, y, 1, 1)
        self.speed = 0.1 # used in the general update function
        self.active = False
        self.left = left # used in the general update function