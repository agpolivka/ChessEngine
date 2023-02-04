import pygame as p
import ChessEngine
#// means divide and return integer instead of a double

WIDTH = HEIGHT = 720
DIMENSION = 8 #dimension of chess board is 8x8

SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30 #for animations
IMAGES = {}

'''
Creates dictionary for the pieces and pictures that corelate to the pieces
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False #helps with effiency to not recreate boards on invalid moves

    loadImages()
    running = True
    squareSelected = () # starts with no square selected, this is a tuple(row,col)
    playerClicks = [] # keeps track of player clicks (two tuples: ([5,4],[4,4]))
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #x,y location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                print((row,col))
                if squareSelected == (row, col):
                    squareSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    print("selected square ", (row,col))
                    playerClicks.append(sqSelected) #append the clicks made
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gameState.makeMove(move)
                        moveMade = True
                        squareSelected = () #reset users clicks
                        playerClicks = []
                    else:
                        # allows for selection and deselection
                        playerClicks = [sqSelected]
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gameState.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
        drawGameState(screen, gameState)
        clock.tick(MAX_FPS)
        p.display.flip()
        
'''
Responsible for all graphics within the current game state
'''
def drawGameState(screen, gameState):
    drawBoard(screen)
    #can add piece highlighting or suggestions here
    drawPieces(screen, gameState.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            #choose color on whether its even number or odd number, even white, odd black
            color = colors[(row + col)%2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
