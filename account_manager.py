"""
Account management module containing AccountDetails and Setting classes.
"""
import re
import smtplib
import dns.resolver
from tkinter import *  # noqa: F403, F401
from tkinter.ttk import Progressbar
from tkinter import messagebox, OptionMenu
from PIL import Image, ImageTk
import pygame
from config import APP_FONT, APP_SCREEN_WIDTH, BLACK, WHITE
from utils import clear_userdetail_textfile, is_file_empty


def get_main_refs():
    """Gets references to main module objects to avoid circular imports."""
    import __main__ as main
    return main


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
        main = get_main_refs()
        check_if_username_taken = main.check_if_username_taken
        if check_if_username_taken():
            self.error6.config(text="Username already taken.", fg="red")
            self.username_textbox.config(highlightbackground="red")
        else:
            self.error6.config(text="")
            self.username_textbox.config(highlightbackground="white")

    def load_screen(self):
        main = get_main_refs()
        root = main.root
        home_page = main.home_page
        variables = main.variables
        
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
        image_label.photo = image  # type: ignore
        image_label.pack(pady=10)
        root.configure(bg=variables.background_colour)
        load.after(5000, home_page)

    # shows the password from "*" to what they wrote
    def show_login_pass(self):
        if self.password1.cget("show") == "*":
            self.password1.config(show="")
            self.show_login_pass_button.config(text="hide\u200A\u200A\u200A")
        else:
            self.password1.config(show="*")
            self.show_login_pass_button.config(text="show")

    def login(self):
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        account_details = main.account_details
        variables = main.variables
        
        clear_window(root)
        root.configure(bg="grey")
        image = (PhotoImage(file="pictures/login bg.png"))
        image_label = Label(root, image=image)
        image_label.photo = image  # type: ignore
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
                                       font=(APP_FONT, 15), command=account_details.register, bg=WHITE, fg=BLACK)
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
        main = get_main_refs()
        query_login_info = main.query_login_info
        
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

    def send_email(self):  # sends an email to the parent/teacher to fill out a survey
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
        main = get_main_refs()
        insert_into_users = main.insert_into_users
        
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
        main = get_main_refs()
        variables = main.variables
        
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
    
    # creates user account
    def create_acc(self):
        main = get_main_refs()
        check_if_username_taken = main.check_if_username_taken
        insert_into_users = main.insert_into_users
        quizz = main.quizz
        
        self.name = self.name_textbox.get()
        self.username = self.username_textbox.get()
        self.password_reg = self.password_textbox.get()
        self.age = self.age_textbox.get()
        self.user_type = self.user_type_textbox.get()

        if len(self.name and self.username and self.password_reg) != 0 and self.user_type != "Select" and self.age != 0:
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
            with open('userdetails.txt', 'r+') as file:  # link to spec - text files - writing to files - files organised for direct access
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
        main = get_main_refs()
        root = main.root
        
        clicked = event.widget
        if not isinstance(clicked, (Button, Entry)):
            root.focus_set()

    def register(self):
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        variables = main.variables
        
        root.configure(bg=variables.background_colour)
        clear_window(root)
        image = (PhotoImage(file="pictures/reg bg.png"))
        image_label = Label(root, image=image)
        image_label.photo = image  # type: ignore
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
        main = get_main_refs()
        account_details = main.account_details
        update_pass_db = main.update_pass_db
        quizz = main.quizz
        clear_userdetail_textfile = main.clear_userdetail_textfile
        
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
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        variables = main.variables
        
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
        main = get_main_refs()
        account_details = main.account_details
        update_name_db = main.update_name_db
        quizz = main.quizz
        clear_userdetail_textfile = main.clear_userdetail_textfile
        
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
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        variables = main.variables
        
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
                     bg=variables.background_colour, fg=BLACK)
        label.grid(row=0, column=0, padx=10, pady=10)

        self.new_name_entry = Entry(second_frame, width=30, bg="white", fg=BLACK, font=(APP_FONT, 20))
        self.new_name_entry.grid(row=0, column=1, padx=10, pady=10)

        submit_button = Button(second_frame, text="Submit", font=(APP_FONT, 20), command=self.change_name)
        submit_button.grid(row=0, column=2, padx=10, pady=10)
        self.new_name_entry.focus_set()

    def change_background_colour(self, new_colour):
        main = get_main_refs()
        root = main.root
        variables = main.variables
        
        variables.changebgcolour(new_colour, root)
        self.pick_background_colour()

    def pick_background_colour(self):
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        variables = main.variables
        
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
        main = get_main_refs()
        clear_userdetail_textfile = main.clear_userdetail_textfile
        update_coin_db = main.update_coin_db
        welcome_page = main.welcome_page
        
        clear_userdetail_textfile()
        update_coin_db()
        welcome_page()

    def delete_acc(self):
        main = get_main_refs()
        delete_user_acc_db = main.delete_user_acc_db
        welcome_page = main.welcome_page
        
        delete_user_acc_db()
        messagebox.showinfo(message="Account deleted.")
        welcome_page()

    def confirm_delete(self):
        q = messagebox.askokcancel(message="Are you sure you want to delete your account?", icon="warning",
                                   detail="This action cannot be undone.")
        if q:
            self.delete_acc()

    def settings(self):
        main = get_main_refs()
        root = main.root
        clear_window = main.clear_window
        home_page = main.home_page
        variables = main.variables
        
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

