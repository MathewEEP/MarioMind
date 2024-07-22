from gameObject import gameObject
class coin(gameObject):
    def __init__(self, x, y, left):
        super().__init__(x, y, 1, 1)
        self.left = left # used in the general update function
    def update():
        #Move update functions here,
        pass
    def collect():