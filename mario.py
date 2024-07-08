class mario(gameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1)
        self.color = (210, 180, 140)
        self.speed = 0.2 # used by general update
        self.accel = 0 # for slipping (set by general update when no keys are pressed)
        self.jumpHeight = 5 # used by general update to jump

    def update(self, dt):
        super().update(dt)
        self.dx += self.accel * dt
