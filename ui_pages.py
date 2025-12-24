"""
UI pages module containing welcome_page, home_page, quiz_page, and learning_page functions.
"""
import pygame
from tkinter import *  # noqa: F403, F401
from tkinter import PhotoImage
from config import APP_FONT, BLACK, RED, ORANGE, WHITE


def get_main_refs():
    """Gets references to main module objects to avoid circular imports."""
    import __main__ as main
    return main


def welcome_page():
    main = get_main_refs()
    root = main.root
    clear_window = main.clear_window
    account_details = main.account_details
    
    clear_window(root)
    root.configure(background="light yellow")
    image = (PhotoImage(file="pictures/Screenshot 2024-02-20 at 22.29.42.png").subsample(1))
    image_label = Label(root, image=image)
    image_label.photo = image  # type: ignore
    image_label.grid(row=0, column=0, columnspan=10, rowspan=30)

    welcome_label = Label(root, text="Welcome To RoadRulez!", font=(APP_FONT, 32, "bold"), bg=BLACK, fg=RED)
    welcome_label.grid(row=17, column=7, padx=(35, 5), pady=5)

    label = Label(root, text="If you're a new user, please register for an\n account. If you are registered, login.",
                  font=(APP_FONT, 28), bg=BLACK, fg=ORANGE)
    label.grid(row=18, column=7, padx=(35, 5), pady=5)
    reg_image = (PhotoImage(file="pictures/register.png").subsample(2))
    reg_image_label = Label(root, image=reg_image)
    reg_image_label.photo = reg_image  # type: ignore

    log_image = (PhotoImage(file="pictures/login.png").subsample(2))
    log_image_label = Label(root, image=log_image)
    log_image_label.photo = log_image  # type: ignore

    register_button = Button(root, image=reg_image, command=account_details.register, highlightbackground=BLACK)
    register_button.grid(row=19, column=7, padx=(35, 5), pady=5)

    login_button = Button(root, image=log_image, command=account_details.login, highlightbackground=BLACK)
    login_button.grid(row=20, column=7, padx=(35, 5), pady=5)


def home_page():
    main = get_main_refs()
    root = main.root
    clear_window = main.clear_window
    game = main.game
    setting = main.setting
    quizz = main.quizz
    account_details = main.account_details
    learning_page = main.learning_page
    quiz_page = main.quiz_page
    user_car_info = main.user_car_info
    car_brands = main.car_brands
    pygame_win = main.pygame_win
    
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
    image = (PhotoImage(file="pictures/Screenshot 2024-02-27 at 12.12.39 pm.png"))
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


def quiz_page():
    main = get_main_refs()
    root = main.root
    clear_window = main.clear_window
    home_page = main.home_page
    variables = main.variables
    quizz = main.quizz
    
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

    button1 = Button(second_frame, text="Road signs", font=(APP_FONT, 20), command=quizz.topic_1)
    button1.grid(row=0, column=0, padx=10, pady=10)

    button2 = Button(second_frame, text="Car safety", font=(APP_FONT, 20), command=quizz.topic_2)
    button2.grid(row=0, column=1, padx=10, pady=10)

    button3 = Button(second_frame, text="Crossing safely", font=(APP_FONT, 20), command=quizz.topic_3)
    button3.grid(row=0, column=2, padx=10, pady=10)


def learning_page():
    main = get_main_refs()
    root = main.root
    clear_window = main.clear_window
    home_page = main.home_page
    variables = main.variables
    learning = main.learning
    
    clear_window(root)
    top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
    top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

    text = Label(top_frame, text="Learning centre:", font=(APP_FONT, 30, "bold", "underline"),
                 bg=variables.background_colour, fg=BLACK)
    text.grid(row=0, column=0, padx=(10, 900), pady=10)

    back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20), command=home_page)
    back_to_homepage_button.grid(row=0, column=1, ipadx=30, padx=10, pady=10)

    second_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
    second_frame.grid(row=2, column=0, columnspan=750, padx=10, pady=10)

    third_frame = Frame(root, bg=variables.background_colour, relief=SOLID)
    third_frame.grid(row=1, column=0, columnspan=750, padx=10, pady=10)

    text = Label(third_frame, text="Select a topic to learn about:", font=(APP_FONT, 25),
                 bg=variables.background_colour, fg=BLACK)
    text.grid(row=0, column=0, padx=10, pady=10)

    button1 = Button(second_frame, text="Road signs",
                    font=(APP_FONT, 20), command=learning.topic_1)
    button1.grid(row=0, column=0, padx=10, pady=10)

    button2 = Button(second_frame, text="Car safety",
                    font=(APP_FONT, 20), command=learning.topic_2)
    button2.grid(row=0, column=1, padx=10, pady=10)

    button3 = Button(second_frame, text="Crossing safely",
                    font=(APP_FONT, 20), command=learning.topic_3)
    button3.grid(row=0, column=2, padx=10, pady=10)

