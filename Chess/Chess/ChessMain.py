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
    moveLog = []  # Initialize an empty move log
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []  # Initialize as a list
    gameOver = False
    
    while running:
        for e in P.event.get():
            if e.type == P.QUIT:
                running = False
            elif e.type == P.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = P.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:                
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # Append to the list
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveLog.append(validMoves[i])  # Add the move to the move log
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                # Move the following block outside of the 'elif' block for MOUSEBUTTONDOWN event
            elif e.type == P.KEYDOWN:
                if e.key == P.K_z:
                    if len(moveLog) > 0:
                        gs.undoMove()
                        moveLog.pop()  # Remove the last move from the move log
                        moveMade = True
                        animate = False
                if e.key == P.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawBoard(screen)
        drawPieces(screen, gs.board)
        drawGameState(screen, gs, validMoves, sqSelected, moveLog)  # Pass the moveLog argument
        
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by Checkmate')
            else:
                drawText(screen, 'White wins by Checkmate')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')
        
        P.display.flip()
        clock.tick(MAX_FPS)
        

def highlightSquares(Screen, gs, validMoves, sqSelected, moveLog):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = P.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(P.Color('#9C780D'))
            Screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.set_alpha(0)
            s.fill(P.Color('#b1781c'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    destR, destC = move.endRow, move.endCol
                    if gs.board[destR][destC] == "--":  # Check if the square is empty
                        dotSurface = P.Surface((SQ_SIZE, SQ_SIZE), P.SRCALPHA)
                        dotSurface.set_alpha(90)
                        P.draw.circle(dotSurface, P.Color('#444654'), (int(SQ_SIZE / 2), int(SQ_SIZE / 2)), 10)
                        Screen.blit(dotSurface, (destC * SQ_SIZE, destR * SQ_SIZE))
                    elif gs.board[destR][destC][0] == ('b' if gs.whiteToMove else 'w'):  # Check if the square is occupied by an enemy piece
                        highlightSurface = P.Surface((SQ_SIZE, SQ_SIZE), P.SRCALPHA)
                        highlightSurface.set_alpha(150)
                        highlightSurface.fill(P.Color('#0E66AA'))
                        P.draw.circle(highlightSurface, P.Color('#FF000000'), (int(SQ_SIZE / 2), int(SQ_SIZE / 2)), 37, 0)
                        Screen.blit(highlightSurface, (destC * SQ_SIZE, destR * SQ_SIZE))
    if moveLog:
        lastMove = moveLog[-1]
        startR, startC = lastMove.startRow, lastMove.startCol
        endR, endC = lastMove.endRow, lastMove.endCol
        lastMoveSurface = P.Surface((SQ_SIZE, SQ_SIZE), P.SRCALPHA)
        lastMoveSurface.set_alpha(70)
        lastMoveSurface.fill(P.Color('#D0C011'))
        Screen.blit(lastMoveSurface, (startC * SQ_SIZE, startR * SQ_SIZE))
        Screen.blit(lastMoveSurface, (endC * SQ_SIZE, endR * SQ_SIZE))
    if gs.inCheck:
        kingRow, kingCol = gs.whiteKingLocation if gs.whiteToMove else gs.blackKingLocation
        kingSurface = P.Surface((SQ_SIZE, SQ_SIZE), P.SRCALPHA)
        kingSurface.set_alpha(150)
        kingSurface.fill(P.Color('#A50D0D'))
        P.draw.circle(kingSurface, P.Color('#FF000000'), (int(SQ_SIZE/2), int(SQ_SIZE/2)), 34, 0)
        Screen.blit(kingSurface, (kingCol * SQ_SIZE, kingRow * SQ_SIZE))
    
        
                    

def drawGameState(screen, gs, validMoves, sqSelected, moveLog):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected, moveLog)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
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


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR * frame/frameCount, move.startCol + dC * frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = P.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        P.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], P.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        P.display.flip()
        clock.tick(480)


def drawText(screen, text):
    font = P.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, P.Color('gray'))
    textLocation = P.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, P.Color('black'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()