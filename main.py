#   SPACE_INVADERS   #

# imports
import pygame
import random
import math
from pygame import mixer
import os
import sys

# initialize pygame
pygame.init()
score = 0
score_font = pygame.font.Font(pygame.font.get_default_font(), 32)
scoreX = 10
scoreY = 550
def show_score(x, y):
    score_display = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_display, (x, y))

# initialize files path
BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# game over
game_over_font = pygame.font.Font(pygame.font.get_default_font(), 64)
def game_over_text():
    game_over_display = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_display, (200, 250))

# background music
mixer.music.load(os.path.join(BASE_PATH, 'Assets', 'Sounds', 'BG_musicLoop.wav'))
mixer.music.play(-1)

# create game screen
screen = pygame.display.set_mode((800, 600))

# background
background =  pygame.image.load(os.path.join(BASE_PATH, 'Assets', 'Images', 'BG.png'))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join(BASE_PATH, 'Assets', 'Images', 'ICON.png'))
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load(os.path.join(BASE_PATH, 'Assets', 'Images', 'SHIP.png'))
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))
    
# enemy
max_enemies = 4
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(max_enemies):
    enemyImg.append(pygame.image.load(os.path.join(BASE_PATH, 'Assets', 'Images', 'ENEMY.png')))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(10, 60))
    enemyX_change.append(random.randint(1, 5))
    enemyY_change.append(random.randint(12, 40))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
    
# bullet
# ready - the bullet is not visible 
# fire - the bullet is visible and moving 
bulletImg = pygame.image.load(os.path.join(BASE_PATH, 'Assets', 'Images', 'BULLET.png'))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+28, y-10))
    
# collision 
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30: 
        return True
    else:
        return False

# game loop
running = True
while running:
    
    #BG RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    # quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # if key is pressed check for left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound(os.path.join(BASE_PATH, 'Assets', 'Sounds', 'lazerShootWAV.wav'))
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    # player call
    playerX += playerX_change
    # check bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    player(playerX, playerY)
    
    # enemy call
    for i in range(max_enemies):        
        # game over
        if enemyY[i] > 460:
            for j in range(max_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        # check bounds
        if enemyX[i] <= 0:
            enemyX_change[i] = enemyX_change[i] * -1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = enemyX_change[i] * -1  
            enemyY[i] += enemyY_change[i]  
        
        # collision resolve
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            vanish_sound = mixer.Sound(os.path.join(BASE_PATH, 'Assets', 'Sounds', 'EnemyHitWAV.wav'))
            vanish_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(10, 60)
        enemy(enemyX[i], enemyY[i], i)
    
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    show_score(scoreX, scoreY)
        
    pygame.display.update()
    
# pyinstaller path 'C:\Users\Carlos Henrique\AppData\Roaming\Python\Python37\Scripts'#