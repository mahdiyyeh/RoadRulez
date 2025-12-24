"""
Game engine module containing game-related classes and logic.
"""
import time
from typing import Optional
import pygame
from config import BLUE_CAR, SCALE
from utils import scale_image


def get_main_refs():
    """Gets references to main module objects to avoid circular imports."""
    import __main__ as main
    return main


class Button1:  # class for buttons in pygame
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
        main = get_main_refs()
        game = main.game
        if self.image is not None:
            game.screen.blit(self.image, self.rect)  # type: ignore
        game.screen.blit(self.text, self.text_rect)  # type: ignore

    def checkForInput(self, position):  # checks if mouse is hovering over the button
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):  # changes the button textcolour is mouse if hovering over it
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


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


class Game:  # link to spec - Complex user-defined use of object- orientated programming (OOP) model, eg classes
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


# Helper functions that use game.screen directly (matching main file pattern)
def blit_rotate_centre(image, top_left, angle):
    """1) rotates image, 2) assigns new centre so image rotates from centre and not the top left."""
    main = get_main_refs()
    game = main.game
    rotated_image = pygame.transform.rotate(image, angle)
    new_rectangle = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    game.screen.blit(rotated_image, new_rectangle.topleft)  # type: ignore


def write_text_to_centre(font, text):
    """Writes text to the centre of the screen."""
    from config import RED, BLACK
    main = get_main_refs()
    game = main.game
    text_bg = font.render(text, True, RED, BLACK)
    game.screen.blit(text_bg, (game.screen.get_width() / 2 - text_bg.get_width() / 2, game.screen.get_height() / 2 - text_bg.get_height() / 2))  # type: ignore


# displays all images on screen during each level
def draw_on_screen(images, user_car):
    """Displays all images on screen during each level."""
    main = get_main_refs()
    game = main.game
    # GAME_DETAIL_FONT is initialized in main file
    try:
        GAME_DETAIL_FONT = main.GAME_DETAIL_FONT
    except:
        import pygame
        GAME_DETAIL_FONT = pygame.font.Font("Flipahaus-Regular.ttf", 20)
    
    from config import WHITE, BLACK
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
