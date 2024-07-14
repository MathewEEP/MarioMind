from gameObject import gameObject
class powerupBlock(gameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1)
        self.speed = 0.02 # speed of mushroom