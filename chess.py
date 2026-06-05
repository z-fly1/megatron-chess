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
    loadImages()

    running = True
    sqSelected = ()
    playerMove = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    gs.makeMove(move)
                    sqSelected = ()
                    playerMove = []
            

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()

        
        clock.tick(MAX_FPS)
        p.display.flip()
        drawGame(screen, gs)

def drawGame(screen, gs):
    drawBoard(screen)
    drawPeice(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]

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


if __name__ == "__main__":
    main()