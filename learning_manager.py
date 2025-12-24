"""
Learning management module containing the Learning class.
"""
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from config import APP_FONT, BLACK


def get_main_refs():
    """Gets references to main module objects to avoid circular imports."""
    import __main__ as main
    return main


class Learning:
    """Manages learning content display."""
    
    def __init__(self):
        self.my_canvas = None
        self.my_canvas2 = None

    def topic_1(self):
        """Displays road signs learning content."""
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        learning_page = main.learning_page
        variables = main.variables
        
        clear_window(root)
        # how to create a scrolling bar
        # create a main frame
        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)

        # create a canvas
        self.my_canvas2 = Canvas(main_frame, bg=variables.background_colour)
        self.my_canvas2.pack(side=LEFT, fill=BOTH, expand=1)

        # add a scroll bar to the canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.my_canvas2.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # configure the canvas
        self.my_canvas2.configure(yscrollcommand=my_scrollbar.set)
        self.my_canvas2.bind('<Configure>',
                             lambda e: self.my_canvas2.configure(scrollregion=self.my_canvas2.bbox("all")))

        # create another frame inside canvas
        second_frame = Frame(self.my_canvas2, bg=variables.background_colour)

        # add that new frame to a window in the canvas
        self.my_canvas2.create_window((0, 0), window=second_frame, anchor="nw")

        top_frame = Frame(second_frame, bg=variables.background_colour, borderwidth=2, relief=SOLID)
        top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

        text = Label(top_frame, text="Road Signs:", font=(APP_FONT, 30, "bold", "underline"),
                     bg=variables.background_colour, fg=BLACK)
        text.grid(row=0, column=0, padx=(10, 660), pady=10)

        back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                         command=home_page)
        back_to_homepage_button.grid(row=0, column=2, ipadx=30, padx=10, pady=10)
        back_to_learningpage_button = Button(top_frame, text="Back To Learning Centre", font=(APP_FONT, 20),
                                             command=learning_page)
        back_to_learningpage_button.grid(row=0, column=1, padx=10, pady=10)

        def on_arrow_key(event):
            if event.keysym == "Up":
                self.my_canvas2.yview_scroll(-1, "units")
            elif event.keysym == "Down":
                self.my_canvas2.yview_scroll(1, "units")

        root.bind("<Up>", on_arrow_key)
        root.bind("<Down>", on_arrow_key)

        self.my_canvas2.configure(yscrollincrement='40')
        count = 0
        row = 1
        # link to spec - single dimensional array
        sign_file_paths = ["answers/1.png",
                          "answers/2.png",
                          "answers/3.png",
                          "answers/4.png",
                          "answers/5.png",
                          "answers/6.png",
                          "answers/7.png",
                          "answers/8.png",
                          "answers/9.png",
                          "answers/10.png",
                          "answers/11.png",
                          "answers/12.png",
                          "answers/13.png",
                          "answers/14.png",
                          "answers/15.png",
                          "answers/16.png",
                          "answers/17.png"
                          ]
        for thing in sign_file_paths:
            image = (PhotoImage(file=thing)).subsample(2)
            image_label = Label(second_frame, image=image)
            image_label.photo = image  # type: ignore  # avoid garbage collection
            image_label.grid(row=row, column=count, padx=20, pady=20)
            if count != 0 and count % 5 == 0:
                count = 0
                row += 1
            else:
                count += 1

    def topic_2(self):
        """Displays car safety learning content."""
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        learning_page = main.learning_page
        variables = main.variables
        
        clear_window(root)
        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)

        self.my_canvas = Canvas(main_frame, bg=variables.background_colour)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        self.my_canvas.configure(yscrollcommand=my_scrollbar.set)
        self.my_canvas.bind('<Configure>',
                            lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))

        second_frame = Frame(self.my_canvas, bg=variables.background_colour)

        self.my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        top_frame = Frame(second_frame, bg=variables.background_colour, borderwidth=2, relief=SOLID)
        top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

        text = Label(top_frame, text="Car safety:", font=(APP_FONT, 30, "bold", "underline"),
                     bg=variables.background_colour, fg=BLACK)
        text.grid(row=0, column=0, padx=(10, 760), pady=10)

        back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                         command=home_page)
        back_to_homepage_button.grid(row=0, column=2, padx=10, pady=10)

        back_to_learning_button = Button(top_frame, text="Back To Learning Centre", font=(APP_FONT, 20),
                                         command=learning_page)
        back_to_learning_button.grid(row=0, column=1, padx=10, pady=10)

        def on_arrow_key(event):
            if event.keysym == "Up":
                self.my_canvas.yview_scroll(-1, "units")
            elif event.keysym == "Down":
                self.my_canvas.yview_scroll(1, "units")

        root.bind("<Up>", on_arrow_key)
        root.bind("<Down>", on_arrow_key)

        self.my_canvas.configure(yscrollincrement='40')

        texts = [
            "Here are some tips on how to stay safe while inside a vehicle:",
            "- Whenever you enter a car always put on your seatbelt. This helps reduce the chance of getting injured if\nanything unexpected occurs.",
            "- Avoid sticking your hands, arms and legs out of the window. It's very dangerous and can cause injury\n especially if the vehicle is moving.",
            "- If your car has a child lock, make sure it's activated to prevent accidentally opening doors while the vehicle\nis moving.",
            "- Never play with the car controls. For example the hand brake or the wheel.",
            "- Don't lean against the door as they might open unexpectedly.",
            "- Never play with the car keys or try to start the car yourself."
        ]
        row = 1
        for thing in texts:
            Label(second_frame, text=thing, font=(APP_FONT, 30), bg=variables.background_colour, fg=BLACK).grid(
                row=row, column=1, padx=20, pady=10, sticky=W)
            row += 1

    def topic_3(self):
        """Displays crossing safely learning content."""
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        learning_page = main.learning_page
        variables = main.variables
        
        clear_window(root)
        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)

        self.my_canvas = Canvas(main_frame, bg=variables.background_colour)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        self.my_canvas.configure(yscrollcommand=my_scrollbar.set)
        self.my_canvas.bind('<Configure>',
                            lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))

        second_frame = Frame(self.my_canvas, bg=variables.background_colour)

        self.my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        top_frame = Frame(second_frame, bg=variables.background_colour, borderwidth=2, relief=SOLID)
        top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

        text = Label(top_frame, text="Crossing safely:", font=(APP_FONT, 30, "bold", "underline"),
                     bg=variables.background_colour, fg=BLACK)
        text.grid(row=0, column=0, padx=(10, 670), pady=10)

        back_to_homepage_button = Button(top_frame, text="Back To Homepage", font=(APP_FONT, 20),
                                         command=home_page)
        back_to_homepage_button.grid(row=0, column=2, padx=10, pady=10)

        back_to_learning_button = Button(top_frame, text="Back To Learning Centre", font=(APP_FONT, 20),
                                         command=learning_page)
        back_to_learning_button.grid(row=0, column=1, padx=10, pady=10)

        def on_arrow_key(event):
            if event.keysym == "Up":
                self.my_canvas.yview_scroll(-1, "units")
            elif event.keysym == "Down":
                self.my_canvas.yview_scroll(1, "units")

        root.bind("<Up>", on_arrow_key)
        root.bind("<Down>", on_arrow_key)

        self.my_canvas.configure(yscrollincrement='40')
        # link to spec - single dimensional arrays
        images = ["pictures/1.png",
                 "pictures/2.png",
                 "pictures/3.png",
                 "pictures/4.png",
                 "pictures/5.png",
                 "pictures/6.png",
                 ]
        texts = [
            "Always try to find a zebra crossing or pelican crossing nearby if theres\n one available. If there isnt, find a safe place that gives you the \nopportunity to cross, usually the sidewalks.",
            "Once you have found a spot, stop at the side of the road making sure your\n not on the street yet.",
            "Check both left and right sides to make sure there is no vehicles \napproching.",
            "If you see a vehicle that is approaching fast you should never take the \nrisk of crossing.Its always better to wait and make sure the threat \nis gone",
            "",
            "Finally you should cross carefully. Whenever you are crossing the road you\nshould never be distracted by being on phones or electronics.",
        ]

        count = 1
        row = 1
        for thing in images:
            step = Label(second_frame, text=f"Step {count}:", font=(APP_FONT, 30, "underline"),
                        bg=variables.background_colour, fg=BLACK)
            step.grid(row=row, column=1, padx=20, pady=1)
            image = (PhotoImage(file=thing)).subsample(3)
            image_label = Label(second_frame, image=image)
            image_label.photo = image  # type: ignore  # avoid garbage collection
            image_label.grid(row=row + 1, column=1, padx=20, pady=20)
            Label(second_frame, text=texts[count - 1], font=(APP_FONT, 30), bg=variables.background_colour, fg=BLACK).grid(
                row=row + 2, column=1, padx=20, pady=10)

            row += 3
            count += 1

        textt = Label(second_frame,
                     text="--------------------------------------------------------------------------",
                     font=(APP_FONT, 30),
                     bg=variables.background_colour, fg=BLACK)
        textt.grid(row=19, column=1, padx=10, pady=10)

        image1 = (PhotoImage(file="pictures/7.png")).subsample(3)
        image1_label = Label(second_frame, image=image1)
        image1_label.photo = image1  # type: ignore  # avoid garbage collection
        image1_label.grid(row=20, column=1, padx=20, pady=20)

        text1 = Label(second_frame,
                     text="A zebra crossing doesnt have a traffic light. At a zebra crossing, cars must stop\n whenever they see someone waiting to cross. Therfore always make sure that \nyou try to find a zebra crossing as its the safest way to cross.",
                     font=(APP_FONT, 30),
                     bg=variables.background_colour, fg=BLACK)
        text1.grid(row=21, column=1, padx=10, pady=10)

        text2 = Label(second_frame,
                     text="--------------------------------------------------------------------------",
                     font=(APP_FONT, 30),
                     bg=variables.background_colour, fg=BLACK)
        text2.grid(row=22, column=1, padx=10, pady=10)

        image2 = (PhotoImage(file="pictures/8.png")).subsample(3)
        image2_label = Label(second_frame, image=image2)
        image2_label.photo = image2  # type: ignore  # avoid garbage collection
        image2_label.grid(row=23, column=1, padx=20, pady=20)

        text3 = Label(second_frame,
                     text="A pelican crossing will have a traffic light with two light up people. If\nthe red person is on, that means do not cross. You need to press the button\nand wait until the green person turns on. Then it is safe to cross.",
                     font=(APP_FONT, 30),
                     bg=variables.background_colour, fg=BLACK)
        text3.grid(row=24, column=1, padx=10, pady=10)

