import pygame
import pygame_menu
from settings import windowWidth, windowHeight, screen, theme, RULES
from board import Board
from game import Game

game = Game()

#This method sets the difficulty of the game. 
def setDifficulty(value, difficulty):
    global game
    game.difficulty = difficulty

#This method sets the size of the board. 
def setBoardSize(_, boardSize):
    global game
    game.size = boardSize
    
#This method sets the difficulty of the Computer1. 
def setDifficultyComputer1(_, difficulty):
    global game
    game.difficulty1 = difficulty
    
#This method sets the difficulty of the Computer2. 
def setDifficultyComputer2(_, difficulty):
    global game
    game.difficulty2 = difficulty

#This method sets the player who plays first. 
def setPlayer(_, player):
    global game
    game.playerSelected = player 

#This method sets the Game Mode. 
def setGameMode(_, gameMode):
    global game
    game.gameMode = gameMode

#This method creates the board, the player and starts the game. 
def play():
    global game
    game.createBoard()
    game.createPlayers()
    game.play()

#This method shows the game modes available. 
def gameMode():
    menu._open(gameModeMenu)

#This method shows the menu to the player to choose who plays first.
def player():
    menu._open(playerMenu)

#This method shows the board sizes available.    
def boardSize():
    menu._open(boardSizeMenu)

#This method shows the instructions to play the game.
def instructions():
    menu._open(instructionsMenu)
    
#This method shows the difficulties available for computer1.
def gameDifficulty():
    menu._open(gameDifficulty1ComputerMenu)

#This method shows the difficulties available for computer2.
def computersDifficulty():
    menu._open(gameDifficulty2ComputersMenu)

#This method calls the following method needed according to the option chosen by the player in the main menu.
def switchGameMode():
    global game
    if(game.gameMode == 1):
        play()
    elif(game.gameMode == 2):
        player()
    elif(game.gameMode == 3):
        computersDifficulty()    


#Main menu of the game
menu = pygame_menu.Menu('BlackHole Escape', windowWidth, windowHeight, theme=theme)
menu.add.button('PLAY', boardSize)
menu.add.button('INSTRUCTIONS', instructions)
menu.add.button('QUIT', pygame_menu.events.EXIT)

# Menu fot the GameMode
gameModeMenu = pygame_menu.Menu('Game Mode', windowWidth, windowHeight, theme=theme)
gameModeMenu.add.selector('', [('PLAYER VS PLAYER',1),('PLAYER VS COMPUTER',2),('COMPUTER VS COMPUTER',3)], onchange=setGameMode)
gameModeMenu.add.button('Next', switchGameMode)

# Menu to choose which player plays first
playerMenu = pygame_menu.Menu('Player Selection', windowWidth, windowHeight, theme=theme)
playerMenu.add.selector('',[('PLAYER 1',1),('PLAYER 2',2)], onchange=setPlayer)
playerMenu.add.button('Next',gameDifficulty)

# Menu to choose the size of the game board
boardSizeMenu = pygame_menu.Menu('Board Size Selection', windowWidth, windowHeight, theme=theme)
boardSizeMenu.add.selector('',[('5 X 5',5),('7 X 7',7),('9 X 9', 9)], onchange= setBoardSize)
boardSizeMenu.add.button('Next',gameMode)

# Menu to choose the difficulty of computer1
gameDifficulty1ComputerMenu = pygame_menu.Menu('Difficulty Selection', windowWidth, windowHeight, theme=theme)
gameDifficulty1ComputerMenu.add.selector('',[('EASY 1',1),('EASY 2',2),('MEDIUM 1',3), ('MEDIUM 2',4), ('HARD 1',5), ('HARD 2',6), ('RANDOM', 0)], onchange=setDifficulty)
gameDifficulty1ComputerMenu.add.button('PLAY', play)

# Menu to choose the difficulty of computer2
gameDifficulty2ComputersMenu = pygame_menu.Menu('Difficulty Selection', windowWidth, windowHeight, theme=theme)
gameDifficulty2ComputersMenu.add.selector('Computer 1 ',[('EASY 1',1),('EASY 2',2),('MEDIUM 1',3), ('MEDIUM 2',4), ('HARD 1',5), ('HARD 2',6), ('MTS', 0)], onchange=setDifficultyComputer1)
gameDifficulty2ComputersMenu.add.selector('Computer 2 ',[('EASY 1',1),('EASY 2',2),('MEDIUM 1',3), ('MEDIUM 2',4), ('HARD 1',5), ('HARD 2',6), ('MTS', 0)], onchange=setDifficultyComputer2)
gameDifficulty2ComputersMenu.add.button('PLAY', play)

# Menu with the instructions of the game
instructionsMenu = pygame_menu.Menu('Instructions', windowWidth, windowHeight, theme=theme)
instructionsMenu.add.label(RULES, wordwrap=True, max_char=-1, align=pygame_menu.locals.ALIGN_LEFT)
pygame.init()
menu.mainloop(screen)

