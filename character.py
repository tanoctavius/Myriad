from cmu_graphics import *
import random 
import math 

class MainCharacter:
    def __init__(self):
        self.onScreenX = app.width//2 - 75
        self.currX = app.width//2 - 75
        self.y = 600
        self.velX = 0
        self.velY = 0
        self.accX = 0.01
        self.accY = 0.1 #Simulation of gravity 
        self.gravityMax = -6
        self.xFriction = 0.1
        self.jumpCount = 0 
        self.characterSizeWidth = 50
        self.characterSizeLength = 60
        self.characterHitBox = (self.currX, self.y, self.characterSizeWidth, self.characterSizeLength)

        '''Base Stats:'''
        self.maxHealth = 180
        self.currHealth = 180
        self.attack = 10 
        self.projectileSpeed = 1
        self.speed = 1
        self.stamina = 10

    def drawMainCharacterSprite(self):
        #Draw the character at the start screen
        if app.paused == True:
            sprite = (app.monsterIdleSprites[app.currMonsterIndex])[0]
            drawImage(sprite, self.onScreenX, self.y, width = app.characterSize, height = app.characterSize)
        #drawRect(self.onScreenX, self.y, 50, 60, fill = None, border = 'black') #Draws the rectangular bounding box around character
        #If character is exploring the game, the character is stationary in one spot 
        if app.paused == False:
            if app.characterAttack == True: 
                sprite = (app.monsterAttackSprites[app.currMonsterIndex])[app.spriteAttackCounter]
                drawImage(sprite, self.onScreenX, self.y, width = app.characterSize, height = app.characterSize)
            elif app.characterMoving == True:
                sprite = (app.monsterWalkSprites[app.currMonsterIndex])[app.spriteWalkCounter]
                drawImage(sprite, self.onScreenX, self.y, width = app.characterSize, height = app.characterSize)
            elif app.characterJumping == True:
                sprite = (app.monsterJumpSprites[app.currMonsterIndex])[app.spriteJumpCounter]
                drawImage(sprite, self.onScreenX, self.y, width = app.characterSize, height = app.characterSize)
            else: 
                sprite = (app.monsterIdleSprites[app.currMonsterIndex])[app.spriteIdleCounter]
                drawImage(sprite, self.onScreenX, self.y, width = app.characterSize, height = app.characterSize)
    
    def getNextObstacle(self):
        for obstacle in range(len(app.obstacles)):
            x, y, w, h = app.obstacles[obstacle][0], app.obstacles[obstacle][1], app.obstacles[obstacle][2], app.obstacles[obstacle][3]
            x1, y1, w1, h1 = self.currX, self.y, self.characterSizeWidth, self.characterSizeLength
            if x1 <= x + w:
                return (app.obstacles[obstacle][0],app.obstacles[obstacle][1], app.obstacles[obstacle][2],app.obstacles[obstacle][3])

    def mainCharacterOnStep(self):
        currObstacle = self.getNextObstacle()
        if currObstacle != None:
            if self.obstacleCollision(currObstacle) == True: 
                if self.obstacleCollisionRight(currObstacle) == True: #Bounces to the right 
                    self.velX *= -1
                elif self.obstacleCollisionBottom(currObstacle) == True: #Bounces to the bottom 
                    self.velY *= -1 #If person hits the bottom of the obstacle, they will bounce back
                elif self.obstacleCollisionTop(currObstacle) == True: 
                    if self.velY < 1:
                        self.velY = 0
                    self.velY *= -0.8 
        app.mainPlayer.itemCollision()
        app.mainPlayer.trapCollision()
        
        #Checks whether the main player collides with the boss, if so, take away health if they are colliding 
        for boss in range(len(app.currBoss)):
            bossPosition = app.currBoss[0][0], app.currBoss[0][1] - int(app.bossWidth) + 40, app.bossWidth, app.bossWidth 
            if app.mainPlayer.obstacleCollision(bossPosition) == True:
                app.currHealth -= 0.3

        #Checking whether the enemy projectiles hit the main player 
        for projectile in range(len(app.enemyProjectiles)):
            enemyProjectile = app.enemyProjectiles[projectile][0], app.enemyProjectiles[projectile][1], app.enemyProjectileWidth, app.enemyProjectileWidth
            if app.mainPlayer.obstacleCollision(enemyProjectile) == True: 
                app.currHealth -= 2
        
        for projectile in range(len(app.enemyProjectiles1)):
            enemyProjectile = app.enemyProjectiles1[projectile][0], app.enemyProjectiles1[projectile][1], app.enemyProjectileWidth, app.enemyProjectileWidth
            if app.mainPlayer.obstacleCollision(enemyProjectile) == True: 
                app.currHealth -= 2

        self.y += self.velY
        self.velY += self.accY
        self.currX += self.velX 

        if self.y == 600: 
            self.jumpCount = 0

        if self.y >= 600:
            self.y = 600 
            self.velY = 0 
        
        if app.bossBattle == True: 
            if self.y + app.characterSize >= 600: 
                self.y = 600 - app.characterSize 
            if self.currX - app.characterSize < 0: 
                self.currX = app.characterSize
            if self.currX + app.characterSize > app.width: 
                self.currX = app.width - app.characterSize

        if app.currHealth < 1: 
            app.endScreen = True
            app.mainScreen = False 

    def jump(self):
        app.characterMoving = False
        app.characterJumping = True 
        self.jumpCount += 1
        if self.jumpCount <= 4:
            self.velY = -100
            if self.velY <= self.gravityMax: 
                self.velY = self.gravityMax 
    
    def moveCharacterRight(self):
        app.characterJumping = False 
        app.characterMoving = True 
        self.velX += 5
        if self.velX > 10:
            self.velX -= self.xFriction
        elif self.velX < 0:
            self.velX += self.xFriction

    def moveCharacterLeft(self):
        app.characterJumping = False 
        app.characterMoving = True 
        self.velX = -self.velX
        if self.velX > 1:
            self.velX -= self.xFriction
        elif self.velX < 0:
            self.velX += self.xFriction

    def stopCharacterMoveLeft(self):
        self.velX = 0
        self.characterMoving = False 

    def stopCharacterMoveRight(self):
        self.velX = 0
        self.characterMoving = False

    def obstacleCollision(self, currObstacle):
        x1, y1, w1, h1 = self.currX, self.y, self.characterSizeWidth, self.characterSizeLength
        x2, y2, w2, h2 = currObstacle
        right0 = x1 + w1
        bottom0 = y1 + h1
        right1 = x2 + w2
        bottom1 = y2 + h2
        if ((right1 >= x1) and (right0 >= x2) and (bottom1 >= y1) and (bottom0 >= y2)):
            return True
        if x2 <= x1 and x1 <= x2 + w2 and y2 <= y1 and y1 <= y2 + h2:
            return True
        return False
    
    def itemCollision(self):
        if app.currItem != []:
            if len(app.currItem) == 1: #If there currently is an item on screen
                currItem = (app.currItem[0][0], app.currItem[0][1], app.sizeItem, app.sizeItem)
                if app.mainPlayer.obstacleCollision(currItem) == True:
                    #Changing attributes based on the collision
                    if app.currItemNum == 0: #chest, randomly gives you health, takes away health or add points
                        num = random.randint(0, 2)
                        if num == 0: #Add Health
                            if app.currHealth + 20 <= app.maxHealth:
                                app.currHealth += 20
                            else:
                                app.currHealth = app.maxHealth
                        if num == 1: #Take away health
                            app.currHealth -= 20
                        if num == 2: #Add score
                            app.currHighScore += 100
                    if app.currItemNum == 1: #coins, adds point
                        app.currHighScore += 200
                    if app.currItemNum == 2: #shield, adds 3 second invincibility
                        app.currHealth += 20
                    if app.currItemNum == 3: #bracelet, faster shooting speed
                        app.currHighScore += 100
                    app.currItem.pop(0)

    def trapCollision(self):
        if app.currTrap != [] and len(app.currTrap) == 1:
            currTrap = (app.currTrap[0][0], app.currTrap[0][1], app.trapWidth, app.trapHeight)
            if app.mainPlayer.obstacleCollision(currTrap) == True:
                app.currHealth -= 0.3
        
        if app.currTopTrap != [] and len(app.currTopTrap) == 1:
            currTopTrap = (app.currTopTrap[0][0], app.currTopTrap[0][1], app.topTrapWidth, app.topTrapHeight)
            if app.mainPlayer.obstacleCollision(currTopTrap) == True:
                app.currHealth -= 0.3
                    
    def obstacleCollisionBottom(self, currObstacle):
        x1, y1, w1, h1 = self.currX, self.y, self.characterSizeWidth, self.characterSizeLength
        x2, y2, w2, h2 = currObstacle
        if (y1) > (y2):
            return True
        return False 

    def obstacleCollisionRight(self, currObstacle): 
        x1, y1, w1, h1 = self.currX, self.y, self.characterSizeWidth, self.characterSizeLength
        x2, y2, w2, h2 = currObstacle
        if (x1) + w1//2 < (x2):
            return True
        return False 
    
    def obstacleCollisionTop(self, currObstacle):
        x1, y1, w1, h1 = self.currX, self.y, self.characterSizeWidth, self.characterSizeLength
        x2, y2, w2, h2 = currObstacle
        if y1 < y2:
            return True
        return False 

def onAttackStep(app):
    app.lineX0 = app.mainPlayer.onScreenX
    app.lineY0 = app.mainPlayer.y

    if app.fireballVisible: 
        newX, newY = getRadiusEnd(app.attackX, app.attackY, 5, app.attackAngle)
        app.attackX, app.attackY = newX, newY
        if (app.attackX + app.attackR <= 0 or app.attackX - app.attackR >= app.width or 
            app.attackY + app.attackR <= 0 or app.attackY - app.attackR >= 600):
            app.fireballVisible = False
        
        #If a fireball hits an obstacle, it will be removed from the screen
        for obstacle in range(len(app.obstacles)):
            fireball = (app.attackX + app.mainPlayer.currX - app.mainPlayer.onScreenX, app.attackY, 20, 20)
            if checkCollision(fireball, app.obstacles[obstacle]):
                app.fireballVisible = False
                app.fireballBurst.append([app.attackX + app.mainPlayer.currX - app.mainPlayer.onScreenX, app.attackY, 20, 20])
        
        for boss in range(len(app.currBoss)):
            fireball = (app.attackX + app.mainPlayer.currX - app.mainPlayer.onScreenX, app.attackY, 20, 20)
            bossPosition = app.currBoss[0][0], app.currBoss[0][1] - int(app.bossWidth) + 40, app.bossWidth, app.bossWidth
            if checkCollision(fireball, bossPosition):
                app.fireballBurst.append([app.attackX + app.mainPlayer.currX - app.mainPlayer.onScreenX, app.attackY, 20, 20])
                app.fireballVisible = False
                app.bossHitCount += 1

#Loosely inspired by Dot Splotter CS3
def getRadiusEnd(x, y, r, z):
    alpha = math.radians(z)
    return (x + r * math.cos(alpha), y - r * math.sin(alpha))

def getDistance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def getEndAngleAndRadius(x, y, targetX, targetY):
    radius = getDistance(x, y, targetX, targetY)
    angle = math.degrees(math.atan2(y - targetY, targetX - x)) % 360
    return (radius, angle)

def drawAttack(app):
    #To ensure the attack comes from the middle 
    drawImage(app.fireballAttack, app.attackX + 15, app.attackY + 25, width = 20, height = 20)
    
def checkCollision(movingObject, stationary):
    x1, y1, w1, h1 = movingObject
    x2, y2, w2, h2 = stationary
    right0 = x1 + w1
    bottom0 = y1 + h1
    right1 = x2 + w2
    bottom1 = y2 + h2
    if ((right1 >= x1) and (right0 >= x2) and (bottom1 >= y1) and (bottom0 >= y2)):
        return True
    if x2 <= x1 and x1 <= x2 + w2 and y2 <= y1 and y1 <= y2 + h2:
        return True
    return False

