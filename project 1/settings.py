import pygame
import pygame_menu
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
grey = (192, 192, 192)
dark_grey = (48, 48, 48)
select_grey = (96, 96, 96)
red = (255, 0, 0)
blue = (0, 0, 255)

# ==================== GAME FONTS ====================

titleFont = pygame.font.Font('freesansbold.ttf', 32)
optionsFont = pygame_menu.font.FONT_MUNRO
menuFont = pygame_menu.font.FONT_8BIT


# ==================== GAME SETTINGS ====================

windowWidth = 890
windowHeight = 740
screen = pygame.display.set_mode((windowWidth, windowHeight))
background = pygame.image.load('background.png')

theme = pygame_menu.themes.THEME_DARK.copy()
theme.title_font = menuFont
theme.title_font_color = white
theme.widget_font = optionsFont
theme.background_color = black
theme.widget_font_color = white
theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
theme.title_background_color = blue
theme.widget_font_size = 50
theme.widget_padding = 10

# ===================== GAME RULES =====================

RULES = "This game is a two player game.\n\
To select a piece you want to move, click it with the mouse.\n\
Move the selected piece with the arrow keys, to the direction you want.\n\
The player who places two of their pieces in the center position, wins."





