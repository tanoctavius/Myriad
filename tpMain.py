from cmu_graphics import *
from PIL import Image
import random 
import terrain 
import shop 
import startScreen 
import endScreen 
import infoScreen
import button
import character
import os, pathlib
import boss
import highScoreScreen
import sys 

#-------------------------------------------------------------------------------
def onAppStart(app):
    #add a countdown text after the main game started
    '''App Size'''
    app.width = 1000
    app.height = 700
    
    '''Screens:'''
    app.shopScreen = False           
    app.mainScreen = False           
    app.startScreen = True           
    app.endScreen = False      
    app.infoScreen = False  
    app.highScoreScreen = False 

    '''High Scores:'''    
    app.allScores = [ ]

    #Changing the recursion limit 
    sys.setrecursionlimit(3000)

    reset(app) #Once the user presses restart, reset values

#-------------------------------------------------------------------------------
def reset(app):
    '''Main GamePlay Screen:'''
    #App Status: 
    app.paused = True 
    app.shopScreen = True

    #Current High Score 
    app.currHighScore = 0

    #Initialising Character Class
    app.mainPlayer = character.MainCharacter() #Initialises the main character Class

    #Initialising Boss Classes:
    app.ogre = boss.boss(200, 15, 96, 3)
    app.plant = boss.boss(220, 14, 96, 5)
    app.shaman = boss.boss(160, 25, 96, 2)
    app.tribe = boss.boss(180, 20, 96, 4)
    app.bossList = [app.ogre, app.plant, app.shaman, app.tribe]

    #Ground:
    app.ground = 600 #Where the character can run on + everytime the ground is touched, the jumps recharge back to 4

    #Background of varying speeds
    app.backgroundx1 = 0
    app.backgroundy1 = 0
    app.backgroundx2 = app.backgroundx1 + app.width
    app.backgroundy2 = 0
    app.backgroundyfloor1 = 660
    app.backgroundyfloor2 = 660

    #Time Elapsed:
    app.minutes = 0
    app.seconds = 0
    app.steps = 0
    app.testVariable = None
    app.timePlacementX, app.timePlacementY = (360, 42)
    app.countDownSteps = 0
    app.countDownSeconds = 0
    app.countDownSecondsPassed = 0

    #Obstacle
    app.obstacles = []
    app.timeSinceLastObstacle = 0

    #Item: 
    app.timeSinceLastItem = 0

    #Health bar in the mainScreen
    app.healthSide = 'steelBlue'
    app.healthBackgroundColour = 'navy'

    #All image casting techniques taken from 15112 Piazza 
    #Background Image Casting:
    #Both platform and background taken from https://craftpix.net/freebies/page/3/ 
    app.secondsPassed = 0 
    app.gameScreenBackgroundImage = Image.open('tempBackground.PNG')
    app.gameScreenBackgroundImage = CMUImage(app.gameScreenBackgroundImage)
    app.gameScreenPlatform = openImage('platform/terrainFloor.PNG')
    app.gameScreenPlatform = CMUImage(app.gameScreenPlatform)

    #Buttons on the right of the main screen: 
    app.rectButtonMainScreenLength = 34
    app.rectButtonMainScreenMostLeft = 786
    app.mainScreenPauseButtonBounds = ((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*3), app.rectButtonMainScreenLength,
                                       app.rectButtonMainScreenLength * 3/4 - 1, app.rectButtonMainScreenLength)
    app.mainScreenMusicButtonBounds = ((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*2), app.rectButtonMainScreenLength,
                                       app.rectButtonMainScreenLength * 3/4 - 1, app.rectButtonMainScreenLength)
    app.mainScreenHighScoreButtonBounds = ((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*1), app.rectButtonMainScreenLength,
                                       app.rectButtonMainScreenLength * 3/4 - 1, app.rectButtonMainScreenLength)
    app.mainScreenRestartButtonBounds = ((app.rectButtonMainScreenMostLeft + (app.rectButtonMainScreenLength * 1.5)*0), app.rectButtonMainScreenLength,
                                       app.rectButtonMainScreenLength * 3/4 - 1, app.rectButtonMainScreenLength)

    #High Score: 
    app.currHighScore = 0
    app.highScorePlacementX, app.highScorePlacementY = (550, 42)

    #Countdown Timer to starting game: 
    app.countDownTimer3 = button.Label('3', (app.width//2, app.height//2), 80, 'impact', 'royalBlue', 'center', True)
    app.countDownTimer2 = button.Label('2', (app.width//2, app.height//2), 80, 'impact', 'royalBlue', 'center', True)
    app.countDownTimer1 = button.Label('1', (app.width//2, app.height//2), 80, 'impact', 'royalBlue', 'center', True)
    app.countDownTimerStart = button.Label('START', (app.width//2, app.height//2), 80, 'impact', 'mediumBlue', 'center', True)

    #Initialising Platform Values:
    #Game platform taken from: https://dribbble.com/shots/7179744-Boss-Monsters-Pixel-Art-Game-Sprites
    app.gameScreenBrickPlatform = openImage('platform/platformFinal.png')
    app.gameScreenBrickPlatform = CMUImage(app.gameScreenBrickPlatform)

    '''Initialising Steps per Second'''
    app.stepsPerSecond = 40

    '''Starting Screen:'''
    #Initialised Name: 
    app.name = None 

    '''Shop Screen'''
    #Rectangular Values for Buttons
    app.rectWidth = 200
    app.rectLength = 270
    app.rectMostLeft = 150
    app.beginningWidthApart = 250
    app.rectHeight = 225
    app.statsRectTop = 460
    app.statsRectHeight = 200
    app.selectedRectIndex = None
    app.borderColour = 'black'
    app.RectHoverIndex = None 

    #Arrow Values: 
    app.arrowLeft = 50
    app.arrowHeight = app.height//2 - 50
    app.arrowWidth = 50
    app.arrowLength = 50
    app.selectedArrowIndex = None 

    #Casting Images using CMUImages: 
    #All sprites sourced from: https://craftpix.net/freebies/page/3/
    app.shopSpriteLength = 160
    app.pinkMonster = openImage('sprite/pinkMonster.png')
    app.pinkMonster = CMUImage(app.pinkMonster)
    app.owlMonster = openImage('sprite/owlMonster.png')
    app.owlMonster = CMUImage(app.owlMonster)
    app.dudeMonster = openImage('sprite/dudeMonster.png')
    app.dudeMonster = CMUImage(app.dudeMonster)
    app.characters = [app.pinkMonster, app.owlMonster, app.dudeMonster]
    app.shopScreenBackground = Image.open('shopbackground2.JPG')
    app.shopScreenBackground = CMUImage(app.shopScreenBackground)

    #Initialising cancel button at side of the screen: 
    app.shopScreenCancelButtonLeft = 715
    app.shopScreenCancelButtonTop = 130
    app.shopScreenCancelButtonWidth = 35
    app.shopScreenCancelButtonLength = 35
    app.shopScreenCancelButtonFillColour = 'salmon'
    app.shopScreenCancelButton = button.Button((app.shopScreenCancelButtonLeft, app.shopScreenCancelButtonTop, app.shopScreenCancelButtonWidth, app.shopScreenCancelButtonLength),
                                         app.shopScreenCancelButtonFillColour, 'black', 3)
    app.shopScreenCancelButton = button.Label('X', (app.shopScreenCancelButtonLeft + app.shopScreenCancelButtonWidth//2, app.shopScreenCancelButtonTop + app.shopScreenCancelButtonLength//2),
                                             20, 'arial', 'darkRed', 'center', True)
    
    '''Start Screen:'''
    #Start Screen Button Values:
    app.startGameRectWidth = 400
    app.startGameRectLength = 85
    app.startGameRectLeft = app.width//2 - app.startGameRectWidth//2
    app.startGameRectTop = app.height//2 + app.startGameRectLength - 20
    app.startScreenRect = 'lightGray'
    app.squareButtonWidth = 50
    app.startHoverIndex = None

    #Initialising the buttons using the Button Class:
    app.startScreenLargeButton = button.Button((app.startGameRectLeft, app.startGameRectTop, app.startGameRectWidth, app.startGameRectLength),
                                        app.startScreenRect, 'black', 5)
    app.startScreenLargeLabel = button.Label('s t a r t', (app.startGameRectLeft + app.startGameRectWidth//2, app.startGameRectTop + app.startGameRectLength//2),
                                           40, 'impact', 'black', 'center', False)
    app.endScreenLargeLabel = button.Label('r e s t a r t', (app.startGameRectLeft + app.startGameRectWidth//2, app.startGameRectTop + app.startGameRectLength//2),
                                           40, 'impact', 'black', 'center', False)
    app.startScreenMusicLabel = button.Label('HS', (app.width - (app.squareButtonWidth * 0.677), app.height - app.squareButtonWidth -2),
                                             26, 'impact', 'black', 'right', True)
    app.startScreenInformationLabel = button.Label(('i'), (app.width - (3.91 * app.squareButtonWidth), app.height - app.squareButtonWidth),
                                                   20, 'impact', 'black', 'right', False)
    app.startScreenShopLabel = button.Label('S', (app.width - (app.squareButtonWidth * 2.3), app.height - app.squareButtonWidth), 
                                            26, 'impact', 'black', 'right', True)
    
    #Initialising the background Image: 
    #Background sourced from: https://craftpix.net/freebies/page/3/
    app.startScreenBackgroundImage = Image.open("shopbackground2.JPG")
    app.startScreenBackgroundImage = CMUImage(app.startScreenBackgroundImage)

    '''Info Screen:'''
    #Initialising the background Images: 
    #Info screen sourced from: https://craftpix.net/freebies/
    app.infoScreenBackgroundImage = Image.open('infoScreen.png')
    app.infoScreenBackgroundImage = CMUImage(app.infoScreenBackgroundImage)

    #Cancel Button Values: 
    app.infoScreenButtonLeft = 870
    app.infoScreenButtonTop = 70
    app.infoScreenButtonWidth = 35
    app.infoScreenButtonLength = 35
    app.shopScreenButtonWidth = 100
    app.shopScreenButtonLength = 40
    app.shopScreenButtonLeft = app.width//2 - app.shopScreenButtonWidth//2
    app.shopScreenButtonTop = 30
    app.startShopScreenButtonWidth = 300
    app.startShopScreenButtonLength = 60
    app.startShopScreenButtonLeft = app.width//2 - app.startShopScreenButtonWidth//2
    app.startShopScreenButtonTop = 100
    app.infoScreenButtonFillColour = 'lightCoral'
    app.startShopScreenButtonColour = 'mediumSeaGreen'
    app.infoScreenButton = button.Button((app.infoScreenButtonLeft, app.infoScreenButtonTop, app.infoScreenButtonWidth, app.infoScreenButtonLength),
                                         app.infoScreenButtonFillColour, 'black', 3)
    app.infoScreenButtonLabel = button.Label('X', (app.infoScreenButtonLeft + app.infoScreenButtonWidth//2, app.infoScreenButtonTop + app.infoScreenButtonLength//2),
                                             20, 'arial', 'darkRed', 'center', True)
    app.shopScreenButton = button.Button((app.shopScreenButtonLeft, app.shopScreenButtonTop, app.shopScreenButtonWidth, app.shopScreenButtonLength),
                                         app.infoScreenButtonFillColour, 'black', 5)
    app.shopScreenButtonLabel = button.Label('B A C K', (app.shopScreenButtonLeft + app.shopScreenButtonWidth//2, app.shopScreenButtonTop + app.shopScreenButtonLength//2),
                                             14, 'impact', 'lightGray', 'center', True)
    app.startShopScreenButton = button.Button((app.startShopScreenButtonLeft, app.startShopScreenButtonTop, app.startShopScreenButtonWidth, app.startShopScreenButtonLength),
                                         app.startShopScreenButtonColour, 'black', 5)
    app.startShopScreenButtonLabel = button.Label('S E L E C T', (app.startShopScreenButtonLeft + app.startShopScreenButtonWidth//2, app.startShopScreenButtonTop + app.startShopScreenButtonLength//2),
                                             30, 'impact', 'darkGreen', 'center', True)


    '''Sprites: Main Characters''' 
    #All sprites (from both the characters + bosses) taken from: https://dribbble.com/shots/6975155-Free-Tiny-Hero-Sprites 
    app.characterSize = 60
    #Pink Monster: 
    #PinkMonster Walking:
    spritestrip = openImage('sprite/pinkMonsterWalk.png')
    app.pinkMonsterWalkSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.pinkMonsterWalkSprites.append(sprite)
    app.spriteWalkCounter = 0

    #PinkMonster Jumping:
    spritestrip = openImage('sprite/pinkMonsterJump.png')   
    app.pinkMonsterJumpSprites = [ ]
    for i in range(8):
        #Sprite for walking 
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.pinkMonsterJumpSprites.append(sprite)
    app.spriteJumpCounter = 0

    #Pink Monster Idle: 
    spritestrip = openImage('sprite/pinkMonsterIdle.png')   
    app.pinkMonsterIdleSprites = [ ]
    for i in range(4):
        #Sprite for walking 
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.pinkMonsterIdleSprites.append(sprite)
    app.spriteIdleCounter = 0

    #Pink Monster Attack: 
    spritestrip = openImage('sprite/pinkMonsterAttack.png')   
    app.pinkMonsterAttackSprites = [ ]
    for i in range(6):
        #Sprite for walking 
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.pinkMonsterAttackSprites.append(sprite)
    app.spriteAttackCounter = 0

    #Dude Monster:
    #DudeMonster Walking:
    spritestrip = openImage('sprite/dudeMonsterRun.png')
    app.dudeMonsterWalkSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.dudeMonsterWalkSprites.append(sprite)
    app.spriteWalkCounter = 0

    #DudeMonster Jumping:
    spritestrip = openImage('sprite/dudeMonsterJump.png')   
    app.dudeMonsterJumpSprites = [ ]
    for i in range(8):
        #Sprite for walking 
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.dudeMonsterJumpSprites.append(sprite)
    app.spriteJumpCounter = 0

    #DudeMonster Idle: 
    spritestrip = openImage('sprite/dudeMonsterIdle.png')   
    app.dudeMonsterIdleSprites = [ ]
    for i in range(4):
        #Sprite for walking 
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.dudeMonsterIdleSprites.append(sprite)
    app.spriteIdleCounter = 0

    #DudeMonster Attack: 
    spritestrip = openImage('sprite/dudeMonsterAttack.png')   
    app.dudeMonsterAttackSprites = [ ]
    for i in range(6):
        #Sprite for walking 
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.dudeMonsterAttackSprites.append(sprite)
    app.spriteAttackCounter = 0

    #Owl Monster:
    #OwlMonster Walking:
    spritestrip = openImage('sprite/owlMonsterRun.png')
    app.owlMonsterWalkSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.owlMonsterWalkSprites.append(sprite)
    app.spriteWalkCounter = 0

    #OwlMonster Jumping:
    spritestrip = openImage('sprite/owlMonsterJump.png')   
    app.owlMonsterJumpSprites = [ ]
    for i in range(8):
        #Sprite for walking 
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.owlMonsterJumpSprites.append(sprite)
    app.spriteJumpCounter = 0

    #OwlMonster Idle: 
    spritestrip = openImage('sprite/owlMonsterIdle.png')   
    app.owlMonsterIdleSprites = [ ]
    for i in range(4):
        #Sprite for walking 
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.owlMonsterIdleSprites.append(sprite)
    app.spriteIdleCounter = 0

    #OwlMonster Attack: 
    spritestrip = openImage('sprite/owlMonsterAttack.png')   
    app.owlMonsterAttackSprites = [ ]
    for i in range(6):
        #Sprite for walking 
        sprite = CMUImage(spritestrip.crop((32*i, 0, 32 + 32*i, 32.5)))
        app.owlMonsterAttackSprites.append(sprite)
    app.spriteAttackCounter = 0

    #Character Status:
    app.maxHealth = 180
    app.currHealth = 180 #If collision, reduce overall health
    app.characterJumping = False
    app.characterMoving = False 
    app.characterAttack = False 
    app.bossBattle = False  

    '''Sprites: Bosses'''
    #All boss sprites sourced from: https://craftpix.net/freebies/ 
    #PlantBoss
    app.plantBossWidth = 96
    app.plantBossHeight = 96
    #plantBoss Walking:
    spritestrip = openImage('sprite/plantBossWalk.png')
    app.plantBossWalkSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.plantBossWalkSprites.append(sprite)
    app.spriteWalkCounter = 0

    #plantBoss Attacking:
    spritestrip = openImage('sprite/plantBossAttack.png')   
    app.plantBossAttackSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.plantBossAttackSprites.append(sprite)
    app.spriteAttackCounter = 0

    #plantBoss Idle: 
    spritestrip = openImage('sprite/plantBossIdle.png')   
    app.plantBossIdleSprites = [ ]
    for i in range(4):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.plantBossIdleSprites.append(sprite)
    app.spriteIdleCounter = 0

    #plantBoss Death: 
    spritestrip = openImage('sprite/plantBossDeath.png')   
    app.plantBossDeathSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.plantBossDeathSprites.append(sprite)
    app.spriteDeathCounter = 0

    #plantBoss Hurt: 
    spritestrip = openImage('sprite/plantBossHurt.png')   
    app.plantBossHurtSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.plantBossHurtSprites.append(sprite)
    app.spriteHurtCounter = 0

    #shamanBoss
    app.shamanBossWidth = 96
    app.shamanBossHeight = 96
    #plantBoss Walking:
    spritestrip = openImage('sprite/shamanWalk.png')
    app.shamanBossWalkSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.shamanBossWalkSprites.append(sprite)
    app.spriteWalkCounter = 0

    #shamanBoss Attacking:
    spritestrip = openImage('sprite/shamanAttack.png')   
    app.shamanBossAttackSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.shamanBossAttackSprites.append(sprite)
    app.spriteAttackCounter = 0

    #shamanBoss Idle: 
    spritestrip = openImage('sprite/shamanIdle.png')   
    app.shamanBossIdleSprites = [ ]
    for i in range(4):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.shamanBossIdleSprites.append(sprite)
    app.spriteIdleCounter = 0

    #shamanBoss Death: 
    spritestrip = openImage('sprite/shamanDeath.png')   
    app.shamanBossDeathSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.shamanBossDeathSprites.append(sprite)
    app.spriteDeathCounter = 0

    #shamanBoss Hurt: 
    spritestrip = openImage('sprite/shamanHurt.png')   
    app.shamanBossHurtSprites = [ ]
    for i in range(4):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.shamanBossHurtSprites.append(sprite)
    app.spriteHurtCounter = 0

    #tribeBoss
    app.tribeBossWidth = 96
    app.tribeBossHeight = 96
    #tribeBoss Walking:
    spritestrip = openImage('sprite/tribeWalk.png')
    app.tribeBossWalkSprites = [ ]
    for i in range(6):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.tribeBossWalkSprites.append(sprite)
    app.spriteWalkCounter = 0

    #tribeBoss Attacking:
    spritestrip = openImage('sprite/tribeAttack.png')   
    app.tribeBossAttackSprites = [ ]
    for i in range(4):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.tribeBossAttackSprites.append(sprite)
    app.spriteAttackCounter = 0

    #tribeBoss Idle: 
    spritestrip = openImage('sprite/tribeIdle.png')   
    app.tribeBossIdleSprites = [ ]
    for i in range(5):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.tribeBossIdleSprites.append(sprite)
    app.spriteIdleCounter = 0

    #tribeBoss Death: 
    spritestrip = openImage('sprite/tribeDead.png')   
    app.tribeBossDeathSprites = [ ]
    for i in range(5):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.tribeBossDeathSprites.append(sprite)
    app.spriteDeathCounter = 0

    #tribeBoss Hurt: 
    spritestrip = openImage('sprite/tribeHurt.png')   
    app.tribeBossHurtSprites = [ ]
    for i in range(2):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.tribeBossHurtSprites.append(sprite)
    app.spriteHurtCounter = 0

    #ogreBoss
    app.ogreBossWidth = 96
    app.orgeBossHeight = 96
    #orgeBoss Walking:
    spritestrip = openImage('sprite/ogreWalk.png')
    app.ogreBossWalkSprites = [ ]
    for i in range(5):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.ogreBossWalkSprites.append(sprite)
    app.spriteWalkCounter = 0

    #ogreBoss Attacking:
    spritestrip = openImage('sprite/ogreAttack.png')   
    app.ogreBossAttackSprites = [ ]
    for i in range(5):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.ogreBossAttackSprites.append(sprite)
    app.spriteAttackCounter = 0

    #ogreBoss Idle: 
    spritestrip = openImage('sprite/ogreIdle.png')   
    app.ogreBossIdleSprites = [ ]
    for i in range(5):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.ogreBossIdleSprites.append(sprite)
    app.spriteIdleCounter = 0

    #ogreBoss Death: 
    spritestrip = openImage('sprite/ogreDead.png')   
    app.ogreBossDeathSprites = [ ]
    for i in range(4):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.ogreBossDeathSprites.append(sprite)
    app.spriteDeathCounter = 0

    #ogreBoss Hurt: 
    spritestrip = openImage('sprite/ogreHurt.png')   
    app.ogreBossHurtSprites = [ ]
    for i in range(2):
        sprite = CMUImage(spritestrip.crop((96*i, 0, 96 + 96*i, 96.5)))
        app.ogreBossHurtSprites.append(sprite)
    app.spriteHurtCounter = 0
    
    '''Current Character Class:'''
    app.currMonsterIndex = 0
    app.monsterIdleSprites = [app.pinkMonsterIdleSprites, app.owlMonsterIdleSprites, app.dudeMonsterIdleSprites]
    app.monsterWalkSprites = [app.pinkMonsterWalkSprites, app.owlMonsterWalkSprites, app.dudeMonsterWalkSprites]
    app.monsterAttackSprites = [app.pinkMonsterAttackSprites, app.owlMonsterAttackSprites, app.dudeMonsterAttackSprites]
    app.monsterJumpSprites = [app.pinkMonsterJumpSprites, app.owlMonsterJumpSprites, app.dudeMonsterJumpSprites]

    '''Current Boss Class:'''
    app.currBossIndex = 0 
    app.bossWidth = 180
    app.bossIdleSprites = [app.plantBossIdleSprites, app.shamanBossIdleSprites, app.tribeBossIdleSprites, app.ogreBossIdleSprites]
    app.bossWalkSprites = [app.plantBossWalkSprites, app.shamanBossWalkSprites, app.tribeBossWalkSprites, app.ogreBossWalkSprites]
    app.bossAttackSprites = [app.plantBossAttackSprites, app.shamanBossAttackSprites, app.tribeBossAttackSprites, app.ogreBossAttackSprites]
    app.bossHurtSprites = [app.plantBossHurtSprites, app.shamanBossHurtSprites, app.tribeBossHurtSprites, app.ogreBossHurtSprites]
    app.bossDeathSprites = [app.plantBossDeathSprites, app.shamanBossDeathSprites, app.tribeBossDeathSprites, app.ogreBossDeathSprites]

    '''Initialising All Game Items'''
    #All images sourced from https://craftpix.net/freebies/ 
    #Chest Item: 
    app.chestItem = openImage('Items/chest.png')  
    app.chestItem = CMUImage(app.chestItem)

    #Coins Item:
    app.coinsItem = openImage('Items/coins.png')  
    app.coinsItem = CMUImage(app.coinsItem)
    
    #Shield item
    app.shieldItem = openImage('Items/shield.png')  
    app.shieldItem = CMUImage(app.shieldItem)

    #Enemy magic projectile: 
    app.magicProjectile = openImage('Items/magic.png')
    app.magicProjectile = CMUImage(app.magicProjectile)

    #Spike 
    app.spikeTrap = openImage('Items/spike.png')
    app.spikeTrap = CMUImage(app.spikeTrap)

    #projectileSpeedBracelet item: 
    app.projectileSpeedBraceletItem = openImage('Items/projectileSpeedBracelet.png')
    app.projectileSpeedBraceletItem = CMUImage(app.projectileSpeedBraceletItem)

    app.allItems = [app.chestItem, app.coinsItem, app.shieldItem, app.projectileSpeedBraceletItem]
    app.currItem = []
    app.currBoss =  []
    app.currBossGround = 0
    app.enemyProjectiles = []
    app.enemyProjectileWidth = 20 
    app.currBossYVelocity = 0
    app.currItemNum = None 
    app.sizeItem = 40
    app.currBossSide1 = 0
    app.currBossSide2 = 0

    '''High Score Screen:'''
    app.xNameCord = 400
    app.xScoreCord = 500
    app.xTimeCord = 600
    app.yTopCord = 250
    app.highScoreFont = 'impact'
    app.startScreenSize = 36

    #Background Image sourced from: https://craftpix.net/freebies/ 
    app.highScoreBackground = openImage('highScoreBackground.png')  
    app.highScoreBackground = CMUImage(app.highScoreBackground)

    '''Boss Battle:'''
    #Image taken from: https://craftpix.net/freebies/ 
    app.bossBattleLabel = openImage('platform/bossBattle.png')
    app.bossBattleLabel = CMUImage(app.bossBattleLabel)
    app.bossBattleLabelLength = 150
    app.bossScreenCount = 0
    app.timeSinceLastBoss = 0
    app.currBossNum = None 
    app.bossAttackCounter = 0
    app.bossHitCount = 0
    app.deadBoss = [] 
    app.enemyProjectiles1 = []

    '''Attack'''
    #Image taken from: https://craftpix.net/freebies/free-pixel-art-tiny-hero-sprites/ 
    #Code is partly inspired by CS3 5.2.4
    app.fireballAttack = openImage('items/fireball.png')
    app.fireballAttack = CMUImage(app.fireballAttack)
    app.fireballBurstImage = openImage('items/fireballBurst.png')
    app.fireballBurstImage = CMUImage(app.fireballBurstImage)
    app.fireballBurst = []
    app.lineX0 = app.mainPlayer.onScreenX
    app.lineY0 = app.mainPlayer.y
    app.lineLength = 5
    app.lineAngle = 90
    app.lineX1 = app.mainPlayer.currX + 5
    app.lineY1 = app.mainPlayer.y + 5
    app.fireballVisible = False
    app.attackX = 0
    app.attackY = 0
    app.attackR = 10
    app.attackAngle = 0

    '''Trap:'''
    #Image taken from: https://craftpix.net/freebies/
    app.bearTrap = openImage('items/bearTrap.png')
    app.bearTrap = CMUImage(app.bearTrap)
    app.trapWidth = 80
    app.trapHeight = 20
    app.currTrap = []
    app.currTopTrap = []
    app.topTrapWidth = 80
    app.topTrapHeight = 40

#-------------------------------------------------------------------------------
def redrawAll(app):
    '''Main Gameplay Screen:'''
    if app.mainScreen == True: 
        terrain.drawBackground(app)
        terrain.drawObstacles(app)
        terrain.drawHealth(app)
        terrain.drawTime(app)
        terrain.drawButtons(app)
        terrain.drawHighScore(app)
        terrain.drawCountDownTime(app)
        terrain.drawItem(app)
        terrain.drawTrap(app)
        terrain.drawTopTrap(app)
        app.tribe.drawBoss()
        boss.drawEnemyProjectile(app)
        app.mainPlayer.drawMainCharacterSprite()
        if app.fireballVisible:
            character.drawAttack(app)

    '''Shop Screen:'''
    if app.shopScreen == True:
        shop.drawBackground(app)
        shop.drawCharacterRectangle(app)
        shop.drawButton(app)

    '''Start Screen:'''
    if app.startScreen == True: 
        startScreen.drawStartScreen(app)
        startScreen.drawStartScreenButtons(app)
        startScreen.drawSquareButtons(app)
        
    '''End Screen:'''
    if app.endScreen == True: 
        endScreen.drawEndScreen(app)
        endScreen.drawResetButton(app)

    '''Info Screen:'''
    if app.infoScreen == True: 
        infoScreen.drawInfoScreen(app)
        infoScreen.drawButton(app)

    '''High Score Screen:'''
    if app.highScoreScreen == True: 
        highScoreScreen.highScoreBackground(app)
        highScoreScreen.highScoreScreenButton(app)
        highScoreScreen.drawFinalHighScoreScreen(app)
            

#-------------------------------------------------------------------------------
def onStep(app):
    '''Main Screen:'''
    if app.mainScreen == True and app.paused == False: 
        app.steps += 1 
        if app.characterMoving == True:
            terrain.onStepTerrainGeneration(app)
        character.onAttackStep(app)
        boss.onStepBoss(app)

        #Counting the time on one round
        if app.steps % app.stepsPerSecond == 0: 
            app.secondsPassed += 1 
            app.minutes = (app.secondsPassed // 60)
            app.seconds = app.secondsPassed % 60
            if len(app.currBoss) == 0:
                app.timeSinceLastBoss += 1
            if len(app.currBoss) > 0:
                app.timeSinceLastBoss = 0

        if app.spriteAttackCounter % 5 == 0:
            app.characterAttack = False 
    
    if app.mainScreen == True and app.paused == True: 
        app.countDownSteps += 1
        if app.countDownSteps % app.stepsPerSecond == 0:
            app.countDownSecondsPassed += 1
            app.countDownSeconds = app.countDownSecondsPassed % 60
            if app.countDownSeconds == 1:
                app.mainPlayer.jump()
        if app.countDownSeconds == 5: #Game will start in inputed no. of seconds
            app.paused = False

    #Sprite Character Counter:
    if app.steps * 2 % app.stepsPerSecond == 0: 
        app.spriteWalkCounter = (app.spriteWalkCounter + 1) % len(app.pinkMonsterWalkSprites)
        app.spriteJumpCounter = (app.spriteJumpCounter + 1) % len(app.pinkMonsterJumpSprites)
        app.spriteIdleCounter = (app.spriteJumpCounter + 1) % len(app.pinkMonsterIdleSprites)
        app.spriteAttackCounter = (app.spriteJumpCounter + 1) % len(app.pinkMonsterAttackSprites)
        app.bossAttackCounter = (app.bossAttackCounter + 1) % 4

    #Character Move: 
    app.mainPlayer.mainCharacterOnStep()

#-------------------------------------------------------------------------------
def onMouseMove(app, mouseX, mouseY):
    if app.shopScreen == True: 
        shop.onMouseMoveShop(app, mouseX, mouseY)
    
    if app.startScreen == True: 
        if (button.Button.buttonBounds(mouseX, mouseY, app.startScreenLargeButton.bounds)):
            app.startScreenRect = 'gray' 
        else: 
            app.startScreenRect = 'lightGray'
        startScreen.getSquareButtonIndexFromMouseMove(app, mouseX, mouseY)
        startScreen.onMouseButtonStartScreen(app, mouseX, mouseY)

    if app.infoScreen == True: 
        if (button.Button.buttonBounds(mouseX, mouseY, app.infoScreenButton.bounds)):
            app.infoScreenButtonFillColour = 'fireBrick' 
        else: 
            app.infoScreenButtonFillColour = 'salmon'
    
    if app.mainScreen == True:
        radius, angle = character.getEndAngleAndRadius(app.lineX0, app.lineY0, mouseX, mouseY)
        app.lineAngle = angle 
        app.lineX1, app.lineY1 = character.getRadiusEnd(app.lineX0, app.lineY0, app.lineLength, angle)

#-------------------------------------------------------------------------------
def onMousePress(app, mouseX, mouseY):
    '''Changing Screen if mouseX, mouseY within Button range'''
    if app.shopScreen == True: 
        shop.onMousePressShop(app, mouseX, mouseY)
        if button.Button.buttonBounds(mouseX, mouseY, app.infoScreenButton.bounds):
            app.startScreen = True
            app.shopScreen = False
        if button.Button.buttonBounds(mouseX, mouseY, app.shopScreenButton.bounds):
            app.startScreen = True
            app.shopScreen = False
        if button.Button.buttonBounds(mouseX, mouseY, app.startShopScreenButton.bounds):
            app.mainScreen = True
            app.shopScreen = False
    
    if app.highScoreScreen == True: 
        if button.Button.buttonBounds(mouseX, mouseY, app.infoScreenButton.bounds):
            app.highScoreScreen = False
            app.mainScreen = True
        
    if app.endScreen == True:
        if button.Button.buttonBounds(mouseX, mouseY, app.startScreenLargeButton.bounds):
            app.startScreen = True
            app.endScreen = False
            if app.minutes < 10 and app.seconds < 10: 
                time = f'0{app.minutes}:0{app.seconds}'
                app.allScores.append((app.currHighScore, time))
            if app.minutes < 10 and app.seconds >= 10: 
                time = f'0{app.minutes}:{app.seconds}'
                app.allScores.append((app.currHighScore, time))
            if app.minutes >= 10 and app.seconds >= 10: 
                time = f'{app.minutes}:{app.seconds}'
                app.allScores.append((app.currHighScore, time))
            if app.minutes >= 10 and app.seconds < 10: 
                time = f'{app.minutes}:0{app.seconds}'
                app.allScores.append((app.currHighScore, time))
            reset(app)
        
    if app.startScreen == True: 
        #Changing screens if the information button is Pressed
        if button.Button.buttonBounds(mouseX, mouseY, (app.width - (1) * app.squareButtonWidth * 1.5, 
                                      app.height - app.squareButtonWidth * 1.5, app.squareButtonWidth, app.squareButtonWidth)):
            app.highScoreScreen = True
            app.mainScreen = False
        
        if button.Button.buttonBounds(mouseX, mouseY, (app.width - (2) * app.squareButtonWidth * 1.5, 
                                      app.height - app.squareButtonWidth * 1.5, app.squareButtonWidth, app.squareButtonWidth)):
            app.startScreen = False #When button is pressed, startScreen turns to shopScreen
            app.shopScreen = True
            
        if button.Button.buttonBounds(mouseX, mouseY, (app.width - (3) * app.squareButtonWidth * 1.5, 
                                      app.height - app.squareButtonWidth * 1.5, app.squareButtonWidth, app.squareButtonWidth)):
            app.startScreen = False #When button is pressed, startScreen turns to InfoScreen
            app.infoScreen = True
        
        #Checks whether the mouse has pressed the button to move to the main screen
        if button.Button.buttonBounds(mouseX, mouseY, app.startScreenLargeButton.bounds): 
            app.startScreen = False 
            app.shopScreen = True 
    
    if app.infoScreen == True:
        if (button.Button.buttonBounds(mouseX, mouseY, app.infoScreenButton.bounds)):
            app.infoScreen = False
            app.startScreen = True
    
    if app.mainScreen == True: 
        if button.Button.buttonBounds(mouseX, mouseY, app.mainScreenPauseButtonBounds):
            app.shopScreen = True
            app.mainScreen = False
        if button.Button.buttonBounds(mouseX, mouseY, app.mainScreenMusicButtonBounds):
            app.infoScreen = True
            app.mainScreen = False
        if button.Button.buttonBounds(mouseX, mouseY, app.mainScreenHighScoreButtonBounds):
            app.highScoreScreen = True 
            app.mainScreen = False
        if button.Button.buttonBounds(mouseX, mouseY, app.mainScreenRestartButtonBounds):
            reset(app)


#-------------------------------------------------------------------------------
def onKeyPress(app, key): 
    #Changing the status of the game, depending on the button pressed 
    if key == 'p': 
        app.paused = not app.paused 
    if key == 'r':
        reset(app)
    if key == 'space' and app.paused == False:
        app.mainPlayer.jump()
    if key == 'right' and app.paused == False:
        app.mainPlayer.moveCharacterRight()
        app.characterMoving = True
    if key == 'down':
        app.characterAttack = True
        app.fireballVisible = True 
        x, y = character.getRadiusEnd(app.lineX0, app.lineY0, app.lineLength + app.attackR, app.lineAngle)
        app.attackX, app.attackY = x, y
        app.attackAngle = app.lineAngle 

#-------------------------------------------------------------------------------
def onKeyRelease(app, key):
    if key == 'right':
        app.mainPlayer.stopCharacterMoveRight()
        app.characterMoving = False
    if key == 'left':
        app.mainPlayer.stopCharacterMoveLeft()
        app.characterMoving = False
        
#-------------------------------------------------------------------------------
#from 15112 image notes: 
def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

runApp()