import pygame
import time
from settings import white, red, blue, black, titleFont, optionsFont, windowWidth, windowHeight, screen, background
from board import Board
from player import Player
from computer import Computer

clock = pygame.time.Clock()

#Game class
class Game:
    #Initializes a Game instance
    def __init__(self) -> None:
        screen.fill(black)
        self.size = 5 #Board matrix size
        self.moveCounter = 0 #Move counter
        self.board = None #Board 
        self.redPieces = [] #List of red pieces
        self.bluePieces = [] #List of blue pieces
        self.player1 = None #Player1
        self.player2 = None #Player2
        self.winner = None #Winner player
        self.currentPlayer = None #Player current playing
        self.gameMode = 1 #Default game mode
        self.playerSelected = 1 #Player selected (1 or 2)
        self.difficulty1 = 1 #Difficulty computer 1 in computerVScomputer
        self.difficulty2 = 1 #Difficulty computer 2 in computerVScomputer
        self.difficulty = 1 #Difficulty computer in playerVScomputer
    
    #This method checks if either player has won the game.        
    def checkWinner(self):
        if(len(self.player1.pieces) == len(self.board.matrix) - 3):
            print("player 1 wins")
            return self.player1.player
        elif(len(self.player2.pieces) == len(self.board.matrix) - 3):
            print("player 2 wins")
            return self.player2.player
        else: return 0
    
    #This method creates the players for the game based on the selected game mode and player choices
    def createPlayers(self):
        if self.gameMode == 1:
            self.player1 = Player(self.redPieces, 1, "person", self.board)
            self.player2 = Player(self.bluePieces, 2, "person", self.board)
            
        elif self.gameMode == 2:
            if self.playerSelected == 1:
                self.player1 = Player(self.redPieces, 1, "person", self.board)
                self.player2 = Computer(self.bluePieces, 2, "computer", self.board, self.difficulty)
            elif self.playerSelected == 2:
                self.player1 = Computer(self.redPieces, 1, "computer", self.board, self.difficulty)
                self.player2 = Player(self.bluePieces, 2, "person", self.board)
                
        elif self.gameMode == 3:
            self.player1 = Computer(self.redPieces, 1, "computer", self.board, self.difficulty1)
            self.player2 = Computer(self.bluePieces, 2, "computer", self.board, self.difficulty2)
            
        self.currentPlayer = self.player1
        
    #This method creates a new game board using the Board class with the specified size 
    def createBoard(self):
        self.board = Board(self.size)
        self.redPieces = self.board.redPieces
        self.bluePieces = self.board.bluePieces

    #This method displays a winner screen on the game window after a player has won.
    def winnerScreen(self):
        screen.fill(black)
        text = titleFont.render(f'Player {self.winner} wins!', True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect() 
        textRect.center = (445, 370) 
        screen.blit(text, textRect) 
        pygame.display.flip()
        clock.tick(60)
        pygame.time.wait(1000)
    
    #Game main loop
    def play(self):
        start = time.time()
        self.board.createInitialState()
        self.board.drawInit()
        
        done = False
        while not done:
            screen.blit(background, (0, 0))

            self.board.draw()
            pygame.display.flip()
            
            if self.currentPlayer.availableMoves() == []:
                if self.currentPlayer == self.player1:
                    self.currentPlayer = self.player2
                else:
                    self.currentPlayer = self.player1
            
            
            if self.currentPlayer.type == "person":
                
                for event in pygame.event.get():
                    
                    if event.type == pygame.QUIT:
                        done = True
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.currentPlayer.selectPiece()
                        
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            
                            pieceMoved = self.currentPlayer.movePiece()
                    
                            if self.currentPlayer == self.player1 and pieceMoved:
                                self.currentPlayer.resetPieces()
                                self.currentPlayer = self.player2
                                
                            else:
                                self.currentPlayer.resetPieces() 
                                self.currentPlayer = self.player1
            
                        
            elif self.currentPlayer.type == "computer":
                pygame.time.wait(500)
                pieceMoved = False

                self.currentPlayer.selectPiece()
                if self.currentPlayer.difficulty == 0:
                    self.currentPlayer.movePieceMonteCarlo(self.currentPlayer.player, self.board.matrix)
                    
                elif self.currentPlayer.difficulty % 2 != 0:
                    self.currentPlayer.movePieceMinimax(self.currentPlayer.player, self.board.matrix)
                    
                elif self.currentPlayer.difficulty % 2 == 0:
                    self.currentPlayer.movePieceNegamax(self.currentPlayer.player, self.board.matrix)
                self.currentPlayer.resetPieces()
  
                if self.currentPlayer == self.player1:
                    self.currentPlayer = self.player2
                else: 
                    self.currentPlayer = self.player1
                self.moveCounter += 1
                    
                
                
            winner = self.checkWinner()
            if winner != 0:
                done = True
                self.winner = winner
                            
            clock.tick(60)
        
        if self.winner != None:
            end = time.time()
            print("time to win: ", end - start)
            print("moves to win: ", self.moveCounter)
            self.winnerScreen()
        
        pygame.quit() 
        exit()


