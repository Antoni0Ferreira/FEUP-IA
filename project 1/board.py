import pygame
from piece import Piece
from settings import black, dark_grey, grey, red, blue, screen

#Board class
class Board:
    #Initializes a Board instance with the given size
    def __init__(self, size) -> None:
        self.pieces = [] #Total pieces
        self.matrix = [[0]*size for _ in range(size)] #Matrix internal representation
        self.blackHole = pygame.Surface((70, 70)) #Blackhole Sprite
        self.redPieces = list() #Red pieces list
        self.bluePieces = list() #Blue pieces list
        self.size = size # Matrix size (5, 7 or 9)
        self.boardSize = 70*size + 4 * (size + 1) #Board draw Size
        self.board = pygame.Surface((self.boardSize, self.boardSize)) #Board Sprite

    #This method creates the initial state of the board.
    def createInitialState(self):
        mid = self.size // 2
        for i in range(0, self.size):
            for j in range(0, self.size):
                if i == j and i!= mid:
                    
                    if i > mid:
                        self.matrix[i][j] = 2
                        self.bluePieces.append(Piece(j, i,blue, screen, self.boardSize, self.size))
                    else:
                        self.matrix[i][j] = 1
                        self.redPieces.append(Piece(j, i,red, screen, self.boardSize, self.size))
                if i + j == self.size - 1 and i!=mid:
                    if i > mid:
                        self.matrix[i][j] = 2
                        self.bluePieces.append(Piece(j, i,blue, screen, self.boardSize, self.size))
                    else:
                        self.matrix[i][j] = 1
                        self.redPieces.append(Piece(j, i, red, screen, self.boardSize, self.size))
                        
        self.pieces = self.redPieces + self.bluePieces

    #This method draws the initial state of the game
    def drawInit(self):
        self.board.fill(dark_grey)
        self.blackHole.fill(black)
        
        for i in range(0, self.size + 1):
            pygame.draw.rect(self.board, grey, ( 0, i * (74), self.boardSize, 4))
            pygame.draw.rect(self.board, grey, ( i * (74), 0, 4, 5280))
        
        for piece in self.pieces:
            piece.draw(screen)

    #This method draws the current board state 
    def draw(self):
        #center board on screen and draw black hole in the middle of the board
        screen.blit(self.board, (screen.get_width()/2 - self.boardSize/2, screen.get_height()/2 - self.boardSize/2))
        screen.blit(self.blackHole, (screen.get_width()/2 - 35, screen.get_height()/2 - 35))
        
        for piece in self.pieces:
            piece.draw(screen)
            if piece.selected:
                piece.drawAvailableMoves(self)

        
    #This method removes a piece from the internal matrix representation and from the pieces list
    def removePiece(self, piece):
        self.matrix[piece.x][piece.y] = 0
        self.pieces.remove(piece)

    #This function prints the current matrix state 
    def printMatrix(self):
        for i in range(0,self.size):
            print(f"{self.matrix[i]}")
        print("\n")    
        
        