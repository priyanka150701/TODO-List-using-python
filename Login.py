# -*- coding: utf-8 -*-
"""
Created on Sat May  4 10:22:12 2024

@author: Esha
"""


from tkinter import *;
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import ttk
import tkinter as tk
import cx_Oracle
from TodoListWindow import todoList 

#function to remove the word username while writing a text there
def username_enter(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0,END)

#function to remove the word password while writing a text there        
def password_enter(event):
    if passwordEntry.get()=='Password':
        passwordEntry.delete(0,END)
             
def hide():
    #change open eye to close eye
    Eye.config(file='hidepswrd.png')
    #change password to *
    passwordEntry.config(show='*')
    #calling function show to change close eye button to open eye
    eyeButton.config(command=show)
    
def show():
    #change close eye to open eye
    Eye.config(file='showpswrd.png')
    #make password visible
    passwordEntry.config(show='')
    #calling function hide to change open eye button to close eye
    eyeButton.config(command=hide)

def login():
    if usernameEntry.get()=='Username' or passwordEntry.get=='Password':
        messagebox.showerror('Error','Invalid username and password')
        
    elif usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','All fields are required')
    
    else:
        u=usernameEntry.get()
        p=passwordEntry.get()
        
        try:
            con=cx_Oracle.connect('PRIYANKA/priyanka@localhost:1521/xe')
            cursor=con.cursor()
            #print("Connected")
            
            c='select * from UserDataTodoList where EMAILID=:u and PASSWORD=:p'
            cursor.execute(c,(u,p))
            #print("Executed")
            
            records=cursor.fetchall()
            #print(records)
            
            if records:
                login_window.destroy()
                todoList(u)
                
            else:
                messagebox.showerror('Error','Invalid credentials')                
            
        except cx_Oracle.DatabaseError as e:
            print("There is a problem with the connection",e)
            
        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()

def resetpswrd():
    login_window.destroy()
    import ResetPswrd

def signup():
    login_window.destroy()
    import signup
      
                   
login_window=Tk()
login_window.geometry("724x408")
#to prevent maximizing login_window window
login_window.resizable(0,0)
login_window.title("TO DO LIST")

bgImage=ImageTk.PhotoImage(file='bg.jpg')
#adding label as login_window to see image on window
bgLabel=Label(login_window,image=bgImage)
#adding position of image on window
#position is top left corner by using bgLabel.grid(row=0,column=0)
#for using pack() no need to mention geometry just write bg.pack()
#for using place() mention geometry 
bgLabel.place(x=0,y=0)

#create label for heading 
heading=Label(login_window,text='USER LOGIN',font=('ALGERIAN',17,'bold'),bg='mediumpurple3',fg='gold')
#place the label at particular position hence use place() method sine place() method is used to place at particular location
heading.place(x=300,y=90)


#Entry field created with the help of Entry class
#text font,color etc of text to be typed
usernameEntry=Entry(login_window,width=17,font=('Microsoft Yahei UI Light',10,'bold'),bd=0,bg='white',fg='black')
#shows username in text box
usernameEntry.insert(0,'Username')
#bind method will remove the word username while writing a text there
#focusIn command used
#on_enter is function to determin what will happen after cursor placed in text box of usernameEntry
usernameEntry.bind('<FocusIn>',username_enter)
usernameEntry.place(x=300,y=160)
#for the underline under username
frame1=Frame(login_window,width=140,height=2,bg='black')
frame1.place(x=300,y=180)


passwordEntry=Entry(login_window,width=12,font=('Microsoft Yahei UI Light',10,'bold'),bd=0,bg='white',fg='black')
passwordEntry.insert(0,'Password')
passwordEntry.bind('<FocusIn>',password_enter)
passwordEntry.place(x=300,y=200)
#for the underline under password
frame2=Frame(login_window,width=100,height=2,bg='black')
frame2.place(x=300,y=220)


Eye=PhotoImage(file='showpswrd.png')
#hide is a function to change open eye img to close eye img
eyeButton=Button(login_window,image=Eye,bd=0,bg='white',activebackground='white',cursor='hand2',command=hide)
eyeButton.place(x=400,y=200)


#button to reset password
forgetButton=Button(login_window,text="Forgot Password?",bd=0,bg='purple4',activebackground='purple4',cursor='hand2',font=('Purisa',8,'bold'),fg='white',activeforeground='red',command=resetpswrd)
forgetButton.place(x=350,y=230)


#button to login
loginButton=Button(login_window,text="LOGIN",bd=3,bg='darkgoldenrod',activebackground='black',cursor='hand2',font=('cylburn',10,'bold'),fg='black',activeforeground='darkgoldenrod',command=login)
loginButton.place(x=335,y=270)


#label to ask if any account present
signupLabel=Label(login_window,text="Don't have an account?",font=('Purisa',8,'bold'),bg='purple4',fg='white')
signupLabel.place(x=280,y=310)


#button to signup / create new account
newAcctButton=Button(login_window,text="Signup",bd=0,bg='purple4',activebackground='purple4',cursor='hand2',font=('Purisa',8,'bold underline'),fg='white',activeforeground='red',command=signup)
newAcctButton.place(x=410,y=310)


login_window.mainloop()

