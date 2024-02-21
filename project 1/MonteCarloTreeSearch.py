from node import Node
import copy
import random

#Monte Carlo Tree Search Algorithm class
class MonteCarloTreeSearch:
    #Initializes the class with an exploration constant that determines the balance between exploration and exploitation.
    def __init__(self, explorationConstant=1.4) -> None:
        self.explorationConstant = explorationConstant
    
    #This method returns the other player given the current player.
    def otherPlayer(self, player):
        if player == 1:
            return 2
        else:
            return 1
        
    #This method checks if the current state is terminal (winning or losing state).
    def isTerminal(self, matrix):
        numPiecesPlayer1 = 0
        numPiecesPlayer2 = 0
        numPieces = len(matrix) - 1
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    numPiecesPlayer1 += 1
                elif matrix[i][j] == 2:
                    numPiecesPlayer2 += 1
                        
        if numPiecesPlayer2 == numPieces - 2 or numPiecesPlayer1 == numPieces - 2:
            return True
        return False

    #This method performs the search by starting at the root node and repeatedly selecting, expanding, simulating, and backpropagating nodes until the maximum number of iterations is reached. 
    def search(self, initialState, player, maxIterations=30):
        root = Node(initialState, player)
        
        for i in range(maxIterations):
            node = root
            state = copy.deepcopy(initialState)
            
            while not self.isTerminal(state):
                                
                if not node.isFullyExpanded():
                    self.expand(node, state)
                else:
                    newNode = self.select(node)
                    if newNode == node:
                        return None, None
                    node = newNode
                    state = node.matrix
                    
            score = self.simulation(node, state)
            self.backpropagate(node, score) 
        
        return self.getBestMove(root)
        
    #This method selects the best child node to expand by computing the UCT for each child node and choosing the one with the highest value.
    def select(self, node):
        if node.children == []:
            return node
        bestChild = node.children[0]
        for child in node.children:
            if child.getUCT() > bestChild.getUCT():
                bestChild = child
            elif child.getUCT() == bestChild.getUCT():
                if random.choice([True, False]):
                    bestChild = child
        return bestChild
    
    #This method creates a new child node by selecting an available move and applying it to the current state
    def expand(self, node, state):
        (coords, move) = node.availableMoves.pop(0)

        newBoardMatrix = self.movePiece(coords, move, state, node.player)
        childNode = Node(newBoardMatrix, self.otherPlayer(node.player), node)
        node.children.append(childNode)
        return childNode
    
    #This method selects moves at random until a terminal state is reached, and then returns the score for the final state.
    def simulation(self, node, state):
        newBoardMatrix = copy.deepcopy(state)
        player = node.player
        currentPlayer = player
        
        while not self.isTerminal(newBoardMatrix):
            
            moves = []
            while moves == []:
                coords, move = random.choice(node.availableMoves)

                newBoardMatrix = self.movePiece(coords, move, node.matrix, currentPlayer)
                node = Node(newBoardMatrix, self.otherPlayer(currentPlayer), node)
                currentPlayer = self.otherPlayer(currentPlayer)
            
        return node.getScore(newBoardMatrix, player)
    
    #This method updates the results and visit count of each node in the path from the newly expanded node to the root node.
    def backpropagate(self, node, score):

        while node is not None:

            visits = node.visits
            node.visits = visits + 1
            node.results[score] += 1
            node = node.parent
            
    #This method moves the given piece to the "coords" location on the board.
    def movePiece(self, piece, coords, matrix, player):
        newMatrix = copy.deepcopy(matrix)
 
        newMatrix[piece[1]][piece[0]] = 0
        newMatrix[coords[1]][coords[0]] = player
        boardSize = len(newMatrix)
        if coords[0] == (boardSize - 1 )/ 2 and coords[1] == (boardSize - 1)/ 2:
            newMatrix[coords[1]][coords[0]] = 0
            
        return newMatrix
    
    #This method returns the best move
    def getBestMove(self, node):
        bestChild = self.select(node)
        node.finalPieces = bestChild.countPieces(node.player)
        return node.getMovingPiece()
    
    
