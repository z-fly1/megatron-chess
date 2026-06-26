import random

materialScore = {"K": 0, "Q": 9, "B": 3, "N": 3, "R": 5, "P" : 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    maxScore = -CHECKMATE
    bestMove = None

    turnMultiplyer = 1 if gs.whiteToMove else -1


    for playerMove in validMoves:
        gs.makeMove(playerMove)

        opponentMoves = gs.getValidMoves()

        if gs.checkMate:
            score = turnMultiplyer * CHECKMATE

        elif gs.staleMate:
            score = STALEMATE
        else:
            score = turnMultiplyer * scoreMaterial(gs.board)

        if score > maxScore:
            maxScore = score
            bestMove = playerMove

        gs.undoMove()

    return bestMove

def scoreMaterial(board):
    score = 0
    for r in board:
        for square in r:
            if square[0] == 'w':
                score += materialScore[square[1]]
            
            elif square[0] == 'b':
                score-= materialScore[square[1]]

    return score