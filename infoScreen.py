from cmu_graphics import *
from PIL import Image
import button

def drawInfoScreen(app):
    #Image sourced from: https://wall.alphacoders.com/big.php?i=705836
    #Image sourced from: http://pixelartmaker.com/art/bb3dc7960467f39
    drawImage(app.infoScreenBackgroundImage, 0, 0, width = app.width, height = app.height)

def drawButton(app):
    button.Button.drawButton(app.infoScreenButton)
    button.Label.drawLabel(app.infoScreenButtonLabel)