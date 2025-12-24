"""
Main application file - imports everything, initializes, and runs the app.
"""
import os
import gc
from tkinter import *  # noqa: F403, F401
from tkinter import PhotoImage, messagebox
import pygame

# Import from organized modules
from config import (
    APP_SCREEN_WIDTH, APP_SCREEN_HEIGHT, APP_FONT, VIOLET
)
from database_manager import DatabaseManager
from utils import clear_userdetail_textfile, scale_image, clear_window
from game_engine import Game
from account_manager import AccountDetails, Setting
from quiz_manager import Quizz
from learning_manager import Learning
from car_manager import CarBrands, UserCarInfo
from ui_pages import welcome_page, home_page, quiz_page, learning_page

# Initialize configuration - maintain backward compatibility with Variables class
class Variables:
    """Backward compatibility wrapper for AppConfig."""
    def __init__(self):
        from config import AppConfig
        self.config = AppConfig()
        self.background_colour = self.config.background_colour
        self.cur = None
        self.conn = None
    
    def changebgcolour(self, newcolour, root):
        """Changes background colour (backward compatibility method)."""
        self.config.change_bg_colour(newcolour, root)
        self.background_colour = self.config.background_colour

variables = Variables()
db_manager = DatabaseManager()

# Initialize the tkinter window
root = Tk()
root.title("app")
root.geometry(f"{APP_SCREEN_WIDTH}x{APP_SCREEN_HEIGHT}+0+0")
root.resizable(True, True)
root.configure(background=variables.background_colour)
APP_ICON = PhotoImage(file="pictures/app-icon.png")
# Try to use Devanagari MT, fallback to system default if not available
try:
    from tkinter import font as tkfont
    available_fonts = tkfont.families()
    if "Devanagari MT" in available_fonts:
        APP_FONT = "Devanagari MT"
    elif "Arial" in available_fonts:
        APP_FONT = "Arial"
    else:
        APP_FONT = "TkDefaultFont"
except:
    APP_FONT = "Arial"  # Safe fallback
root.iconphoto(True, APP_ICON)

# Initialize pygame assets
pygame.init()
pygame.mixer.music.load("background music.mp3")
pygame.mixer.music.play(-1)
GAME_ICON = pygame.image.load("pictures/app-icon.png")
GAME_FONT = pygame.font.Font("Pokemon GB.ttf", 20)
GAME_DETAIL_FONT = pygame.font.Font("Flipahaus-Regular.ttf", 20)
COIN = pygame.image.load("pictures/coin.png")
BG = pygame.image.load("pictures/Background.png")
BG2 = pygame.image.load("pictures/Background 2.png")
BG3 = pygame.image.load("pictures/Background 3.png")
Q2 = pygame.image.load("pictures/q2.png")
Q2_rect = Q2.get_rect(x=180, y=550)
Q5 = pygame.image.load("pictures/q5.png")
Q5_rect = Q5.get_rect(x=1260, y=510)
L1R1 = pygame.image.load("pictures/rect1.png")
L1R2 = pygame.image.load("pictures/rect2.png")
L1R3 = pygame.image.load("pictures/rect3.png")
L1R4 = pygame.image.load("pictures/rect4.png")
L1R5 = pygame.image.load("pictures/rect5.png")
L1R6 = pygame.image.load("pictures/rect6.png")
L1R1_RECT = pygame.mask.from_surface(L1R1)
L1R2_RECT = pygame.mask.from_surface(L1R2)
L1R3_RECT = pygame.mask.from_surface(L1R3)
L1R4_RECT = pygame.mask.from_surface(L1R4)
L1R5_RECT = pygame.mask.from_surface(L1R5)
L1R6_RECT = pygame.mask.from_surface(L1R6)
L2R1 = pygame.image.load("pictures/rect7.png")
L2R1_RECT = pygame.mask.from_surface(L2R1)
L2R2 = pygame.image.load("pictures/rect8.png")
L2R2_RECT = pygame.mask.from_surface(L2R2)
L2R3 = pygame.image.load("pictures/rect9.png")
L2R3_RECT = pygame.mask.from_surface(L2R3)
L2R4 = pygame.image.load("pictures/rect10.png")
L2R4_RECT = pygame.mask.from_surface(L2R4)
L2R5 = pygame.image.load("pictures/rect11.png")
L2R5_RECT = pygame.mask.from_surface(L2R5)
L2R6 = pygame.image.load("pictures/rect12.png")
L2R6_RECT = pygame.mask.from_surface(L2R6)
from config import (
    LEV1_START_POSITION, LEV2_START_POSITION, LEV3_START_POSITION,
    LEV1_FLAG_POSITION, LEV2_FLAG_POSITION, LEV3_FLAG_POSITION
)
LEV1 = pygame.image.load("pictures/lev 1.png")
LEV1_TRACK_BORDER = pygame.image.load("pictures/lev 1 track border.png")
LEV2 = pygame.image.load("pictures/lev 2.tiff")
LEV2_TRACK_BORDER = pygame.image.load("pictures/lev 2 track border.png")
LEV3 = pygame.image.load("pictures/lev 3.tiff")
LEV3_TRACK_BORDER = pygame.image.load("pictures/lev 3 track border.png")

FLAG = scale_image(pygame.image.load("pictures/red flag.png"), 0.2)
FLAG_MASK = pygame.mask.from_surface(FLAG)

# Initialize game and other objects
game = Game()
account_details = AccountDetails()
quizz = Quizz()
learning = Learning()
user_car_info = UserCarInfo()
setting = Setting()
car_brands = CarBrands()

# Import game functions
from game_levels import level1, level2, level3
from game_ui import (
    pygame_win, how_to_play, level1_results_page, level2_results_page, level3_results_page,
    close_pygame_and_return_home, ensure_root_for_easygui, check_coins_to_start_level,
    set_focus_to_window, get_font
)

# Database helper functions
from utils import merge_sort, bubble_sort

def create_database_tables():
    """Creates the tables in the database."""
    db_manager.create_tables()

def delete_user_acc_db():
    """Deletes user account from database."""
    db_manager.delete_user_account(account_details.username)

def l1_leaderboard():
    """Gets Level 1 leaderboard."""
    return db_manager.get_l1_leaderboard(account_details.username, merge_sort)

def l2_leaderboard():
    """Gets Level 2 leaderboard."""
    return db_manager.get_l2_leaderboard(account_details.username, merge_sort)

def l3_leaderboard():
    """Gets Level 3 leaderboard."""
    return db_manager.get_l3_leaderboard(account_details.username, bubble_sort)

def get_l3_highscore():
    """Gets Level 3 highscore."""
    return db_manager.get_highscore(3, account_details.username, bubble_sort)

def get_l2_highscore():
    """Gets Level 2 highscore."""
    return db_manager.get_highscore(2, account_details.username, merge_sort)

def get_l1_highscore():
    """Gets Level 1 highscore."""
    return db_manager.get_highscore(1, account_details.username)

def insert_into_l3():
    """Inserts Level 3 time into database."""
    db_manager.insert_level_time(3, account_details.username, game.level3_time)

def insert_into_l2():
    """Inserts Level 2 time into database."""
    db_manager.insert_level_time(2, account_details.username, game.level2_time)

def insert_into_l1():
    """Inserts Level 1 time into database."""
    db_manager.insert_level_time(1, account_details.username, game.level1_time)

def insert_into_users():
    """Inserts user into database."""
    db_manager.insert_user(account_details.username, account_details.name, account_details.age,
                          account_details.email, account_details.password_reg, quizz.user_coins)

def update_name_db():
    """Updates user name in database."""
    db_manager.update_user_name(account_details.username, account_details.name)

def update_coin_db():
    """Updates user coins in database."""
    db_manager.update_user_coins(account_details.username, quizz.user_coins)

def update_pass_db():
    """Updates user password in database."""
    db_manager.update_user_password(account_details.username, account_details.password_reg)

def set_initial_variables():
    """Sets initial variables from database."""
    item = db_manager.get_user_details(account_details.username, account_details.password_reg)
    if item:
        account_details.name, account_details.age, account_details.email, quizz.user_coins = item

def check_if_username_taken():
    """Checks if username is taken."""
    return db_manager.check_username_exists(account_details.username_textbox.get())

def query_login_info():
    """Queries login information from database."""
    item = db_manager.verify_login(account_details.username1.get(), account_details.password1.get())
    if not item:
        messagebox.showerror("error",
                             "Invalid details.\nPlease try again or register for an account ",
                             icon="warning")
    else:
        account_details.username, account_details.password_reg = item
        set_initial_variables()
        account_details.load_screen()

# Putting game window at the start position 0,0 on the screen display
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)

clear_userdetail_textfile()
create_database_tables()
welcome_page()
# Ensure window is visible and on top
root.deiconify()  # Make sure window is not minimized
root.lift()  # Bring window to front
root.attributes('-topmost', True)  # Bring to front
root.after_idle(lambda: root.attributes('-topmost', False))  # Then allow it to go behind other windows
root.mainloop()
update_coin_db()
pygame.quit()
gc.collect()

