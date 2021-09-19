import pygame
import random
import math

# initialize game
pygame.init()

# screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Game')
icon = pygame.image.load('C:/Private/Program_Apps/Python/PyGame/Icons/screenIco.png')
pygame.display.set_icon(icon)

# player settings
playerImg = pygame.transform.scale(pygame.image.load('C:/Private/Program_Apps/Python/PyGame/Icons/battleship.png'), (60, 60))
playerX = screen.get_width() / 2 - playerImg.get_width() / 2
playerY = screen.get_height() - 1.5 * playerImg.get_height()
playerSpeedX = 0

# bullet settings
bulletImg = pygame.transform.scale(pygame.image.load('C:/Private/Program_Apps/Python/PyGame/Icons/bullet.png'), (20, 20))
bulletY = screen.get_height() - 1.5 * playerImg.get_height()
bulletX = 0
bulletSpeedY = 0.6
isBulletVisible = False

# enemy settings
enemyImg = []
enemyX = []
enemyY = []
enemySpeedX = []
num = random.randint(5, 8)

for i in range(num):
    enemyImg.append(pygame.transform.scale(pygame.image.load('C:/Private/Program_Apps/Python/PyGame/Icons/enemy_spaceship.png'), (50, 50)))
    enemyY.append(20)
    enemyX.append(random.randint(10, screen.get_width() - 10 - enemyImg[i].get_width()))
    enemySpeedX.append(0.3)

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
fontX = 10
fontY = 10
gameOver = font.render("GAME OVER", True, (255, 255, 255))

# functions
def showScore(x, y):
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (x, y))

def gameOverTxt(x, y):
    screen.blit(gameOver, (x, y))

def createPlayer(x, y):
    screen.blit(playerImg, (x, y))

def createEnemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def shootBullet(x, y):
    global isBulletVisible
    isBulletVisible = True
    screen.blit(bulletImg, (x + playerImg.get_width() / 2 - bulletImg.get_width() / 2, y))

def isCollision(enX, enY, blX, blY, i):
    distance = math.sqrt(math.pow(enX - blX, 2) + math.pow(enY - blY, 2))
    if distance < enemyImg[i].get_height():
        return True
    else:
        return False

# game loop
running = True
while running:
    screen.fill((0, 0, 0)) # needs to be first
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # movement
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerSpeedX = -0.3
        if event.key == pygame.K_RIGHT:
            playerSpeedX = 0.3

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerSpeedX = 0
    playerX += playerSpeedX

    # bullet shooting & movement
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and isBulletVisible == False:
            bulletX = playerX
            shootBullet(bulletX, bulletY)

    if isBulletVisible:
        shootBullet(bulletX, bulletY)
        bulletY -= bulletSpeedY

    if bulletY <= 0:
        bulletY = screen.get_height() - 1.5 * playerImg.get_height()
        isBulletVisible = False

    # window boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= screen.get_width() - playerImg.get_width():
        playerX = screen.get_width() - playerImg.get_width()

    # enemy movement
    for i in range(num):
        enemyX[i] += enemySpeedX[i]
        if enemyX[i] >= screen.get_width() - enemyImg[i].get_width():
            enemySpeedX[i] = -enemySpeedX[i]
            enemyY[i] += enemyImg[i].get_height()
        elif enemyX[i] <= 0:
            enemySpeedX[i] = -enemySpeedX[i]
            enemyY[i] += enemyImg[i].get_height()

    # collision
    for i in range(num):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY, i)
        if collision:
            bulletY = screen.get_height() - 1.5 * playerImg.get_height()
            isBulletVisible = False
            enemyX[i] = random.randint(10, screen.get_width() - 10 - enemyImg[i].get_width())
            enemyY[i] = 20
            score += 1

    # game over
    for i in range(num):
        if enemyY[i] >= playerY - 50:
            for j in range(num):
                enemyY[j] = 2000
                score = 0
                gameOverTxt(screen.get_width() / 2 - gameOver.get_width() / 2, screen.get_height() / 2 - gameOver.get_height() / 2)
                break

    # initializing player & enemies
    createPlayer(playerX, playerY)
    showScore(fontX, fontY)

    for i in range(num):
        createEnemy(enemyX[i], enemyY[i], i)

    pygame.display.update() # needs to be last