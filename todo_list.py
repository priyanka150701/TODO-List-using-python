# -*- coding: utf-8 -*-
"""
Created on Sat May  4 10:22:12 2024

@author: Esha
"""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import cx_Oracle

def open_todo_list(email_id):
    todo_window = Tk()
    todo_window.title("My To Do List")
    todo_window.geometry("600x400")
    
    # Add a heading
    heading = Label(todo_window, text='My To Do List', font=('ALGERIAN', 17, 'bold'), bg='mediumpurple3', fg='gold')
    heading.pack(pady=20)

    try:
        con = cx_Oracle.connect('PRIYANKA/priyanka@localhost:1521/xe')
        cursor = con.cursor()
        
        # Fetch tasks associated with the email_id
        cursor.execute("SELECT TASKNO, TASKNAME, TASKDATE, TASKTIME FROM TaskTodoList WHERE EMAILID = :email_id", email_id=email_id)
        tasks = cursor.fetchall()
        
        if tasks:
            # Create a Treeview widget
            tree = ttk.Treeview(todo_window, columns=("TaskNo", "TaskName", "TaskDate", "TaskTime"), show='headings')
            tree.heading("TaskNo", text="Task No")
            tree.heading("TaskName", text="Task Name")
            tree.heading("TaskDate", text="Task Date")
            tree.heading("TaskTime", text="Task Time")
            tree.pack(pady=20)
            
            # Insert tasks into the Treeview
            for task in tasks:
                tree.insert("", "end", values=(task[0], task[1], task[2], task[3]))
        else:
            welcome_label = Label(todo_window, text="Welcome!", font=('Purisa', 12), bg='white', fg='black')
            welcome_label.pack(pady=20)
        
        cursor.close()
        con.close()
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 942:  # Table or view does not exist
            welcome_label = Label(todo_window, text="Welcome!", font=('Purisa', 12), bg='white', fg='black')
            welcome_label.pack(pady=20)
        else:
            messagebox.showerror("Database Error", f"Error: {error.message}")
            return
    
    todo_window.mainloop()

# Test the function (for testing purposes, remove or comment out in production)
# open_todo_list('abc@gmail.com')
