import pygame
from settings import black, red, blue, screen, select_grey

#Piece class
class Piece(pygame.sprite.Sprite):
    #Initializes a Piece instance with the given x and y coordinates, color, screen, board Size and size.
    def __init__(self, x, y, color, screen, boardSize, size):
        super().__init__()
        self.x = x #X position in matrix
        self.y = y #Y position in matrix
        self.color = color #piece color
        self.screenWidth = screen.get_width() #screen Width
        self.screenHeight = screen.get_height() #screen Height
        self.boardSize = boardSize #Board draw size 
        self.xDraw = self.screenWidth/2 - self.boardSize/2 + 4 + self.x * 74 #X position in the screen
        self.yDraw = self.screenHeight/2 - self.boardSize/2 + 4 + self.y * 74 #Y position in the screen
        self.size = size  # Board size (5, 7 or 9)
        self.selected = False #Selected attribute
        
        self.pieceSurface = pygame.Surface((70,70), pygame.SRCALPHA) #Piece Sprite
        pygame.draw.circle(self.pieceSurface, self.color, (35, 35), 30)        
        self.rect = self.pieceSurface.get_rect(center=(self.xDraw + 35, self.yDraw + 35))  #Piece rectangle
    
    #Operator overload to check if two pieces are the same comparing their positions
    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False
    
    #This method updates the color attribute
    def changeColor(self,color):
        self.color = color
        pygame.draw.circle(self.pieceSurface, self.color, (35, 35), 30)
    
    #This method draws the piece 
    def draw(self, screen):
        screen.blit(self.pieceSurface, (self.xDraw, self.yDraw))
    
    #This method updates de X drawing position
    def setDrawX(self):
        self.xDraw = self.screenWidth/2 - self.boardSize/2 + 4 + self.x * 74
        
    #This method updates de Y drawing position
    def setDrawY(self):
        self.yDraw = self.screenHeight/2 - self.boardSize/2 + 4 + self.y * 74
    
    #This method checks if any piece collides with (tempX, tempY) position
    def checkCollision(self, board, tempX, tempY):
        for piece in board.pieces:
            
            if piece.x == tempX and piece.y == tempY:
                return True
        
        if tempX < 0 or tempX > (self.size - 1) or tempY < 0 or tempY > (self.size - 1):
            return True

        return False
    
    #This method checks if the position (tempX, tempY) collides with the black hole
    def checkBlackHole(self, tempX, tempY):
        mid = self.size // 2
        if tempX == mid and tempY == mid:
            return True
        return False
    
    #This method moves the piece to the "coords" position and updates Xdraw and Ydraw
    def moveCoords(self, coords, board, player):
        board.matrix[self.y][self.x] = 0
        self.x = coords[0]
        self.y = coords[1]
        board.matrix[self.y][self.x] = player
        self.xDraw = self.screenWidth/2 - self.boardSize/2 + 4 + self.x * 74
        self.yDraw = self.screenHeight/2 - self.boardSize/2 + 4 + self.y * 74
        self.rect = self.pieceSurface.get_rect(center=(self.xDraw + 35, self.yDraw + 35))
    
    #This method moves the piece according to the direction received
    def moveDirection(self, direction, board, player):
        initialX = self.x
        initialY = self.y
        moved = False
        while not moved:
            if direction == "right":
                notCollision = True
                while notCollision:
                    tempX = self.x + 1
                    tempY = self.y
                        
                    if not self.checkCollision(board, tempX, tempY):
                        board.matrix[self.y][self.x] = 0
                        self.x = tempX
                        board.matrix[self.y][self.x] = player
                        self.setDrawX()
                        self.rect = self.pieceSurface.get_rect(center=(self.xDraw + 35, self.yDraw + 35))
                    else:
                        notCollision = False
                moved = True
                
            elif direction == "left":
                notCollision = True
                while notCollision:
                    tempX = self.x - 1
                    tempY = self.y
                    if not self.checkCollision(board, tempX, tempY):
                        board.matrix[self.y][self.x] = 0
                        self.x = tempX
                        board.matrix[self.y][self.x] = player
                        self.setDrawX()
                        self.rect = self.pieceSurface.get_rect(center=(self.xDraw + 35, self.yDraw + 35))
                        
                    else:
                        
                        notCollision = False
                moved = True
                
            elif direction == "up":
                notCollision = True
                while notCollision:
                    tempX = self.x
                    tempY = self.y - 1
                    if not self.checkCollision(board, tempX, tempY):
                        board.matrix[self.y][self.x] = 0
                        self.y = tempY
                        board.matrix[self.y][self.x] = player
                        self.setDrawY()
                        self.rect = self.pieceSurface.get_rect(center=(self.xDraw + 35, self.yDraw + 35))
                    else:
                        
                        notCollision = False
                moved = True
                
            elif direction == "down":
                notCollision = True
                while notCollision:
                    tempX = self.x
                    tempY = self.y + 1
                    if not self.checkCollision(board, tempX, tempY):
                        board.matrix[self.y][self.x] = 0
                        self.y = tempY
                        board.matrix[self.y][self.x] = player
                        self.setDrawY()
                        self.rect = self.pieceSurface.get_rect(center=(self.xDraw + 35, self.yDraw + 35))
                    else:
                        
                        notCollision = False   

                
                moved = True
        
        return initialX != self.x or initialY != self.y	
    
    #This method checks if a piece has been clicked
    def isClicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
    
    #This method draws circles on the board to represent available moves for the selected piece
    def drawAvailableMoves(self, board):
        for move in self.availableMoves(board):
            pygame.draw.circle(screen, select_grey, (move[0] * 74 + 35 + self.screenWidth/2 - self.boardSize/2 + 4, move[1] * 74 + 35 + self.screenHeight/2 - self.boardSize/2 + 4), 30) 
    
    #This method returns all possible moves to the current piece
    def availableMoves(self,board):
        availableMoves = []
        
        for dir in ["right","left","up","down"]:
            if dir == "right":
                tempX = self.x + 1
                notCollision = True
                while notCollision:
                    if not self.checkCollision(board, tempX, self.y):
                        tempX += 1
                    else:
                        notCollision = False
                        tempX = tempX - 1
                
                if tempX != self.x:
                    availableMoves.append((tempX,self.y))

            elif dir == "left":
                tempX = self.x - 1
                notCollision = True
                while notCollision:
                    if not self.checkCollision(board, tempX, self.y):
                        tempX -= 1
                    else:
                        notCollision = False
                        tempX = tempX + 1
                        
                if tempX != self.x:
                    availableMoves.append((tempX,self.y))
                    
            elif dir == "up":
                tempY = self.y - 1
                notCollision = True
                while notCollision:
                    if not self.checkCollision(board, self.x, tempY):
                        tempY -= 1
                    else:
                        notCollision = False
                        tempY = tempY + 1
                        
                if tempY != self.y:
                    availableMoves.append((self.x,tempY))
            elif dir == "down":
                tempY = self.y + 1
                notCollision = True
                while notCollision:
                    if not self.checkCollision(board, self.x, tempY):
                        tempY += 1
                    else:
                        notCollision = False
                        tempY = tempY - 1
                        
                if tempY != self.y:
                    availableMoves.append((self.x,tempY))
        
        return availableMoves
                
                        

    