import random
import pygame
import math
import copy
from settings import white, red, blue
from node import Node
from MonteCarloTreeSearch import MonteCarloTreeSearch

#Computer player class
class Computer:
    #Initializes a Computer instance with the given list of pieces, player number,type, board and difficulty
    def __init__(self, pieces, player, type, board, difficulty) -> None:
        self.pieces = pieces #List of player pieces 
        self.player = player #Player number
        self.type = type #Player Type (Computer or Person)
        if player == 1:
            self.color = red #Player 1 color
        else: 
            self.color = blue # Player 2 color
        self.board = board #Board game
        self.difficulty = difficulty #Difficulty(0-6)
        self.heuristic = None #Current heuristic
        self.depth = 0 #Current depth for minimax or negamax
        
        if self.difficulty == 1 or self.difficulty == 2:
            self.heuristic = self.evaluateAvailableMoves
            self.depth = 2
            
        elif self.difficulty == 3 or self.difficulty == 4:
            self.heuristic = self.evaluateManhattan
            self.depth = 3
            
        elif self.difficulty == 5 or self.difficulty == 6:
            self.heuristic = self.evaluateBlackHole
            self.depth = 5
    
    #This method randomly selects a piece from the player pieces. The selected piece is marked as selected.
    def selectPiece(self):
        piece = random.choice(self.pieces)
        piece.selected = True
    
    #This method moves a piece for a random direction 
    def movePieceRandom(self):
        direction = random.choice(["left", "right", "up", "down"])
        for piece in self.pieces:
            if piece.selected:
                pieceMoved = piece.moveDirection(direction, self.board, self.player)
                if piece.checkBlackHole(piece.x, piece.y):
                    self.board.removePiece(piece)
                    self.removePiece(piece)
                return pieceMoved                  
    
    #This method resets the selected attribute of all pieces 
    def resetPieces(self):
        for piece in self.pieces:
            piece.selected = False
    
    #This method removes a piece from the list of pieces
    def removePiece(self, piece):
        self.pieces.remove(piece)
    
    #This method returns a list of the available moves of the player
    def availableMoves(self):
        availableMoves = []
        for piece in self.pieces:
            availableMoves.append(piece.availableMoves(self.board))
        return availableMoves
    
    #This method moves a piece to the position "coords" and returns a new matix with the position updated.
    def movePiece(self, piece, coords, matrix, player):

        newMatrix = copy.deepcopy(matrix)
        newMatrix[piece[1]][piece[0]] = 0
        newMatrix[coords[1]][coords[0]] = player
        boardSize = len(newMatrix)
        if coords[0] == (boardSize - 1 )/ 2 and coords[1] == (boardSize - 1)/ 2:
            newMatrix[coords[1]][coords[0]] = 0
        
        return newMatrix
    
    #This method takes in the current position of a piece (x,y) and a matrix and returns a list of available moves that the piece can make.
    def availableMovesPiece(self, x, y, matrix):
        availableMoves = []
                
        #left
        if x > 0 and matrix[y][x - 1] == 0:
            tempX = x - 1
            while (tempX >= 0  and matrix[y][tempX] == 0):
                tempX -= 1
            availableMoves.append((tempX + 1, y))
            
        #right    
        if x < len(matrix) - 1 and matrix[y][x + 1] == 0:
            tempX = x + 1
            while (tempX <= len(matrix) - 1 and matrix[y][tempX] == 0):
                tempX += 1
            availableMoves.append((tempX - 1, y))
            
        #up   
        if y > 0 and matrix[y - 1][x] == 0:
            tempY = y - 1
            while (tempY >= 0  and matrix[tempY][x] == 0):
                tempY -= 1
            availableMoves.append((x, tempY + 1))
            
        #down
        if y < len(matrix[x]) - 1 and matrix[y + 1][x] == 0:
            tempY = y + 1
            while (tempY <= len(matrix) - 1  and matrix[tempY][x] == 0):
                tempY += 1
            availableMoves.append((x, tempY - 1))
            
        return availableMoves
    
    #This method returns a dictionary of available moves for each piece position.
    def availableMovesPlayer(self, player, matrix):
        availableMoves = {}
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == player:
                    availableMoves[(j,i)]=self.availableMovesPiece(j, i, matrix)
                    
        return availableMoves
        
    #This method checks if either player has won 
    def checkWinner(self, matrix):
        numRedPieces = 0
        numBluePieces = 0
        numPieces = len(matrix) - 1
        for line in matrix:
            for piece in line:
                if piece == 1:
                    numRedPieces += 1
                elif piece == 2:
                    numBluePieces += 1   
                    
        if numRedPieces == numPieces - 2:
            return 1
        
        if numBluePieces == numPieces - 2:
            return 2
                
        return 0

    #This method implements a evaluation function according to the Manhattan distance
    def evaluateManhattan(self, matrix, player):
        manhattanDistance = 0
        numPieces = 0
        otherPlayer = 1 if player == 2 else 2
        numOtherPieces = 0
        boardSize = len(matrix)
        mid = len(matrix) // 2
        
        boardSize = len(matrix)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == player:
                    manhattanDistance -= abs(i - mid) + abs(j - mid)
                    numPieces += 1
                elif matrix[i][j] == otherPlayer:
                    numOtherPieces += 1
        
        if manhattanDistance < boardSize - 1:
            manhattanDistance -= 100000
            
        if manhattanDistance < boardSize - 2:
            manhattanDistance -= 100000
            
        if numOtherPieces < boardSize - 1:
            manhattanDistance += 100000
        
        if numOtherPieces < boardSize - 2:
            manhattanDistance += 100000
        
        return manhattanDistance
    
    #This method implements an evaluation function according to the number of available moves of each player 
    def evaluateAvailableMoves(self, matrix, player):
        numAvailableMoves = 0
        numPieces = 0
        numOtherPieces = 0
        if player == 1:
            otherPlayer = 2
        else: otherPlayer = 1
        boardSize = len(matrix)
        
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == player:
                    numAvailableMoves += len(self.availableMovesPiece(j, i, matrix))
                    numPieces += 1
                elif matrix[i][j] == otherPlayer:
                    numOtherPieces += 1
        
        if numPieces < boardSize - 1:
            numAvailableMoves += 100000
            
        if numPieces < boardSize - 2:
            numAvailableMoves += 100000
            
        if numOtherPieces < boardSize - 1:
            numAvailableMoves -= 100000
        
        if numOtherPieces < boardSize - 2:
            numAvailableMoves -= 100000
            
        return numAvailableMoves
    
    #This method implements an evaluation function according to the key positions surrounding the black hole 
    def evaluateBlackHole(self, matrix, player):
        total = 0
        numPieces = 0
        boardSize = len(matrix)
        mid = len(matrix) // 2
        otherPlayer = 1 if player == 2 else 2
        numOtherPieces = 0
        
        #Left
        if (matrix[mid - 1][mid] != 0):
            total += 2
            if(matrix[mid + 1][mid] == player): total += 4
            elif(matrix[mid + 1][mid] != 0): total -= 4
            
            for i in range(mid + 2, len(matrix)):
                if(matrix[i][mid] == player): total += 1
                elif(matrix[i][mid] != 0): total -= 1

        #Right
        if (matrix[mid + 1][mid] != 0):
            total += 2
            if(matrix[mid - 1][mid] == player): total += 4
            elif(matrix[mid - 1][mid] != 0): total -= 4
            
            for i in range(mid - 2, -1, -1):
                if(matrix[i][mid] == player): total += 1
                elif(matrix[i][mid] != 0): total -= 1

        #Top
        if (matrix[mid][mid - 1] != 0):
            total += 2
            if(matrix[mid][mid + 1] == player): total += 4
            elif(matrix[mid][mid + 1] != 0): total -= 4

            for i in range(mid - 2, -1, -1):
                if(matrix[mid][i] == player): total += 1
                elif(matrix[mid][i] != 0): total -= 1
 
        #Down
        if (matrix[mid][mid + 1] != 0):
            total += 2
            if(matrix[mid][mid - 1] == player): total += 4
            elif(matrix[mid][mid - 1] != 0): total -= 4

            for i in range(mid + 2, len(matrix)):
                if(matrix[mid][i] == player): total += 1
                elif(matrix[mid][i] != 0): total -= 1

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == player:
                    numPieces += 1
                elif matrix[i][j] == otherPlayer:
                    numOtherPieces -= 1

        if numPieces < boardSize - 1:
            total += 100000

        if numPieces < boardSize - 2:
            total += 100000
            
        if numOtherPieces < boardSize - 1:
            total -= 100000
        
        if numOtherPieces < boardSize - 2:
            total -= 100000
            
        return total

    # Minimax algorithm
    def minimax(self, depth, maximizingPlayer, player, alpha, beta, matrix, evaluate):

        if depth == 0 or self.checkWinner(matrix) != 0:
            return (), evaluate(matrix, player)
        
        if maximizingPlayer == 1:
            otherMaximizingPlayer = 2
        else:
            otherMaximizingPlayer = 1
        
        bestMove = ()
        availableMoves = self.availableMovesPlayer(maximizingPlayer, matrix)
        if maximizingPlayer == player:
            maxEval = float('-inf')
            for piece in availableMoves:
                for coords in availableMoves[piece]:
                    
                    newBoardMatrix = self.movePiece(piece,coords, matrix, maximizingPlayer)                    
                    eval = self.minimax(depth - 1, otherMaximizingPlayer, player, alpha, beta, newBoardMatrix, evaluate)
                    
                    if eval[1] > maxEval:
                        maxEval = eval[1]
                        bestMove = (piece,coords)
                    elif eval[1] == maxEval:
                        if random.choice([True, False]):
                            bestMove = (piece,coords)
                            
                    alpha = max(alpha, eval[1])
                    if beta <= alpha:
                        break
            return bestMove, maxEval
        
        else:
            minEval = float('inf')
            for piece in availableMoves:
                for coords in availableMoves[piece]:

                    newBoardMatrix = self.movePiece(piece,coords, matrix, maximizingPlayer)
                    eval = self.minimax(depth - 1, otherMaximizingPlayer, player, alpha, beta, newBoardMatrix, evaluate)
                    
                    if eval[1] < minEval:
                        minEval = eval[1]
                        bestMove = (piece,coords)
                    elif eval[1] == minEval:
                        if random.choice([True, False]):
                            bestMove = (piece,coords)
                            
                    beta = min(beta, eval[1])
                    if beta <= alpha:
                        break
            return bestMove, minEval
    
    #Negamax Algorithm
    def negamax(self, depth, color, player, alpha, beta, matrix, evaluate):
        if depth == 0 or self.checkWinner(matrix) != 0:
            return (), color * evaluate(matrix, player)
        
        if color == 1:
            currentPlayer = player
        else:
            currentPlayer = 3 - player
        
        bestMove = ()
        availableMoves = self.availableMovesPlayer(currentPlayer, matrix)
        value = float('-inf')
        for piece in availableMoves:
            for coords in availableMoves[piece]:
                    
                newBoardMatrix = self.movePiece(piece,coords, matrix, currentPlayer)
                
                eval = self.negamax(depth - 1, -color, player, -alpha, -beta, newBoardMatrix, evaluate)
                
                if -eval[1] > value:
                    value = -eval[1]
                    bestMove = (piece,coords)
                elif -eval[1] == value:
                    if random.choice([True, False]):
                        bestMove = (piece,coords)
                        
                alpha = max(alpha, eval[1])
                if beta <= alpha:
                    break
        return bestMove, value
    
    #This method uses minimax to determine the best move and plays according to it
    def movePieceMinimax(self, player, matrix):
        bestMove, _ = self.minimax(self.depth, player, player, float('-inf'), float('inf'), matrix, self.heuristic)
        for piece in self.pieces:
            if piece.x == bestMove[0][0] and piece.y == bestMove[0][1]:
                pieceMoved = piece.moveCoords(bestMove[1], self.board, self.player)
                if piece.checkBlackHole(piece.x, piece.y):
                    self.board.removePiece(piece)
                    self.removePiece(piece)
                return pieceMoved
    
    #This method uses negamax to determine the best move and plays according to it
    def movePieceNegamax(self, player, matrix):
        bestMove, _ = self.negamax(self.depth, 1, player, float('-inf'), float('inf'), matrix, self.heuristic)
        for piece in self.pieces:
            if piece.x == bestMove[0][0] and piece.y == bestMove[0][1]:
                pieceMoved = piece.moveCoords(bestMove[1], self.board, self.player)
                if piece.checkBlackHole(piece.x, piece.y):
                    self.board.removePiece(piece)
                    self.removePiece(piece)
                return pieceMoved
    
    #This method uses monte carlo tree search to determine the best move and plays according to it
    def movePieceMonteCarlo(self, player, matrix):
        
        mcts = MonteCarloTreeSearch()
        initialCoords, finalCoords = mcts.search(matrix, player)
        if not initialCoords == None and not finalCoords == None:

            for piece in self.pieces:
                if piece.x == initialCoords[0] and piece.y == initialCoords[1]:
                    pieceMoved = piece.moveCoords(finalCoords, self.board, self.player)
                    if piece.checkBlackHole(piece.x, piece.y):
                        self.board.removePiece(piece)
                        self.removePiece(piece)
                    return pieceMoved
                
        return False
            
    