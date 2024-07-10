import pygame
import sys
import math
from gameObject import gameObject
from entities.goomba import goomba
from entities.coin import coin

pygame.init()
size = 16 # Size of squares
# independent from sizex, sizey
width, height = 256, 240 # Game dimensions
mariox, marioy = 0, 0
velo_x, velo_y = 0, 0 # Difference in x and y
# these are velocities, need acceleration for both dx and dy (there's horizontal acceleration in actual game

sizex, sizey = 20, 20 # Doesn't do anything rn

PLAYER_MAX_SPEED = 0.2
acceleration = 0

camerax, cameray = 0, 0

window = pygame.display.set_mode((width, height))

colorWhite = (255, 255, 255)
colorBlack = (0, 0, 0)
colorBlue = (125, 206, 235)
colorBrown = (139, 69, 19)
colorGreen = (3, 252, 194)
colorYellow = (255, 211, 67)
colorTan = (210, 180, 140)
colorRed = (255, 0, 0)

gameEnded = False
clock = pygame.time.Clock()

blocks = {}
flag = {}

end_x = 100 # start of the ending platform/ end of main level;
end_dist = 10 # how wide ending platform is
flag_height = 7 # how tall flag is 
flag_x = end_x + (end_dist * 0.75)

entities = []
goombas = []
coins = []

def add_flag(x, y, color):
    if not (x, y) in flag: flag[(x, y)] = [color]

def add_flag(x, y, color):
    if not (x, y) in flag: flag[(x, y)] = [color]
def add_block(x, y, color):
    if not (x, y) in blocks: blocks[(x, y)] = [color]

def add_entity(x, y, left, entity_type, entity):
    # left is direction
    if not (x, y) in entities:
        entities.append([x, y, left, entity_type, entity])

def delete_block(x, y):
    if (x, y) in blocks: del blocks[(x, y)]

def draw_background(color):
    pygame.draw.rect(window, color, pygame.Rect(0, 0, width, height))

def draw_square(surface, color, top_left, size):
    global width, height
    rect = pygame.Rect(top_left[0]*size+width/2, top_left[1]*size+height/2, size, size)

    pygame.draw.rect(surface, color, pygame.Rect(top_left[0]*size+width/2, top_left[1]*size+height/2, size, size))
    return rect

def draw_flag(surface, color, top_left, size):
    global width, height

    pygame.draw.rect(surface, color, pygame.Rect(top_left[0]*size+width/2, top_left[1]*size+height/2, size/5, size))

def draw_triangle(surface, color, first, second, third):
    global width, height

    pygame.draw.polygon(surface, color, ((first[0]*size + width/2, first[1]*size + height/2), (second[0]*size + width/2, second[1]*size + height/2), (third[0]*size + width/2, third[1]*size + height/2)))


def draw_circle(surface, color, center, radius):
    global width, height
    pygame.draw.circle(surface, color, (center[0]*size + width/2, center[1]*size + height/2), radius)

def draw_flag(surface, color, top_left, size):
    global width, height

    pygame.draw.rect(surface, color, pygame.Rect(top_left[0]*size+width/2, top_left[1]*size+height/2, size/5, size))

def draw_triangle(surface, color, first, second, third):
    global width, height

    pygame.draw.polygon(surface, color, ((first[0]*size + width/2, first[1]*size + height/2), (second[0]*size + width/2, second[1]*size + height/2), (third[0]*size + width/2, third[1]*size + height/2)))


def draw_circle(surface, color, center, radius):
    global width, height
    pygame.draw.circle(surface, color, (center[0]*size + width/2, center[1]*size + height/2), radius)

def draw_square_rect(surface, color, rect):
    global width, height
    pygame.draw.rect(surface, color, rect)

# Rendering
def render_scene(x, y):
    global sizex, sizey
    draw_background(colorWhite)
    draw_background(colorBlue)
    for block in blocks:
        draw_square(window, blocks[block][0], (block[0] - x/size, -block[1] + y/size), size)

    # Render flag
    # Pole
    for line in flag:
        draw_flag(window, flag[line][0], (line[0] - x/size, -line[1] + y/size), size)
    # Flag triangle
    draw_triangle(window, colorGreen, (flag_x - x/size, -(flag_height - 2) + y/size), (flag_x - x/size, -(flag_height - 1.25) + y/size), (flag_x - x/size - 1, -(flag_height - 1.25) + y/size))
    # Circle on top
    draw_circle(window, colorGreen, (flag_x + 0.1 - x/size, -(flag_height - 1) + y/size), 4)
    # Render flag
    # Pole
    for line in flag:
        draw_flag(window, flag[line][0], (line[0] - x/size, -line[1] + y/size), size)
    # Flag triangle
    draw_triangle(window, colorGreen, (flag_x - x/size, -(flag_height - 2) + y/size), (flag_x - x/size, -(flag_height - 1.25) + y/size), (flag_x - x/size - 1, -(flag_height - 1.25) + y/size))
    # Circle on top
    draw_circle(window, colorGreen, (flag_x + 0.1 - x/size, -(flag_height - 1) + y/size), 4)

    #Entity rendering
    #...

    # Mario Rendering
    global mario
    mario = draw_square(window, colorTan, (mariox - x/size, -marioy + y/size), size)

    #Entity rendering

    # Goomba Rendering / Goombas are red
    global goomba_rects
    goomba_rects = [] # Rect objects for each goomba

    # Coin Rendering / Coins are Yellow
    global coin_rects
    coin_rects = [] # Rect objects for each coin

    for goomba in goombas:
        goomba_rect = draw_square(window, colorRed, (goomba.x - x/size, - goomba.y + y/size), size)
        goomba_rects.append([goomba_rect, goombas.index(goomba)])

    for coin in coins:
        coin_rect = draw_square(window, colorYellow, (coin.x - x/size, - coin.y + y/size), size)
        coin_rects.append([coin_rect, coins.index(coin)])


def updateGoombas():
     for goomba in goombas:
        goomba.update()
        if goomba.left:
            goomba.dx = -goomba.speed
        else:
            goomba.dx = goomba.speed
        #print(f"goomba at {goomba.x/size, goomba.y/size}")
        #print(f"goomba is on ground: {isOnGround(goomba.x, goomba.y)}")
        if (math.ceil(goomba.x-1), round(goomba.y)) in blocks and goomba.left:
            goomba.left = False
        elif (math.floor(goomba.x+1), round(goomba.y)) in blocks and not goomba.left:
            goomba.left = True
        if (round(goomba.x), math.floor(goomba.y)) in blocks and goomba.dy < 0:
            goomba.y = math.floor(goomba.y)+1
            goomba.dy = 0
        if not(round(goomba.x), math.floor(goomba.y-0.2)) in blocks:
            goomba.dy -= 0.02


def goombaCollision():
    global gameEnded
    for i in range(len(goomba_rects)):
        goomba_rect = goomba_rects[i][0]
        if goomba_rect.colliderect(mario):
            if mario.bottom > goomba_rect.top and mario.top < goomba_rect.top:
                print("Goomba dead")
                goombas.pop(goomba_rects[i][1])
                break
            elif goomba_rect.left <= mario.left <= goomba_rect.right and mario.top <= goomba_rect.top <= mario.bottom:
                print("RIGHT INTERSECTION")
                gameEnded = True
            elif mario.left <= goomba_rect.left <= mario.right and mario.top <= goomba_rect.top <= mario.bottom:
                print("LEFT INTERSECTION")
                gameEnded = True

def coinCollision():
    for i in range(len(coin_rects)):
        coin_rect = coin_rects[i][0]
        if coin_rect.colliderect(mario):
            print("Coin collected")
            coins.pop(coin_rects[i][1])
            break

def isOnGround(x, y):
    x, y = round(x), math.ceil(y)-1
    return (x, y) in blocks

def blockOnLeft(x, y):
    x, y = math.ceil(x)-1, round(y)
    return (x, y) in blocks

def blockOnRight(x, y):
    x, y = math.floor(x)+1, round(y)
    return (x, y) in blocks


### From this point we should turn this into a class for goombas and stuff. Mario's should be kept as-is though.
def getInputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #CPU thing goes here
    keys = pygame.key.get_pressed()
    output = []
    if keys[pygame.K_w]: output.append("w")
    if keys[pygame.K_a]: output.append("a")
    if keys[pygame.K_s]: output.append("s")
    if keys[pygame.K_d]: output.append("d")
    if keys[pygame.K_SPACE]: output.append("space")
    if keys[pygame.K_f]: output.append("f")

    return output

def camera():
    global camerax, cameray
    if mariox * size > camerax:
        camerax = mariox * size - width/100
        
def physics(inputs):
    global mariox, marioy, velo_x, velo_y
    if isOnGround(mariox, marioy) and velo_y <= 0:
        marioy -= velo_y
        velo_y = 0
        marioy = round(marioy)

    #Mario should be able to jump over 4 blocks
    if ("w" in inputs or "space" in inputs) and isOnGround(mariox, marioy): velo_y = 0.425
    if "a" in inputs:
        velo_x -= 0.01
        velo_x = max(velo_x, -PLAYER_MAX_SPEED)
    elif "d" in inputs:
        velo_x += 0.01
        velo_x = min(velo_x, PLAYER_MAX_SPEED)
    else:
        if velo_x < 0 and not velo_x > 0:
            velo_x += 0.01
        elif velo_x > 0 and not velo_x < 0:
            velo_x -= 0.01 
    #if "f" in inputs: #debug key
    
    mariox, marioy = mariox + velo_x, marioy + velo_y

    if (blockOnLeft(mariox, marioy)) or (blockOnRight(mariox, marioy)) or ((mariox * size) <= (camerax - width/2)):
        mariox -= velo_x
        velo_x = 0

    velo_y -= 0.025
    velo_y = max(-size, velo_y)   

# Generation code goes in init.
def init():
    x = 0
    for i in range(-50, 50):
        j = int(math.sin(i/6) * 3)
        #if x % y == 0: #executes every y blocks
        if x % 13 == 0:
            add_entity(i, j + 2, i > 0, "block", "coin")
        if x % 16 == 0: # place goomba every 15 blocks
            goombas.append(goomba(i, j + 1, i > 0))
        while j >= -9:
            add_block(i, j, colorBrown)
            j -= 1
        x += 1

def initTest(): 
    x = -50

    for i in range(-width, 0):
        j = -1
        while j >= -2: 
            add_block(i, j, colorBrown)
            j -= 1

    for i in range(0, end_x):
        #j = int(math.sin(i/6) * 3)
        j = -1
        #if x % y == 0: #executes every y blocks
        if x % 13 == 0:
            coins.append(coin(i, j + 2, i > 0)) 
        if x % 15 == 0: 
            goombas.append(goomba(i+3, j + 1, i > 0))
            add_block(i+1, j + 1, colorGreen)
            add_block(i+1, j + 2, colorGreen)
            add_block(i+1, j + 3, colorGreen)
            add_block(i+1, j + 4, colorGreen)
        while j >= -2: 
            add_block(i, j, colorBrown)
            j -= 1

        x += 1

    # ending area
    for i in range(end_x, end_x + end_dist):
        j = -1
        while j >= -2:
            add_block(i, j, colorGreen)
            j -= 1

    # flag
    # floor y value is -2
    add_block(flag_x - 0.45, 0, colorBrown)
    for i in range(1, flag_height):
        add_flag(flag_x, i, colorRed)

initTest()

while not gameEnded:
    pygame.time.delay(int(1000/60))
    camera()
    render_scene(camerax, cameray) # mario is always centered
    pygame.display.flip()
    inputs = getInputs()
    physics(inputs)
    goombaCollision()
    coinCollision()
    updateGoombas()
