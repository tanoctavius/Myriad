from cmu_graphics import *
import button
import copy 
import os 

#taking things from the os system 
def highScoreBackground(app):
    #Image sourced from: https://www.blogger.com/blogin.g?blogspotURL=https://sonic-wallpaper.blogspot.com/2020/08/sfondo-pixel.html&type=blog 
    #Image sourced from: https://www.bing.com/images/search?view=detailV2&ccid
    drawImage(app.highScoreBackground, 0, 0, width = app.width, height = app.height)

#Draws the button to exit the screen, back to the main game screen
def highScoreScreenButton(app):
    button.Button.drawButton(app.infoScreenButton)
    button.Label.drawLabel(app.infoScreenButtonLabel) #Draws the same buttons with the info Screen

def drawFinalHighScoreScreen(app):
    #Draws the titles for the high score screen 
    organisedList = getOrganisedListOfHighScores(app)
    drawLabel('Rank', app.width//2 - 135, app.yTopCord, font = app.highScoreFont, size = app.startScreenSize)
    drawLabel('Score', app.width//2 - 20, app.yTopCord, font = app.highScoreFont, size = app.startScreenSize)
    drawLabel('Time', app.width//2 + 110, app.yTopCord, font = app.highScoreFont, size = app.startScreenSize)
    
    #Draws all the scores stored
    for i in range(len(organisedList)):
        score, time = organisedList[i]
        drawLabel(f'{i + 1}.', app.width//2 - 110, app.yTopCord + (i+1)*45, font = app.highScoreFont, size = app.startScreenSize)
        drawLabel(f'{score}', app.width//2 - 24, app.yTopCord + (i+1)*45, font = app.highScoreFont, size = app.startScreenSize)
        drawLabel(f'{time}', app.width//2 + 115, app.yTopCord + (i+1)*45, font = app.highScoreFont, size = app.startScreenSize)

def getOrganisedListOfHighScores(app):
    result = []
    resultSet = set()
    resultDict = dict()
    for scores in range(len(app.allScores)):
        score, time = app.allScores[scores]
        resultSet.add(score)
        resultDict[score] = time 
    sortedDict = (sorted(resultSet))[::-1]
    for i in range(len(sortedDict)):
        time = resultDict[sortedDict[i]]
        result.append((sortedDict[i], time))
    return result 