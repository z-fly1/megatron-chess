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
        self.kingLocations = [(0, 4), (7,4)] #black -> white
        self.checkMate = False
        self.staleMate = False

        self.moveFunctions = {
            "P" : self.getPawnMoves,
            "R" : self.getRookMoves,
            "N" : self.getKnightMoves,
            "B" : self.getBishopMoves,
            "Q" : self.getQueenMoves,
            "K" : self.getKingMoves
        }

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.peiceMoved
        self.whiteToMove = not self.whiteToMove 
        self.moveLog.append(move)

        if move.peiceMoved == "bK":
            self.kingLocations[0] = (move.endRow, move.endCol)

        elif move.peiceMoved == "wK":
            self.kingLocations[1] = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.peiceMoved
            self.board[move.endRow][move.endCol] = move.peiceCaptured
            self.whiteToMove = not self.whiteToMove

            if move.peiceMoved == "bK":
                self.kingLocations[0] = (move.startRow, move.startCol)

            elif move.peiceMoved == "wK":
                self.kingLocations[1] = (move.startRow, move.startCol)


    def getValidMoves(self):
        moves = self.getAllMoves()

        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
    

            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
                

            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:

            if self.inCheck():
                self.checkMate = True

            else:
                self.staleMate = True

        else:
            self.checkMate = False
            self.staleMate = False
            
        return moves
        
    
    def inCheck(self):

        if self.whiteToMove:
            return self.sqAttacked(self.kingLocations[1])
        else:
            return self.sqAttacked(self.kingLocations[0])

    def sqAttacked(self, kl):

        self.whiteToMove = not self.whiteToMove

        oppsMoves = self.getAllMoves()

        for m in oppsMoves:
            if m.endRow == kl[0] and m.endCol == kl[1]:
                self.whiteToMove = not self.whiteToMove
                return True
        
        self.whiteToMove = not self.whiteToMove
        return False
        

    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]

                if(turn == 'w' and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    peice = self.board[r][c][1]

                    self.moveFunctions[peice](r,c, moves)

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

            if c-1 >=0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c), (r+1, c-1), self.board))

            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c), (r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):

        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right

        for d in directions:
            for i in range(1, len(self.board) + 1):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                    endPeice = self.board[endRow][endCol]

                    if endPeice[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break

                    elif endPeice == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    else:
                        break
                else:
                    break
                

    def getKnightMoves(self, r, c, moves):
        
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"


        knightSquares = ((-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1))

        for m in knightSquares:
            endRow = r + m[0]
            endCol = c + m[1]

            if 0 <= endRow < 8  and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]

                if endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

                elif endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"

        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1)) #left-up, left-dow, right-up, right-down

        for d in directions: 
            for i in range(1, len(self.board) + 1):

                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                    endPiece = self.board[endRow][endCol]

                    if endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break

                    elif endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    else:
                        break
                else:
                    break


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    def getKingMoves(self, r, c, moves):
        
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"

        kingSquares = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))

        for sq in kingSquares:
            
            endRow = r + sq[0]
            endCol = c + sq[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]

                if endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

                elif endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))



class Move():
    def __init__(self, sqStart, sqEnd, board):
        self.startRow = sqStart[0]
        self.startCol = sqStart[1]
        self.endRow = sqEnd[0]
        self.endCol = sqEnd[1]

        self.peiceMoved = board[self.startRow][self.startCol]
        self.peiceCaptured = board[self.endRow][self.endCol]


        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

        self.isPawnPromotion = False
        if (self.peiceMoved == "wP" and self.endRow == 0) or (self.peiceMoved == "bP" and self.endRow == 7):
            self.isPawnPromotion = True
        

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