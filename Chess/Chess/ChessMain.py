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
        drawGameState(screen, gs)
        P.display.flip()
        clock.tick(MAX_FPS)
        P.display.flip()
        


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [P.Color("#FADAB4"), P.Color("#B2855F")]
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