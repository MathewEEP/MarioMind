import pygame
import sys
import math

pygame.init()
size = 16 # Size of squares
# independent from sizex, sizey
width, height = 256, 240 # Game dimensions
mariox, marioy = 0, 0
velo_x, velo_y = 0, 0 # Difference in x and y
# these are velocities, need acceleration for both dx and dy (there's horizontal acceleration in actual game

sizex, sizey = 20, 20 # Doesn't do anything rn

PLAYER_MAX_SPEED = 3
acceleration = 0

mario = pygame.Rect(width/2, height/2-size, size, size)

window = pygame.display.set_mode((width, height))

colorWhite = (255, 255, 255)
colorBlack = (0, 0, 0)
colorBlue = (125, 206, 235)
colorBrown = (139, 69, 19)
colorYellow = (255,211,67)
colorTan = (210, 180, 140)
colorRed = (255, 0, 0)

gameEnded = False
clock = pygame.time.Clock()

blocks = {}

entities = [] # Goombas for now. each entry is (x, y, direction)

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

    #Entity rendering
    #...

    # Mario Rendering
    pygame.draw.rect(window, colorTan, mario)

    # Goomba Rendering / Goombas are red
    global goomba_rects
    goomba_rects = [] # Rect objects for each goomba

    # Coin Rendering / Coins are Yellow
    global coin_rects
    coin_rects = [] # Rect objects for each coin

    for entity in entities:
        if entity[4] == "goomba":
            goomba_rect = draw_square(window, colorRed, (entity[0] - x/size, -entity[1] + y/size), size)
            goomba_rects.append([goomba_rect, entities.index(entity)])
        #print(len(entities))
        elif entity[4] == "coin":
            coin_rect = draw_square(window, colorYellow, (entity[0] - x/size, -entity[1] + y/size), size)
            coin_rects.append([coin_rect, entities.index(entity)])

def updateGoombas():
    speed = 0.125
    for goomba in entities:
        if goomba[4] == "goomba":
            if abs(goomba[0] - round(goomba[0])) < 1e-5:
                if not (goomba[0] - 1, goomba[1] - 1) in blocks and goomba[2]:
                    goomba[2] = False
                elif not (goomba[0] + 1, goomba[1] - 1) in blocks and not goomba[2]:
                    goomba[2] = True
                elif (goomba[0] - 1, goomba[1]) in blocks and goomba[2]:
                    goomba[2] = False
                elif (goomba[0] + 1, goomba[1]) in blocks and not goomba[2]:
                    goomba[2] = True

            if (goomba[2]): # go left
                goomba[0] -= speed
            else:   #go right
                goomba[0] += speed


def goombaCollision():
    global gameEnded
    for i in range(len(goomba_rects)):
        goomba_rect = goomba_rects[i][0]
        if goomba_rect.colliderect(mario):
            if mario.bottom > goomba_rect.top and mario.top < goomba_rect.top:
                print("Goomba dead")
                entities.pop(goomba_rects[i][1])
                #goomba_rects.remove(goomba_rects[i]) Not needed for some reason?
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
            entities.pop(coin_rects[i][1])
            #coin_rects.remove(coin_rect[i]) Not needed for some reason automatically removes idk why
            break



def isOnGround(x, y):
    x, y = round(x/size), math.ceil(y/size)
    return (x, y) in blocks

def blockOnLeft(x, y):
    x, y = math.ceil(x/size)-1, round(y/size)
    return (x, y+1) in blocks

def blockOnRight(x, y):
    x, y = math.floor(x/size)+1, round(y/size)
    return (x, y+1) in blocks


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

def physics(inputs):
    global mariox, marioy, velo_x, velo_y
    if isOnGround(mariox, marioy - 1) and velo_y <= 0:
        velo_y = 0
        # print(marioy)
        marioy = math.floor(marioy)

    if (blockOnLeft(mariox, marioy)) or (blockOnRight(mariox, marioy)):
        velo_x = 0

    if ("w" in inputs or "space" in inputs) and isOnGround(mariox, marioy): velo_y = 4
    if "a" in inputs:
        velo_x -= 0.2
        velo_x = max(velo_x, -PLAYER_MAX_SPEED)
        print(velo_x)
    elif "d" in inputs:
        velo_x += 0.2
        velo_x = min(velo_x, PLAYER_MAX_SPEED)
    else:
        if velo_x < 0:
            velo_x += 0.02
        elif velo_x > 0:
            velo_x -= 0.02

    if "f" in inputs: #debug key
        print("first")
        print(coin_rects)
        print("coin above")
        print(goomba_rects)
        print("Next")
    
    mariox, marioy = mariox + velo_x, marioy + velo_y

    velo_y -= 0.25
    velo_y = max(-size, velo_y)   

# Generation code goes in init.
def init():
    x = 0
    for i in range(-50, 50):
        j = int(math.sin(i/6) * 3)
        #if x % y == 0: #executes every y blocks
        if x % 13 == 0:
            add_entity(i, j + 2, i > 0, "block", "coin")
        if x % 15 == 0: # place goomba every 15 blocks
            add_entity(i, j + 1, i > 0, "mob", "goomba") # one tile above the ground
            #add_entity(i, j + 2, i > 0, "block", "coin")
        while j >= -9:
            add_block(i, j, colorBrown)
            j -= 1

        x += 1


init()

while not gameEnded:
    pygame.time.delay(int(1000/60))
    render_scene(mariox, marioy) # mario is always centered
    pygame.display.flip()
    inputs = getInputs()
    physics(inputs)
    goombaCollision()
    coinCollision()
    updateGoombas()