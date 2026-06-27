import random

materialScore = {"K": 0, "Q": 9, "B": 3, "N": 3, "R": 5, "P" : 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    opponentMinmaxScore = CHECKMATE
    bestPlayerMove = None
    

    turnMultiplyer = 1 if gs.whiteToMove else -1
    random.shuffle(validMoves)


    for playerMove in validMoves:
        gs.makeMove(playerMove)

        opponentMoves = gs.getValidMoves()

        if gs.checkMate:
            opponentMaxScore = -CHECKMATE

        elif gs.staleMate:
            opponentMaxScore = STALEMATE
        
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE

                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplyer * scoreMaterial(gs.board)

                if score > opponentMaxScore:
                    opponentMaxScore = score

                gs.undoMove()

        if opponentMaxScore < opponentMinmaxScore:
            opponentMinmaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()

    return bestPlayerMove

#make the first reccursive call
def findMinMaxBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    findMinMaxMove(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove


def findMinMaxMove(gs, validMoves, depth, whiteToMove):
    global nextMove

    if depth == 0:
        return scoreMaterial(gs.board)


def scoreMaterial(board):
    score = 0
    for r in board:
        for square in r:
            if square[0] == 'w':
                score += materialScore[square[1]]
            
            elif square[0] == 'b':
                score-= materialScore[square[1]]

    return score