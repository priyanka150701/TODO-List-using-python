from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cx_Oracle
import re

def login():
    signup_window.destroy()
    from Login import login

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

def signup():
    username = userEntry.get()
    email = emailEntry.get()
    password = passEntry.get()
    confirm_password = conpassEntry.get()

    # Check if any field is empty
    if not (username and email and password and confirm_password):
        messagebox.showerror("Error", "All fields are required")
        return

    # Check if email is valid
    if not is_valid_email(email):
        messagebox.showerror("Error", "Please enter a valid Gmail address")
        return

    # Check if password length is at least 8 characters
    if len(password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters long")
        return

    # Check if Terms & Conditions are agreed
    if not terms_checked.get():
        messagebox.showerror("Error", "Please agree to the Terms & Conditions")
        return

    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    # Connect to Oracle Database
    try:
        con = cx_Oracle.connect('PRIYANKA/priyanka@localhost:1521/xe')
        cursor = con.cursor()

        # Insert data into UserDataTodoList table (replace column names if needed)
        cursor.execute("""
            INSERT INTO UserDataTodoList (EMAILID, PASSWORD, NAME)
            VALUES (:email, :password, :username)
        """, email=email, password=password, username=username)

        con.commit()
        cursor.close()
        con.close()

        messagebox.showinfo("Success", "Account created successfully!")

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        messagebox.showerror("Database Error", f"Error: {error.message}")
        return

signup_window = Tk()
signup_window.title('SignUp Page')
signup_window.resizable(False, False)
signup_window.geometry("900x600")

image = Image.open("su.jpg")
resized_image = image.resize((900, 600))
bgImage = ImageTk.PhotoImage(resized_image)
bgLabel = Label(signup_window, image=bgImage)
bgLabel.grid(row=0, column=0)

frame = Frame(signup_window, bg='gold')
frame.place(x=500, y=50)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('ALGERIAN', 17, 'bold'), bg='white', fg='firebrick1')
heading.grid(row=0, column=0, padx=10, pady=20)

emailLabel = Label(frame, text='Email', font=('ALGERIAN', 10, 'bold'), bg='white', fg='firebrick1')
emailLabel.grid(row=1, column=0, sticky='w', padx=25)

emailEntry = Entry(frame, width=30, font=('ALGERIAN', 10, 'bold'))
emailEntry.grid(row=2, column=0, sticky='w', padx=25, pady=5)

userName = Label(frame, text='User Name', font=('ALGERIAN', 10, 'bold'), bg='white', fg='firebrick1')
userName.grid(row=3, column=0, sticky='w', padx=25, pady=(10, 0))

userEntry = Entry(frame, width=30, font=('ALGERIAN', 10, 'bold'))
userEntry.grid(row=4, column=0, sticky='w', padx=25, pady=5)

passLabel = Label(frame, text='Password', font=('ALGERIAN', 10, 'bold'), bg='white', fg='firebrick1')
passLabel.grid(row=5, column=0, sticky='w', padx=25, pady=(10, 0))

passEntry = Entry(frame, width=30, font=('ALGERIAN', 10, 'bold'), show='*')
passEntry.grid(row=6, column=0, sticky='w', padx=25, pady=5)

conpassLabel = Label(frame, text='Confirm Password', font=('ALGERIAN', 10, 'bold'), bg='white', fg='firebrick1')
conpassLabel.grid(row=7, column=0, sticky='w', padx=25, pady=(10, 0))

conpassEntry = Entry(frame, width=30, font=('ALGERIAN', 10, 'bold'), show='*')
conpassEntry.grid(row=8, column=0, sticky='w', padx=25, pady=5)

terms_checked = BooleanVar()
terms_checked.set(False)

terms = Checkbutton(frame, text='I agree to the Terms & conditions', font=('ALGERIAN', 9, 'bold'), bg='white', fg='firebrick1', activebackground='white', activeforeground='firebrick1', cursor='hand2', variable=terms_checked)
terms.grid(row=9, column=0, sticky='w', padx=25, pady=10)

signup_button = Button(frame, text='Sign Up', font=('ALGERIAN', 16, 'bold'), bd=0, bg='firebrick1', fg='white', activebackground='green', activeforeground='firebrick1', cursor='hand2', command=signup)
signup_button.grid(row=10, column=0, padx=25, pady=10)

alreadyaccount = Label(frame, text="Already have an account?", font=('Purisa', 8, 'bold'), fg='black')
alreadyaccount.grid(row=11, column=0, sticky='w', padx=25, pady=10)

loginButton = Button(frame, text="LogIn", font=('Open Sans', 9, 'bold underline'), bd=0, bg='white', fg='blue', activebackground='green', activeforeground='firebrick1', cursor='hand2', command=login)
loginButton.place(x=172, y=422)

signup_window.mainloop()

