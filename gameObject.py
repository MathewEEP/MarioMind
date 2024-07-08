class gameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dx = 0
        self.dy = 0
        self.color = (0, 0, 0)

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

    def collidesWith(self, other):
        return self.x + self.width > other.x and self.x < other.x + other.width and self.y + self.height > other.y and self.y < other.y + other.height

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
