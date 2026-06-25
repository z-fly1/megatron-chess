import pygame as p
from engine import GameState
from engine import Move as m

WIDTH = HEIGHT = 512
DIMENTION = 8
SQ_SIZE = WIDTH / DIMENTION

MAX_FPS = 15

IMAGES = {}

p.init()


def loadImages():
    peices = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bB", "bN", "bK", "bQ"]

    for peice in peices:
        IMAGES[peice] = p.transform.scale(p.image.load("imgs/svg/"+ peice + ".svg"), (SQ_SIZE, SQ_SIZE))

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()

    running = True
    sqSelected = ()
    playerMove = []

    animate = False
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = int(location[0]//SQ_SIZE)
                    row = int(location[1] // SQ_SIZE)
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerMove = []
                    else:
                        sqSelected = (row, col)
                        playerMove.append(sqSelected)

                    if len(playerMove) == 2:
                        move = m(playerMove[0], playerMove[1], gs.board)
                        move.getChessNotaion(playerMove[0], playerMove[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerMove = []

                        if not moveMade:
                            playerMove = [sqSelected]
            

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    animate = False
                    moveMade = True

                if e.key == p.K_r:
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerMove = []
                    moveMade = False
                    animate = False



        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        clock.tick(MAX_FPS)
        p.display.flip()
        drawGame(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")

            else:
                drawText(screen, "White wins by checkmate")

        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")

def drawGame(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPeice(screen, gs.board)
   

def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected

        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b" ):

            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(150)
            s.fill(p.Color('#94A684'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('#C89B3C'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    s.fill(p.Color('#C89B3C'))
                    if gs.board[move.endRow][move.endCol] != "==" and gs.board[move.endRow][move.endCol][0] == ("b" if gs.whiteToMove else "w"):
                        s.fill(p.Color('#A66A5B'))
                    
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
                    



def drawBoard(screen):
    global colors
    colors = [p.Color("#DCCFC0"), p.Color("#5C6B4F")]

    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            

def drawPeice(screen, board):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            peice = board[r][c]
            if peice != "--":
                screen.blit(IMAGES[peice], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):
    global colors
    animationCoordinates = []

    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol

    fps = 5

    frameCount = (abs(dR) + abs(dC)) * fps

    for f in range(frameCount + 1):
        r,c = (move.startRow + dR * f/frameCount, move.startCol + dC * f/frameCount)
        drawBoard(screen)
        drawPeice(screen, board)

        color = colors[((move.endRow+move.endCol)%2)]

        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)


        if move.peiceCaptured != "--":
            screen.blit(IMAGES[move.peiceCaptured], endSquare)

        screen.blit(IMAGES[move.peiceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont('Helvetica', 32, True, False)
    txtObj = font.render(text, 0, p.Color("#2F352A"))
    txtObj2 = font.render(text, 0, p.Color("#D4B26A"))

    txtLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - txtObj.get_width()/2, HEIGHT/2 - txtObj.get_height()/2)
    
    screen.blit(txtObj, txtLocation)
    screen.blit(txtObj2, txtLocation.move(-2,-2))



if __name__ == "__main__":
    main()