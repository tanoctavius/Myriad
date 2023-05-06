from cmu_graphics import *
import button

def drawEndScreen(app):
    #Image sourced from: https://www.wallpaperflare.com/white-clouds-illustration-pixel-art-8-bit-cloud-sky-blue-wallpaper-cjeg  
    drawImage('endScreen.JPG', 0, 0, width = app.width, height = app.height)

def drawResetButton(app):
    button.Button.drawButton(app.startScreenLargeButton)
    button.Label.drawLabel(app.endScreenLargeLabel)