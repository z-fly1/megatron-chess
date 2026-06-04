class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--","--", "--",],
            ["--", "--", "--", "--", "--", "--","--", "--",],
            ["--", "--", "--", "--", "--", "--","--", "--",],
            ["--", "--", "--", "--", "--", "--","--", "--",],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.peiceMoved
        self.whiteToMove = not self.whiteToMove 
        self.moveLog.append(move)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.peiceMoved
            self.board[move.endRow][move.endCol] = move.peiceCaptured
            self.whiteToMove = not self.whiteToMove


class Move():
    def __init__(self, sqStart, sqEnd, board):
        self.startRow = sqStart[0]
        self.startCol = sqStart[1]
        self.endRow = sqEnd[0]
        self.endCol = sqEnd[1]

        self.peiceMoved = board[self.startRow][self.startCol]
        self.peiceCaptured = board[self.endRow][self.endCol]

    def getChessNotaion(self):
        pass #add this later 