"""
Game engine module containing game-related classes and logic.
"""
import time
import math
import pygame
from config import BLUE_CAR, SCALE, LEV1_START_POSITION, LEV2_START_POSITION, LEV3_START_POSITION
from utils import scale_image, blit_rotate_centre as blit_rotate_centre_util


class PygameButton:
    """Class for buttons in pygame."""
    
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, screen=None):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.screen = screen
        
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
    def update(self, screen=None):
        """Updates the button on the screen."""
        display_screen = screen if screen else self.screen
        if display_screen is None:
            return
        
        if self.image is not None:
            display_screen.blit(self.image, self.rect)
        display_screen.blit(self.text, self.text_rect)
    
    def check_for_input(self, position):
        """Checks if mouse is hovering over the button."""
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def change_color(self, position):
        """Changes the button text color if mouse is hovering over it."""
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Game:
    """Manages game state and logic."""
    
    def __init__(self, assets=None, user_car_info=None):
        self.level_started = False
        self.level_ended = False
        self.chosen_car_game = scale_image(pygame.image.load(BLUE_CAR), SCALE) if assets else None
        self.game_width = 1440
        self.game_height = 790
        self.screen = None
        self.back_to_game_page = None
        self.level1_time = None
        self.level2_time = None
        self.level3_time = None
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
        self.start_time = 0
        self.startq_time = 0
        self.elapsed_time = 0
        self.paused_time = 0
        self.assets = assets
        self.user_car_info = user_car_info
    
    def reset(self):
        """Resets the quiz states and times when level is complete or escape pressed."""
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
        """Starts a level and begins timing."""
        self.level_started = True
        self.start_time = time.time()
    
    def get_time(self):
        """Returns time for level."""
        if not self.level_started:
            self.elapsed_time = 0
            return 0
        elif self.level_ended:
            self.elapsed_time = round(time.time() - self.start_time - self.paused_time - 5, 2)
            return self.elapsed_time
        self.elapsed_time = round(time.time() - self.start_time - self.paused_time, 2)
        return self.elapsed_time
    
    def set_chosen_car(self, car_path):
        """Sets the chosen car image for the game."""
        if self.assets:
            self.chosen_car_game = scale_image(pygame.image.load(car_path), SCALE)


class ParentCar:
    """Base class for car objects."""
    
    def __init__(self, rotation_velocity, start_position, game=None, user_car_info=None):
        self.START_POSITION = start_position
        self.velocity = 0
        self.rotation_velocity = rotation_velocity
        self.angle = 0
        self.game = game
        self.user_car_info = user_car_info
        self.image = game.chosen_car_game if game else None
        self.acceleration = 0.05
        self.x, self.y = self.START_POSITION
    
    def rotate(self, left=False, right=False):
        """Changes angle of the car for rotation."""
        if left:
            self.angle += self.rotation_velocity
        elif right:
            self.angle -= self.rotation_velocity
    
    def draw_on_screen(self, screen=None):
        """Draws the car on the screen."""
        display_screen = screen if screen else (self.game.screen if self.game else None)
        if display_screen and self.image:
            blit_rotate_centre_util(display_screen, self.image, (self.x, self.y), self.angle)
    
    def move_forward(self):
        """Increases the velocity of the car based on the acceleration."""
        max_velocity = self.user_car_info.max_velocity if self.user_car_info else 2.5
        self.velocity = round(min(self.velocity + self.acceleration, max_velocity), 2)
        self.move()
    
    def move_backward(self):
        """Decreases the velocity of the car."""
        max_velocity = self.user_car_info.max_velocity if self.user_car_info else 2.5
        self.velocity = round(max(self.velocity - self.acceleration, (-max_velocity / 3)), 2)
        self.move()
    
    def move(self):
        """Calculates x and y displacement of car when moving."""
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity
        self.y -= vertical
        self.x -= horizontal
    
    def collide(self, mask, x=0, y=0):
        """Checks for collision between two objects."""
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x - x)), (int(self.y - y))
        intersection_point = mask.overlap(car_mask, offset)
        return intersection_point
    
    def reset(self):
        """Resets the car to starting position."""
        self.x, self.y = self.START_POSITION
        self.angle = 0
        self.velocity = 0


class UserCar(ParentCar):
    """User-controlled car class."""
    
    def reduce_speed(self):
        """Reduces the car's speed gradually."""
        self.velocity = round(max(self.velocity - self.acceleration, 0), 2)
        self.move()
    
    def bounce(self):
        """Causes the car to bounce by reversing velocity."""
        self.velocity = -self.velocity
        self.move()


def move_user(user_car):
    """Moves the car using the arrow keys."""
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


def draw_on_screen(screen, images, user_car, game, detail_font):
    """Displays all images on screen during each level."""
    for image, position in images:
        screen.blit(image, position)
    
    time_text = detail_font.render(f"Time:  {game.get_time()} seconds", True, (255, 255, 255), (0, 0, 0))
    screen.blit(time_text, (1250, 10))
    
    speed_text = detail_font.render(f"Speed: {10 * round(user_car.velocity, 2)}mph", True, (255, 255, 255), (0, 0, 0))
    screen.blit(speed_text, (1250, 40))
    user_car.draw_on_screen(screen)
    pygame.display.update()
