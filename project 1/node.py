import random
import math
import copy
from collections import defaultdict

#Node class
class Node:
    #Initializes a Node instance with the given board matrix, player, parent node (defaulted to None), and parentMove (defaulted to None)
    def __init__(self, matrix, player, parent=None, parentMove=None):
        self.matrix = matrix #Matrix internal representation
        self.player = player #Player current playing
        self.children = [] #List of node children
        self.visits = 0 # visits
        self.score = 0 # score
        self.results = defaultdict(int) # results of the game
        self.parent = parent # parent node
        self.availableMoves = self.availableMovesPlayer(player, matrix) #available moves for the current matrix
        self.initialPieces = self.countPieces(player) #list of initial pieces of the player
        self.finalPieces = [] #list of final pieces of the player
        
    #This method returns a list of the pieces of a given player
    def countPieces(self, player):
        pieces = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == player:
                    pieces.append((j, i))
                    
        return pieces
    
    #This method calculates the Q-value (wins minus losses) of the node.
    def q(self):
        wins = self.results[1]
        losses = self.results[-1]
        return wins - losses
    
    #This method returns the initial and final coordinates of the piece being moved.
    def getMovingPiece(self):
        initialCoords = ()
        finalCoords = ()
        
        for coords in self.initialPieces:
            if coords not in self.finalPieces:
                initialCoords = coords
                
        for coords in self.finalPieces:
            if coords not in self.initialPieces:
                finalCoords = coords
                
        return initialCoords, finalCoords
    
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
        
    #This method adds a child node to the node's list of children and sets the child's parent.
    def addChild(self, child):
        child.parent = self
        self.children.append(child)
    
    #This method returns the score of a given matrix according a given player
    def getScore(self, matrix, MCTSplayer):     
        if self.checkWinner(matrix) == MCTSplayer:
            return 1
        return -1
    
    #This method calculates the UCT value
    def getUCT(self):
        if self.visits == 0:
            return float('inf')
        return (self.q() / self.visits) + 0.1 * math.sqrt(2 * math.log(self.visits) / self.visits)
    
        
    #This method returns True if the node has no available moves left to expand.
    def isFullyExpanded(self):
        return len(self.availableMoves) == 0
    
    #This method returns a list of all available moves for a given player 
    def availableMovesPlayer(self, player, matrix):
        availableMoves = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == player:
                    for move in self.availableMovesPiece(j,i,matrix):
                        availableMoves.append(((j,i),move))
        return availableMoves
    
    #This method returns a list of all available moves for a piece at the given x and y coordinates
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
    
    

    