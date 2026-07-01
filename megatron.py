import random

materialScore = {"K": 0, "Q": 900, "B": 330, "N": 320, "R": 500, "P" : 100}

knightScores = [[-50,-40,-30,-30,-30,-30,-40,-50],
                [-40,-20,  0,  0,  0,  0,-20,-40],
                [-30,  0, 10, 15, 15, 10,  0,-30],
                [-30,  5, 15, 20, 20, 15,  5,-30],
                [-30,  0, 15, 20, 20, 15,  0,-30],
                [-30,  5, 10, 15, 15, 10,  5,-30],
                [-40,-20,  0,  5,  5,  0,-20,-40],
                [-50,-40,-30,-30,-30,-30,-40,-50],]

bishopScores = [[-20,-10,-10,-10,-10,-10,-10,-20],
                [-10,  5,  0,  0,  0,  0,  5,-10],
                [-10, 10, 10, 10, 10, 10, 10,-10],
                [-10,  0, 10, 10, 10, 10,  0,-10],
                [-10,  5,  5, 10, 10,  5,  5,-10],
                [-10,  0,  5, 10, 10,  5,  0,-10],
                [-10,  0,  0,  0,  0,  0,  0,-10],
                [-20,-10,-10,-10,-10,-10,-10,-20],]

queenScores = [[-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [ -5,  0,  5,  5,  5,  5,  0, -5],
            [  0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20],]

kingScores = [[-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20,20, 0, 0, 0, 0,20,20],
            [20,30,10, 0, 0,10,30,20],]

pawnScores = [[ 0, 0, 0, 0, 0, 0, 0, 0],
            [50,50,50,50,50,50,50,50],
            [10,10,20,30,30,20,10,10],
            [ 5, 5,10,25,25,10, 5, 5],
            [ 0, 0, 0,20,20, 0, 0, 0],
            [ 5,-5,-10, 0, 0,-10,-5, 5],
            [ 5,10,10,-20,-20,10,10, 5],
            [ 0, 0, 0, 0, 0, 0, 0, 0],]


rookScores = [[ 0, 0, 5,10,10, 5, 0, 0],
            [-5, 0, 0, 0, 0, 0, 0,-5],
            [-5, 0, 0, 0, 0, 0, 0,-5],
            [-5, 0, 0, 0, 0, 0, 0,-5],
            [-5, 0, 0, 0, 0, 0, 0,-5],
            [-5, 0, 0, 0, 0, 0, 0,-5],
            [ 5,10,10,10,10,10,10, 5],
            [ 0, 0, 5,10,10, 5, 0, 0],]


piecePositionScores = {
    "P": pawnScores,
    "N": knightScores,
    "B": bishopScores,
    "R": rookScores,
    "Q": queenScores,
    "K": kingScores,
}

CHECKMATE = 1000
STALEMATE = 0
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves, depth=3):
    global nextMove
    nextMove = None
    findMoveNegaMaxAlphaBeta(gs, validMoves, depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1, depth)
    return nextMove


def findMinMaxMove(gs, validMoves, depth, whiteToMove, originalDepth=None):
    global nextMove
    if originalDepth is None:
        originalDepth = depth

    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMinMaxMove(gs, nextMoves, depth-1, False, originalDepth)
            if score > maxScore:
                maxScore = score
                
                if depth == originalDepth:
                    nextMove = move
            gs.undoMove()

        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMinMaxMove(gs, nextMoves, depth-1, True, originalDepth)

            if score < minScore:
                minScore = score

                if depth == originalDepth:
                    nextMove = move
            
            gs.undoMove()

        return minScore
    
def findMoveNegaMax(gs, validMoves, depth, turnMultiplyer, originalDepth=None):
    global nextMove
    if originalDepth is None:
        originalDepth = depth
    if depth == 0:
        return turnMultiplyer * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()

        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplyer, originalDepth)
        
        if score > maxScore:
            maxScore = score

            if depth == originalDepth:
                nextMove = move

        gs.undoMove()

    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplyer, originalDepth=None):
    global nextMove
    if originalDepth is None:
        originalDepth = depth
    if depth == 0:
        return turnMultiplyer * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()

        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplyer, originalDepth)

        if score > maxScore:
            maxScore = score

            if depth == originalDepth:
                nextMove = move

        gs.undoMove()

        if maxScore > alpha:
            alpha = maxScore

        if alpha >= beta:
            break

    return maxScore

    
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        
        else:
            return CHECKMATE
    
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            
            if square!= "--":

                piece = square[1]

            if square[0] == 'w':
                score += materialScore[square[1]] + piecePositionScores[piece][row][col] * .1
            
            elif square[0] == 'b':
                score-= materialScore[square[1]] + piecePositionScores[piece][7- row][col] * .1
    
    return score


def scoreMaterial(board):
    score = 0
    for r in board:
        for square in r:
            if square[0] == 'w':
                score += materialScore[square[1]]
            
            elif square[0] == 'b':
                score-= materialScore[square[1]]

    return score