"""
Game UI module containing pygame_win, how_to_play, results pages, and helper functions.
"""
import time
import pygame
import pyautogui
from config import (
    RED, LIGHT_RED, ORANGE, YELLOW, DARK_GREEN, LIGHT_GREEN, LIGHT_BLUE,
    DARK_BLUE, VIOLET, PURPLE, PINK, GREY, BLACK, WHITE
)
from game_engine import Button1, write_text_to_centre
# home_page will be accessed via get_main_refs() to avoid circular imports


def get_main_refs():
    """Gets references to main module objects to avoid circular imports."""
    import __main__ as main
    return main


def set_focus_to_window():
     """Helper function for focus management during quizzes."""
     main = get_main_refs()
     root = main.root
     # Don't deiconify root during game levels - easygui creates its own dialogs
     # Just update root to ensure it's accessible if needed
     try:
          root.update()
     except:
          pass
     x, y = pyautogui.position()
     pyautogui.click(50, 100, duration=0)
     pyautogui.moveTo(x=x, y=y, duration=0)


def get_font(size):
     return pygame.font.Font("font.ttf", size)


# displays all instructions and rules for each level


def how_to_play():
     main = get_main_refs()
     game = main.game
     BG = main.BG
     BG2 = main.BG2
     BG3 = main.BG3
     # pygame_win is in the same module, so it's accessible directly

     pygame.display.quit()
     game.screen = None  # Reset screen reference after quit
     game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
     running = True
     while running:
          PLAY_MOUSE_POS = pygame.mouse.get_pos()
          game.screen.blit(BG2, (0, 0))  # type: ignore
          PLAY_BACK = Button1(image=None, pos=(1200, 50),
                              text_input="BACK TO GAME PAGE", font=get_font(20), base_color=GREY, hovering_color=PURPLE)

          PLAY_BACK.changeColor(PLAY_MOUSE_POS)
          PLAY_BACK.update()

          texts = [
               (get_font(30).render("LEVEL 1:", True, DARK_GREEN), (90, 70)),
               (get_font(20).render("- all quizzes are compulsory", True, WHITE), (90, 120)),
               (get_font(20).render("- reward for answering a compulsory quiz correctly is 3 coins", True, WHITE),
                (90, 170)),
               (get_font(20).render("- timer pauses while doing quizzes", True, WHITE), (90, 220)),
               (get_font(30).render("LEVEL 2:", True, DARK_GREEN), (90, 270)),
               (get_font(20).render("- some quizzes are compulsory and some are optional", True, WHITE), (90, 320)),
               (get_font(20).render("- reward for a compulsory quiz = 3 coins, optional quiz = 5 coins", True, WHITE),
                (90, 370)),
               (get_font(20).render("- to do an optional quiz, you have to be near the sign and click it", True, WHITE),
                (90, 420)),
               (get_font(20).render("- timer pauses while doing compulsory quizzes but not optional ones", True, WHITE),
                (90, 470)),
               (get_font(20).render("- cumpulsary quiz = green sign , optional quiz = pink sign", True, WHITE),
                (90, 520)),
               (get_font(30).render("LEVEL 3:", True, DARK_GREEN), (90, 570)),
               (get_font(20).render("- there are no quizzez but you have to get through a maze.", True, WHITE),
                (90, 620)), #but you can collect coins in the maze
               (get_font(20).render("PRESS THE ESCAPE KEY TO EXIT A LEVEL AT ANY TIME!", True, RED), (90, 690)),
          ]

          for surface, pos in texts:
               game.screen.blit(surface, pos)  # type: ignore
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
                    break

               if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                         pygame_win()
                         running = False
                         break

          pygame.display.update()

# displays the time taken, best score, and leader board of level 3


def level3_results_page():
     main = get_main_refs()
     game = main.game
     quizz = main.quizz
     l3_leaderboard = main.l3_leaderboard
     get_l3_highscore = main.get_l3_highscore
     update_coin_db = main.update_coin_db
     BG = main.BG
     BG2 = main.BG2
     BG3 = main.BG3

     quizz.user_coins += game.level_coins
     update_coin_db()  # Save coins to database
     if game.screen is None:
          game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
     top_5 = l3_leaderboard()
     print(top_5)
     running = True
     while running:
          PLAY_MOUSE_POS = pygame.mouse.get_pos()
          if game.screen is None:
               game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
          game.screen.blit(BG3, (0, 0))  # type: ignore
          pygame.display.set_caption("results page")
          back_game = Button1(image=None, pos=(1200, 90),
                              text_input=f"BACK TO GAME PAGE", font=get_font(20), base_color=GREY,
                              hovering_color=PURPLE)

          back_game.changeColor(PLAY_MOUSE_POS)
          back_game.update()

          texts = [
               (get_font(30).render("LEVEL 3 RESULTS:", True, DARK_GREEN), (500, 70)),
               (get_font(20).render(f"Time taken to complete: {game.level3_time} seconds", True, WHITE), (50, 200)),
               (get_font(20).render(f"Best score: {get_l3_highscore()} seconds", True, WHITE), (50, 300)),
               (get_font(20).render(f"Leader board:", True, WHITE), (50, 350)),
          ]
          # Add leaderboard entries only if they exist
          for i in range(min(5, len(top_5))):
               texts.append((get_font(20).render(f"{i+1} - {top_5[i][0]} seconds", True, WHITE), (50, 400 + i * 50)))

          for surface, pos in texts:
               game.screen.blit(surface, pos)  # type: ignore

          # Add quit button
          quit_button = Button1(image=None, pos=(1200, 150), text_input="QUIT TO HOMEPAGE", font=get_font(20),
                               base_color=RED, hovering_color=LIGHT_RED)
          quit_button.changeColor(PLAY_MOUSE_POS)
          quit_button.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
                    break

               if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.checkForInput(PLAY_MOUSE_POS):
                         running = False
                         break
                    if back_game.checkForInput(PLAY_MOUSE_POS):
                         game.level_coins = 0
                         pygame_win()
                         running = False
                         break

          pygame.display.update()
     
     # After loop exits, quit pygame and return to home
     if not running:
          close_pygame_and_return_home()

# level 3 game page


def level2_results_page():
     main = get_main_refs()
     game = main.game
     quizz = main.quizz
     l2_leaderboard = main.l2_leaderboard
     get_l2_highscore = main.get_l2_highscore
     update_coin_db = main.update_coin_db
     BG = main.BG
     BG2 = main.BG2
     BG3 = main.BG3

     quizz.user_coins += game.level_coins
     update_coin_db()  # Save coins to database
     if game.screen is None:
          game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
     top_5 = l2_leaderboard()
     running = True
     while running:
          PLAY_MOUSE_POS = pygame.mouse.get_pos()
          if game.screen is None:
               game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
          game.screen.blit(BG3, (0, 0))  # type: ignore
          pygame.display.set_caption("results page")
          back_game = Button1(image=None, pos=(1200, 90), text_input=f"BACK TO GAME PAGE", font=get_font(20),
                              base_color=GREY, hovering_color=PURPLE)
          back_game.changeColor(PLAY_MOUSE_POS)
          back_game.update()

          texts = [
               (get_font(30).render("LEVEL 2 RESULTS:", True, DARK_GREEN), (500, 70)),
               (get_font(20).render(f"Time taken to complete: {game.level2_time} seconds", True, WHITE), (50, 200)),
               (get_font(20).render(f"Total coins earned: {game.level_coins}", True, WHITE), (50, 250)),
               (get_font(20).render(f"Best score: {get_l2_highscore()} seconds", True, WHITE), (50, 300)),
               (get_font(20).render("Leader board:", True, WHITE), (50, 350)),
          ]
          # Add leaderboard entries only if they exist
          for i in range(min(5, len(top_5))):
               texts.append((get_font(20).render(f"{i+1} - {top_5[i][0]} seconds", True, WHITE), (50, 400 + i * 50)))

          for surface, pos in texts:
               game.screen.blit(surface, pos)  # type: ignore

          # Add quit button
          quit_button = Button1(image=None, pos=(1200, 150), text_input="QUIT TO HOMEPAGE", font=get_font(20),
                               base_color=RED, hovering_color=LIGHT_RED)
          quit_button.changeColor(PLAY_MOUSE_POS)
          quit_button.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
                    break

               if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.checkForInput(PLAY_MOUSE_POS):
                         running = False
                         break
                    if back_game.checkForInput(PLAY_MOUSE_POS):
                         game.level_coins = 0
                         pygame_win()
                         running = False
                         break

          pygame.display.update()
     
     # After loop exits, quit pygame and return to home
     if not running:
          close_pygame_and_return_home()

# quizzez for level 2


def close_pygame_and_return_home():
     """Properly closes pygame window and returns to homepage."""
     main = get_main_refs()
     game = main.game
     root = main.root
     home_page = main.home_page
     game.level_coins = 0
     game.rootdestroyed = False
     
     # Save music state before quitting
     music_was_playing = False
     try:
          music_was_playing = pygame.mixer.music.get_busy()
     except:
          pass
     
     # Post QUIT event to pygame to properly close the window
     try:
          if pygame.display.get_init():
               pygame.event.post(pygame.event.Event(pygame.QUIT))
               pygame.display.quit()
          # Fully quit pygame to ensure window closes on macOS
          pygame.quit()
     except:
          pass
     
     # Wait a moment to ensure pygame window closes (important on macOS)
     time.sleep(0.1)
     
     # Reinitialize pygame for music (but don't create display)
     pygame.init()
     try:
          pygame.mixer.music.load("background music.mp3")
          if music_was_playing:
               pygame.mixer.music.play(-1)
     except:
          pass
     
     game.screen = None
     
     # Force Tkinter window to front - use multiple methods for reliability
     root.deiconify()
     root.attributes('-topmost', True)
     root.lift()
     root.update()
     root.update_idletasks()
     root.attributes('-topmost', False)
     root.lift()
     root.update()
     try:
          root.focus_force()
     except:
          pass
     # Call home_page which will also ensure pygame is closed
     home_page()

# displays the time taken, best score, and leader board of level 1


def level1_results_page():
     main = get_main_refs()
     game = main.game
     quizz = main.quizz
     l1_leaderboard = main.l1_leaderboard
     get_l1_highscore = main.get_l1_highscore
     update_coin_db = main.update_coin_db
     BG = main.BG
     BG2 = main.BG2
     BG3 = main.BG3

     quizz.user_coins += game.level_coins
     update_coin_db()  # Save coins to database
     if game.screen is None:
          game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
     top_5 = l1_leaderboard()
     running = True
     while running:
          PLAY_MOUSE_POS = pygame.mouse.get_pos()
          if game.screen is None:
               game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
          game.screen.blit(BG3, (0, 0))  # type: ignore
          pygame.display.set_caption("results page")
          back_game = Button1(image=None, pos=(1200, 90), text_input=f"BACK TO GAME PAGE", font=get_font(20),
                              base_color=GREY, hovering_color=PURPLE)
          back_game.changeColor(PLAY_MOUSE_POS)
          back_game.update()

          texts = [
               (get_font(30).render("LEVEL 1 RESULTS:", True, DARK_GREEN), (500, 70)),
               (get_font(20).render(f"Time taken to complete: {game.level1_time} seconds", True, WHITE), (50, 200)),
               (get_font(20).render(f"Total coins earned: {game.level_coins}", True, WHITE), (50, 250)),
               (get_font(20).render(f"Best score: {get_l1_highscore()} seconds", True, WHITE), (50, 300)),
               (get_font(20).render("Leader board:", True, WHITE), (50, 350)),
          ]
          # Add leaderboard entries only if they exist
          for i in range(min(5, len(top_5))):
               texts.append((get_font(20).render(f"{i+1} - {top_5[i][0]} seconds", True, WHITE), (50, 400 + i * 50)))

          for surface, pos in texts:
               game.screen.blit(surface, pos)  # type: ignore

          # Add quit button
          quit_button = Button1(image=None, pos=(1200, 150), text_input="QUIT TO HOMEPAGE", font=get_font(20),
                               base_color=RED, hovering_color=LIGHT_RED)
          quit_button.changeColor(PLAY_MOUSE_POS)
          quit_button.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
                    break

               if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.checkForInput(PLAY_MOUSE_POS):
                         running = False
                         break
                    if back_game.checkForInput(PLAY_MOUSE_POS):
                         game.level_coins = 0
                         pygame_win()
                         running = False
                         break

          pygame.display.update()
     
     # After loop exits, quit pygame and return to home
     if not running:
          close_pygame_and_return_home()

# Helper function to ensure root window is available for easygui


def ensure_root_for_easygui():
     main = get_main_refs()
     root = main.root

     """Ensure Tkinter root window is available for easygui dialogs without showing it."""
     # Easygui needs the root window to exist but doesn't need it to be visible
     # If we're in a game level (rootdestroyed=True), keep the root hidden
     # Just ensure it's accessible for easygui's internal use by updating it
     # Don't deiconify - easygui creates its own Toplevel windows
     try:
          root.update()
          root.update_idletasks()
     except:
          # If root was destroyed, we need to recreate it (shouldn't happen)
          pass

# the quizzez for level 1


def check_coins_to_start_level():
     main = get_main_refs()
     quizz = main.quizz
     update_coin_db = main.update_coin_db
     from tkinter import messagebox

     if quizz.user_coins >= 2:
          quizz.user_coins -= 2
          update_coin_db()  # Save coins to database
          return True
     else:
          messagebox.showerror("error", "Not enough coins to start level.\n You need at least 2 coins.")
          return False


# inital game window with all level buttons


def pygame_win():
     # Always reinitialize display if screen is None or display was quit
     main = get_main_refs()
     game = main.game
     quizz = main.quizz
     root = main.root
     BG = main.BG
     BG2 = main.BG2
     BG3 = main.BG3
     level1 = main.level1
     level2 = main.level2
     level3 = main.level3
     check_coins_to_start_level = main.check_coins_to_start_level
     how_to_play = main.how_to_play

     if game.screen is None:
          game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
     # Ensure pygame.display is initialized
     if not pygame.display.get_init():
          pygame.display.init()
          game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
     if not game.rootdestroyed:
          root.withdraw()
          game.rootdestroyed = True
     running = True
     while running:
          # Reinitialize if screen is None or display was quit
          if game.screen is None or not pygame.display.get_init():
               pygame.display.init()
               game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
          try:
               game.screen.blit(BG, (0, 0))  # type: ignore
          except pygame.error:
               # Display was quit, reinitialize
               pygame.display.init()
               game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
               game.screen.blit(BG, (0, 0))  # type: ignore
          GAME_MOUSE_POS = pygame.mouse.get_pos()
          GAME_TEXT = get_font(50).render("GAME PAGE", True, PURPLE)
          GAME_RECT = GAME_TEXT.get_rect(center=(720, 100))

          user_coin_text = get_font(20).render(f"total coins: {quizz.user_coins}", True, WHITE)
          user_coin_rect = user_coin_text.get_rect(center=(1200, 50))

          HOW_TO_PLAY_BUTTON = Button1(image=pygame.image.load("pictures/how to play rect.png"),
                                       text_input="HOW TO PLAY",
                                       pos=(720, 250), font=get_font(40), base_color=WHITE, hovering_color=LIGHT_BLUE)

          LEVEL1_BUTTON = Button1(image=pygame.image.load("pictures/level 1 rect.png"), pos=(720, 350),
                                  text_input="LEVEL 1",
                                  font=get_font(40), base_color=WHITE, hovering_color=LIGHT_GREEN)
          LEVEL2_BUTTON = Button1(image=pygame.image.load("pictures/level 2 rect.png"), pos=(720, 450),
                                  text_input="LEVEL 2", font=get_font(40), base_color=WHITE, hovering_color=LIGHT_GREEN)
          LEVEL3_BUTTON = Button1(image=pygame.image.load("pictures/level 3 rect.png"), pos=(720, 550),
                                  text_input="LEVEL 3", font=get_font(40), base_color=WHITE, hovering_color=LIGHT_GREEN)
          QUIT_BUTTON = Button1(image=pygame.image.load("pictures/quit rect.png"), pos=(720, 650),
                                text_input="QUIT", font=get_font(40), base_color=WHITE, hovering_color=RED)
          game.screen.blit(GAME_TEXT, GAME_RECT)  # type: ignore
          game.screen.blit(user_coin_text, user_coin_rect)  # type: ignore
          for button in [HOW_TO_PLAY_BUTTON, LEVEL1_BUTTON, LEVEL2_BUTTON, LEVEL3_BUTTON, QUIT_BUTTON]:
               button.changeColor(GAME_MOUSE_POS)
               button.update()
          pygame.display.update()

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
                    break

               if event.type == pygame.MOUSEBUTTONDOWN:
                    if HOW_TO_PLAY_BUTTON.checkForInput(GAME_MOUSE_POS):
                         how_to_play()
                    if LEVEL1_BUTTON.checkForInput(GAME_MOUSE_POS):
                         if check_coins_to_start_level():
                              level1()
                    if LEVEL2_BUTTON.checkForInput(GAME_MOUSE_POS):
                         if check_coins_to_start_level():
                              level2()
                    if LEVEL3_BUTTON.checkForInput(GAME_MOUSE_POS):
                         if check_coins_to_start_level():
                              level3()

                    if QUIT_BUTTON.checkForInput(GAME_MOUSE_POS):
                         running = False
                         break
     
     # After loop exits, quit pygame and return to home
     if not running:
          close_pygame_and_return_home()

# link to spec - bubble sort
# Sorting functions are now imported from utils module
# merge function is also in utils module

# link to spec - Complex data model in database (eg several interlinked tables)



