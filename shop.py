from cmu_graphics import *
from PIL import Image
import os, pathlib
import button

def drawBackground(app):
    #Sourced from: https://www.reddit.com/r/Terraria/comments/qnpu34/new_wallpaper_the_workshop_1920x1080_made_mostly/
    drawImage(app.startScreenBackgroundImage, 0, 0, width = app.width, height = app.height)

def drawCharacterRectangle(app):
    #Drawing the rectangle with change border colour and fill Colour
    for rect in range(3):
        if ((rect) == app.selectedRectIndex):
            rectFillColour = rgb(170,189,160)  
        elif app.RectHoverIndex == rect: 
            rectFillColour = 'gainsboro'
        elif (rect) != app.selectedRectIndex and app.RectHoverIndex != rect:
                rectFillColour = 'white'
        rectBorderColour = 'darkGreen' if ((rect) == app.selectedRectIndex) else 'black'
        drawRect(app.rectMostLeft + (app.beginningWidthApart * rect), app.rectHeight, app.rectWidth, app.rectLength, fill = rectFillColour, border = rectBorderColour, borderWidth = 7)

        #Draw the stats rectangles:
        #drawRect(app.rectMostLeft + (app.beginningWidthApart * rect), app.statsRectTop, app.rectWidth, app.statsRectHeight, fill = rectFillColour, border = rectBorderColour, borderWidth = 7)

        #Draw the character images: 
        drawImage(app.characters[rect], app.rectMostLeft + (app.beginningWidthApart * rect) + app.shopSpriteLength//4 - 15, app.rectHeight + app.shopSpriteLength//4, width = app.shopSpriteLength, height = app.shopSpriteLength)

def onMouseMoveShop(app, mouseX, mouseY):
    #Check if the mouse Hovers over the image 
    rectHoverIndex = getIndexFromMouseMove(app, mouseX, mouseY)
    if (rectHoverIndex == None):
        app.RectHoverIndex = None 
    elif app.RectHoverIndex == None: 
        app.RectHoverIndex = rectHoverIndex

def getIndexFromMouseMove(app, mouseX, mouseY):
    #Checks the rectangle that the mouse is hovering over 
    for rectNum in range(3): 
        if app.rectMostLeft + (app.beginningWidthApart * rectNum) <= mouseX <= app.rectMostLeft + (app.beginningWidthApart * rectNum) + app.rectWidth:
            if app.rectHeight <= mouseY <= app.rectLength + app.rectHeight:
                return rectNum
    return None

def onMousePressShop(app, mouseX, mouseY):
    #Checking if mouseX and mouseY are pressed within the range of the rects, if it is, change rectColour and borderColour
    rectIndex = getRectIndexFromMouse(app, mouseX, mouseY)
    if (rectIndex == None) or (rectIndex == app.selectedRectIndex):
        app.selectedRectIndex = None 
    elif app.selectedRectIndex == None: 
        app.selectedRectIndex = rectIndex 
        app.currMonsterIndex = app.selectedRectIndex

    #Checking if mouseX and mouseY are within the range of the arrow buttons
    #[insert code here]
    
def getRectIndexFromMouse(app, mouseX, mouseY):
    #Check the rectangle that the mouse pressed 
    for rectNum in range(3): 
        if app.rectMostLeft + (app.beginningWidthApart * rectNum) <= mouseX <= app.rectMostLeft + (app.beginningWidthApart * rectNum) + app.rectWidth:
            if app.rectHeight <= mouseY <= app.rectLength + app.rectHeight:
                return rectNum
    return None

def drawButton(app):
    button.Button.drawButton(app.shopScreenButton)
    button.Label.drawLabel(app.shopScreenButtonLabel)
    button.Button.drawButton(app.startShopScreenButton)
    button.Label.drawLabel(app.startShopScreenButtonLabel)