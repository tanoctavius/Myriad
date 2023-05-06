from cmu_graphics import *
import random
import button
import character

def drawBackground(app):
    #Background taken from: https://vnitti.itch.io/glacial-mountains-parallax-background/download/eyJleHBpcmVzIjoxNjgxMTU3MzA0LCJpZCI6MTk5OTg3fQ%3d%3d.zWdKLj%2fyd5FMOi75ve85%2b24K35s%3d
    #Stone Platform taken from: https://www.artstation.com/artwork/4Xqg9L 
    drawImage(app.gameScreenBackgroundImage, app.backgroundx1, app.backgroundy1, width = app.width+2, height = app.height)
    drawImage(app.gameScreenBackgroundImage,app.backgroundx2, app.backgroundy2, width = app.width+2, height = app.height)
    drawImage(app.gameScreenPlatform, app.backgroundx1, app.backgroundyfloor1, width = app.width+1, height = app.height//10)
    drawImage(app.gameScreenPlatform, app.backgroundx2, app.backgroundyfloor2, width = app.width+1, height = app.height//10)

def drawObstacles(app):
    #Ensures obstacles are not created too frequently 
    if app.timeSinceLastObstacle % 1 == 0 and len(app.obstacles) <= 2: 
        generateObstacle(app)
    for item in range(len(app.obstacles)):
        drawImage(app.gameScreenBrickPlatform, (app.obstacles[item][0] - app.mainPlayer.currX + app.mainPlayer.onScreenX), app.obstacles[item][1], width = app.obstacles[item][2], height = app.obstacles[item][3])

def drawItem(app):
    if app.timeSinceLastItem % 10 == 0 and len(app.currItem) == 0: 
        generateItem(app)
    if app.currItemNum != None: 
        for item in range(len(app.currItem)):
            drawImage(app.allItems[app.currItemNum], (app.currItem[item][0] - app.mainPlayer.currX + app.mainPlayer.onScreenX), app.currItem[item][1], width = app.sizeItem, height = app.sizeItem)

def drawTrap(app):
    if app.timeSinceLastItem % 10 == 0 and len(app.currTrap) < 1:
        generateTrap(app)
    for item in range(len(app.currTrap)):
        drawImage(app.bearTrap, (app.currTrap[item][0] - app.mainPlayer.currX + app.mainPlayer.onScreenX), app.currTrap[item][1] - app.trapHeight, width = app.trapWidth, height = app.trapHeight)

def drawTopTrap(app):
    if app.timeSinceLastItem % 10 == 0 and len(app.currTopTrap) < 1:
        generateTopTrap(app)
    for item in range(len(app.currTopTrap)):
        drawImage(app.spikeTrap, (app.currTopTrap[item][0] - app.mainPlayer.currX + app.mainPlayer.onScreenX), app.currTopTrap[item][1], width = app.topTrapWidth, height = app.topTrapHeight)

def generateTopTrap(app):
    xPos = random.randint(int(app.mainPlayer.currX + app.width - app.mainPlayer.onScreenX), int(app.mainPlayer.currX + app.width*3))
    yPos = 0
    return app.currTopTrap.append([xPos, yPos])

def generateObstacle(app): 
    #Random obstacle generation
    xPos = random.randint(int(app.mainPlayer.currX + app.width - app.mainPlayer.onScreenX), int(app.mainPlayer.currX + app.width*3))
    yPos = random.randint(75, app.ground - app.characterSize - 5)
    xLen = random.randint(100, 250)
    yLen = random.randint(40, 60)
    tempObstacle = [xPos, yPos, xLen, yLen]

    #Recursion to check that the obstacles are not too close to each other 
    if overlap(app, tempObstacle) == False: 
        app.obstacles.append([xPos, yPos, xLen, yLen])
        return  
    else: 
        generateObstacle(app)

def generateItem(app):
    if len(app.obstacles) > 0:
        num = random.randint(0, len(app.obstacles)-1)
        x2, y2, w2, h2 = app.obstacles[num][0], app.obstacles[num][1], app.obstacles[num][2], app.obstacles[num][3]
        return app.currItem.append([x2  + w2//2 - app.sizeItem//2, y2 - app.sizeItem, w2, h2])
    
def generateTrap(app):
    xPos = random.randint(int(app.mainPlayer.currX + app.width - app.mainPlayer.onScreenX), int(app.mainPlayer.currX + app.width*3))
    yPos = 600 + app.characterSize
    return app.currTrap.append([xPos, yPos])

def onStepTerrainGeneration(app):
    #Background with varying speeds 
    if app.backgroundx1 == -app.width: 
        app.backgroundx1 = app.backgroundx2 + app.width
    if app.backgroundx2 == -app.width: 
        app.backgroundx2 = app.backgroundx1 + app.width
    
    if app.characterMoving == True:
        app.backgroundx1 -= 10 
        app.backgroundx2 -= 10

    #Obstacle 
    app.timeSinceLastObstacle += 1
    for i in range(len(app.obstacles)):
        if app.obstacles[i][0] + app.obstacles[i][2] - app.mainPlayer.currX + app.mainPlayer.onScreenX<= 0: 
            app.obstacles.pop(i) #pops the obstacle if it is the negative of its width
            break 

    #Item:
    app.timeSinceLastItem += 1
    for i in range(len(app.currItem)):
        if app.currItem[i][0] * 1.3 - app.mainPlayer.currX + app.mainPlayer.onScreenX<= 0:
            app.currItem.pop(i) #Pops off the existing item once it leaves the screen
            break 

    for i in range(len(app.currTrap)):
        if app.currTrap[i][0] + app.trapWidth - app.mainPlayer.currX + app.mainPlayer.onScreenX < 0:
            app.currTrap.pop(i)
            break

    if app.timeSinceLastItem % 20 == 0 and len(app.currItem) == 0: 
        num = random.randint(0, len(app.allItems) - 1)
        app.currItemNum = num
    
    for i in range(len(app.currTopTrap)):
        if app.currTopTrap[i][0] + app.topTrapWidth - app.mainPlayer.currX + app.mainPlayer.onScreenX < 0:
            app.currTopTrap.pop(i)
            break
    
#Checks if the obstacles are too close to each other 
def overlap(app, newObstacle): 
    for item in range(len(app.obstacles)): 
        if abs(app.obstacles[item][1] - (newObstacle[1])) <= 65: #If obstacles are too close on the y-axis
            return True
        if ((newObstacle[0]) - (app.obstacles[item][0] + app.obstacles[item][2])) <= 0: #Ensures obstacles are further on x-axis
            return True 
    return False 

def drawHealth(app):
    xLocation = 80 
    yLocation = app.rectButtonMainScreenLength * 3/4 + 10
    drawRect(xLocation - 4, yLocation - 4, app.maxHealth + 8, 24, fill = app.healthSide)
    drawRect(xLocation, yLocation, app.maxHealth, 16, fill = app.healthBackgroundColour)

    #Getting the health bar's rgb values 
    rgbMax = 255
    red = int((app.maxHealth - app.currHealth) / app.maxHealth * rgbMax)
    green = int(app.currHealth / app.maxHealth * rgbMax)
    blue = 0 
    drawRect(xLocation, yLocation, int(app.currHealth), 16, fill = rgb(red, green, blue))

def drawButtons(app):
    for item in range(4):
        drawRect(((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*item)), app.rectButtonMainScreenLength * 3/4 , app.rectButtonMainScreenLength, app.rectButtonMainScreenLength, 
                 fill = 'lightGray', border = 'black', borderWidth = 3)
        
    #Draw Pause Button: 
    drawLabel('S',((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*3)) + app.rectButtonMainScreenLength//2, 
             app.rectButtonMainScreenLength * 3/4 + app.rectButtonMainScreenLength//2 - 1, bold = True, size = 24)
    drawLabel('i',((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*2)) + app.rectButtonMainScreenLength//2, 
             app.rectButtonMainScreenLength * 3/4 + app.rectButtonMainScreenLength//2, bold = True, size = 16)
    drawCircle(((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*2)) + app.rectButtonMainScreenLength//2, 
               app.rectButtonMainScreenLength * 3/4 + app.rectButtonMainScreenLength//2, 11, fill = None, borderWidth = 2, border = 'black')
    drawLabel('HS',((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*1)) + app.rectButtonMainScreenLength//2, 
             app.rectButtonMainScreenLength * 3/4 + app.rectButtonMainScreenLength//2 - 1, bold = True, size = 18)
    drawLabel('R',((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*0)) + app.rectButtonMainScreenLength//2, 
             app.rectButtonMainScreenLength * 3/4 + app.rectButtonMainScreenLength//2 - 1, bold = True, size = 18)
    
def drawTime(app):
    #Get the minutes and seconds of the time 
    if app.minutes < 10 and app.seconds < 10: 
        drawLabel(f'0{app.minutes}:0{app.seconds}', app.timePlacementX, app.timePlacementY, bold = True, font = 'Euphemia', size = 20)
    if app.minutes < 10 and app.seconds >= 10: 
        drawLabel(f'0{app.minutes}:{app.seconds}', app.timePlacementX, app.timePlacementY, bold = True, font = 'Euphemia', size = 20)
    if app.minutes >= 10 and app.seconds >= 10: 
        drawLabel(f'{app.minutes}:{app.seconds}', app.timePlacementX, app.timePlacementY, bold = True, font = 'Euphemia', size = 20)
    if app.minutes >= 10 and app.seconds < 10: 
        drawLabel(f'{app.minutes}:0{app.seconds}', app.timePlacementX, app.timePlacementY, bold = True, font = 'Euphemia', size = 20)

def drawHighScore(app):
    #Draw the High Score of the Current Game:
    if app.currHighScore < 10:
        drawLabel(f'Score: 000{app.currHighScore}', app.highScorePlacementX, app.highScorePlacementY, bold = True, font = 'Euphemia', size = 20)
    if app.currHighScore < 100 and app.currHighScore >= 10:
        drawLabel(f'Score: 00{app.currHighScore}', app.highScorePlacementX, app.highScorePlacementY, bold = True, font = 'Euphemia', size = 20)
    if app.currHighScore < 1000 and app.currHighScore >= 100:
        drawLabel(f'Score: 0{app.currHighScore}', app.highScorePlacementX, app.highScorePlacementY, bold = True, font = 'Euphemia', size = 20)
    if app.currHighScore < 10000 and app.currHighScore >= 1000:
        drawLabel(f'Score: {app.currHighScore}', app.highScorePlacementX, app.highScorePlacementY, bold = True, font = 'Euphemia', size = 20)

def drawCountDownTime(app):
    if app.countDownSeconds == 1:
        button.Label.drawLabel(app.countDownTimer3)
    if app.countDownSeconds == 2:
        button.Label.drawLabel(app.countDownTimer2)
    if app.countDownSeconds == 3:
        button.Label.drawLabel(app.countDownTimer1)
    if app.countDownSeconds == 4:
        button.Label.drawLabel(app.countDownTimerStart)