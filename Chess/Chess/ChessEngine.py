"""
this class is responsible for storing all the information about the current state of a chess game
"""

class GameState():
   def __init__(self):
      # Initialize the starting chess board with the standard starting positions of pieces
      self.board =  [
         ["bR" , "bN" , "bB" , "bQ" , "bK" , "bB" , "bN" , "bR"],
         ["bp" , "bp" , "bp" , "bp" , "bp" , "bp" , "bp" , "bp"],
         ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
         ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
         ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
         ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
         ["wp" , "wp" , "wp" , "wp" , "wp" , "wp" , "wp" , "wp"],
         ["wR" , "wN" , "wB" , "wQ" , "wK" , "wB" , "wN" , "wR"]
      ]

      # A dictionary that maps each piece to its respective move generating function
      self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

      # A boolean variable indicating whether it's white's turn to move or not
      self.whitelToMove = True

      # A list to keep track of the moves played in the game
      self.moveLog = []


   def makeMove(self, move):
      # Set the starting square of the move to empty
      self.board[move.startRow][move.startCol] = "--"
      # Set the ending square of the move to the piece that was moved
      self.board[move.endRow][move.endCol] = move.pieceMoved
      # Add the move to the move log
      self.moveLog.append(move)
      # Switch the player turn
      self.whitelToMove = not self.whitelToMove
   
   # This function undoes the previous move made on the chess board. 
   # If there are moves in the moveLog, it removes the last move from the 
   # log and reverts the changes made to the board. 
   # The piece that was moved is returned to its original position and 
   # any captured piece is put back on the board. Finally, it switches 
   # the turn of the player to the one who made the previous move.

   def undoMove(self):
      # Check if there are any moves to undo
      if len(self.moveLog) != 0:
         # Remove the last move from the move log
         move = self.moveLog.pop()
         # Move the piece back to its original position
         self.board[move.startRow][move.startCol] = move.pieceMoved
         # If a piece was captured, put it back on the board
         self.board[move.endRow][move.endCol] = move.pieceCaptured
         # Switch the turn of the player to the one who made the previous move
         self.whitelToMove = not self.whitelToMove
   
   def getValidMoves(self):
      # Returns all the valid moves for the current player
      return self.getAllPossibleMoves()

   def getAllPossibleMoves(self):
      # Generates all possible moves for all the pieces of the current player
      
      # Create an empty list to store all the moves
      moves = []
      
      # Loop through each cell of the board to find all the pieces of the current player
      for r in range(len(self.board)):
         for c in range(len(self.board[r])):
            # Check if the piece belongs to the current player
            turn = self.board[r][c][0]
            if (turn == 'w' and self.whitelToMove) or (turn == 'b' and not self.whitelToMove):
               
               # Get the type of the piece
               piece = self.board[r][c][1]
               
               # Call the move function for the piece to get all its possible moves
               self.moveFunctions[piece](r, c, moves)
      
      # Return the list of all possible moves
      return moves

   # This function is used to get all possible moves for a pawn.

   def getPawnMoves(self, r, c, moves):
    # If it is white's turn, check for possible moves for white pawns
    if self.whitelToMove:
        # If the cell in front of the pawn is empty, the pawn can move there
        if self.board[r-1][c] == "--":
            moves.append(Move((r, c), (r-1, c), self.board))
            # If the pawn is at the initial row (row 6) and the two cells in front of it are empty,
            #  the pawn can move two cells
            if r == 6 and self.board[r-2][c] == "--":
                moves.append(Move((r, c), (r-2,c), self.board))
        # If there is a black piece on the diagonal left to the pawn,
        #  the pawn can capture it by moving there
        if c-1 >= 0:
            if self.board[r-1][c-1][0] =='b':
                moves.append(Move((r, c), (r-1, c-1), self.board))
        # If there is a black piece on the diagonal right to the pawn,
        #  the pawn can capture it by moving there
        if c+1 <= 7:
            if self.board[r-1][c+1][0] == 'b':
                moves.append(Move((r, c), (r-1, c+1), self.board))
    # If it is black's turn, check for possible moves for black pawns
    else:
        # If the cell in front of the pawn is empty, the pawn can move there
        if self.board[r+1][c] == "--":
            moves.append(Move((r, c), (r+1, c), self.board))
            # If the pawn is at the initial row (row 1) and the two cells in front of it are empty,
            #  the pawn can move two cells
            if r == 1 and self.board[r+2][c] == "--":
                moves.append(Move((r, c), (r+2,c), self.board))
        # If there is a white piece on the diagonal left to the pawn,
        #  the pawn can capture it by moving there
        if c-1 >= 0:
            if self.board[r+1][c-1][0] =='w':
                moves.append(Move((r, c), (r+1, c-1), self.board))
        # If there is a white piece on the diagonal right to the pawn,
        #  the pawn can capture it by moving there
        if c+1 <= 7:
            if self.board[r+1][c+1][0] == 'w':
                moves.append(Move((r, c), (r+1, c+1), self.board))


   def getRookMoves(self, r, c, moves):
    # Define the possible directions for the rook
    directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
    # Determine the enemy color based on whose turn it is
    enemyColor = 'b' if self.whitelToMove else 'w'
    
    # Loop through each direction
    for d in directions:
        # Loop through each square in the direction until we reach
        #  the end of the board or a piece blocks the way
        for i in range(1, 8):
            endRow = r + d[0] * i
            endCol = c + d[1] * i
            
            # If the square is within the board bounds
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                
                # If the square is empty, add a move to the list of possible moves
                if endPiece == '--':
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                # If the square contains an enemy piece, add a capture move and stop searching in this direction
                elif endPiece[0] == enemyColor:
                     moves.append(Move((r, c), (endRow, endCol), self.board))
                     break
                # If the square contains a friendly piece, stop searching in this direction
                else:
                    break
            # If the square is outside the board bounds, stop searching in this direction
            else:
                break



   def getKnightMoves(self, r, c, moves):
      knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
      allyColor = 'w' if self.whitelToMove else 'b'
      for m in knightMoves:
         endRow = r + m[0]
         endCol = c + m[1]
         if 0 <= endRow < 8 and 0 <= endCol < 8:
            endPiece = self.board[endRow][endCol]
            if endPiece[0] != allyColor:
               moves.append(Move((r, c), (endRow, endCol), self.board))

   def getBishopMoves(self, r, c, moves):
      directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
      enemyColor = 'b' if self.whitelToMove else 'w'
      for d in directions:
            for i in range(1, 8):
               endRow = r + d[0] * i
               endCol = c + d[1] * i
               if 0 <= endRow < 8 and 0 <= endCol < 8:
                  endPiece = self.board[endRow][endCol]
                  if endPiece == '--':
                     moves.append(Move((r, c), (endRow, endCol), self.board))
                  elif endPiece[0] == enemyColor:
                     moves.append(Move((r, c), (endRow, endCol), self.board))
                     break
                  else:
                     break
               else:
                  break

   def getQueenMoves(self, r, c, moves):
      self.getRookMoves(r, c, moves)
      self.getBishopMoves(r, c, moves)

   def getKingMoves(self, r, c, moves):
      kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
      allyColor = 'w' if self.whitelToMove else 'b'
      for i in range(8):
         endRow = r + kingMoves[i][0]
         endCol = c + kingMoves[i][1]
         if 0 <= endRow < 8 and 0 <= endCol < 8:
            endPiece = self.board[endRow][endCol]
            if endPiece[0] != allyColor:
               moves.append(Move((r, c), (endRow, endCol), self.board))

class Move():

   ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
   rowsToRanks = {v: k for k, v in ranksToRows.items()}
   filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
   colsToFiles = {v: k for k, v in filesToCols.items()}

   def __init__(self, startSq, endSq, board):
      self.startRow = startSq[0]
      self.startCol = startSq[1]
      self.endRow = endSq[0]
      self.endCol = endSq[1]
      self.pieceMoved = board[self.startRow][self.startCol]
      self.pieceCaptured = board[self.endRow][self.endCol]
      self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
      print(self.moveID)

   def __eq__(self, other):
      if isinstance(other, Move):
         return self.moveID == other.moveID
      return False

   
   def getChessNotation(self):
      return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

   def getRankFile(self, r, c):
      return self.colsToFiles[c] + self.rowsToRanks[r]
   
