class goomba(gameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1)
        self.color = (255, 0, 0)
        self.speed = 0.02 # used in the general update function

