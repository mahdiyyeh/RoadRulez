import os
import re
import time
import math
from typing import Optional
from tkinter import *  # noqa: F403, F401
from tkinter.ttk import Progressbar
from tkinter import ttk, messagebox
import easygui as eg
import pygame
import pyautogui
import smtplib
import dns.resolver
import gc
import sqlite3
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Import from organized modules
from config import (
    APP_SCREEN_WIDTH, APP_SCREEN_HEIGHT, RED, LIGHT_RED, ORANGE, YELLOW, DARK_GREEN,
    LIGHT_GREEN, LIGHT_BLUE, DARK_BLUE, VIOLET, PURPLE, PINK, GREY, BLACK, WHITE,
    APP_FONT, FRAMES_PER_SEC, SCALE, BLUE_CAR, RED_CAR, ORANGE_CAR, YELLOW_CAR,
    GREEN_CAR, PURPLE_CAR, WHITE_CAR, POLICE_CAR, LEV1_START_POSITION,
    LEV2_START_POSITION, LEV3_START_POSITION, AppConfig, COLOUR_DICT
)
from database_manager import DatabaseManager
from utils import (
    clear_userdetail_textfile, is_file_empty, scale_image, bubble_sort, merge_sort, merge
)
from quiz_manager import Quizz
from learning_manager import Learning

# Initialize configuration - maintain backward compatibility with Variables class
class Variables:
    """Backward compatibility wrapper for AppConfig."""
    def __init__(self):
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


# initialising the tkinter window
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

# initialising pygame assets
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
SCALE = 0.07
BLUE_CAR = "pictures/blue car.png"
RED_CAR = "pictures/red car.png"
ORANGE_CAR = "pictures/orange car.png"
YELLOW_CAR = "pictures/yellow car.png"
GREEN_CAR = "pictures/green car.png"
PURPLE_CAR = "pictures/purple car.png"
WHITE_CAR = "pictures/white car.png"
POLICE_CAR = "pictures/police car.png"
LEV1 = pygame.image.load("pictures/lev 1.png")
LEV1_TRACK_BORDER = pygame.image.load("pictures/lev 1 track border.png")
LEV1_START_POSITION = (70, 725)
LEV1_FLAG_POSITION = (1010, 0)
LEV2 = pygame.image.load("pictures/lev 2.tiff")
LEV2_TRACK_BORDER = pygame.image.load("pictures/lev 2 track border.png")
LEV2_START_POSITION = (720, 330)
LEV2_FLAG_POSITION = (690, 80)
LEV3 = pygame.image.load("pictures/lev 3.tiff")
LEV3_TRACK_BORDER = pygame.image.load("pictures/lev 3 track border.png")
LEV3_START_POSITION = (80, 725)
LEV3_FLAG_POSITION = (1040, 710)
FRAMES_PER_SEC = 60

# link to spec - Complex user-defined use of object- orientated programming (OOP) model, eg classes
class Button1():  # class for buttons in pygame
     def __init__(self, image, pos, text_input, font, base_color, hovering_color):
          self.image = image
          self.x_pos = pos[0]
          self.y_pos = pos[1]
          self.font = font
          self.base_color, self.hovering_color = base_color, hovering_color
          self.text_input = text_input
          self.text = self.font.render(self.text_input, True, self.base_color)
          if self.image is None:
               self.image = self.text
          self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
          self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

     def update(self):
          if self.image is not None:
               game.screen.blit(self.image, self.rect)  # type: ignore
          game.screen.blit(self.text, self.text_rect)  # type: ignore

     def checkForInput(self, position): #checks if mouse is hovering over the button
          if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                            self.rect.bottom):
               return True
          return False

     def changeColor(self, position): #changes the button textcolour is mouse if hovering over it
          if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                            self.rect.bottom):
               self.text = self.font.render(self.text_input, True, self.hovering_color)
          else:
               self.text = self.font.render(self.text_input, True, self.base_color)


# Utility functions are now imported from utils module


# 1) rotates image , 2)assigns new centre so image rotates from centre and not the top left
def blit_rotate_centre(image, top_left, angle):
     rotated_image = pygame.transform.rotate(image, angle)
     new_rectangle = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
     game.screen.blit(rotated_image, new_rectangle.topleft)  # type: ignore


def write_text_to_centre(font, text):
     text_bg = font.render(text, True, RED, BLACK)
     game.screen.blit(text_bg,(game.screen.get_width() / 2 - text_bg.get_width() / 2,game.screen.get_height() / 2 - text_bg.get_height() / 2))  # type: ignore


# displays all images on screen during each level
def draw_on_screen(images, user_car):
     for image, position in images:
          game.screen.blit(image, position)  # type: ignore

     time_text = GAME_DETAIL_FONT.render(f"Time:  {game.get_time()} seconds", True, WHITE, BLACK)
     game.screen.blit(time_text, (1250, 10))  # type: ignore

     speed_text = GAME_DETAIL_FONT.render(f"Speed: {10 * round(user_car.velocity, 2)}mph", True, WHITE, BLACK)
     game.screen.blit(speed_text, (1250, 40))  # type: ignore
     user_car.draw_on_screen()
     pygame.display.update()

# moves the car using the arrow keys
def move_user(user_car):
     keys = pygame.key.get_pressed()
     if keys[pygame.K_LEFT]:
          user_car.rotate(left=True)
     elif keys[pygame.K_RIGHT]:
          user_car.rotate(right=True)
     if keys[pygame.K_UP]:
          user_car.move_forward()
     elif keys[pygame.K_DOWN]:
          user_car.move_backward()
     else:
          user_car.reduce_speed()


# clears everything in tkinter window
def clear_window(name_of_window):
     for widget in name_of_window.winfo_children():
          widget.destroy()


def set_focus_to_window():
     """Helper function for focus management during quizzes."""
     # Don't deiconify root during game levels - easygui creates its own dialogs
     # Just update root to ensure it's accessible if needed
     try:
          root.update()
     except:
          pass
     x, y = pyautogui.position()
     pyautogui.click(50, 100, duration=0)
     pyautogui.moveTo(x=x, y=y, duration=0)


FLAG = scale_image(pygame.image.load("pictures/red flag.png"), 0.2)
FLAG_MASK = pygame.mask.from_surface(FLAG)


class Game:# link to spec - Complex user-defined use of object- orientated programming (OOP) model, eg classes
     def __init__(self):
          self.level_started = False
          self.level_ended = False
          self.chosen_car_game = scale_image(pygame.image.load(BLUE_CAR), SCALE)
          self.game_width = 1440
          self.game_height = 790
          self.screen: Optional[pygame.Surface] = None  # type: ignore
          self.back_to_game_page = None
          self.level1_time: Optional[float] = None  # type: ignore
          self.level2_time: Optional[float] = None  # type: ignore
          self.level3_time: Optional[float] = None  # type: ignore
          self.rootdestroyed = False
          self.q1 = False
          self.q2 = False
          self.q3 = False
          self.q4 = False
          self.q5 = False
          self.q6 = False
          self.q7 = False
          self.q8 = False
          self.q9 = False
          self.q10 = False
          self.q11 = False
          self.q12 = False
          self.level_coins = 0
          self.start_time: float = 0.0  # type: ignore
          self.startq_time: float = 0.0  # type: ignore
          self.elapsed_time: float = 0.0  # type: ignore
          self.paused_time: float = 0.0  # type: ignore
     # resets the quiz states and times when level is complete or escape pressed
     def reset(self):
          self.level_started = False
          self.start_time = 0
          self.level_ended = False
          self.startq_time = 0
          self.paused_time = 0
          self.q1 = False
          self.q2 = False
          self.q3 = False
          self.q4 = False
          self.q5 = False
          self.q6 = False
          self.q7 = False
          self.q8 = False
          self.q9 = False
          self.q10 = False
          self.q11 = False
          self.q12 = False

     def start_level(self):
          self.level_started = True
          self.start_time = time.time()

     def get_time(self):  # returns time for level
          if not self.level_started:
               self.elapsed_time = 0
               return 0
          elif self.level_ended:
               self.elapsed_time = round(time.time() - self.start_time - self.paused_time - 5, 2)
               return self.elapsed_time
          self.elapsed_time = round(time.time() - self.start_time - self.paused_time, 2)
          return self.elapsed_time


game = Game()


def welcome_page():
     clear_window(root)
     root.configure(background="light yellow")
     image = (PhotoImage(file="pictures/Screenshot 2024-02-20 at 22.29.42.png").subsample(1))
     image_label = Label(root, image=image)
     image_label.photo = image  # type: ignore
     image_label.grid(row=0, column=0, columnspan=10, rowspan=30)

     welcome_label = Label(root, text="Welcome To RoadRulez!", font=(APP_FONT, 32, "bold"), bg=BLACK, fg=RED)
     welcome_label.grid(row=17, column=7, padx=(35, 5), pady=5)

     label = Label(root, text="If you’re a new user, please register for an\n account. If you are registered, login.",
                   font=(APP_FONT, 28), bg=BLACK, fg=ORANGE)
     label.grid(row=18, column=7, padx=(35, 5), pady=5)
     reg_image = (PhotoImage(file="pictures/register.png").subsample(2))
     reg_image_label = Label(root, image=reg_image)
     reg_image_label.photo = reg_image  # type: ignore

     log_image = (PhotoImage(file="pictures/login.png").subsample(2))
     log_image_label = Label(root, image=log_image)
     log_image_label.photo = log_image  # type: ignore

     register_button = Button(root, image=reg_image, command=account_details.register, highlightbackground=BLACK)  # type: ignore
     register_button.grid(row=19, column=7, padx=(35, 5), pady=5)

     login_button = Button(root, image=log_image, command=account_details.login, highlightbackground=BLACK)  # type: ignore
     login_button.grid(row=20, column=7, padx=(35, 5), pady=5)


class AccountDetails:  # link to spec - records
     def __init__(self):
          self.name_textbox = None
          self.username_textbox = None
          self.password_textbox = None
          self.email_textbox = None
          self.age_textbox = None
          self.user_type_textbox = StringVar()
          self.name = ""
          self.username = ""
          self.password_reg = ""
          self.email = None
          self.age = 0
          self.user_type = None
          self.password_meet = False
          self.name_meet = False
          self.age_meet = False
          self.type_meet = False
          self.username1 = None
          self.password1 = None
          self.show_pass_button = None
          self.show_login_pass_button = None
          self.error1 = None
          self.error2 = None
          self.error3 = None
          self.error4 = None
          self.error5 = None
          self.error6 = None
          self.top = None

     # the validate functions check if input is valid otherwise display an error
     def validate_reg_name(self, event):
          value = self.name_textbox.get()
          if not value.isalpha():
               self.error1.config(text="Invalid name entered", fg="red")
               self.name_textbox.config(highlightbackground="red")
          else:
               self.error1.config(text="")
               self.name_textbox.config(highlightbackground="white")

     def validate_type(self, event):
          value = self.user_type_textbox.get()
          if value == "Select":
               self.error5.config(text="Please select an option", fg="red")
          else:
               self.error5.config(text="")

     def validate_reg_pass(self, event):
          value = self.password_textbox.get()
          if (len(value) >= 8) and self.num_in_password(value):
               self.error3.config(text="")
               self.password_textbox.config(highlightbackground="white")

          else:

               self.error3.config(text="Invalid password entered", fg="red")
               self.password_textbox.config(highlightbackground="red")

     def validate_reg_age(self, event):
          value = self.age_textbox.get()
          if value.isdigit():
               if int(value) > 0:
                    self.error4.config(text="")
                    self.age_textbox.config(highlightbackground="white")
               else:
                    self.error4.config(text="Invalid age entered", fg="red")
                    self.age_textbox.config(highlightbackground="red")
          else:
               self.error4.config(text="Invalid age entered", fg="red")
               self.age_textbox.config(highlightbackground="red")

     def validate_reg_user(self, event):
          if check_if_username_taken():
               self.error6.config(text="Username already taken.", fg="red")
               self.username_textbox.config(highlightbackground="red")

          else:
               self.error6.config(text="")
               self.username_textbox.config(highlightbackground="white")

     def load_screen(self):
          load = Toplevel(background="#00A5D3")
          load.title("Loading...")
          load.geometry("300x300+570+245")
          load.resizable(False, False)
          label = Label(load, text="Logging in...", font=(APP_FONT, 20, "bold"), bg="#00A5D3", fg=BLACK)
          label.pack(pady=20)

          progress = Progressbar(load, orient="horizontal", mode="indeterminate", length=200, )
          progress.pack()
          progress.start(200)

          image = (PhotoImage(file="pictures/bee.png").subsample(2))
          image_label = Label(load, image=image)
          image_label.photo = image  # type: ignore  # type: ignore
          image_label.pack(pady=10)
          root.configure(bg=variables.background_colour)
          load.after(5000, home_page)

     #shows the password from "*" to what they wrote
     def show_login_pass(self):
          if self.password1.cget("show") == "*":
               self.password1.config(show="")
               self.show_login_pass_button.config(text="hide\u200A\u200A\u200A")
          else:
               self.password1.config(show="*")
               self.show_login_pass_button.config(text="show")

     def login(self):
          clear_window(root)
          root.configure(bg="grey")
          image = (PhotoImage(file="pictures/login bg.png"))
          image_label = Label(root, image=image)
          image_label.photo = image  # type: ignore  # type: ignore
          image_label.grid(row=0, column=0, columnspan=10, rowspan=30)
          details_frame = Frame(root, bg=WHITE)
          details_frame.grid(row=2, column=0, columnspan=5, rowspan=10, ipady=10, padx=13, pady=(80, 5), sticky=W)

          second_frame = Frame(root, bg=WHITE)
          second_frame.grid(row=12, column=0, padx=13, sticky=W)

          login_label = Label(details_frame, text="LOGIN ", font=(APP_FONT, 20, "underline", "bold"), bg=WHITE, fg=BLACK)
          login_label.grid(row=5, column=0, padx=10, pady=1, sticky=W)

          username_label = Label(details_frame, text="Username: ", font=(APP_FONT, 20), bg=WHITE, fg=BLACK)
          username_label.grid(row=6, column=0, padx=4, pady=1)

          password_label = Label(details_frame, text="Password: ", font=(APP_FONT, 20), bg=WHITE, fg=BLACK)
          password_label.grid(row=7, column=0, padx=4, pady=1)

          self.username1 = Entry(details_frame, width=30, bg="white", fg=BLACK)
          self.username1.grid(row=6, column=1, padx=5, pady=1)

          self.password1 = Entry(details_frame, width=30, bg="white", fg=BLACK, show="*")
          self.password1.grid(row=7, column=1, padx=(5, 1), pady=1)

          self.show_login_pass_button = Button(details_frame, text="show", font=(APP_FONT, 15),
                                               command=self.show_login_pass, bg=WHITE, fg=BLACK)
          self.show_login_pass_button.grid(row=7, column=2, padx=1, pady=1)

          click_to_login_button = Button(second_frame, text="Click To Login", font=(APP_FONT, 15, "bold"),
                                         command=self.check_login_info, bg=WHITE, fg=BLACK)
          click_to_login_button.grid(row=1, column=1, padx=0, pady=10)

          go_to_register_button = Button(second_frame, text="Not registered yet? Click here to make an account",
                                         font=(APP_FONT, 15), command=account_details.register, bg=WHITE, fg=BLACK)  # type: ignore
          go_to_register_button.grid(row=1, column=0, padx=(5, 15), pady=5)
          self.username1.focus_set()

     # function for checking if a variable contains a number
     # link to spec - linear search
     def num_in_password(self, password):
          for character in password:
               if character.isdigit():
                    return True
          return False

     def check_login_info(self):
          username_input = self.username1.get()
          password_input = self.password1.get()
          if len(username_input and password_input) != 0:
               if is_file_empty():
                    query_login_info()
               else:
                    with open('userdetails.txt',
                              'r') as file:  # link to spec - text files - reading from files- files organised for direct access
                         for line in file:
                              section = line.strip().split(",")  # link to spec - use of single dimensional array
                              username2 = section[0]
                              password2 = section[4]
                    if username_input == username2:
                         if password_input == password2:
                              self.load_screen()
                         else:
                              messagebox.showerror("error", "Wrong password. please try again")
                              self.password1.delete(0, END)
                              self.password1.focus_set()
                    elif password2 == password_input:
                         messagebox.showerror("error", "Wrong username for given password", icon="warning")
                    else:
                         messagebox.showerror("error",
                                              "This username is not registered to an account.\nPlease try again or go to register to make an account ",
                                              icon="warning")
          else:
               messagebox.showerror("error", "Make sure all the fields are filled in", icon="warning")

     def validate_email_format(self):
          pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
          return re.match(pattern, self.email) if self.email else None  # type: ignore

     def validate_mx_records(self):
          try:
               mx_records = dns.resolver.resolve(self.domain, 'MX')
               return any(mx_records)
          except dns.resolver.NoAnswer:
               return False
          except dns.resolver.NXDOMAIN:
               return False
          except dns.resolver.Timeout:  # type: ignore
               return False

     def validate_email_address(self):

          if not self.validate_email_format():
               return False

          self.domain = self.email.split('@')[1]
          if not self.validate_mx_records():
               return False

          return True

     def send_email(self): # sends an email to the parent/teacher to fill out a survey
          try:
               smtplibobj = smtplib.SMTP("smtp.gmail.com", 587)
               smtplibobj.ehlo()
               smtplibobj.starttls()
               smtplibobj.login("roadsafetyforkids1@gmail.com", "ribg whmq ourj lsvu")
               smtplibobj.sendmail("roadsafetyforkids1@gmail.com", self.email or "",  # type: ignore
                                   "Subject:Road Safety Feedback\nThank you for registering. Please complete this form whenever you can.\nhttps://www.surveymonkey.com/r/YVQ8CML\nYour feedback is appreciated.")

          except smtplib.SMTPException as e:
               messagebox.showerror(message=f"Failed to send email. SMTP error: {e}")

          except Exception as e:
               messagebox.showerror(message=f"An unexpected error occurred: {e}")
          finally:
               if 'smtplibobj' in locals():
                    smtplibobj.quit()

     def check_email_provided(self):
          self.email = self.email_textbox.get()
          if self.email:
               if self.validate_email_address():
                    self.top.destroy()
                    self.send_email()
                    insert_into_users()
                    self.login()
               else:
                    messagebox.showerror(message="Invalid email address.")
          else:
               insert_into_users()
               self.login()

     def check_survey_participation(self):
          self.top = Toplevel(background=variables.background_colour)
          self.top.title("Quick question")
          self.top.geometry(
               f"600x300+{int((APP_SCREEN_WIDTH - 600) / 2)}+200")  # link to spec - simple mathematical calculations
          self.top.resizable(False, False)
          label = Label(self.top,
                        text="Before you continue...\nIf you would like to complete a survey to provide feedback on the\napp, please provide your email address.\n Otherwise leave it blank and continue.",
                        font=(APP_FONT, 20), bg=variables.background_colour)
          label.grid(row=0, column=0, padx=10, pady=10)

          self.email_textbox = Entry(self.top, width=40, bg="white", fg=BLACK, highlightthickness=2, font=(APP_FONT, 20))
          self.email_textbox.grid(row=1, column=0, padx=10, pady=2)

          button = Button(self.top, text="Continue", font=(APP_FONT, 20), command=self.check_email_provided)
          button.grid(row=2, column=0, padx=10, pady=10)
          self.top.mainloop()
     # creats user account
     def create_acc(self):
          self.name = self.name_textbox.get()
          self.username = self.username_textbox.get()
          self.password_reg = self.password_textbox.get()
          self.age = self.age_textbox.get()
          self.user_type = self.user_type_textbox.get()

          if len(self.name and self.username and self.password_reg) != 0 and self.user_type != "Select" and self.age !=0:
               if (len(self.password_reg) >= 8) and self.num_in_password(self.password_reg):
                    self.password_meet = True
               else:
                    self.password_meet = False
                    messagebox.showerror("error", "Choose another password that meets the requirements", icon="warning")

               if self.name.isalpha():
                    self.name_meet = True
               else:
                    self.name_meet = False
                    messagebox.showerror("error", "Make sure name only contains letters", icon="warning")

               if self.age.isdigit() and int(self.age) > 0:
                    self.age_meet = True
               else:
                    self.age_meet = False
                    messagebox.showerror("error", "Make sure age is more than 0 and only contains digits",
                                         icon="warning")


               if check_if_username_taken():
                    messagebox.showerror("error", "Please choose another username as this is already taken.",
                                         icon="warning")


          else:
               messagebox.showerror("error", "Make sure all the fields are filled in", icon="warning")

          if self.password_meet and self.age_meet and self.name_meet and not check_if_username_taken():
               with open('userdetails.txt', 'r+') as file: # link to spec - text files - writing to files - files organised for direct access
                    clear_userdetail_textfile()
                    file.write(f"{self.username},{self.name},{self.age},{self.email},{self.password_reg},{quizz.user_coins}")
               messagebox.showinfo("Success",
                                   f"Your account has been created, {self.name}.\nYou may now close this message and login.")
               if self.user_type == "Teacher" or self.user_type == "Parent":
                    self.check_survey_participation()
               else:
                    insert_into_users()
                    self.login()

     def show_pass(self):
          if self.password_textbox.cget("show") == "*":
               self.password_textbox.config(show="")
               self.show_pass_button.config(text="hide\u200A\u200A\u200A")
          else:
               self.password_textbox.config(show="*")
               self.show_pass_button.config(text="show")

     def clicked_out(self, event):
          clicked = event.widget
          if not isinstance(clicked, (Button, Entry)):
               root.focus_set()

     def register(self):
          root.configure(bg=variables.background_colour)
          clear_window(root)
          image = (PhotoImage(file="pictures/reg bg.png"))
          image_label = Label(root, image=image)
          image_label.photo = image  # type: ignore  # type: ignore
          image_label.grid(row=0, column=0, columnspan=10, rowspan=30)

          detail_frame = Frame(root, bg=WHITE, relief=SOLID, borderwidth=2)
          detail_frame.grid(row=1, column=0, padx=0, pady=10)

          register_label = Label(detail_frame, text="Register", font=(APP_FONT, 20, "underline", "bold"),
                                 bg=WHITE, fg=BLACK)
          register_label.grid(row=0, column=0, padx=5, pady=10, sticky=W)

          name_label = Label(detail_frame, text="Name: ", font=(APP_FONT, 20), bg=WHITE, fg=BLACK)
          name_label.grid(row=1, column=0, padx=10, pady=2, sticky=E)

          username_label = Label(detail_frame, text="Username: ", font=(APP_FONT, 20), bg=WHITE, fg=BLACK)
          username_label.grid(row=3, column=0, padx=10, pady=2, sticky=E)

          password_label = Label(detail_frame, text="Password: ", font=(APP_FONT, 20), bg=WHITE, fg=BLACK)
          password_label.grid(row=5, column=0, padx=10, pady=2, sticky=E)

          password_label1 = Label(detail_frame,
                                  text="(Minimum 8 characters\nand at least one number)",
                                  font=(APP_FONT, 15), bg=WHITE, fg=BLACK)
          password_label1.grid(row=6, column=0, padx=10, pady=2, sticky=N)

          age_label = Label(detail_frame, text="Age: ", font=(APP_FONT, 20), bg=WHITE, fg=BLACK)
          age_label.grid(row=7, column=0, padx=10, pady=2, sticky=E)

          self.name_textbox = Entry(detail_frame, width=20, bg="white", fg=BLACK, highlightthickness=2)
          self.name_textbox.grid(row=1, column=1, padx=10, pady=2)
          self.error1 = Label(detail_frame, text="", fg="red", bg=WHITE)
          self.error1.grid(row=2, column=1, pady=2, sticky=N)
          self.name_textbox.bind("<FocusOut>", self.validate_reg_name)

          self.username_textbox = Entry(detail_frame, width=20, bg="white", fg=BLACK, highlightthickness=2)
          self.username_textbox.grid(row=3, column=1, padx=10, pady=2)
          self.error6 = Label(detail_frame, text="", fg="red", bg=WHITE)
          self.error6.grid(row=4, column=1, pady=2, sticky=N)
          self.username_textbox.bind("<FocusOut>", self.validate_reg_user)

          self.password_textbox = Entry(detail_frame, width=20, bg="white", fg=BLACK, show="*", highlightthickness=2)
          self.password_textbox.grid(row=5, column=1, padx=10, pady=2)
          self.error3 = Label(detail_frame, text="", fg="red", bg=WHITE)
          self.error3.grid(row=6, column=1, pady=2, sticky=N)
          self.password_textbox.bind("<FocusOut>", self.validate_reg_pass)

          self.show_pass_button = Button(detail_frame, text="show", font=(APP_FONT, 15), command=self.show_pass)
          self.show_pass_button.grid(row=5, column=2, padx=5, pady=2)

          self.age_textbox = Entry(detail_frame, width=20, bg="white", fg=BLACK, highlightthickness=2)
          self.age_textbox.grid(row=7, column=1, padx=10, pady=2)
          self.error4 = Label(detail_frame, text="", fg="red", bg=WHITE)
          self.error4.grid(row=8, column=1, pady=2, sticky=N)
          self.age_textbox.bind("<FocusOut>", self.validate_reg_age)

          text = Label(detail_frame, text="Which best \ndescribes you:", font=(APP_FONT, 20), bg=WHITE, fg=BLACK)
          text.grid(row=9, column=0, padx=10, pady=2, sticky=E)

          self.user_type_textbox.set("Select")

          drop = OptionMenu(detail_frame, self.user_type_textbox, "Student", "Teacher", "Parent")
          drop.grid(row=9, column=1)
          self.error5 = Label(detail_frame, text="", fg="red", bg=WHITE)
          self.error5.grid(row=10, column=1, pady=2, sticky=N)
          drop.bind("<ButtonRelease-1>", self.validate_type)

          create_acc_button = Button(detail_frame, text="Create Account", font=(APP_FONT, 15, "bold"),
                                     command=self.create_acc, bg=WHITE, fg=BLACK)
          create_acc_button.grid(row=11, column=1, padx=10, pady=10)

          login_button = Button(detail_frame, text="Login page", font=(APP_FONT, 15), command=self.login, bg=WHITE, fg=BLACK)
          login_button.grid(row=11, column=0, padx=10, pady=10)
          self.name_textbox.focus_set()
          root.bind("<Button-1>", self.clicked_out)

account_details = AccountDetails()

# link to spec - Complex user-defined use of object-orientated programming (OOP) model - inheritance
class Setting(AccountDetails):
     def __init__(self):
          super().__init__()
          self.old_pass_textbox = None
          self.new_pass_textbox1 = None
          self.new_pass_textbox2 = None
          self.correct_oldpass = False
          self.correct_newpass = False
          self.password_meet = False
          self.new_name_entry = None
          self.show_old = None
          self.show_new = None
          self.show_new2 = None

     def audio_off(self):
          pygame.mixer.music.stop()

     def audio_on(self):
          pygame.mixer.music.play(-1)

     def check_pass(self):
          old_pass = account_details.password_reg
          old_pass_entered = self.old_pass_textbox.get()
          new_pass1 = self.new_pass_textbox1.get()
          new_pass2 = self.new_pass_textbox2.get()

          if len(old_pass_entered and new_pass1 and new_pass2) != 0:
               if old_pass == old_pass_entered:
                    self.correct_oldpass = True
               else:
                    messagebox.showerror("error", "Old password is wrong. Please try again", icon="warning")
               if (len(new_pass1) >= 8) and self.num_in_password(new_pass1):
                    self.password_meet = True
               else:
                    messagebox.showerror("error",
                                         """Please choose another password that meets the requirements.\nMust be minimum 8 characters and contain at least 1 number """,
                                         icon="warning")
               if new_pass1 == new_pass2:
                    self.correct_newpass = True
               else:
                    messagebox.showerror("error", "The new passwords do not match. Please try again", icon="warning")

          else:
               messagebox.showerror("error", "Make sure all the fields are filled in", icon="warning")
          if self.correct_oldpass and self.correct_newpass and self.password_meet:
               account_details.password_reg = new_pass1
               update_pass_db()
               with open('userdetails.txt', 'r+') as file:
                    clear_userdetail_textfile()
                    file.write(f"{account_details.username},{account_details.name},{account_details.age},{account_details.email},{account_details.password_reg},{quizz.user_coins}")
               messagebox.showinfo("info", "Password changed successfully")
               self.old_pass_textbox.delete(0, END)
               self.new_pass_textbox1.delete(0, END)
               self.new_pass_textbox2.delete(0, END)
               self.old_pass_textbox.focus_set()

     # link to spec - polymorphism - the function show_pass is defined in the accountdetail class but it is overriden here.
     def show_pass(self):
          if self.old_pass_textbox.cget("show") == "*":
               self.old_pass_textbox.config(show="")
               self.show_old.config(text="hide\u200A\u200A\u200A")
          else:
               self.old_pass_textbox.config(show="*")
               self.show_old.config(text="show")

     def show_new_pass(self):
          if self.new_pass_textbox1.cget("show") == "*":
               self.new_pass_textbox1.config(show="")
               self.show_new.config(text="hide\u200A\u200A\u200A")
          else:
               self.new_pass_textbox1.config(show="*")
               self.show_new.config(text="show")

     def show_new2_pass(self):
          if self.new_pass_textbox2.cget("show") == "*":
               self.new_pass_textbox2.config(show="")
               self.show_new2.config(text="hide\u200A\u200A\u200A")
          else:
               self.new_pass_textbox2.config(show="*")
               self.show_new2.config(text="show")

     def change_pass(self):
          clear_window(root)
          top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          top_frame.grid(row=0, column=0, padx=10, pady=10)
          text = Label(top_frame, text="Change Password:", font=(APP_FONT, 25, "bold", "underline"),
                       bg=variables.background_colour, fg=BLACK)
          text.grid(row=0, column=0, padx=(10, 720), pady=10)

          back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                           command=home_page)
          back_to_homepage_button.grid(row=0, column=2, ipadx=10, padx=10, pady=10)

          back_to_setting_button = Button(top_frame, text="Back To settings", font=(APP_FONT, 20),
                                          command=self.settings)
          back_to_setting_button.grid(row=0, column=1, ipadx=10, padx=10, pady=10)

          second_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          second_frame.grid(row=1, column=0, columnspan=750, padx=10, pady=10)

          label = Label(second_frame, text="Enter old password: ", font=(APP_FONT, 20), bg=variables.background_colour, fg=BLACK)
          label.grid(row=0, column=0, padx=10, pady=10)

          label = Label(second_frame, text="Enter new password: ", font=(APP_FONT, 20), bg=variables.background_colour, fg=BLACK)
          label.grid(row=1, column=0, padx=10, pady=10)

          label = Label(second_frame, text="Re-enter new password: ", font=(APP_FONT, 20),
                        bg=variables.background_colour, fg=BLACK)
          label.grid(row=2, column=0, padx=10, pady=10)

          self.old_pass_textbox = Entry(second_frame, width=30, bg="white", fg=BLACK, show="*", font=("Helvetica", 18))
          self.old_pass_textbox.grid(row=0, column=1, padx=1, pady=10)

          self.new_pass_textbox1 = Entry(second_frame, width=30, bg="white", fg=BLACK, show="*", font=("Helvetica", 18))
          self.new_pass_textbox1.grid(row=1, column=1, padx=1, pady=10)

          self.new_pass_textbox2 = Entry(second_frame, width=30, bg="white", fg=BLACK, show="*", font=("Helvetica", 18))
          self.new_pass_textbox2.grid(row=2, column=1, padx=1, pady=10)

          self.show_old = Button(second_frame, text="show", font=(APP_FONT, 15), command=self.show_pass)
          self.show_old.grid(row=0, column=2, padx=1, pady=10)

          self.show_new = Button(second_frame, text="show", font=(APP_FONT, 15), command=self.show_new_pass)
          self.show_new.grid(row=1, column=2, padx=1, pady=10)

          self.show_new2 = Button(second_frame, text="show", font=(APP_FONT, 15), command=self.show_new2_pass)
          self.show_new2.grid(row=2, column=2, padx=1, pady=10)

          submit_button = Button(root, text="Submit", font=(APP_FONT, 20, "bold"), command=self.check_pass)
          submit_button.grid(row=2, column=0, padx=10, pady=10)

          self.old_pass_textbox.focus_set()

     def change_name(self):
          new_name = self.new_name_entry.get()
          if len(new_name) != 0 and new_name.isalpha():
               account_details.name = new_name
               update_name_db()
               with open('userdetails.txt', 'w') as file:
                    clear_userdetail_textfile()
                    file.write(
                    f"{account_details.username},{account_details.name},{account_details.age},{account_details.email},{account_details.password_reg},{quizz.user_coins}")
               messagebox.showinfo("info", "Name changed successfully ")
               self.new_name_entry.delete(0, END)
               self.new_name_entry.focus_set()
          else:
               messagebox.showerror("info", "Make sure name only contains letters", icon="warning")

     def change_name_page(self):
          clear_window(root)
          top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)
          text = Label(top_frame, text="Change Name:", font=(APP_FONT, 25, "bold", "underline"),
                       bg=variables.background_colour, fg=BLACK)
          text.grid(row=0, column=0, padx=(10, 700), pady=10)

          back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                           command=home_page)
          back_to_homepage_button.grid(row=0, column=2, ipadx=30, padx=10, pady=10)

          back_to_setting_button = Button(top_frame, text="Back To settings", font=(APP_FONT, 20),
                                          command=self.settings)
          back_to_setting_button.grid(row=0, column=1, ipadx=30, padx=10, pady=10)

          second_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          second_frame.grid(row=1, column=0, columnspan=750, padx=10, pady=10)

          label = Label(second_frame, text="What would you like to change your name to? ", font=(APP_FONT, 20),
                        bg=variables.background_colour)
          label.grid(row=0, column=0, padx=10, pady=10)

          self.new_name_entry = Entry(second_frame, width=30, bg="white", fg=BLACK, font=(APP_FONT, 20))
          self.new_name_entry.grid(row=0, column=1, padx=10, pady=10)

          submit_button = Button(second_frame, text="Submit", font=(APP_FONT, 20), command=self.change_name)
          submit_button.grid(row=0, column=2, padx=10, pady=10)
          self.new_name_entry.focus_set()

     def change_background_colour(self, new_colour):
          variables.changebgcolour(new_colour, root)
          self.pick_background_colour()

     def pick_background_colour(self):
          clear_window(root)
          top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10, sticky=W)
          text = Label(top_frame, text="Change background colour:", font=(APP_FONT, 25, "bold", "underline"),
                       bg=variables.background_colour, fg=BLACK)
          text.grid(row=0, column=0, padx=(10, 600), pady=10)

          back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                           command=home_page)
          back_to_homepage_button.grid(row=0, column=2, ipadx=10, padx=10, pady=10)

          back_to_setting_button = Button(top_frame, text="Back To settings", font=(APP_FONT, 20),
                                          command=self.settings)
          back_to_setting_button.grid(row=0, column=1, ipadx=30, padx=10, pady=10)

          second_frame = Frame(root, bg=variables.background_colour)
          second_frame.grid(row=1, column=0, columnspan=750, padx=10, pady=10)
          third_frame = Frame(root, bg=variables.background_colour)
          third_frame.grid(row=2, column=0, columnspan=750, padx=10, pady=10)

          label = Label(second_frame, text="What would you like to change your background colour to? ",
                        font=(APP_FONT, 25),
                        bg=variables.background_colour, fg=BLACK)
          label.grid(row=0, column=0, padx=10, pady=10)

          button1 = Button(third_frame, text="Red",
                           font=(APP_FONT, 25), command=lambda: self.change_background_colour("RED"))
          button1.grid(row=0, column=1, padx=10, pady=10, ipadx=10)

          button2 = Button(third_frame, text="Orange",
                           font=(APP_FONT, 25), command=lambda: self.change_background_colour("ORANGE"))
          button2.grid(row=0, column=2, padx=10, pady=10)

          button3 = Button(third_frame, text="Yellow",
                           font=(APP_FONT, 25), command=lambda: self.change_background_colour("YELLOW"))
          button3.grid(row=0, column=3, padx=10, pady=10)

          button4 = Button(third_frame, text="Dark green",
                           font=(APP_FONT, 25), command=lambda: self.change_background_colour("DARK_GREEN"))
          button4.grid(row=0, column=4, padx=10, pady=10)

          button5 = Button(third_frame, text="Light green",
                           font=(APP_FONT, 25), command=lambda: self.change_background_colour("LIGHT_GREEN"))
          button5.grid(row=0, column=5, padx=10, pady=10)

          button6 = Button(third_frame, text="Light blue",
                           font=(APP_FONT, 25), command=lambda: self.change_background_colour("LIGHT_BLUE"))
          button6.grid(row=0, column=6, padx=10, pady=10)

          button7 = Button(third_frame, text="Dark blue",
                           font=(APP_FONT, 25), command=lambda: self.change_background_colour("DARK_BLUE"))
          button7.grid(row=0, column=7, padx=10, pady=10)

          button8 = Button(third_frame, text="Violet",
                           font=(APP_FONT, 25), command=lambda: self.change_background_colour("VIOLET"))
          button8.grid(row=1, column=1, padx=10, pady=10)

          button9 = Button(third_frame, text="Purple",
                           font=(APP_FONT, 25), command=lambda: self.change_background_colour("PURPLE"))
          button9.grid(row=1, column=2, padx=10, pady=10, ipadx=3)

          button10 = Button(third_frame, text="Pink",
                            font=(APP_FONT, 25), command=lambda: self.change_background_colour("PINK"))
          button10.grid(row=1, column=3, padx=10, pady=10, ipadx=13)

          button11 = Button(third_frame, text="Grey",
                            font=(APP_FONT, 25), command=lambda: self.change_background_colour("GREY"))
          button11.grid(row=1, column=4, padx=10, pady=10, ipadx=32)

          button12 = Button(third_frame, text="White",
                            font=(APP_FONT, 25), command=lambda: self.change_background_colour("WHITE"))
          button12.grid(row=1, column=5, padx=10, pady=10, ipadx=27)

     def logout(self):
          clear_userdetail_textfile()
          update_coin_db()
          welcome_page()

     def delete_acc(self):
          delete_user_acc_db()
          messagebox.showinfo(message="Account deleted.")
          welcome_page()

     def confirm_delete(self):
          q = messagebox.askokcancel(message="Are you sure you want to delete your account?", icon="warning",
                                     detail="This action cannot be undone.")
          if q:
               self.delete_acc()

     def settings(self):
          clear_window(root)
          top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          top_frame.grid(row=0, column=0, padx=10, pady=10)

          text = Label(top_frame, text="Settings:", font=(APP_FONT, 35, "bold", "underline"),
                       bg=variables.background_colour, fg=BLACK)
          text.grid(row=0, column=0, padx=(10, 970), pady=10)

          back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20), command=home_page)
          back_to_homepage_button.grid(row=0, column=1, ipadx=30, padx=10, pady=10)

          second_frame = Frame(root, bg=variables.background_colour)
          second_frame.grid(row=1, column=0, padx=10, pady=10, ipady=25)

          change_name_button = Button(second_frame, text="Change Name", font=(APP_FONT, 20),
                                      command=self.change_name_page)
          change_name_button.grid(row=0, column=0, ipadx=30, padx=10, pady=10)

          change_pass_button = Button(second_frame, text="Change Password", font=(APP_FONT, 20),
                                      command=self.change_pass)
          change_pass_button.grid(row=1, column=0, ipadx=30, padx=10, pady=10)

          change_background_button = Button(second_frame, text="Change background colour", font=(APP_FONT, 20),
                                            command=self.pick_background_colour)
          change_background_button.grid(row=2, column=0, ipadx=30, padx=40, pady=10)

          text = Label(second_frame, text="Turn Audio: ", font=(APP_FONT, 20), bg=variables.background_colour, fg=BLACK)
          text.place(x=70, y=200)

          audio_on_button = Button(second_frame, text="ON", font=(APP_FONT, 15), command=self.audio_on)
          audio_on_button.place(x=180, y=200)

          text = Label(second_frame, text="/", font=(APP_FONT, 20), bg=variables.background_colour, fg=BLACK)
          text.place(x=245, y=200)

          audio_off_button = Button(second_frame, text="OFF", font=(APP_FONT, 15), command=self.audio_off)
          audio_off_button.place(x=260, y=200)

          logout_button = Button(second_frame, text="Logout", font=(APP_FONT, 20), command=self.logout)
          logout_button.grid(row=3, column=0, ipadx=30, padx=40, pady=(60, 10))

          delete_acc_button = Button(second_frame, text="Delete Account", font=(APP_FONT, 20),
                                     command=self.confirm_delete)
          delete_acc_button.grid(row=4, column=0, ipadx=30, padx=40, pady=10)

setting = Setting()


def quiz_page():
     clear_window(root)
     top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
     top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

     text = Label(top_frame, text="Quizzes:", font=(APP_FONT, 35, "bold", "underline"), bg=variables.background_colour, fg=BLACK)
     text.grid(row=0, column=0, padx=(10, 980), pady=10)

     back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20), command=home_page)
     back_to_homepage_button.grid(row=0, column=1, ipadx=30, padx=10, pady=10)

     second_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
     second_frame.grid(row=2, column=0, columnspan=750, padx=10, pady=10)

     third_frame = Frame(root, bg=variables.background_colour)
     third_frame.grid(row=1, column=0, columnspan=750, padx=10, pady=10)

     text = Label(third_frame, text="Select a quiz topic:", font=(APP_FONT, 25), bg=variables.background_colour, fg=BLACK)
     text.grid(row=0, column=0, padx=10, pady=10)

     button1 = Button(second_frame, text="Road signs", font=(APP_FONT, 20), command=quizz.topic_1)  # type: ignore
     button1.grid(row=0, column=0, padx=10, pady=10)

     button2 = Button(second_frame, text="Car safety", font=(APP_FONT, 20), command=quizz.topic_2)  # type: ignore
     button2.grid(row=0, column=1, padx=10, pady=10)

     button3 = Button(second_frame, text="Crossing safely", font=(APP_FONT, 20), command=quizz.topic_3)  # type: ignore
     button3.grid(row=0, column=2, padx=10, pady=10)


def learning_page():
     clear_window(root)
     top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
     top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

     text = Label(top_frame, text="Learning centre:", font=(APP_FONT, 30, "bold", "underline"),
                  bg=variables.background_colour)
     text.grid(row=0, column=0, padx=(10, 900), pady=10)

     back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20), command=home_page)
     back_to_homepage_button.grid(row=0, column=1, ipadx=30, padx=10, pady=10)

     second_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
     second_frame.grid(row=2, column=0, columnspan=750, padx=10, pady=10)

     third_frame = Frame(root, bg=variables.background_colour, relief=SOLID)
     third_frame.grid(row=1, column=0, columnspan=750, padx=10, pady=10)

     text = Label(third_frame, text="Select a topic to learn about:", font=(APP_FONT, 25),
                  bg=variables.background_colour)
     text.grid(row=0, column=0, padx=10, pady=10)

     button1 = Button(second_frame, text="Road signs",
                      font=(APP_FONT, 20), command=learning.topic_1)  # type: ignore
     button1.grid(row=0, column=0, padx=10, pady=10)

     button2 = Button(second_frame, text="Car safety",
                      font=(APP_FONT, 20), command=learning.topic_2)  # type: ignore
     button2.grid(row=0, column=1, padx=10, pady=10)

     button3 = Button(second_frame, text="Crossing safely",
                      font=(APP_FONT, 20), command=learning.topic_3)  # type: ignore
     button3.grid(row=0, column=2, padx=10, pady=10)

# Quizz class is now imported from quiz_manager module
quizz = Quizz()

# Learning class is now imported from learning_manager module
learning = Learning()


class CarBrands:
     def __init__(self):
          self.brand_entry = None

     def fetch_logo(self, brand):
          try:
               url = f"https://raw.githubusercontent.com/filippofilip95/car-logos-dataset/master/logos/original/{brand.lower()}.png"
               response = requests.get(url)
               if response.status_code == 200:
                    return response.content
               else:
                    raise ValueError
          except ValueError:
               url = f"https://raw.githubusercontent.com/filippofilip95/car-logos-dataset/master/logos/original/{brand.lower()}.jpg"
               response = requests.get(url)
               if response.status_code == 200:
                    return response.content
               else:
                    return None

     def search(self):
          brand = self.brand_entry.get()
          logo_data = self.fetch_logo(brand)
          if logo_data:
               # Open and resize the image to fit on screen
               img = Image.open(BytesIO(logo_data))
               # Set maximum dimensions (width, height) to fit on screen
               max_width = 500
               max_height = 400
               
               # Calculate new size maintaining aspect ratio
               original_width, original_height = img.size
               aspect_ratio = original_width / original_height
               
               if original_width > max_width or original_height > max_height:
                    if aspect_ratio > 1:  # Width is larger
                         new_width = max_width
                         new_height = int(max_width / aspect_ratio)
                    else:  # Height is larger
                         new_height = max_height
                         new_width = int(max_height * aspect_ratio)
                    
                    # Resize the image (use LANCZOS for high quality resizing)
                    try:
                         # Try newer PIL/Pillow API first
                         img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    except (AttributeError, TypeError):
                         # Fallback for older PIL versions - use integer constant
                         # LANCZOS = 1 in older PIL versions
                         img = img.resize((new_width, new_height), 1)  # 1 = LANCZOS
               
               logo_image = ImageTk.PhotoImage(img)
               self.logo_display.configure(image=logo_image)
               self.logo_display.image = logo_image  # type: ignore
          else:
               self.logo_display.configure(image="", text="Logo not found.")

     def update(self, brand_listbox, data):
          brand_listbox.delete(0, END)
          for brand in data:
               brand_listbox.insert(END, brand)

     def fill_entry(self, brand_entry, brand_listbox, event):
          brand_entry.delete(0, END)
          brand_entry.insert(0, brand_listbox.get(ANCHOR))

     def check(self, brand_entry, brand_list, brand_listbox):
          type = brand_entry.get()
          if type == "":
               data = brand_list
          else:
               data = []
               for item in brand_list:
                    if item.lower().startswith(type.lower()):
                         data.append(item)

          self.update(brand_listbox, data)

     def display_search_page(self):
          clear_window(root)

          top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

          search_frame = Frame(root, bg=variables.background_colour, relief=SOLID )
          search_frame.grid(row=1, column=0, padx=10, pady=0, sticky= W)

          scroll_frame = Frame(root, bg=variables.background_colour, relief=SOLID )

          scroll_bar = Scrollbar(scroll_frame, orient=VERTICAL, )

          text = Label(top_frame, text="Car Brands:", font=(APP_FONT, 30, "bold", "underline"),
                       bg=variables.background_colour, fg=BLACK)
          text.grid(row=0, column=0, padx=(10, 950), pady=10)

          back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                           command=home_page)
          back_to_homepage_button.grid(row=0, column=1, ipadx=30, padx=10, pady=10)

          self.brand_entry = Entry(search_frame, width=44, font=(APP_FONT, 20), bg="white", fg=BLACK)
          self.brand_entry.grid(row=0, column=0, padx=0, pady=3)
          self.brand_entry.focus_set()

          Label(root, text="Logo:", font=(APP_FONT, 30),
                bg=variables.background_colour, fg=BLACK).grid(row= 3, column=0)

          self.logo_display = Label(root)
          self.logo_display.grid(row=4, column=0)

          search_button = Button(search_frame, text="Search", font=(APP_FONT, 20), command=car_brands.search)
          search_button.grid(row=0, column=1, pady=1)

          brand_listbox = Listbox(scroll_frame, width=50, height=5, font=(APP_FONT, 20), bg="white", fg=BLACK,
                                  yscrollcommand=scroll_bar.set)
          scroll_bar.config(command=brand_listbox.yview)
          scroll_bar.pack(fill=Y, side=RIGHT)
          scroll_frame.grid(row=2, column=0, columnspan=749, padx=10, pady=0, sticky=W)
          brand_listbox.pack()


          brand_list = [
               "9ff", "Abadal", "Abarth", "Abbott-Detroit", "Abt", "Ac", "Acura", "Aiways", "Aixam", "Alfa-Romeo",
               "Alpina", "Alpine", "Alta", "Alvis", "Amc", "Apollo", "Arash", "Arcfox", "Ariel", "Aro", "Arrinera",
               "Arrival", "Artega", "Ascari", "Askam", "Aspark", "Aston-Martin", "Atalanta", "Auburn", "Audi-Sport",
               "Audi", "Austin", "Autobacs", "Autobianchi", "Axon", "Bac", "Baic-Motor", "Baojun", "Beiben", "Bentley",
               "Berkeley", "Berliet", "Bertone", "Bestune", "Bharatbenz", "Bitter", "Bizzarrini", "Bmw-M", "Bmw",
               "Borgward", "Bowler", "Brabus", "Brammo", "Brilliance", "Bristol", "Brooke", "Bufori", "Bugatti",
               "Buick",
               "Byd", "Byton", "Cadillac", "Camc", "Canoo", "Caparo", "Carlsson", "Caterham", "Changan", "Changfeng",
               "Chery", "Chevrolet-Corvette", "Chevrolet", "Chrysler", "Cisitalia", "Citroen", "Cizeta", "Cole",
               "Corre-La-Licorne", "Dacia", "Daewoo", "Daf", "Daihatsu", "Daimler", "Dartz", "Datsun", "David-Brown",
               "Dayun", "De-Tomaso", "Delage", "Desoto", "Detroit-Electric", "Devel-Sixteen", "Diatto", "Dina", "Dkw",
               "Dmc", "Dodge-Viper", "Dodge", "Dongfeng", "Donkervoort", "Drako", "Ds", "Duesenberg", "Eagle", "Edag",
               "Edsel", "Eicher", "Elemental", "Elfin", "Elva", "Englon", "Erf", "Eterniti", "Exeed", "Facel-Vega",
               "Faraday-Future", "Faw-Jiefang", "Faw", "Ferrari", "Fiat", "Fioravanti", "Fisker", "Foden",
               "Force-Motors",
               "Ford-Mustang", "Ford", "Foton", "Fpv", "Franklin", "Freightliner", "Fso", "Gac-Group",
               "Gardner-Douglas",
               "Gaz", "Geely", "General-Motors", "Genesis", "Geo", "Geometry", "Gilbern", "Gillet", "Ginetta", "Gmc",
               "Golden-Dragon", "Gonow", "Great-Wall", "Grinnall", "Gumpert", "Hafei", "Haima", "Haval", "Hawtai",
               "Hennessey", "Higer", "Hillman", "Hindustan-Motors", "Hino", "Hiphi", "Hispano-Suiza", "Holden",
               "Hommell",
               "Honda", "Hongqi", "Hongyan", "Horch", "Hsv", "Hudson", "Hummer", "Hupmobile", "Hyundai", "Ic-Bus", "Ih",
               "Ikco", "Infiniti", "Innocenti", "Intermeccanica", "International", "Irizar", "Isdera", "Iso", "Isuzu",
               "Iveco", "Jac", "Jaguar", "Jawa", "Jba-Motors", "Jeep", "Jensen", "Jetta", "Jmc", "Kaiser", "Kamaz",
               "Karlmann-King", "Karma", "Keating", "Kenworth", "Kia", "King-Long", "Koenigsegg", "Ktm", "Lada",
               "Lagonda",
               "Lamborghini", "Lancia", "Land-Rover", "Landwind", "Laraki", "Leapmotor", "Levc", "Lexus", "Leyland",
               "Li-Auto", "Lifan", "Ligier", "Lincoln", "Lister", "Lloyd", "Lobini", "Lordstown", "Lotus", "Lucid",
               "Luxgen", "Lynk-And-Co", "Mack", "Mahindra", "Man", "Mansory", "Marcos", "Marlin", "Maserati",
               "Mastretta",
               "Maxus", "Maybach", "Maz", "Mazda", "Mazzanti", "Mclaren", "Melkus", "Mercedes-Amg", "Mercedes-Benz",
               "Mercury", "Merkur", "Mev", "Mg", "Microcar", "Mini", "Mitsubishi", "Mitsuoka", "Mk", "Morgan", "Morris",
               "Mosler", "Navistar", "Nevs", "Nikola", "Nio", "Nissan-Gt-R", "Nissan-Nismo", "Nissan", "Noble",
               "Oldsmobile", "Oltcit", "Opel", "Osca", "Paccar", "Packard", "Pagani", "Panhard", "Panoz", "Pegaso",
               "Perodua", "Peterbilt", "Peugeot", "Pgo", "Pierce-Arrow", "Pininfarina", "Plymouth", "Polestar",
               "Pontiac",
               "Porsche", "Praga", "Premier", "Prodrive", "Proton", "Qoros", "Radical", "Ram", "Rambler", "Ranz",
               "Renault-Samsung", "Renault", "Rezvani", "Riley", "Rimac", "Rinspeed", "Rivian", "Roewe", "Rolls-Royce",
               "Ronart", "Rossion", "Rover", "Ruf", "Saab", "Saic-Motor", "Saipa", "Saleen", "Saturn", "Scania",
               "Scion",
               "Seat", "Setra", "Shacman", "Simca", "Singer", "Singulato", "Sinotruk", "Sisu", "Skoda", "Smart",
               "Soueast",
               "Spania-Gta", "Spirra", "Spyker", "Ssangyong", "Ssc", "Sterling", "Studebaker", "Stutz", "Subaru",
               "Suffolk",
               "Suzuki", "Talbot", "Tata", "Tatra", "Tauro", "Techart", "Tesla", "Toyota-Alphard", "Toyota-Century",
               "Toyota-Crown", "Toyota", "Tramontana", "Trion", "Triumph", "Troller", "Tucker", "Tvr", "Uaz", "Ud",
               "Ultima", "Vandenbrink", "Vauxhall", "Vector", "Vencer", "Venturi", "Venucia", "Vinfast", "Vlf",
               "Volkswagen", "Volvo", "W-Motors", "Wanderer", "Wartburg", "Weltmeister", "Western-Star", "Westfield",
               "Wey", "Wiesmann", "Willys-Overland", "Workhorse", "Wuling", "Xpeng", "Yulon", "Yutong", "Zarooq-Motors",
               "Zastava", "Zaz", "Zeekr", "Zenos", "Zenvo", "Zhongtong", "Zinoro", "Zotye"
          ]

          self.update(brand_listbox, brand_list)
          # create binding on listbox
          brand_listbox.bind("<<ListboxSelect>>",
                             lambda event: self.fill_entry(self.brand_entry, brand_listbox,
                                                           brand_listbox.curselection()))
          # create binding on entry box
          self.brand_entry.bind("<KeyRelease>", lambda event: self.check(self.brand_entry, brand_list, brand_listbox))


car_brands = CarBrands()


class UserCarInfo:
     def __init__(self):
          self.selected_car_image = PhotoImage(file=BLUE_CAR).subsample(5)
          self.max_velocity = 2.5
          self.first_frame = None

     # changes the colour of car if the user has enough coins
     def change_car_colour(self, car):
          if quizz.user_coins >= 2:
               self.selected_car_image = PhotoImage(file=car).subsample(5)
               game.chosen_car_game = scale_image(pygame.image.load(car), SCALE)
               quizz.user_coins -= 2
               update_coin_db()  # Save coins to database
               self.change_car_colour_page()
               messagebox.showinfo("msj", "Car successfully changed")

          else:
               messagebox.showerror("msj", "Unfortunately you do not have enough coins.\nYou need at least 2 coins.")

     def change_car_colour_page(self):
          clear_window(root)
          top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

          first_frame = Frame(root, bg=variables.background_colour)
          first_frame.grid(row=1, column=0, columnspan=750, padx=10, pady=10)

          second_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          second_frame.grid(row=2, column=0, columnspan=750, padx=10, pady=10)

          text = Label(top_frame, text="Change Car Colour:", font=(APP_FONT, 25, "bold", "underline"),
                       bg=variables.background_colour, fg=BLACK)
          text.grid(row=0, column=0, padx=(10, 510), pady=10)

          user_coins_display = Label(top_frame, text=f"Total Coins: {quizz.user_coins}", font=(APP_FONT, 20),
                                     relief="groove", borderwidth=2, bg=variables.background_colour, fg=BLACK)
          user_coins_display.grid(row=0, column=1, padx=10, pady=10)

          back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                           command=home_page)
          back_to_homepage_button.grid(row=0, column=3, ipadx=10, padx=10, pady=10)
          back_to_customise_button = Button(top_frame, text="Back To Customise Car", font=(APP_FONT, 20),
                                            command=self.customise_car)
          back_to_customise_button.grid(row=0, column=2, ipadx=10, padx=10, pady=10)
          text = Label(first_frame, text="Click on a car to select: ", font=(APP_FONT, 20),
                       bg=variables.background_colour, fg=BLACK)
          text.grid(row=0, column=0, padx=10, pady=10, ipadx=20)
          car_images = [RED_CAR, ORANGE_CAR, YELLOW_CAR, GREEN_CAR, BLUE_CAR, PURPLE_CAR, WHITE_CAR,
                        POLICE_CAR]
          count = 0
          row = 1
          for thing in car_images:
               image = (PhotoImage(file=thing)).subsample(4)
               image_label = Label(second_frame, image=image)
               image_label.photo = image  # type: ignore  # avoid garbage collection
               button = Button(second_frame, image=image,
                               command=lambda c=thing: self.change_car_colour(c))
               button.grid(row=row, column=count, padx=20, pady=20)
               if count != 0 and count % 4 == 0:
                    count = 0
                    row += 1
               else:
                    count += 1

     def customise_car(self):
          clear_window(root)
          top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
          top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

          first_frame = Frame(root, bg=variables.background_colour)
          first_frame.grid(row=1, column=1, columnspan=750, padx=10, pady=10)
          second_frame = Frame(root, bg=variables.background_colour)
          second_frame.grid(row=1, column=0, columnspan=750, padx=10, pady=10)

          user_coins_display = Label(top_frame, text=f"Total Coins: {quizz.user_coins}", font=(APP_FONT, 20),
                                     relief="groove", borderwidth=2, bg=variables.background_colour)
          user_coins_display.grid(row=0, column=1, padx=10, pady=10)

          text = Label(top_frame, text="Customise car:", font=(APP_FONT, 25, "bold", "underline"),
                       bg=variables.background_colour, fg=BLACK)
          text.grid(row=0, column=0, padx=(10, 800), pady=10)

          back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                           command=home_page)
          back_to_homepage_button.grid(row=0, column=2, ipadx=30, padx=10, pady=10)

          text = Label(first_frame, text="Your selected car:", font=(APP_FONT, 20), bg=variables.background_colour, fg=BLACK)
          text.grid(row=0, column=1, padx=10, pady=10)

          selected_car_image_label = Label(first_frame, image=self.selected_car_image)
          selected_car_image_label.grid(row=2, column=1, padx=10, pady=10)
          selected_car_image_label.photo = self.selected_car_image  # type: ignore

          change_colour_button = Button(first_frame, text="Change colour of car", font=(APP_FONT, 20),
                                        command=self.change_car_colour_page)
          change_colour_button.grid(row=3, column=1, ipadx=30, padx=10, pady=10)

          text2 = Label(first_frame, text="Note: in order to change you car colour, you need to pay 2 coins.",
                        font=(APP_FONT, 20), bg=variables.background_colour, fg=BLACK)
          text2.grid(row=4, column=1, padx=10, pady=10)


user_car_info = UserCarInfo()


# link to spec - Simple OOP model
class ParentCar:
     def __init__(self, rotation_velocity, start_position):
          self.START_POSITION = start_position
          self.velocity = 0
          self.rotation_velocity = rotation_velocity
          self.angle = 0
          self.image = game.chosen_car_game
          self.acceleration = 0.05
          self.x, self.y = self.START_POSITION

     def rotate(self, left=False, right=False):  # changes angle of the car for rotation
          if left:
               self.angle += self.rotation_velocity
          elif right:
               self.angle -= self.rotation_velocity

     def draw_on_screen(self):
          blit_rotate_centre(self.image, (self.x, self.y), self.angle)

     def move_forward(self):  # increases the velocity of the car based on the acceleration
          self.velocity = round(min(self.velocity + self.acceleration, user_car_info.max_velocity), 2)
          self.move()

     def move_backward(self):
          self.velocity = round(max(self.velocity - self.acceleration, (- user_car_info.max_velocity / 3)), 2)
          self.move()
     # link to spec - Simple user defined algorithms (eg a range of mathematical/statistical calculations)
     def move(self):  # calculates x and y displacement of car when moving
          radians = math.radians(self.angle)
          vertical = math.cos(radians) * self.velocity
          horizontal = math.sin(radians) * self.velocity
          self.y -= vertical
          self.x -= horizontal
     # checks for collision between two objects
     def collide(self, mask, x=0, y=0):
          car_mask = pygame.mask.from_surface(self.image)
          offset = (int(self.x - x)), (int(self.y - y))
          intersection_point = mask.overlap(car_mask, offset)
          return intersection_point

     def reset(self):
          self.x, self.y = self.START_POSITION
          self.angle = 0
          self.velocity = 0


class UserCar(ParentCar):  # link to spec - inheritance
     def reduce_speed(self):
          self.velocity = round(max(self.velocity - self.acceleration, 0), 2)
          self.move()

     def bounce(self):
          self.velocity = -self.velocity
          self.move()

# home page of app - tkinter
def home_page():
     # Ensure pygame display is fully closed if it was open
     if pygame.display.get_init():
          pygame.display.quit()
          game.screen = None
     game.rootdestroyed = False
     root.deiconify()
     # Use macOS-compatible method to bring window to front
     root.attributes('-topmost', True)
     root.lift()  # Bring window to front
     root.update()  # Process any pending window manager events
     root.attributes('-topmost', False)  # Then allow it to go behind other windows
     try:
          root.focus_force()  # Force focus to Tkinter window (may not work on macOS without permissions)
     except:
          pass  # Ignore if focus_force fails (common on macOS)
     root.update_idletasks()  # Ensure all pending tasks are processed
     clear_window(root)
     image = (PhotoImage(file="pictures/Screenshot 2024-02-27 at 12.12.39 pm.png"))
     image_label = Label(root, image=image)
     image_label.photo = image  # type: ignore
     image_label.place(x=0, y=0)

     setting_button = Button(root, text="Settings", font=(APP_FONT, 20), command=setting.settings)
     setting_button.place(x=350, y=600)

     user_coins_display = Label(root, text=f" Total Coins: {quizz.user_coins}", font=(APP_FONT, 19), relief="groove",
                                borderwidth=2, bg="#1D094A", fg=WHITE)
     user_coins_display.place(x=1290, y=10)

     message1 = Label(root, text=f"Welcome {account_details.name} !", font=(APP_FONT, 20), bg="#EA5C2F")
     message1.place(x=640, y=60)

     message2 = Label(root,
                      text="Here you can learn all about the fun facts and information\nabout rules of the road. After you are done learning, you\ncan do a short quiz in order to earn coins. You can then\nuse these coins to play a game!",
                      font=(APP_FONT, 17), bg="#1D094A", fg=WHITE)
     message2.place(x=490, y=470)

     learn_button = Button(root, text="Learning centre", font=(APP_FONT, 20), command=learning_page)
     learn_button.place(x=270, y=660)

     quiz_button = Button(root, text="Quiz centre",
                          font=(APP_FONT, 20), command=quiz_page)
     quiz_button.place(x=200, y=720)

     text = Label(root, text="Your selected car:", font=(APP_FONT, 20), bg="#161490", fg=WHITE)
     text.place(x=625, y=600)

     selected_car_image_label = Label(root, image=user_car_info.selected_car_image)
     selected_car_image_label.place(x=670, y=650)
     selected_car_image_label.photo = user_car_info.selected_car_image  # type: ignore

     customise_button = Button(root, text="Customise car",
                               font=(APP_FONT, 20), command=user_car_info.customise_car)
     customise_button.place(x=1020, y=660)

     learn_cars_button = Button(root, text="Car brands",
                                font=(APP_FONT, 20), command=car_brands.display_search_page)
     learn_cars_button.place(x=1095, y=720)
     play_button = Button(root, text="Game", font=(APP_FONT, 20), command=pygame_win)
     play_button.place(x=950, y=600)

def get_font(size):
     return pygame.font.Font("font.ttf", size)


# displays all instructions and rules for each level
def how_to_play():
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
def level3():
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
def level2_results_page():
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
def l2_quiz6():
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
def close_pygame_and_return_home():
     """Properly closes pygame window and returns to homepage."""
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
def l1_quiz1():
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
def level1():
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
def check_coins_to_start_level():
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

def create_database_tables(): # creates the tables in the database
     db_manager.create_tables()
def delete_user_acc_db():
     db_manager.delete_user_account(account_details.username)

def l1_leaderboard():
     return db_manager.get_l1_leaderboard(account_details.username, merge_sort)

def l2_leaderboard():
     return db_manager.get_l2_leaderboard(account_details.username, merge_sort)

def l3_leaderboard():
     return db_manager.get_l3_leaderboard(account_details.username, bubble_sort)


def get_l3_highscore():
     return db_manager.get_highscore(3, account_details.username, bubble_sort)

def get_l2_highscore():
     return db_manager.get_highscore(2, account_details.username, merge_sort)

def get_l1_highscore():
     return db_manager.get_highscore(1, account_details.username)

def insert_into_l3():
     db_manager.insert_level_time(3, account_details.username, game.level3_time)

def insert_into_l2():
     db_manager.insert_level_time(2, account_details.username, game.level2_time)

def insert_into_l1():
     db_manager.insert_level_time(1, account_details.username, game.level1_time)
def insert_into_users():
     db_manager.insert_user(account_details.username, account_details.name, account_details.age,
                           account_details.email, account_details.password_reg, quizz.user_coins)

def update_name_db():
     db_manager.update_user_name(account_details.username, account_details.name)

def update_coin_db():
     db_manager.update_user_coins(account_details.username, quizz.user_coins)

def update_pass_db():
     db_manager.update_user_password(account_details.username, account_details.password_reg)

def set_initial_variables():
     item = db_manager.get_user_details(account_details.username, account_details.password_reg)
     if item:
         account_details.name, account_details.age, account_details.email, quizz.user_coins = item

def check_if_username_taken():
     return db_manager.check_username_exists(account_details.username_textbox.get())

def query_login_info():
     item = db_manager.verify_login(account_details.username1.get(), account_details.password1.get())
     if not item:
          messagebox.showerror("error",
                               "Invalid details.\nPlease try again or register for an account ",
                               icon="warning")
     else:
          account_details.username, account_details.password_reg = item
          set_initial_variables()
          account_details.load_screen()

# putting game window at the start position 0,0 on the screen display
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
