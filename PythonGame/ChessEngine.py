'''
NOTES:
1) possible rewatch part 5 to look at king logic if the check stuff is not working.
believe this is working now
2) lots of custimization still available
3) on episode 7, working on the advanced algorithm
4) go watch episode 6 ending to get checkmate to end game //maybe

right now the basic game of chess works but no
en passant or promoting pawns

'''
class GameState():
    def __init__(self):
        '''
            b represents BLACK pieces and w represents WHITE pieces.
            p stands for PAWN
            R stands for ROOK
            B stands for BISHOP
            N stands for KNIGHT
            Q stands for QUEEN
            K stands for KING
            -- represents empty spots on the board
        '''
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR" ],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp" ],
            ["--", "--", "--", "--", "--", "--", "--", "--" ],
            ["--", "--", "--", "--", "--", "--", "--", "--" ],
            ["--", "--", "--", "--", "--", "--", "--", "--" ],
            ["--", "--", "--", "--", "--", "--", "--", "--" ],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp" ],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR" ],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                                'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    #does not work for castling, en passant, and pawn promotion
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # keeps track of the moves played
        self.whiteToMove = not self.whiteToMove #swaps players turns
        
        # tracks king locations
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
    
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            
            # tracks king locations
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        #1 get all possible moves
        moves = self.getAllPossibleMoves()
        
        #2 make move
        for x in range(len(moves)-1, -1, -1):
            self.makeMove(moves[x])

            #3 generate all opponents moves, see if king is attacked
            #4 if attacked, not valid move
            self.whiteToMove = not self.whiteToMove # have to switch back because makeMove switched the turn
            if self.inCheck():
                moves.remove(moves[x])
            
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    '''
    Checks if current player is under attack
    '''    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    
    '''
    Determine if enemy can attack the square located at row, col
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch to opponents moves
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # make sure to switch back 

        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        
        return False
        

    def getAllPossibleMoves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                turn = self.board[row][col][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    # call the valid move function on the specific piece type
                    self.moveFunctions[piece](row, col, moves)
                    
        return moves
    
    def getPawnMoves(self, r, c, moves):
        # white pawn moves that are available
        if self.whiteToMove:
            # 1 square pawn advance
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                # 2 square pawn advance
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            # pawn capture left
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            # pawn capture right
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        #NEEDS WORK ON DOUBLE AND DIAGNOL MOVES
        # black pawn moves that are available
        if not self.whiteToMove:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                # 2 square pawn advance
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            # pawn capture left
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            # pawn capture right
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
        # pawn promotions and en passant down here

    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for x in range(1, 8):
                endRow = r + d[0] * x
                endCol = c + d[1] * x
                if 0 <= endRow < 8 and 0 <= endCol < 8: 
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    # friendly piece
                    else:
                        break
                # out of board
                else:
                    break
        
    def getBishopMoves(self, r, c, moves):
        directions = [(-1, 1), (1, -1), (-1, -1), (1, 1)]
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for x in range(1, 8):
                endRow = r + d[0] * x
                endCol = c + d[1] * x
                if 0 <= endRow < 8 and 0 <= endCol < 8: 
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    # friendly piece
                    else:
                        break
                # out of board
                else:
                    break
        
    def getKnightMoves(self, r, c, moves):
        directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (2, -1), (1, -2), (-2, -1), (-1, -2)]
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for x in range(1, 2):
                endRow = r + d[0] * x
                endCol = c + d[1] * x
                if 0 <= endRow < 8 and 0 <= endCol < 8: 
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    # friendly piece
                    else:
                        break
                # out of board
                else:
                    break
        
    def getKingMoves(self, r, c, moves):
        directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        allyColor = 'w' if self.whiteToMove else 'b'

        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

        # directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        # enemy = 'b' if self.whiteToMove else 'w'
        # for d in directions:
            
        #     endRow = r + d[0] 
        #     endCol = c + d[1] 
        #     if 0 <= endRow < 8 and 0 <= endCol < 8: 
        #         endPiece = self.board[endRow][endCol]
        #         if endPiece == '--':
        #             moves.append(Move((r, c), (endRow, endCol), self.board))
        #         elif endPiece[0] == enemy:
        #             moves.append(Move((r, c), (endRow, endCol), self.board))
        #             break
        #         # friendly piece
        #         else:
        #             break
        
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
        


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    #may need to re edit this to make more proper chess notation
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]