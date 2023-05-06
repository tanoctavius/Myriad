from cmu_graphics import *
### your code
cmu_graphics.run()

from cmu_graphics import *

def onAppStart(app):
    app.rows = 6
    app.cols = 5
    app.boardLeft = 75
    app.boardTop = 50
    app.boardWidth = 250
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.board[0][0] = 'red'
    app.board[-1][-1] = 'blue'
    

def redrawAll(app):
    drawLabel("Tetris (Step 1)", 200, 30, size=16)
    drawBoard(app)
    drawBoardBorder(app)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def main():
    runApp()

main()
