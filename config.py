"""
Configuration module containing constants, colors, and application settings.
"""
import pygame
from tkinter import PhotoImage

# Screen dimensions
APP_SCREEN_WIDTH, APP_SCREEN_HEIGHT = 1440, 790

# Color constants
RED = "#E60000"
LIGHT_RED = "#FF4444"
ORANGE = "#FF9100"
YELLOW = "#FFFF00"
DARK_GREEN = "#007F15"
LIGHT_GREEN = "#5EFF36"
LIGHT_BLUE = "#00EFFF"
DARK_BLUE = "#0033FF"
VIOLET = "#CCCCFF"
PURPLE = "#9933FF"
PINK = "#FF00EF"
GREY = "#8D8D8D"
BLACK = "#000000"
WHITE = "#FFFFFF"

# App settings
APP_FONT = "Devanagari MT"
FRAMES_PER_SEC = 60
SCALE = 0.07

# Car file paths
BLUE_CAR = "pictures/blue car.png"
RED_CAR = "pictures/red car.png"
ORANGE_CAR = "pictures/orange car.png"
YELLOW_CAR = "pictures/yellow car.png"
GREEN_CAR = "pictures/green car.png"
PURPLE_CAR = "pictures/purple car.png"
WHITE_CAR = "pictures/white car.png"
POLICE_CAR = "pictures/police car.png"

# Level positions
LEV1_START_POSITION = (70, 725)
LEV1_FLAG_POSITION = (1010, 0)
LEV2_START_POSITION = (720, 330)
LEV2_FLAG_POSITION = (690, 80)
LEV3_START_POSITION = (80, 725)
LEV3_FLAG_POSITION = (1040, 710)

# Color dictionary for background changes
COLOUR_DICT = {
    "RED": RED,
    "ORANGE": ORANGE,
    "YELLOW": YELLOW,
    "DARK_GREEN": DARK_GREEN,
    "LIGHT_GREEN": LIGHT_GREEN,
    "LIGHT_BLUE": LIGHT_BLUE,
    "DARK_BLUE": DARK_BLUE,
    "VIOLET": VIOLET,
    "PURPLE": PURPLE,
    "PINK": PINK,
    "GREY": GREY,
    "WHITE": WHITE
}


class AppConfig:
    """Manages application configuration and global state."""
    
    def __init__(self):
        self.background_colour = VIOLET
        self.cur = None
        self.conn = None
    
    def change_bg_colour(self, newcolour, root):
        """Changes the background colour of the root window."""
        if newcolour in COLOUR_DICT:
            root.configure(background=COLOUR_DICT[newcolour])
            self.background_colour = COLOUR_DICT[newcolour]


class PygameAssets:
    """Manages pygame assets and initialization."""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load("background music.mp3")
        pygame.mixer.music.play(-1)
        
        # Load images
        self.GAME_ICON = pygame.image.load("pictures/app-icon.png")
        self.GAME_FONT = pygame.font.Font("Pokemon GB.ttf", 20)
        self.GAME_DETAIL_FONT = pygame.font.Font("Flipahaus-Regular.ttf", 20)
        self.COIN = pygame.image.load("pictures/coin.png")
        self.BG = pygame.image.load("pictures/Background.png")
        self.BG2 = pygame.image.load("pictures/Background 2.png")
        self.BG3 = pygame.image.load("pictures/Background 3.png")
        
        # Question images
        self.Q2 = pygame.image.load("pictures/q2.png")
        self.Q2_rect = self.Q2.get_rect(x=180, y=550)
        self.Q5 = pygame.image.load("pictures/q5.png")
        self.Q5_rect = self.Q5.get_rect(x=1260, y=510)
        
        # Level 1 rectangles
        self.L1R1 = pygame.image.load("pictures/rect1.png")
        self.L1R2 = pygame.image.load("pictures/rect2.png")
        self.L1R3 = pygame.image.load("pictures/rect3.png")
        self.L1R4 = pygame.image.load("pictures/rect4.png")
        self.L1R5 = pygame.image.load("pictures/rect5.png")
        self.L1R6 = pygame.image.load("pictures/rect6.png")
        self.L1R1_RECT = pygame.mask.from_surface(self.L1R1)
        self.L1R2_RECT = pygame.mask.from_surface(self.L1R2)
        self.L1R3_RECT = pygame.mask.from_surface(self.L1R3)
        self.L1R4_RECT = pygame.mask.from_surface(self.L1R4)
        self.L1R5_RECT = pygame.mask.from_surface(self.L1R5)
        self.L1R6_RECT = pygame.mask.from_surface(self.L1R6)
        
        # Level 2 rectangles
        self.L2R1 = pygame.image.load("pictures/rect7.png")
        self.L2R1_RECT = pygame.mask.from_surface(self.L2R1)
        self.L2R2 = pygame.image.load("pictures/rect8.png")
        self.L2R2_RECT = pygame.mask.from_surface(self.L2R2)
        self.L2R3 = pygame.image.load("pictures/rect9.png")
        self.L2R3_RECT = pygame.mask.from_surface(self.L2R3)
        self.L2R4 = pygame.image.load("pictures/rect10.png")
        self.L2R4_RECT = pygame.mask.from_surface(self.L2R4)
        self.L2R5 = pygame.image.load("pictures/rect11.png")
        self.L2R5_RECT = pygame.mask.from_surface(self.L2R5)
        self.L2R6 = pygame.image.load("pictures/rect12.png")
        self.L2R6_RECT = pygame.mask.from_surface(self.L2R6)
        
        # Level tracks
        self.LEV1 = pygame.image.load("pictures/lev 1.png")
        self.LEV1_TRACK_BORDER = pygame.image.load("pictures/lev 1 track border.png")
        self.LEV2 = pygame.image.load("pictures/lev 2.tiff")
        self.LEV2_TRACK_BORDER = pygame.image.load("pictures/lev 2 track border.png")
        self.LEV3 = pygame.image.load("pictures/lev 3.tiff")
        self.LEV3_TRACK_BORDER = pygame.image.load("pictures/lev 3 track border.png")
        
        # Flag
        self.FLAG = self.scale_image(pygame.image.load("pictures/red flag.png"), 0.2)
        self.FLAG_MASK = pygame.mask.from_surface(self.FLAG)
    
    @staticmethod
    def scale_image(image, scale_factor):
        """Resizes an image based on a scale factor."""
        size = round(image.get_width() * scale_factor), round(image.get_height() * scale_factor)
        return pygame.transform.scale(image, size)


class TkinterAssets:
    """Manages Tkinter assets."""
    
    def __init__(self):
        self.APP_ICON = PhotoImage(file="pictures/app-icon.png")
