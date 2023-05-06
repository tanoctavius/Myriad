from cmu_graphics import *
import button 

def drawStartScreen(app):
    #Draws the background on the start screen
    #Image sourced from: https://twitter.com/VideoArtGame/status/1619470375703793666 
    drawImage('startScreen.JPG', 0, 0, width = app.width, height = app.height)

def drawStartScreenButtons(app): 
    #Draws the large button with the start symbol on it 
    button.Button.drawButton(app.startScreenLargeButton)
    button.Label.drawLabel(app.startScreenLargeLabel)

def drawSquareButtons(app):
    #Draw three rectangular squares at bottom of start Screen
    for square in range(3):
        rectFillColour = 'gray' if ((square) == app.startHoverIndex) else 'lightgray'
        drawRect(app.width - ((square + 1) * app.squareButtonWidth * 1.5), app.height - app.squareButtonWidth * 1.5, app.squareButtonWidth, app.squareButtonWidth,
                 borderWidth = 3, fill = rectFillColour, border = 'black')
    
    #Draw information symbol circle:
    drawCircle(app.width - (3.98 * app.squareButtonWidth), app.height - app.squareButtonWidth, 13.5, fill = None, border = 'black', borderWidth = 3)
        
    #Draw the symbols on the buttons 
    button.Label.drawLabel(app.startScreenMusicLabel)
    button.Label.drawLabel(app.startScreenInformationLabel)
    button.Label.drawLabel(app.startScreenShopLabel)

def onMouseButtonStartScreen(app, mouseX, mouseY):
    #Check if the mouse Hovers over the image 
    rectHoverIndex = getSquareButtonIndexFromMouseMove(app, mouseX, mouseY)
    if (rectHoverIndex == None):
        app.startHoverIndex = None 
    elif app.startHoverIndex == None: 
        app.startHoverIndex = rectHoverIndex

def getSquareButtonIndexFromMouseMove(app, mouseX, mouseY):
    #Checks the rectangle that the mouse is hovering over 
    for buttonNum in range(3): 
        if app.width - ((buttonNum + 1) * app.squareButtonWidth * 1.5) <= mouseX <= (app.width - ((buttonNum + 1) * app.squareButtonWidth * 1.5) + app.squareButtonWidth):
            if app.height - app.squareButtonWidth * 1.5 <= mouseY <= app.squareButtonWidth + (app.height - app.squareButtonWidth * 1.5):
                return buttonNum
    return None

