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

    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]

                if(turn == 'w' and self.whiteToMove) and (turn == "b" and not self.whiteToMove):
                    peice = self.board[r][c][1]

                    if peice == 'p':
                        pass



class Move():
    def __init__(self, sqStart, sqEnd, board):
        self.startRow = sqStart[0]
        self.startCol = sqStart[1]
        self.endRow = sqEnd[0]
        self.endCol = sqEnd[1]

        self.peiceMoved = board[self.startRow][self.startCol]
        self.peiceCaptured = board[self.endRow][self.endCol]

    def getChessNotaion(self, sqStart, sqEnd, board):

        self.startRow = sqStart[0]
        self.startCol = sqStart[1]
        self.endRow = sqEnd[0]
        self.endCol = sqEnd[1]

        rankToFile = {0: "A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7: "H"}

        notation = ""
        color = board[self.startRow][self.startCol][0]
        peice = board[self.startRow][self.startCol][1]
        
        return peice + rankToFile[self.endCol] + (self.startRow + 1)