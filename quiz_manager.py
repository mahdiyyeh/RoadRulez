"""
Quiz management module containing the Quizz class.
"""
from tkinter import *
from tkinter import Radiobutton
from PIL import Image, ImageTk
from config import APP_FONT, BLACK
import sys


def get_main_refs():
    """Gets references to main module objects to avoid circular imports."""
    # When the main file is run, it's available as __main__
    import __main__ as main
    return main


class Quizz:
    """Manages quiz functionality and user interactions."""
    
    def __init__(self):
        self.user_answer = StringVar()
        self.user_score = IntVar()
        self.current_question_num = 0
        self.question = None
        self.answer = None
        self.frame_1 = None
        self.next_button = Button
        self.start_quiz_button = Button
        self.finish_button = Button
        self.user_coins = 0
        self.top_frame = None
        self.quiz_topic = None
        self.signlist = None

    def topic_1(self):
        """Sets up quiz for Road signs topic."""
        self.quiz_topic = "Road signs"
        # link to spec - dictionaries
        self.question = {
            "Q1 ) whats this sign?": ['a) hospital', 'b) do not enter', 'c) school zone', 'd) railroad crossing'],
            "Q2 ) whats this sign?": ['a) speed advisory', 'b) no bicycles', 'c) hospital', 'd) left turn'],
            "Q3 ) whats this sign?": ['a) airport', 'b) train station', 'c) no airport', 'd) do not enter'],
            "Q4 ) whats this sign?": ['a) do not enter', 'b) no stopping', 'c) wait here', 'd) no waiting'],
            "Q5 ) whats this sign?": ['a) no left turn', 'b) train station', 'c) level crossing without barrier',
                                     'd) level crossing with barrier'],
            "Q6 ) whats this sign?": ['a) wild animals', 'b) wild horses', 'c) no animals allowed',
                                     'd) pedestrian crossing'],
            "Q7 ) whats this sign?": ['a) roundabout', 'b) no right turn', 'c) hospital', 'd) left turn'],
            "Q8 ) whats this sign?": ['a) no waiting', 'b) pelican crossing', 'c) no parking', 'd) parking'],
            "Q9 ) whats this sign?": ['a) hospital', 'b) traffic light ahead', 'c) happy', 'd) dead end'],
            "Q10 ) whats this sign?": ['a) puffin crossing', 'b) zebra crossing', 'c) pelican crossing',
                                      'd) railroad crossing'],
            "Q11 ) whats this sign?": ['a) level crossing without barrier', 'b) tunnel ahead', 'c) dead end',
                                      'd) road works ahead'],
            "Q12 ) whats this sign?": ['a) zebra crossing', 'b) no waiting', 'c) do not enter', 'd) no parking'],
            "Q13 ) whats this sign?": ['a) no right turn', 'b) no left turn', 'c) right turn ahead',
                                      'd) left turn ahead'],
            "Q14 ) whats this sign?": ['a) right turn ahead', 'b) no right turn', 'c) left turn ahead',
                                      'd) no left turn'],
            "Q15 ) whats this sign?": ['a) road works ahead', 'b) traffic light ahead', 'c) no parking',
                                      'd) no stopping'],
            "Q16 ) whats this sign?": ['a) tunnel ahead', 'b) zebra crossing', 'c) no parking', 'd) parking'],
            "Q17 ) whats this sign?": ['a) road works ahead', 'b) traffic light ahead',
                                      'c) level crossing with barrier',
                                      'd) level crossing without barrier']
        }
        # link to spec - single dimensional arrays
        self.answer = ['c) school zone',
                      'b) no bicycles',
                      'a) airport',
                      'd) no waiting',
                      'c) level crossing without barrier',
                      'b) wild horses',
                      'a) roundabout',
                      'd) parking',
                      'a) hospital',
                      'b) zebra crossing',
                      'c) dead end',
                      'c) do not enter',
                      'a) no right turn',
                      'd) no left turn',
                      'b) traffic light ahead',
                      'a) tunnel ahead',
                      'c) level crossing with barrier']
        # link to spec - lists
        self.signlist = ["questions/1.png",
                        "questions/2.png",
                        "questions/3.png",
                        "questions/4.png",
                        "questions/5.png",
                        "questions/6.png",
                        "questions/7.png",
                        "questions/8.png",
                        "questions/9.png",
                        "questions/10.png",
                        "questions/11.png",
                        "questions/12.png",
                        "questions/13.png",
                        "questions/14.png",
                        "questions/15.png",
                        "questions/16.png",
                        "questions/17.png"
                        ]

        self.put_quiz()

    def topic_2(self):
        """Sets up quiz for Car safety topic."""
        self.quiz_topic = "Car safety"
        # link to spec - dictionaries
        self.question = {
            "Q1) How often should you put on your seatbelt?": ['a) once a week', 'b) always', 'c) never', 'd) only if its raining'],
            "Q2) what are you allowed to put out the window?": ['a) hands', 'b) feet', 'c) head', 'd) arms', 'e) none of the above'],
            "Q3) Why should you make sure your child lock is activated?": ['a) to feel like a prisoner',
                'b) you develop problem-solving skills by figuring out how to open it',
                'c) to prevent accidentally opening the doors while the vehicle is moving',
                'd) to make sure its easy for you to open the doors while the vehicle is moving.'],
            "Q4) When are you allowed to play with the controls": ['a) never', 'b) always', 'c) when theres no one in the car', 'd) when theres a cat in the vehicle'],
            "Q5) Why shouldn't you lean on the doors?": ['a) its comfortable', 'b) to prevent the warm air from escaping', 'c) to prevent it from raining inside ', 'd) they might open unexpectedly'],
            "Q6) Should you ever try to turn on the car by yourself?" : ['a) only if your in a garage', 'b) yes', 'c) no', 'd) yes but dont drive it']
        }
        # link to spec - single dimensional array
        self.answer = ['b) always', 'e) none of the above', 'c) to prevent accidentally opening the doors while the vehicle is moving', 'a) never', 'd) they might open unexpectedly','c) no']
        self.put_quiz()

    def topic_3(self):
        """Sets up quiz for Crossing safely topic."""
        self.quiz_topic = "Crossing safely"
        self.question = {
            "Q1) Does a zebra crossing have a traffic light?": ['a) yes', 'b) sometimes', 'c) no', 'd) only on mondays'],
            "Q2) What does it mean when the red person is on at a pelican crossing traffic light?": [
                'a) do not cross', 'b) you should argue with the traffic light', 'c) cross without looking',
                'd) the traffic light is angry'],
            "Q3) Where should you stand when wanting to cross the road?": [
                'a) in the middle of the road so the cars have to stop', 'b) in the bushes next to the side walk',
                'c) climb the nearest traffic light and stand on top',
                'd) at the side of the road on the side walk'],
            "Q4) What two things should you use to spot any moving vehicles?": ['a) feet and mouth',
                                                                               'b) eyes and ears',
                                                                               'c) hair and bag ',
                                                                               'd) eyes and pencils'],
            "Q5) What should you do if your waiting to cross but a vehicle is approaching?": [
                'a) continue waiting until vehicle has passed', 'b) step onto the road',
                'c) scream at the passing vehicle',
                'd) start dancing in the middle of the road to distract the driver making them stop so you can cross '],
            "Q6) When is it ok to be on your phone while crossing?": ['a) when you have a blue shirt ',
                                                                     'b) when its sunny',
                                                                     'c) when you see a yellow car', 'd) never'],
            "Q7) Which direction should you look at when waiting to cross": ['a) behind you', 'b) down',
                                                                            'c) left and right', 'd) at the sky'],

        }
        self.answer = ['c) no', 'a) do not cross', 'd) at the side of the road on the side walk', 'b) eyes and ears',
                      'a) continue waiting until vehicle has passed', 'd) never', 'c) left and right']
        self.put_quiz()

    def put_quiz(self):
        """Displays the quiz interface."""
        # Get main module references (when file is run, it's __main__)
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        quiz_page = main.quiz_page
        home_page = main.home_page
        
        self.current_question_num = 0
        self.user_answer.set("None")
        self.user_score.set(0)
        clear_window(root)
        user_answer = self.user_answer
        user_answer.set("None")
        user_score = self.user_score
        user_score.set(0)

        main = get_main_refs()
        variables = main.variables
        
        self.top_frame = Frame(root, bg=variables.background_colour)
        self.top_frame.grid(row=0, column=0, padx=20, pady=10, sticky=W)

        self.frame_1 = Frame(root, bg=variables.background_colour)
        self.frame_1.grid(row=1, column=0, padx=20, pady=10, sticky=W)

        login_label = Label(self.top_frame, text=f"Quiz on {self.quiz_topic}:",
                           font=(APP_FONT, 30, "underline", "bold"), bg=variables.background_colour, fg=BLACK)
        login_label.grid(row=0, column=0, padx=(20, 400), pady=10, sticky=W)

        self.start_quiz_button = Button(root, text="Start Quiz", font=(APP_FONT, 25, "bold"), command=self.start_quiz)
        self.start_quiz_button.grid(row=1, column=0, padx=20, pady=10)
        back_to_quizpage_button = Button(self.top_frame, text="Back To Quiz Centre", font=(APP_FONT, 20),
                                         command=quiz_page)
        back_to_quizpage_button.grid(row=0, column=1, padx=10, pady=10)

        back_to_homepage_button = Button(self.top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                         command=home_page)
        back_to_homepage_button.grid(row=0, column=2, padx=10, pady=10)
        self.next_button = Button(root, text="Submit and go to next Question", font=(APP_FONT, 16, "bold"),
                                 command=self.next_question)

    def check_answer(self):
        """Checks if the user's answer is correct."""
        temp_answer = self.user_answer.get()
        if temp_answer != "None" and temp_answer == self.answer[self.current_question_num - 1]:
            self.user_score.set(self.user_score.get() + 1)

    def display_quiz_results(self):
        """Displays the quiz results."""
        main = get_main_refs()
        variables = main.variables
        
        self.user_coins += self.user_score.get()
        # Save coins to database
        update_coin_db = main.update_coin_db
        update_coin_db()
        question_len = len(self.question) if self.question else 0  # type: ignore
        Label(self.frame_1, text=f"Your score is {self.user_score.get()} out of {question_len}",
              font=(APP_FONT, 25), bg=variables.background_colour, fg=BLACK).grid(
            row=0, column=0, padx=10, pady=10, sticky=W)
        Label(self.top_frame, text=f"Total Coins: {self.user_coins}",
              font=(APP_FONT, 20), relief="solid", borderwidth=2, bg=variables.background_colour, fg=BLACK).grid(
            row=0, column=3, padx=10, pady=10, sticky=W)

    def next_question(self):
        """Displays the next question in the quiz."""
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        
        if self.question and self.current_question_num < len(self.question):  # type: ignore
            if self.current_question_num == (len(self.question) - 1):  # type: ignore
                self.next_button.destroy()  # type: ignore
                self.finish_button = Button(root, text="Submit and finish", font=(APP_FONT, 16, "bold"),
                                           command=self.next_question)
                self.finish_button.grid(row=2, column=0, padx=20, pady=10, sticky=W)

            self.check_answer()
            self.user_answer.set('None')
            current_question = list(self.question.keys())[self.current_question_num]  # link to spec - list operations
            main = get_main_refs()
            variables = main.variables
            
            clear_window(self.frame_1)
            Label(self.frame_1, text=f"{current_question}", padx=15, font=(APP_FONT, 20),
                 bg=variables.background_colour, fg=BLACK).pack(anchor=NW)
            if self.quiz_topic == "Road signs":
                image = (PhotoImage(file=self.signlist[self.current_question_num])).subsample(3)
                image_label = Label(self.frame_1, image=image)
                image_label.photo = image  # type: ignore
                image_label.pack(pady=10)

            for text in self.question[current_question]:
                Radiobutton(self.frame_1, text=text, variable=self.user_answer, value=text, padx=28,
                           font=(APP_FONT, 20)).pack(anchor=W)
            self.current_question_num += 1
        else:
            self.finish_button.destroy()  # type: ignore
            self.check_answer()
            clear_window(self.frame_1)
            self.display_quiz_results()

    def start_quiz(self):
        """Starts the quiz."""
        main = get_main_refs()
        root = main.root
        
        self.start_quiz_button.destroy()  # type: ignore
        self.next_button.grid(row=2, column=0, padx=20, pady=10, sticky=W)  # type: ignore
        self.next_question()

