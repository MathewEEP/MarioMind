from gameObject import gameObject
class koopa(gameObject):
    def __init__(self, x, y, left):
        super().__init__(x, y, 1, 1)
        self.speed = 0.02 # used in the general update function
        self.left = left # used in the general update function