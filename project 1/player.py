import pygame
from settings import white, red, blue

#Player class
class Player:
    #Initializes a Player instance with the given list of pieces, player number, type of player and board
    def __init__(self, pieces, player, type, board) -> None:
        self.pieces = pieces #List of player pieces 
        self.player = player #Player number
        self.type = type  # Player Type (Computer or Person)
        if player == 1:
            self.color = red #PLayer 1 color
        else: 
            self.color = blue #Player 2 color
        self.board = board #Board game

    #This method moves a selected piece according to player input 
    def movePiece(self):
        for piece in self.pieces:
            if piece.selected:

                moved = False
                pieceMoved = False
                direction = ""
                while not moved:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        direction = "left"

                    elif keys[pygame.K_RIGHT]:
                        direction = "right"
   
                    elif keys[pygame.K_UP]:
                        direction = "up"
  
                    elif keys[pygame.K_DOWN]:
                        direction = "down"
  
                    pieceMoved = piece.moveDirection(direction, self.board, self.player)
                    moved = True
                          
                if piece.checkBlackHole(piece.x, piece.y):

                    self.board.removePiece(piece)
                    self.removePiece(piece)
                    
                return pieceMoved
        
    #This method selects a piece changes his color and activates the selected attribute.
    def selectPiece(self): 
        
        for piece in self.pieces:
            if piece.isClicked():
                piece.changeColor(white)
                piece.selected = True
                
            else:
                piece.changeColor(self.color)
                piece.selected = False
                
    #This method resets the color and selected attributes of all pieces 
    def resetPieces(self):
        for piece in self.pieces:
            piece.changeColor(self.color)
            piece.selected = False
    
    #This method removes a piece from the list of pieces
    def removePiece(self, piece):
        self.pieces.remove(piece)

    #This method returns a list of the available moves of the player
    def availableMoves(self):
        availableMoves = []
        for piece in self.pieces:
            for piece in self.pieces:
                availableMoves.append(piece.availableMoves(self.board))
        return availableMoves
    
