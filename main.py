import pygame
import sys
import math
import random
from entities.koopa import koopa
from entities.goomba import goomba
from entities.coin import coin
from entities.powerupBlock import powerupBlock
from entities.shell import shell

pygame.init()
size = 16 # Size of squares
# independent from sizex, sizey
width, height = 256, 240 # Game dimensions
mariox, marioy = -6, -5
velo_x, velo_y = 0, 0 # Difference in x and y
# these are velocities, need acceleration for both dx and dy (there's horizontal acceleration in actual game

sizex, sizey = 20, 20 # Doesn't do anything rn

timer = 0

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
colorPink = (255, 192, 203)
colorPureBlue = (0, 0, 255)

gameEnded = False
clock = pygame.time.Clock()

blocks = {} 
flag = {}

end_x = 100 # start of the ending platform/ end of main level;
end_dist = 10 # how wide ending platform is
flag_height = 7 # how tall flag is 
flag_x = end_x + (end_dist * 0.75)

koopas = []
goombas = []
coins = []
powerupBlocks = []
shells = []


def add_flag(x, y, color):
    if not (x, y) in flag: flag[(x, y)] = [color]

def add_flag(x, y, color):
    if not (x, y) in flag: flag[(x, y)] = [color]
def add_block(x, y, color):
    if not (x, y) in blocks: blocks[(x, y)] = [color]

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

    # Koopa Rendering / Koopas are red
    global koopa_rects
    koopa_rects = [] # Rect objects for each goomba

    # Goomba Rendering / Goombas are red
    global goomba_rects
    goomba_rects = [] # Rect objects for each goomba

    # Coin Rendering / Coins are Yellow
    global coin_rects
    coin_rects = [] # Rect objects for each coin

    # Powerup block Rendering / Blocks are pink
    global powerup_rects
    powerup_rects = []

    # Shell Render / Shells are Pure Blue
    global shell_rects
    shell_rects = []

    for koopa in koopas:
        koopa_rect = draw_square(window, colorGreen, (koopa.x - x/size, - koopa.y + y/size), size)
        koopa_rects.append([koopa_rect, koopas.index(koopa)])

    for goomba in goombas:
        goomba_rect = draw_square(window, colorRed, (goomba.x - x/size, - goomba.y + y/size), size)
        goomba_rects.append([goomba_rect, goombas.index(goomba)])

    for coin in coins:
        coin_rect = draw_square(window, colorYellow, (coin.x - x/size, - coin.y + y/size), size)
        coin_rects.append([coin_rect, coins.index(coin)])

    for powerup in powerupBlocks:
        powerup_rect = draw_square(window, colorPink, (powerup.x - x/size, - powerup.y + y/size), size)
        powerup_rects.append([powerup_rect, powerupBlocks.index(powerup)])

    for shell in shells:
        shell_rect = draw_square(window, colorPureBlue, (shell.x - x/size, - shell.y + y/size), size)
        shell_rects.append([shell_rect, shells.index(shell)])


def updateGoombas():
     for goomba in goombas:
        goomba.update()
        if goomba.left:
            goomba.dx = -goomba.speed
        else:
            goomba.dx = goomba.speed
        
        if (math.ceil(goomba.x-1), round(goomba.y)) in blocks and goomba.left:
            goomba.left = False
        elif (math.floor(goomba.x+1), round(goomba.y)) in blocks and not goomba.left:
            goomba.left = True
        if (round(goomba.x), math.floor(goomba.y)) in blocks and goomba.dy < 0:
            goomba.y = math.floor(goomba.y)+1
            goomba.dy = 0
        if not(round(goomba.x), math.floor(goomba.y-0.2)) in blocks:
            goomba.dy -= 0.02

def updateShells():
     for shell in shells:
        if not shell.active:
            continue

        shell.update()
        if shell.left:
            shell.dx = -shell.speed
        else:
            shell.dx = shell.speed
        
        if (math.ceil(shell.x-1), round(shell.y)) in blocks and shell.left:
            shell.left = False
        elif (math.floor(shell.x+1), round(shell.y)) in blocks and not shell.left:
            shell.left = True
        if (round(shell.x), math.floor(shell.y)) in blocks and shell.dy < 0:
            shell.y = math.floor(shell.y)+1
            shell.dy = 0
        if not(round(shell.x), math.floor(shell.y-0.2)) in blocks:
            shell.dy -= 0.02

def updateKoopas():
    for koopa in koopas:
        koopa.update()
        if koopa.left:
            koopa.dx = -koopa.speed
        else:
            koopa.dx = koopa.speed
        
        if (math.ceil(koopa.x-1), round(koopa.y)) in blocks and koopa.left:
            koopa.left = False
        elif (math.floor(koopa.x+1), round(koopa.y)) in blocks and not koopa.left:
            koopa.left = True
        if (round(koopa.x), math.floor(koopa.y)) in blocks and koopa.dy < 0:
            koopa.y = math.floor(koopa.y)+1
            koopa.dy = 0
        if not(round(koopa.x), math.floor(koopa.y-0.2)) in blocks:
            koopa.dy -= 0.02

def timerCount():
    global timer
    timer += 1

def koopaCollision():
    global gameEnded, timer
    for i in range(len(koopa_rects)):
        koopa_rect = koopa_rects[i][0]
        if koopa_rect.colliderect(mario):
            if mario.bottom > koopa_rect.top and mario.top < koopa_rect.top and timer >= 5:
                print("Koopa dead")
                shells.append(shell(koopas[i].x, koopas[i].y, random.randint(0, 2))) # goombas.append(goomba(block[0], block[1] + 2, random.randint(0, 2)))
                koopas.pop(koopa_rects[i][1])
                bounceMario()
                break
            elif koopa_rect.left <= mario.left <= koopa_rect.right and mario.top <= koopa_rect.top <= mario.bottom:
                print("Koopa - RIGHT INTERSECTION")
                gameEnded = True
            elif mario.left <= koopa_rect.left <= mario.right and mario.top <= koopa_rect.top <= mario.bottom:
                print("Koopa - LEFT INTERSECTION")
                gameEnded = True

def goombaCollision():
    global gameEnded, timer
    for i in range(len(goomba_rects)):
        goomba_rect = goomba_rects[i][0]
        if goomba_rect.colliderect(mario):
            if mario.bottom > goomba_rect.top and mario.top < goomba_rect.top and timer >= 5:
                print("Goomba dead")
                goombas.pop(goomba_rects[i][1])
                bounceMario()
                break
            elif goomba_rect.left <= mario.left <= goomba_rect.right and mario.top <= goomba_rect.top <= mario.bottom:
                print("Goomba - RIGHT INTERSECTION")
                gameEnded = True
            elif mario.left <= goomba_rect.left <= mario.right and mario.top <= goomba_rect.top <= mario.bottom:
                print("Goomba - LEFT INTERSECTION")
                gameEnded = True

def shellCollision():
    global gameEnded, velo_y, marioy, timer
    for i in range(len(shell_rects)):
        shell_rect = shell_rects[i][0]

        if (shells[i].active == True):
            if shell_rect.colliderect(mario) and timer >= 5:
                if mario.bottom > shell_rect.top and mario.top < shell_rect.top:
                    bounceMario()
                    print("Shell toggled")
                    shells[i].active = False
                    break
                elif shell_rect.left <= mario.left <= shell_rect.right and mario.top <= shell_rect.top <= mario.bottom:
                    print("Shell - RIGHT INTERSECTION")
                    gameEnded = True
                elif mario.left <= shell_rect.left <= mario.right and mario.top <= shell_rect.top <= mario.bottom:
                    print("Shell - LEFT INTERSECTION")
                    gameEnded = True
        else:
            if shell_rect.colliderect(mario) and timer >= 5:
                shells[i].active = True
                if mario.y > shells[i].y:
                    bounceMario()
                if shell_rect.left <= mario.left <= shell_rect.right and mario.top <= shell_rect.top <= mario.bottom:
                    print("Shell - RIGHT INTERSECTION")
                    shells[i].left = True
                else:
                    print("Shell - LEFT INTERSECTION")
                    shells[i].left = False

def coinCollision():
    for i in range(len(coin_rects)):
        coin_rect = coin_rects[i][0]
        if coin_rect.colliderect(mario):
            print("Coin collected")
            coins.pop(coin_rects[i][1])
            break

def powerupCollision():
    for i in range(len(powerup_rects)):
        powerup_rect = powerup_rects[i][0]
        if powerup_rect.colliderect(mario):
            print("powerup collide")
            print(powerup_rect.bottom, mario.top)
            if powerup_rect.bottom >= mario.top:  # bottom intersection
                print("mario got the power up")

def bounceMario():
    global velo_y, marioy, timer
    timer = 0
    velo_y = 0.2
    marioy += velo_y

def isOnGround(x, y):
    x, y = round(x), math.ceil(y)-1
    return (x, y) in blocks

def blockOnLeft(x, y):
    x, y = math.ceil(x)-1, round(y)
    return (x, y) in blocks

def blockOnRight(x, y):
    x, y = math.floor(x)+1, round(y)
    return (x, y) in blocks

def blockOnTop(x, y):
    x, y = round(x), math.ceil(y)
    return (x, y) in blocks

def getInputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
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
        camerax = mariox * size
        
def physics(inputs):
    global mariox, marioy, velo_x, velo_y, gameEnded

    if marioy < -10: # mario is in the void
        gameEnded = True

    if (isOnGround(mariox, marioy) and velo_y <= 0) or blockOnTop(mariox, marioy):
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

def generateMap():
    gaps = []
    platformBlocks = []
    for x in range(0, 148):
        if random.randint(1, 20) == 1:
            gaps.append(x)
            gaps.append(x+1)
            gaps.append(x+2)
    for i in range(10):
        platx = random.randint(0, 150)
        platy = -2
        for block in platformBlocks:
            if platx - block[0] <= 5 and platx - block[0] >= 0:
                platy = block[1] + 2
        platwidth = random.randint(1, 10)
        for j in range(platwidth):
            for block in platformBlocks:
                if platx + j == block[0]:
                    break
            add_block(platx + j, platy, colorBlack)
            platformBlocks.append([platx + j, platy])
    for x in range(-50, 150):
        if not x in gaps:
            add_block(x, -7, colorBrown)
            add_block(x, -6, colorBrown)
        if random.randint(1, 50) == 1:
            goombas.append(goomba(x, -5, random.randint(0, 2)))
        if random.randint(1, 50) == 1:
            koopas.append(koopa(x, -5, random.randint(0, 2)))
        if random.randint(1, 50) == 1:
            coins.append(coin(x, random.randint(-5, -2), random.randint(0, 2)))
    for block in platformBlocks:
        if random.randint(1, 20) == 1:
            goombas.append(goomba(block[0], block[1] + 2, random.randint(0, 2)))
        if random.randint(1, 20) == 1:
            koopas.append(koopa(block[0], block[1] + 2, random.randint(0, 2)))
        if random.randint(1, 20) == 1:
            coins.append(coin(block[0], random.randint(2, 5) + block[1], random.randint(0, 2)))
        if random.randint(1, 20) == 1:
            powerupBlocks.append(powerupBlock(block[0], block[1]))

generateMap()

while not gameEnded:
    pygame.time.delay(int(1000/60))
    camera()
    render_scene(camerax, cameray)
    pygame.display.flip()
    inputs = getInputs()
    physics(inputs)
    timerCount()
    koopaCollision()
    goombaCollision()
    coinCollision()
    powerupCollision()
    shellCollision()

    updateKoopas()
    updateGoombas()
    updateShells()
