import math
import random
import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
# mixer.music.play(-1)


# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Score and Lives
score_value = 0
lives = 3
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

def show_score_and_lives(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    lives_text = font.render("Lives : " + str(lives), True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(lives_text, (x, y + 40))

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Create enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + (math.pow(y1 - y2, 2)))
    return distance < 27

def set_background():
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

def move_bullet():
    global bulletY, bullet_state
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change    

def game_input():
    global running, playerX_change, playerY_change, playerY, bulletX, bulletY, bullet_state, playerX
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_RETURN:  # Utiliser "Entrée" pour tirer
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    # Limites pour le joueur
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:  # Limite en haut
        playerY = 0
    elif playerY >= 536:  # Limite en bas
        playerY = 536

def enemy_movement():
    global enemyX, enemyX_change, enemyY, enemyY_change
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)

def collision():
    global num_of_enemies, enemyX, enemyY, bulletX, bulletY, bullet_state, score_value, lives
    for i in range(num_of_enemies):
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # Vérifier collision avec le joueur
        if isCollision(playerX, playerY, enemyX[i], enemyY[i]):
            lives -= 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            if lives <= 0:
                print("Game Over!")
                pygame.quit()
                exit()

# Game Loop
running = True
while running:
    set_background()
    game_input() 
    enemy_movement()
    collision()
    move_bullet()
    player(playerX, playerY)
    show_score_and_lives(textX, testY)
    pygame.display.update()

