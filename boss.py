from cmu_graphics import *
import random
import math 

class boss:
    def __init__(self, health, strength, size, speed):
        #Differing attributes for the different bosses
        self.jumpCount = 0 
        self.health = health
        self.strength = strength
        self.size = size
        self.speed = speed
        
        self.x = 750
        self.y = 600
        self.velX = 0
        self.velY = 0
        self.accX = 0.01
        self.accY = 0.1 #Simulation of gravity 
        self.gravityMax = -6
        self.xFriction = 0.1
        
    def drawBoss(self):
        for item in range(len(app.currBoss)):
            sprite = (app.plantBossAttackSprites)[app.bossAttackCounter]
            drawImage(sprite, app.currBoss[0][0] - app.mainPlayer.currX + app.mainPlayer.onScreenX - app.bossWidth//2, app.currBoss[0][1] - int(app.bossWidth) + 40, width = app.bossWidth, height = app.bossWidth)
        for item in range(len(app.deadBoss)):
            sprite = (app.plantBossDeathSprites)[app.bossAttackCounter]
            drawImage(sprite, app.deadBoss[0][0] - app.mainPlayer.currX + app.mainPlayer.onScreenX - app.bossWidth//2, app.deadBoss[0][1] - int(app.bossWidth) + 40, width = app.bossWidth, height = app.bossWidth)

def drawEnemyProjectile(app):
    if len(app.enemyProjectiles) <= 3 and len(app.currBoss) == 1 and abs(app.mainPlayer.currX - app.currBoss[0][0]) <= app.width//2 :
        generateEnemyProjectile(app)
    for item in range(len(app.enemyProjectiles)):
        drawImage(app.magicProjectile, app.enemyProjectiles[item][0] - app.mainPlayer.currX + app.mainPlayer.onScreenX, app.enemyProjectiles[item][1], width = app.enemyProjectileWidth, height = app.enemyProjectileWidth)
    for item in range(len(app.enemyProjectiles1)):
        drawImage(app.magicProjectile, app.enemyProjectiles1[item][0] - app.mainPlayer.currX + app.mainPlayer.onScreenX, app.enemyProjectiles1[item][1], width = app.enemyProjectileWidth, height = app.enemyProjectileWidth)

def generateBoss(app):
    if len(app.obstacles) > 0:
        num = random.randint(0, len(app.obstacles)-1)
        x2, y2, w2, h2 = app.obstacles[num][0], app.obstacles[num][1], app.obstacles[num][2], app.obstacles[num][3]
        app.currBoss.append([x2  + w2//2 - app.sizeItem//2, y2 - app.sizeItem, w2, h2])
        app.currBossGround = y2 - app.sizeItem
        app.currBossSide1 = x2  + w2//2 - app.sizeItem//2
        app.currBossSide2 = x2  + w2//2 - app.sizeItem//2 + w2
        return
    
def generateEnemyProjectile(app):
    startX = int(app.currBoss[0][0] - app.bossWidth//2)
    startY = int(app.currBoss[0][1])
    endX = app.mainPlayer.onScreenX
    bulletVelocity = 1
    endY = app.mainPlayer.y
    yVelocity = 0
    dx = endX - startX
    dy = endY - startY
    angle = math.atan2(dy, dx)
    velX = 4 * math.cos(angle)
    velY = bulletVelocity * math.sin(angle)
    radius, angle = getEndAngleAndRadius(startX, startY, endX, endY)
    app.enemyProjectiles.append([startX, startY, velX, velY, angle, yVelocity])

    #Straight Projectiles
    startX1 = int(app.currBoss[0][0] - app.bossWidth//2)
    startY1 = int(app.currBoss[0][1])
    endX1 = app.mainPlayer.onScreenX
    endY1 = app.mainPlayer.y
    radius1, angle1 = getEndAngleAndRadius(startX1, startY1, endX1, endY1)
    app.enemyProjectiles1.append([startX1, startY1, endX1, endY1, angle1])

def onStepBoss(app):
    if app.timeSinceLastBoss % 5 == 0 and len(app.currBoss) == 1: 
        num = random.randint(0, 3)
        app.currBossNum = num
    
    if app.timeSinceLastBoss % 10 == 0 and len(app.currBoss) == 0:
        app.bossHitCount = 0
        generateBoss(app)
    
    if app.bossAttackCounter == 3 and len(app.deadBoss) >= 1: 
        app.deadBoss.pop()
    
    for i in range(len(app.currBoss)):
        if app.currBoss[i][0] + 92 - app.mainPlayer.currX + app.mainPlayer.onScreenX < 0:
            app.currBoss.pop(i)
            break
        if app.bossHitCount == 2:
            app.currHighScore += 300
            app.deadBoss.append(app.currBoss[i])
            app.currBoss.pop(i)

    if len(app.enemyProjectiles) != 0:
        for i in range(len(app.enemyProjectiles)):
            newX = app.enemyProjectiles[i][0] + app.enemyProjectiles[i][2]
            newY = app.enemyProjectiles[i][1] + app.enemyProjectiles[i][3]
            app.enemyProjectiles[i][3] += 0.1
            app.enemyProjectiles[i][0], app.enemyProjectiles[i][1] = newX, newY
        if (app.enemyProjectiles[i][0]) - app.mainPlayer.currX + app.mainPlayer.onScreenX < 0:
            app.enemyProjectiles.pop(i)
        elif (app.enemyProjectiles[i][1]) > 650 or app.enemyProjectiles[i][1] < 0:
            app.enemyProjectiles.pop(i)
        elif (app.enemyProjectiles[i][0]) - app.mainPlayer.currX + app.mainPlayer.onScreenX > app.width:
            app.enemyProjectiles.pop(i)
    
    if len(app.currBoss) >= 1:
        num = random.randint(100, 300)
        if int(app.attackX + app.mainPlayer.currX - app.mainPlayer.onScreenX + num) == int(app.currBoss[0][0]):
            if int(app.currBoss[0][1]) == app.currBossGround:
                app.currBoss[0][1] -= 50
                app.currBossYVelocity = 0
        if int(app.currBoss[0][1]) != app.currBossGround:
            app.currBoss[0][1] += 1
        if int(app.currBoss[0][1]) == app.currBossGround:
            app.currBoss[0][1] = app.currBoss[0][1]

    if len(app.enemyProjectiles1) != 0:
        for i in range(len(app.enemyProjectiles1)):
            newX, newY = getRadiusEnd(app.enemyProjectiles1[i][0], app.enemyProjectiles1[i][1], 5, app.enemyProjectiles1[i][4])
            app.enemyProjectiles1[i][0], app.enemyProjectiles1[i][1] = newX, newY
        if (app.enemyProjectiles1[i][0]) - app.mainPlayer.currX + app.mainPlayer.onScreenX < 0:
            app.enemyProjectiles1.pop(i)
        elif (app.enemyProjectiles1[i][1]) > 650 or app.enemyProjectiles1[i][1] < 0:
            app.enemyProjectiles1.pop(i)
        elif (app.enemyProjectiles1[i][0]) - app.mainPlayer.currX + app.mainPlayer.onScreenX > app.width:
            app.enemyProjectiles1.pop(i)
    
def getRadiusEnd(x, y, r, z):
    alpha = math.radians(z)
    return (x + r * math.cos(alpha), y - r * math.sin(alpha))

def obstacleCollision(self, item):
        x1, y1, w1, h1 = self.currX, self.y, self.characterSizeWidth, self.characterSizeLength
        x2, y2, w2, h2 = item 
        right0 = x1 + w1
        bottom0 = y1 + h1
        right1 = x2 + w2
        bottom1 = y2 + h2
        if ((right1 >= x1) and (right0 >= x2) and (bottom1 >= y1) and (bottom0 >= y2)):
            return True
        if x2 <= x1 and x1 <= x2 + w2 and y2 <= y1 and y1 <= y2 + h2:
            return True
        return False

def drawBossBattleLabel(app):
    drawImage(app.bossBattleLabel, 125, app.height//2 - app.bossBattleLabelLength//2, width = app.width - 250, height = 100)

def getDistance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def getEndAngleAndRadius(x, y, targetX, targetY):
    radius = getDistance(x, y, targetX, targetY)
    angle = math.degrees(math.atan2(y - targetY, targetX - x)) % 360
    return (radius, angle)