import pygame as p
from engine import GameState
from engine import Move as m
import math
import megatron

WIDTH = HEIGHT = 512
MOVE_LOG_WIDTH = 250
MOVE_LOG_HEIGHT = HEIGHT
DIMENTION = 8
SQ_SIZE = WIDTH / DIMENTION

MAX_FPS = 15

IMAGES = {}

p.init()


def loadImages():
    peices = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bB", "bN", "bK", "bQ"]

    for peice in peices:
        IMAGES[peice] = p.transform.scale(p.image.load("imgs/svg/"+ peice + ".svg"), (SQ_SIZE, SQ_SIZE))


#The drawmenu function code is ai assisted (I asked chatgpt how to so certain things)
def drawMenu(screen, selectedMode, aiDepth, modeRects, depthRects, startRect, menuBg):
    screen.blit(menuBg, (WIDTH, 0))

    titleFont = p.font.SysFont('Arial', 16, True, False)
    menuFont = p.font.SysFont('Arial', 13, False, False)

    title = titleFont.render("MEGATRON CHESS", True, p.Color("#D4B26A"))
    screen.blit(title, (WIDTH + 12, 12))

    modeLabel = menuFont.render("Game Mode:", True, p.Color("#DDD4C8"))
    screen.blit(modeLabel, (WIDTH + 12, 40))

    modes = ["2 Player", "vs AI (White)", "vs AI (Black)"]
    for i, mode in enumerate(modes):
        if i == selectedMode:
            p.draw.rect(screen, p.Color("#3D4F3A"), modeRects[i], border_radius=13)
        color = p.Color("#C89B3C") if i == selectedMode else p.Color("#94A684")
        text = menuFont.render(f"{mode}", True, color)
        screen.blit(text, modeRects[i].topleft)

    if selectedMode != 0:
        depthLabel = menuFont.render(f"Depth: {aiDepth}", True, p.Color("#DDD4C8"))
        screen.blit(depthLabel, (WIDTH + 12, depthRects[0].top - 14))

        p.draw.rect(screen, p.Color("#D4B26A"), depthRects[0], border_radius=3)
        minusText = menuFont.render("-", True, p.Color("#2F352A"))
        screen.blit(minusText, minusText.get_rect(center=depthRects[0].center))

        p.draw.rect(screen, p.Color("#D4B26A"), depthRects[1], border_radius=3)
        plusText = menuFont.render("+", True, p.Color("#2F352A"))
        screen.blit(plusText, plusText.get_rect(center=depthRects[1].center))

        noteFont = p.font.SysFont('Arial', 11, False, False)
        noteLines = [
            "Increasing depth will",
            "slow down the engine",
            "and it will take time",
            "to make moves.",
        ]
        for j, line in enumerate(noteLines):
            note = noteFont.render(line, True, p.Color("white"))
            screen.blit(note, (WIDTH + 12, depthRects[1].bottom + 12 + j * 12))

    p.draw.rect(screen, p.Color("#D4B26A"), startRect, border_radius=6)
    startText = titleFont.render("START", True, p.Color("#2F352A"))
    screen.blit(startText, startText.get_rect(center=startRect.center))


def main():
    screen = p.display.set_mode((WIDTH + MOVE_LOG_WIDTH, HEIGHT))
    p.display.set_caption("Megatron Chess")
    clock = p.time.Clock()
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()

    running = True
    sqSelected = ()
    playerMove = []
    animate = False
    gameOver = False

    move_sfx = p.mixer.Sound('sounds/move-self.mp3')
    capture_sfx = p.mixer.Sound('sounds/capture.mp3')
    gameover_sfx = p.mixer.Sound('sounds/game-end.mp3')
    promote_sfx = p.mixer.Sound('sounds/promote.mp3')
    castle_sfx = p.mixer.Sound('sounds/castle.mp3')
    check_sfx = p.mixer.Sound('sounds/move-check.mp3')

    moveLogFont = p.font.SysFont('Arial', 12, False, False)

    gameStarted = False
    selectedMode = 1
    aiDepth = 3
    DEPTH_MIN = 1
    DEPTH_MAX = 5
    playerOne = True
    playerTwo = False

    modeRects = []
    y = 55
    for _ in range(3):
        modeRects.append(p.Rect(WIDTH + 10, y, 230, 24))
        y += 35

    depthRects = [
        p.Rect(WIDTH + 85, y + 2, 24, 20),
        p.Rect(WIDTH + 115, y + 2, 24, 20),
    ]
    startY = y + 110
    startRect = p.Rect(0, 0, 130, 36)
    startRect.center = (WIDTH + MOVE_LOG_WIDTH // 2, startY)

    menuBg = p.transform.scale(p.image.load("imgs/menu-bg.png"), (MOVE_LOG_WIDTH, MOVE_LOG_HEIGHT))

    while running:

        isHumanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                mx, my = p.mouse.get_pos()

                if not gameStarted and mx >= WIDTH:
                    for i, rect in enumerate(modeRects):
                        if rect.collidepoint(mx, my):
                            selectedMode = i

                    if selectedMode != 0:
                        if depthRects[0].collidepoint(mx, my):
                            aiDepth = max(DEPTH_MIN, aiDepth - 1)
                        if depthRects[1].collidepoint(mx, my):
                            aiDepth = min(DEPTH_MAX, aiDepth + 1)

                    if startRect.collidepoint(mx, my):
                        playerOne = selectedMode != 2
                        playerTwo = selectedMode == 0
                        gameStarted = True

                elif gameStarted and not gameOver and isHumanTurn:
                    location = p.mouse.get_pos()
                    col = int(location[0] // SQ_SIZE)
                    row = int(location[1] // SQ_SIZE)
                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = ()
                        playerMove = []
                    else:
                        sqSelected = (row, col)
                        playerMove.append(sqSelected)

                    if len(playerMove) == 2:
                        move = m(playerMove[0], playerMove[1], gs.board)
                        move.getChessNotaion()
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
                if e.key == p.K_z and gameStarted:
                    gs.undoMove()
                    animate = False
                    moveMade = True
                    gameOver = False

                if e.key == p.K_r:
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerMove = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    gameStarted = False

        if gameStarted and not gameOver and not isHumanTurn:
            computerMove = megatron.findBestMove(gs, validMoves, aiDepth)
            if computerMove is None:
                computerMove = megatron.findRandomMove(validMoves)
            gs.makeMove(computerMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        clock.tick(MAX_FPS)
        p.display.flip()
        drawGame(screen, gs, validMoves, sqSelected, moveLogFont, gameStarted, selectedMode, aiDepth, modeRects, depthRects, startRect, menuBg)

        if gameStarted:
            if gs.checkMate:
                gameOver = True
                if gs.whiteToMove:
                    drawText(screen, "Black wins by checkmate")
                else:
                    drawText(screen, "White wins by checkmate")
            elif gs.staleMate:
                gameOver = True
                drawText(screen, "Stalemate")


def drawGame(screen, gs, validMoves, sqSelected, moveLogFont, gameStarted, selectedMode, aiDepth, modeRects, depthRects, startRect, menuBg):
    drawBoard(screen)
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPeice(screen, gs.board)
    if gameStarted:
        drawMoveLog(screen, gs, moveLogFont)
    else:
        drawMenu(screen, selectedMode, aiDepth, modeRects, depthRects, startRect, menuBg)

def drawBoard(screen):
    global colors
    colors = [p.Color("#DCCFC0"), p.Color("#5C6B4F")]

    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
   

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
                    


def drawPeice(screen, board):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            peice = board[r][c]
            if peice != "--":
                screen.blit(IMAGES[peice], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs, font):

    moveLogContainer = p.Rect(WIDTH, 0, MOVE_LOG_WIDTH, MOVE_LOG_HEIGHT)
    p.draw.rect(screen, p.Color("#4A5643"), moveLogContainer)

    moveLog = gs.moveLog
    moveTexts = []

    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i+1])

        moveTexts.append(moveString)


    padding = 5
    textY = padding
    lineSpacing = 4

    for i in range(len(moveTexts)):
        text = moveTexts[i]
        txtObj = font.render(text, True, p.Color("#DDD4C8"))
        txtLocation = moveLogContainer.move(padding, textY)
        screen.blit(txtObj, txtLocation)

        textY += txtObj.get_height() + lineSpacing

def animateMove(move, screen, board, clock):
    global colors
    animationCoordinates = []

    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol

    squaresMoved = math.sqrt(dR**2 + dC**2)

    fps = 4

    frameCount = max(1, int(squaresMoved * fps))


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