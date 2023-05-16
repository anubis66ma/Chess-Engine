"""
this is our main driver file. it will be responsible for handling user input and displaying the current gamestate object
"""

import pygame as P

import ChessEngine


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 
IMAGES = {}

'''
Initialize a global dictionary of images
'''

def loadImages():
    pieces = ['wp' ,'wR' ,'wN' ,'wB' ,'wQ' ,'wK' ,'bp' ,'bR' ,'bN' ,'bB' ,'bQ' ,'bK']
    for piece in pieces:
        IMAGES[piece] = P.transform.scale(P.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
the main driver
'''

def main():
    P.init()
    screen = P.display.set_mode((WIDTH, HEIGHT))
    clock = P.time.Clock()
    screen.fill(P.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in P.event.get():
            if e.type == P.QUIT:
                running = False
            elif e.type == P.MOUSEBUTTONDOWN:
                location = P.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:                
                    sqSelected =  (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == P.KEYDOWN:
                if e.key ==P.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False


        drawBoard(screen)
        drawPieces(screen, gs.board)
        drawGameState(screen, gs, validMoves, sqSelected)
        P.display.flip()
        clock.tick(MAX_FPS)
        P.display.flip()
        

def highlightSquares(Screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = P.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(P.Color('#9C780D'))
            Screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.set_alpha(20)
            s.fill(P.Color('#b1781c'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    destR, destC = move.endRow, move.endCol
                    if gs.board[destR][destC] == "--":  # Check if the square is empty
                        dotSurface = P.Surface((SQ_SIZE, SQ_SIZE), P.SRCALPHA)
                        dotSurface.set_alpha(90)
                        P.draw.circle(dotSurface, P.Color('#444654'), (int(SQ_SIZE/2), int(SQ_SIZE/2)), 10)
                        Screen.blit(dotSurface, (destC * SQ_SIZE, destR * SQ_SIZE))
                    elif gs.board[destR][destC][0] == ('b' if gs.whiteToMove else 'w'):  # Check if the square is occupied by an enemy piece
                        highlightSurface = P.Surface((SQ_SIZE, SQ_SIZE), P.SRCALPHA)
                        highlightSurface.set_alpha(150)
                        highlightSurface.fill(P.Color('#202124'))
                        P.draw.circle(highlightSurface, P.Color('#FF000000'), (int(SQ_SIZE/2), int(SQ_SIZE/2)), 37, 0) # set thickness parameter to 0
                        Screen.blit(highlightSurface, (destC * SQ_SIZE, destR * SQ_SIZE))
                    Screen.blit(s, (destC * SQ_SIZE, destR * SQ_SIZE))
                    

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [P.Color("#f0d9b5"), P.Color("#b58863")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            P.draw.rect(screen, color, P.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], P.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()