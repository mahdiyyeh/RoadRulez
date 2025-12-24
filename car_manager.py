"""
Car management module containing CarBrands, UserCarInfo, ParentCar, and UserCar classes.
"""
import math
import pygame
from tkinter import *  # noqa: F403, F401
from tkinter import Scrollbar, messagebox
from PIL import Image, ImageTk
from io import BytesIO
import requests
from config import (
    APP_FONT, BLACK, BLUE_CAR, RED_CAR, ORANGE_CAR, YELLOW_CAR,
    GREEN_CAR, PURPLE_CAR, WHITE_CAR, POLICE_CAR, SCALE
)
from utils import scale_image
from game_engine import blit_rotate_centre


def get_main_refs():
    """Gets references to main module objects to avoid circular imports."""
    import __main__ as main
    return main


class CarBrands:
    def __init__(self):
        self.brand_entry = None
        self.logo_display = None

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
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        variables = main.variables
        car_brands = main.car_brands
        
        clear_window(root)

        top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
        top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

        search_frame = Frame(root, bg=variables.background_colour, relief=SOLID)
        search_frame.grid(row=1, column=0, padx=10, pady=0, sticky=W)

        scroll_frame = Frame(root, bg=variables.background_colour, relief=SOLID)

        scroll_bar = Scrollbar(scroll_frame, orient=VERTICAL)

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
              bg=variables.background_colour, fg=BLACK).grid(row=3, column=0)

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


class UserCarInfo:
    def __init__(self):
        self.selected_car_image = PhotoImage(file=BLUE_CAR).subsample(5)
        self.max_velocity = 2.5
        self.first_frame = None

    # changes the colour of car if the user has enough coins
    def change_car_colour(self, car):
        main = get_main_refs()
        quizz = main.quizz
        game = main.game
        update_coin_db = main.update_coin_db
        
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
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        variables = main.variables
        quizz = main.quizz
        
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
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        variables = main.variables
        quizz = main.quizz
        
        clear_window(root)
        top_frame = Frame(root, bg=variables.background_colour, relief=SOLID, borderwidth=2)
        top_frame.grid(row=0, column=0, columnspan=750, padx=10, pady=10)

        first_frame = Frame(root, bg=variables.background_colour)
        first_frame.grid(row=1, column=1, columnspan=750, padx=10, pady=10)
        second_frame = Frame(root, bg=variables.background_colour)
        second_frame.grid(row=1, column=0, columnspan=750, padx=10, pady=10)

        user_coins_display = Label(top_frame, text=f"Total Coins: {quizz.user_coins}", font=(APP_FONT, 20),
                                   relief="groove", borderwidth=2, bg=variables.background_colour, fg=BLACK)
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


# link to spec - Simple OOP model
class ParentCar:
    def __init__(self, rotation_velocity, start_position):
        main = get_main_refs()
        game = main.game
        
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
        main = get_main_refs()
        user_car_info = main.user_car_info
        
        self.velocity = round(min(self.velocity + self.acceleration, user_car_info.max_velocity), 2)
        self.move()

    def move_backward(self):
        main = get_main_refs()
        user_car_info = main.user_car_info
        
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

