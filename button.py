from cmu_graphics import *

class Button:
    def __init__(self, bounds, fill, outlineColour, outlineWidth):
        #Bounds is a tuple of (left, top, width, length)
        self.bounds = bounds 
        self.fill = fill
        self.outlineColour = outlineColour
        self.outlineWidth = outlineWidth
    
    def buttonBounds(mouseXCord, mouseYCord, bounds):
        x0, y0, width, length = bounds
        return (x0 <= mouseXCord <= x0 + width and y0 <= mouseYCord <= y0 + length)
    
    def drawButton(self):
        x0, y0, width, length = self.bounds
        drawRect(x0, y0, width, length, fill = self.fill, border = self.outlineColour, 
                 borderWidth = self.outlineWidth)

#-------------------------------------------------------------------------------
class Label: 
    def __init__(self, message, bounds, size, font, colour, alignment, bold):
        self.message = message #str of the label 
        self.bounds = bounds #tuple of the starting x and y values 
        self.size = size
        self.font = font 
        self.colour = colour 
        self.alignment = alignment 
        self.bold = bold
        
    def drawLabel(self):
        x0, y0 = self.bounds 
        drawLabel(self.message, x0, y0, size = self.size, font = self.font, fill = self.colour, 
                  align = self.alignment, bold = self.bold)