"""
Game levels module containing level1, level2, level3 and all quiz functions.
"""
import time
import pygame
import easygui as eg
from config import (
    FRAMES_PER_SEC, LEV1_START_POSITION, LEV2_START_POSITION, LEV3_START_POSITION,
    LEV1_FLAG_POSITION, LEV2_FLAG_POSITION, LEV3_FLAG_POSITION
)
from game_engine import move_user, draw_on_screen, write_text_to_centre
from car_manager import UserCar


def get_main_refs():
    """Gets references to main module objects to avoid circular imports."""
    import __main__ as main
    return main


def l2_quiz6():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     game.startq_time = time.time()  # type: ignore
     q = "Whats this sign?"
     ans = "no bicycle"
     text = eg.enterbox(msg=q, title="quiz 6")
     if text:
          if text.lower() == ans:
               game.level_coins += 3
               game.q12 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
               game.q12 = True
     else:
          game.q12 = False




def l2_quiz5():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     q = "Whats this sign?"
     ans = "no waiting"
     text = eg.enterbox(msg=q, title="quiz 5")
     if text:
          if text.lower() == ans:
               game.level_coins += 5
               game.q11 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")

          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")

               game.q11 = True




def l2_quiz4():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     game.startq_time = time.time()  # type: ignore
     q = "Whats this sign?"
     ans = "airport"
     text = eg.enterbox(msg=q, title="quiz 4")
     if text:
          if text.lower() == ans:
               game.level_coins += 3
               game.q10 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
               game.q10 = True
     else:
          game.q10 = False




def l2_quiz3():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     game.startq_time = time.time()  # type: ignore
     q = "Whats this sign?"
     ans = "wild horses"
     text = eg.enterbox(msg=q, title="quiz 3")
     if text:
          if text.lower() == ans:
               game.level_coins += 3
               game.q9 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
               game.q9 = True
     else:
          game.q9 = False




def l2_quiz2():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     q = "Whats this sign?"
     ans = "level crossing without barrier"
     text = eg.enterbox(msg=q, title="quiz 2")
     if text:
          if text.lower() == ans:
               game.level_coins += 5
               game.q8 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")

          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")

               game.q8 = True




def l2_quiz1():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     game.startq_time = time.time()  # type: ignore
     q = "Whats this sign?"
     ans = "parking"
     text = eg.enterbox(msg=q, title="quiz 1")
     if text:
          if text.lower() == ans:
               game.level_coins += 3
               game.q7 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
               game.q7 = True

     else:
          game.q7 = False

# level 2 game page


def level2():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     set_focus_to_window = main.set_focus_to_window
     pygame_win = main.pygame_win
     level2_results_page = main.level2_results_page
     LEV2 = main.LEV2
     LEV2_TRACK_BORDER = main.LEV2_TRACK_BORDER
     FLAG = main.FLAG
     FLAG_MASK = main.FLAG_MASK
     GAME_FONT = main.GAME_FONT
     Q2 = main.Q2
     Q5 = main.Q5
     Q2_rect = main.Q2_rect
     Q5_rect = main.Q5_rect
     L2R1_RECT = main.L2R1_RECT
     L2R2_RECT = main.L2R2_RECT
     L2R3_RECT = main.L2R3_RECT
     L2R4_RECT = main.L2R4_RECT
     L2R5_RECT = main.L2R5_RECT
     L2R6_RECT = main.L2R6_RECT
     pygame.display.quit()
     game.screen = None  # Reset screen reference after quit
     user_car_info.max_velocity = 2
     game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
     TRACK_BORDER_MASK = pygame.mask.from_surface(LEV2_TRACK_BORDER)
     user_car = UserCar(3, LEV2_START_POSITION)
     pygame.display.set_caption("level 2")
     clock = pygame.time.Clock()
     images = [[Q2, (180, 550)], [Q5, (1260, 510)], (LEV2, (0, 0)), (FLAG, LEV2_FLAG_POSITION)]
     run = True

     while run:
          clock.tick(FRAMES_PER_SEC)
          GAME_MOUSE_POS = pygame.mouse.get_pos()
          draw_on_screen(images, user_car)
          while not game.level_started:
               write_text_to_centre(GAME_FONT, "PRESS ANY KEY TO START LEVEL 2!")
               pygame.display.update()
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         game.reset()
                         run = False
                         pygame_win()
                         break
                    if event.type == pygame.KEYDOWN:
                         if event.key != pygame.K_ESCAPE:
                              game.start_level()

                         else:
                              pygame_win()
                              break

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    game.reset()
                    run = False
                    pygame_win()
                    break
               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         game.reset()
                         run = False
                         pygame_win()
                         break
               if event.type == pygame.MOUSEBUTTONDOWN:
                    if not game.q8 and Q2_rect.collidepoint(GAME_MOUSE_POS) and user_car.collide(L2R2_RECT, 90, 620):
                         l2_quiz2()
                         set_focus_to_window()

                    if not game.q11 and Q5_rect.collidepoint(GAME_MOUSE_POS) and user_car.collide(L2R5_RECT, 1310, 480):
                         l2_quiz5()
                         set_focus_to_window()

          if not game.q7 and user_car.collide(L2R1_RECT, 290, 630):
               l2_quiz1()
               set_focus_to_window()
          if not game.q9 and user_car.collide(L2R3_RECT, 30, 230):
               l2_quiz3()
               set_focus_to_window()

          if not game.q10 and user_car.collide(L2R4_RECT, 1310, 230):
               l2_quiz4()
               set_focus_to_window()
          if not game.q12 and user_car.collide(L2R6_RECT, 1150, 630):
               l2_quiz6()
               set_focus_to_window()
          move_user(user_car)

          if user_car.collide(TRACK_BORDER_MASK) != None:
               user_car.bounce()

          finish_intersection_point_collide = user_car.collide(FLAG_MASK, *LEV2_FLAG_POSITION)
          if finish_intersection_point_collide != None:  # * is for separating position into two
               write_text_to_centre(GAME_FONT, "LEVEL COMPLETED. LOADING RESULTS...")
               pygame.display.update()
               pygame.time.wait(5000)
               user_car.reset()
               game.level_ended = True
               game.level2_time = game.get_time()  # type: ignore
               insert_into_l2()
               game.reset()
               level2_results_page()
               break

# Helper function to properly close pygame and return to Tkinter


def level3():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     pygame_win = main.pygame_win
     level3_results_page = main.level3_results_page
     LEV3 = main.LEV3
     LEV3_TRACK_BORDER = main.LEV3_TRACK_BORDER
     FLAG = main.FLAG
     FLAG_MASK = main.FLAG_MASK
     GAME_FONT = main.GAME_FONT
     pygame.display.quit()
     game.screen = None  # Reset screen reference after quit
     game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
     user_car_info.max_velocity = 1.5
     TRACK_BORDER_MASK = pygame.mask.from_surface(LEV3_TRACK_BORDER)
     # link to spec - Generation of objects based on simple OOP model
     user_car = UserCar(3, LEV3_START_POSITION)
     pygame.display.set_caption("level 3")
     clock = pygame.time.Clock()
     images = [(LEV3, (0, 0)), (FLAG, LEV3_FLAG_POSITION) ]
     run = True
     while run:
          clock.tick(FRAMES_PER_SEC)
          draw_on_screen(images, user_car)
          while not game.level_started:
               write_text_to_centre(GAME_FONT, "PRESS ANY KEY TO START LEVEL 3!")
               pygame.display.update()

               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         game.reset()
                         run = False
                         pygame_win()
                         break
                    if event.type == pygame.KEYDOWN:
                         if event.key != pygame.K_ESCAPE:
                              game.start_level()

                         else:
                              pygame_win()
                              break

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    game.reset()
                    run = False
                    pygame_win()
                    break
               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         game.reset()
                         run = False
                         pygame_win()
                         break

          move_user(user_car)
          if user_car.collide(TRACK_BORDER_MASK) != None:
               user_car.bounce()


          finish_intersection_point_collide = user_car.collide(FLAG_MASK, *LEV3_FLAG_POSITION)
          if finish_intersection_point_collide != None:  # * is for separating position into two
               write_text_to_centre(GAME_FONT, "LEVEL COMPLETED. LOADING RESULTS...")
               pygame.display.update()
               pygame.time.wait(5000)
               user_car.reset()
               game.level_ended = True
               game.level3_time = game.get_time()  # type: ignore
               insert_into_l3()
               game.reset()
               level3_results_page()
               break

# displays the time taken, best score, and leader board of level 2


def level1():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     set_focus_to_window = main.set_focus_to_window
     pygame_win = main.pygame_win
     level1_results_page = main.level1_results_page
     LEV1 = main.LEV1
     LEV1_TRACK_BORDER = main.LEV1_TRACK_BORDER
     FLAG = main.FLAG
     FLAG_MASK = main.FLAG_MASK
     GAME_FONT = main.GAME_FONT
     L1R1_RECT = main.L1R1_RECT
     L1R2_RECT = main.L1R2_RECT
     L1R3_RECT = main.L1R3_RECT
     L1R4_RECT = main.L1R4_RECT
     L1R5_RECT = main.L1R5_RECT
     L1R6_RECT = main.L1R6_RECT
     pygame.display.quit()
     game.screen = None  # Reset screen reference after quit
     user_car_info.max_velocity = 2.5
     game.screen = pygame.display.set_mode((game.game_width, game.game_height))  # type: ignore
     TRACK_BORDER_MASK = pygame.mask.from_surface(LEV1_TRACK_BORDER)
     user_car = UserCar(3, LEV1_START_POSITION)
     pygame.display.set_caption("level 1")
     clock = pygame.time.Clock()
     images = [(LEV1, (0, 0)), (FLAG, LEV1_FLAG_POSITION)]
     run = True
     while run:
          clock.tick(FRAMES_PER_SEC)
          draw_on_screen(images, user_car)
          while not game.level_started:
               write_text_to_centre(GAME_FONT, "PRESS ANY KEY TO START LEVEL 1!")
               pygame.display.update()

               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         game.reset()
                         run = False
                         pygame_win()
                         break
                    if event.type == pygame.KEYDOWN:
                         if event.key != pygame.K_ESCAPE:
                              game.start_level()

                         else:
                              pygame_win()
                              break

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    game.reset()
                    run = False
                    pygame_win()
                    break
               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         game.reset()
                         run = False
                         pygame_win()
                         break

          if not game.q1 and user_car.collide(L1R1_RECT, 50, 400):
               l1_quiz1()
               set_focus_to_window()

          else:
               if not user_car.collide(L1R1_RECT, 50, 400):
                    user_car_info.max_velocity = 2.5
               else:
                    user_car_info.max_velocity = 2

          if not game.q2 and user_car.collide(L1R2_RECT, 170, 290):
               l1_quiz2()
               set_focus_to_window()
          if not game.q3 and user_car.collide(L1R3_RECT, 450, 290):
               l1_quiz3()
               set_focus_to_window()
          if not game.q4 and user_car.collide(L1R4_RECT, 520, 620):
               l1_quiz4()
               set_focus_to_window()
          if not game.q5 and user_car.collide(L1R5_RECT, 320, 620):
               l1_quiz5()
               set_focus_to_window()
          if not game.q6 and user_car.collide(L1R6_RECT, 900, 620):
               l1_quiz6()
               set_focus_to_window()

          move_user(user_car)

          if user_car.collide(TRACK_BORDER_MASK) != None:
               user_car.bounce()

          finish_intersection_point_collide = user_car.collide(FLAG_MASK, *LEV1_FLAG_POSITION)
          if finish_intersection_point_collide != None:  # * is for separating position into two
               write_text_to_centre(GAME_FONT, "LEVEL COMPLETED. LOADING RESULTS...")
               pygame.display.update()
               pygame.time.wait(5000)
               user_car.reset()
               game.level_ended = True
               game.level1_time = game.get_time()  # type: ignore
               insert_into_l1()
               game.reset()
               level1_results_page()
               break

# checks whether the user has enough coins to start a level


def l1_quiz1():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     if not game.q1 and game.rootdestroyed:
          ensure_root_for_easygui()  # Ensure root is available before easygui calls
          user_car_info.max_velocity = 2
          game.startq_time = time.time()  # type: ignore
          q = "What is the speed limit for a school zone?"
          ans = "20"
          text = eg.buttonbox(msg=q, title="Quiz 1", choices=["10", "15", "20", "25", "27", "30", "50"])
          if text:
               if text == ans:
                    game.q1 = True
                    game.level_coins += 3
                    eg.msgbox(
                         f"Correct!\nTotal coins earned this level: {game.level_coins}\n \n \nNote: maximum speed for school zone will change to 20 automatically whenever you enter it.",
                         title="Quiz result", ok_button="Resume Level")
                    game.paused_time += time.time() - game.startq_time  # type: ignore
               else:
                    game.q1 = True
                    eg.msgbox(
                         f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}\n \n \nNote: maximum speed for school zone will change to 20 automatically whenever you enter it.",
                         title="Quiz result", ok_button="Resume Level")
                    game.paused_time += time.time() - game.startq_time  # type: ignore

          else:
               game.q1 = False




def l1_quiz2():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     game.startq_time = time.time()  # type: ignore
     q = "Whats this sign?"
     ans = "do not enter"
     text = eg.enterbox(msg=q, title="quiz 2")
     if text:
          if text.lower() == ans:
               game.level_coins += 3
               game.q2 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
               game.q2 = True
     else:
          game.q2 = False




def l1_quiz3():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     game.startq_time = time.time()  # type: ignore
     q = "Whats this sign?"
     ans = "roundabout"
     text = eg.enterbox(msg=q, title="Quiz 3")
     if text:
          if text.lower() == ans:
               game.level_coins += 3
               game.q3 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
               game.q3 = True
     else:
          game.q3 = False




def l1_quiz4():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     game.startq_time = time.time()  # type: ignore
     q = "Whats this sign?"
     ans = "hospital"
     text = eg.enterbox(msg=q, title="Quiz 4")
     if text:
          if text.lower() == ans:
               game.level_coins += 3
               game.q4 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
               game.q4 = True
     else:
          game.q4 = False




def l1_quiz5():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     game.startq_time = time.time()  # type: ignore
     q = "Whats this sign?"
     ans = "dead end"
     text = eg.enterbox(msg=q, title="Quiz 5")
     if text:
          if text.lower() == ans:
               game.level_coins += 3
               game.q5 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
               game.q5 = True
     else:
          game.q5 = False




def l1_quiz6():
     main = get_main_refs()
     game = main.game
     user_car_info = main.user_car_info
     insert_into_l1 = main.insert_into_l1
     insert_into_l2 = main.insert_into_l2
     insert_into_l3 = main.insert_into_l3
     ensure_root_for_easygui = main.ensure_root_for_easygui
     ensure_root_for_easygui()  # Ensure root is available before easygui calls
     game.startq_time = time.time()  # type: ignore
     q = "Whats this sign?"
     ans = "zebra crossing"
     text = eg.enterbox(msg=q, title="Quiz 6")
     if text:
          if text.lower() == ans:
               game.level_coins += 3
               game.q6 = True
               eg.msgbox(f"Correct!\nTotal coins earned this level: {game.level_coins}", title="Quiz result",
                         ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
          else:
               eg.msgbox(f"Wrong!\nCorrect answer: {ans}\nTotal coins earned this level: {game.level_coins}",
                         title="Quiz result", ok_button="Resume Level")
               game.paused_time += time.time() - game.startq_time  # type: ignore
               game.q6 = True
     else:
          game.q6 = False


# level 1 game page


