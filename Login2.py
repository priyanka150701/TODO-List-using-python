# -*- coding: utf-8 -*-
"""
Created on Sat May  4 10:22:12 2024

@author: Esha
"""

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import cx_Oracle
import re
import os
from TodoListWindow import todoList  # Import the function

# Function to remove the word 'Username' while writing a text there
def username_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

# Function to remove the word 'Password' while writing a text there
def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

def hide():
    # Change open eye to close eye
    Eye.config(file='hidepswrd.png')
    # Change password to *
    passwordEntry.config(show='*')
    # Calling function show to change close eye button to open eye
    eyeButton.config(command=show)

def show():
    # Change close eye to open eye
    Eye.config(file='showpswrd.png')
    # Make password visible
    passwordEntry.config(show='')
    # Calling function hide to change open eye button to close eye
    eyeButton.config(command=hide)

def login():
    username = usernameEntry.get()
    password = passwordEntry.get()

    # Check if fields are empty
    if username == '' or username == 'Username' or password == '' or password == 'Password':
        messagebox.showerror("Error", "All fields are required")
        return

    # Connect to Oracle Database
    try:
        con = cx_Oracle.connect('PRIYANKA/priyanka@localhost:1521/xe')
        cursor = con.cursor()

        # Check if username and password match
        cursor.execute("SELECT * FROM UserDataTodoList WHERE emailid = :username AND PASSWORD = :password", 
                       username=username, password=password)
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()  # Close the login window
            todoList(user_id)  # Open the to-do list window
        else:
            messagebox.showerror("Error", "Invalid username or password")

        cursor.close()
        con.close()

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        messagebox.showerror("Database Error", f"Error: {error.message}")
        return

login_window = Tk()
login_window.geometry("900x600")
# To prevent maximizing login_window window
login_window.resizable(0, 0)
login_window.title("TO DO LIST")

image = Image.open("su.jpg")
resized_image = image.resize((900, 600))
bgImage = ImageTk.PhotoImage(resized_image)
bgLabel = Label(login_window, image=bgImage)
bgLabel.grid(row=0, column=0)

# Adding background image
bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

# Create label for heading
heading = Label(login_window, text='USER LOGIN', font=('ALGERIAN', 17, 'bold'), bg='mediumpurple3', fg='gold')
heading.place(x=350, y=130)

# Entry field for username
usernameEntry = Entry(login_window, width=20, font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, bg='white', fg='black')
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', username_enter)
usernameEntry.place(x=350, y=200)

# Underline for username
frame1 = Frame(login_window, width=250, height=2, bg='black')
frame1.place(x=350, y=225)

# Entry field for password
passwordEntry = Entry(login_window, width=20, font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, bg='white', fg='black')
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)
passwordEntry.place(x=350, y=250)

# Underline for password
frame2 = Frame(login_window, width=250, height=2, bg='black')
frame2.place(x=350, y=275)

Eye = PhotoImage(file='showpswrd.png')
# Button to show/hide password
eyeButton = Button(login_window, image=Eye, bd=0, bg='white', activebackground='white', cursor='hand2', command=hide)
eyeButton.place(x=560, y=250)

# Button to reset password
forgetButton = Button(login_window, text="Forgot Password?", bd=0, bg='purple4', activebackground='purple4', cursor='hand2', font=('Purisa', 8, 'bold'), fg='white', activeforeground='red')
forgetButton.place(x=420, y=300)

# Button to login
loginButton = Button(login_window, text="LOGIN", bd=3, bg='darkgoldenrod', activebackground='black', cursor='hand2', font=('cylburn', 12, 'bold'), fg='black', activeforeground='darkgoldenrod', command=login)
loginButton.place(x=400, y=350)

# Label to ask if any account present
signupLabel = Label(login_window, text="Don't have an account?", font=('Purisa', 10, 'bold'), bg='purple4', fg='white')
signupLabel.place(x=350, y=400)

# Button to signup/create new account
newAcctButton = Button(login_window, text="Signup", bd=0, bg='purple4', activebackground='purple4', cursor='hand2', font=('Purisa', 10, 'bold underline'), fg='white', activeforeground='red')
newAcctButton.place(x=500, y=400)

login_window.mainloop()
