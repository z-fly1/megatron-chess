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

    def getValidMoves(self):
        return self.getAllMoves()

    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]

                if(turn == 'w' and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    peice = self.board[r][c][1]

                    if peice == 'P':
                        self.getPawnMoves(r, c, moves)

        return moves
                    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1, c), self.board))
                

                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2, c), self.board))

            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))

            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board))

                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2, c), self.board))




class Move():
    def __init__(self, sqStart, sqEnd, board):
        self.startRow = sqStart[0]
        self.startCol = sqStart[1]
        self.endRow = sqEnd[0]
        self.endCol = sqEnd[1]

        self.peiceMoved = board[self.startRow][self.startCol]
        self.peiceCaptured = board[self.endRow][self.endCol]


        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        else:
            return False
        

    def getChessNotaion(self, sqStart, sqEnd, board):

        self.startRow = sqStart[0]
        self.startCol = sqStart[1]
        self.endRow = sqEnd[0]
        self.endCol = sqEnd[1]

        rankToFile = {0: "a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7: "h"}
        rowToRank = {0 : 8, 1:7, 2:6, 3:5, 4:4, 5:3, 6:2, 7:1}

        notation = ""
        color = board[self.startRow][self.startCol][0]
        peice = board[self.startRow][self.startCol][1]

        if peice == "P":
            print(rankToFile[self.endCol] + str(rowToRank[self.endRow]))

        elif board[self.endRow][self.endCol][1] != "-":
            print( peice + "x" + rankToFile[self.endCol] + str(rowToRank[self.endRow]))

        else:
            print( peice + rankToFile[self.endCol] + str(rowToRank[self.endRow]))