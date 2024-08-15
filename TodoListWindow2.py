from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import tkinter as tk
import cx_Oracle
import hashlib
import os
import json

# Database connectivity
con = cx_Oracle.connect('PRIYANKA/priyanka@localhost:1521/xe')
cursor = con.cursor()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

SESSION_FILE = "session.json"

def save_session(email):
    with open(SESSION_FILE, "w") as file:
        json.dump({"email": email}, file)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as file:
            data = json.load(file)
            return data.get("email")
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def signup():
    signup_window = Toplevel()
    signup_window.geometry("300x250")
    signup_window.title("Sign Up")

    Label(signup_window, text="Email:").grid(row=0, column=0, padx=10, pady=10)
    email_entry = Entry(signup_window)
    email_entry.grid(row=0, column=1)

    Label(signup_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = Entry(signup_window, show="*")
    password_entry.grid(row=1, column=1)

    def create_account():
        email = email_entry.get()
        password = hash_password(password_entry.get())
        try:
            cursor.execute("INSERT INTO Users (EmailId, Password) VALUES (:1, :2)", (email, password))
            con.commit()
            messagebox.showinfo("Success", "Account created successfully")
            signup_window.destroy()
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", str(e))
    
    Button(signup_window, text="Sign Up", command=create_account).grid(row=2, column=1, pady=10)

def login():
    login_window = Toplevel()
    login_window.geometry("300x250")
    login_window.title("Login")

    Label(login_window, text="Email:").grid(row=0, column=0, padx=10, pady=10)
    email_entry = Entry(login_window)
    email_entry.grid(row=0, column=1)

    Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    def authenticate():
        email = email_entry.get()
        password = password_entry.get()
        cursor.execute("SELECT Password FROM Users WHERE EmailId = :1", (email,))
        record = cursor.fetchone()
        if record and check_password(record[0], password):
            save_session(email)
            login_window.destroy()
            todoList(email)
        else:
            messagebox.showerror("Error", "Invalid email or password")

    Button(login_window, text="Login", command=authenticate).grid(row=2, column=1, pady=10)

def logout():
    clear_session()
    messagebox.showinfo("Logout", "You have been logged out.")

def todoList(email):
    root = Tk()
    root.geometry("800x620")
    root.resizable(0, 0)
    root.title("TO DO LIST")

    heading1 = Label(root, text='TODO LIST', font=('ALGERIAN', 30, 'bold'), bg='purple', fg='gold', bd=12, relief='groove')
    heading1.pack(fill=X)
    heading2 = Label(root, text=f'WELCOME {email}', font=('ALGERIAN', 20, 'bold'), bg='white', fg='purple')
    heading2.pack(fill=X)

    frame1 = LabelFrame(root, bg='deep pink', bd=5, relief='groove')
    frame1.pack(fill=X)

    name = Label(frame1, text='Task Name', font=('Times New Roman', 10, 'bold'), bg='white', fg='Red')
    name.grid(row=0, column=2, padx=5, pady=10)
    nameEntry = Entry(frame1, width=30, font=('Times New Roman', 10, 'bold'), bd=5, bg='white', fg='black')
    nameEntry.grid(row=0, column=3, padx=10, pady=10)

    date = Label(frame1, text='Date', font=('Times New Roman', 10, 'bold'), bg='white', fg='red')
    date.grid(row=1, column=2, padx=5, pady=10)
    dateEntry = DateEntry(frame1, width=30, font=('Times New Roman', 10, 'bold'), bd=5, bg='white', fg='black', date_pattern='yyyy-mm-dd', mindate=datetime.now().date())
    dateEntry.grid(row=1, column=3, padx=10, pady=10)

    time = Label(frame1, text='Time', font=('Times New Roman', 10, 'bold'), bg='white', fg='red')
    time.grid(row=2, column=2, padx=5, pady=10)
    timeEntry = Entry(frame1, width=30, font=('Times New Roman', 10, 'bold'), bd=5, bg='white', fg='black')
    timeEntry.grid(row=2, column=3, padx=10, pady=10)

    searchLabel = Label(frame1, text='Search Task', font=('Times New Roman', 10, 'bold'), bg='white', fg='Red')
    searchLabel.grid(row=3, column=2, padx=5, pady=10)
    searchEntry = Entry(frame1, width=30, font=('Times New Roman', 10, 'bold'), bd=5, bg='white', fg='black')
    searchEntry.grid(row=3, column=3, padx=10, pady=10)

    def validate_time(event):
        try:
            task_time = datetime.strptime(timeEntry.get(), "%H:%M").time()
            task_datetime = datetime.combine(dateEntry.get_date(), task_time)
            if task_datetime < datetime.now():
                messagebox.showwarning("Invalid Time", "Selected date and time cannot be in the past.")
                timeEntry.delete(0, END)
        except ValueError:
            timeEntry.delete(0, END)

    timeEntry.bind("<FocusOut>", validate_time)

    def add(email):
        cursor.execute("SELECT MAX(TaskNo) FROM TaskTodoList WHERE EmailId = :email", email=email)
        max_task_no = cursor.fetchone()[0]
        if max_task_no is None:
            max_task_no = 0
        task_no = max_task_no + 1
        
        task_name = nameEntry.get()
        task_date = dateEntry.get_date()
        task_time = timeEntry.get()
        
        if not task_name or not task_date or not task_time:
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        try:
            task_datetime = datetime.combine(task_date, datetime.strptime(task_time, "%H:%M").time())
            if task_datetime < datetime.now():
                messagebox.showwarning("Invalid Time", "Selected date and time cannot be in the past.")
                return
            
            cursor.execute("""
                INSERT INTO TaskTodoList (EmailId, TaskNo, TaskName, TaskDate, TaskTime) 
                VALUES (:1, :2, :3, :4, :5)
            """, (email, task_no, task_name, task_date, task_time))
            con.commit()
            
            tree.insert('', 'end', values=(task_no, task_name, task_date, task_time))
            messagebox.showinfo("Success", "Task added successfully")
            
            nameEntry.delete(0, END)
            dateEntry.set_date(datetime.now().date())
            timeEntry.delete(0, END)
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid date or time format.")

    def load_tasks():
        for i in tree.get_children():
            tree.delete(i)
        cursor.execute("SELECT TaskNo, TaskName, TaskDate, TaskTime FROM TaskTodoList WHERE emailid=:u ORDER BY TaskNo ASC", u=email)
        records = cursor.fetchall()
        
        for i, r in enumerate(records):
            tree.insert('', i, text="", values=(r[0], r[1], r[2], r[3]))

    def search_tasks():
        search_term = searchEntry.get()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a task name to search.")
            return
        for i in tree.get_children():
            tree.delete(i)
        cursor.execute("SELECT TaskNo, TaskName, TaskDate, TaskTime FROM TaskTodoList WHERE emailid=:u AND TaskName LIKE :1", {'u': email, '1': f'%{search_term}%'})
        records = cursor.fetchall()
        
        for i, r in enumerate(records):
            tree.insert('', i, text="", values=(r[0], r[1], r[2], r[3]))

    def show_all_tasks():
        searchEntry.delete(0, END)
        load_tasks()

    def delete_task():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "No task selected")
            return
        
        task_no = tree.item(selected_item, 'values')[0]
        
        cursor.execute("DELETE FROM TaskTodoList WHERE TaskNo = :1 AND emailid = :2", (task_no, email))
        con.commit()
        
        cursor.execute("SELECT TaskNo FROM TaskTodoList WHERE emailid = :1 ORDER BY TaskNo ASC", (email,))
        records = cursor.fetchall()
        new_task_numbers = list(range(1, len(records) + 1))
        
        for new_task_no, (old_task_no,) in enumerate(records, start=1):
            if new_task_no != old_task_no:
                cursor.execute("UPDATE TaskTodoList SET TaskNo = :1 WHERE TaskNo = :2 AND emailid = :3", (new_task_no, old_task_no, email))
        
        con.commit()
        
        load_tasks()
        messagebox.showinfo("Success", "Task deleted successfully")

    def update_task():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "No task selected")
            return

        task_no, task_name, task_date, task_time = tree.item(selected_item, 'values')
        
        popup = Toplevel(root)
        popup.geometry("400x200")
        popup.title("Update Task")
        popup.configure(bg="light pink")
        
        Label(popup, text="Task Name").grid(row=0, column=0)
        name_entry = Entry(popup)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        name_entry.insert(0, task_name)
        
        Label(popup, text="Date").grid(row=1, column=0)
        date_entry = DateEntry(popup, date_pattern='yyyy-mm-dd', mindate=datetime.now().date())
        date_entry.grid(row=1, column=1, padx=10, pady=10)
        date_entry.set_date(task_date)
        
        Label(popup, text="Time").grid(row=2, column=0)
        time_entry = Entry(popup)
        time_entry.grid(row=2, column=1, padx=10, pady=10)
        time_entry.insert(0, task_time)
        
        def save_changes():
            new_name = name_entry.get()
            new_date = date_entry.get_date()
            new_time = time_entry.get()
            new_datetime = datetime.combine(new_date, datetime.strptime(new_time, "%H:%M").time())
            
            if new_datetime < datetime.now():
                messagebox.showwarning("Invalid Time", "Selected date and time cannot be in the past.")
                return
            
            cursor.execute("""
                UPDATE TaskTodoList 
                SET TaskName = :1, TaskDate = :2, TaskTime = :3 
                WHERE TaskNo = :4 AND emailid = :5
            """, (new_name, new_date, new_time, task_no, email))
            con.commit()
            
            tree.item(selected_item, values=(task_no, new_name, new_date, new_time))
            popup.destroy()
        
        Button(popup, text="Save", command=save_changes).grid(row=3, column=1)

    tree = ttk.Treeview(root)
    tree['show'] = 'headings'
    
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", font=('Helvetica', 11))
    s.configure("Treeview.Heading", foreground='red', font=('Helvetica', 11, 'bold'))
    
    tree["columns"] = ("Task No.", "Task Name", "Date", "Time")
    tree.column("Task No.", width=100, minwidth=100, anchor=tk.CENTER)
    tree.column("Task Name", width=300, minwidth=300, anchor=tk.CENTER)
    tree.column("Date", width=200, minwidth=100, anchor=tk.CENTER)
    tree.column("Time", width=100, minwidth=100, anchor=tk.CENTER)
    
    tree.heading("Task No.", text="Task No.", anchor=tk.CENTER)
    tree.heading("Task Name", text="Task Name", anchor=tk.CENTER)
    tree.heading("Date", text="Date", anchor=tk.CENTER)
    tree.heading("Time", text="Time", anchor=tk.CENTER)

    load_tasks()
    tree.pack()

    searchButton = Button(frame1, text="SEARCH", bd=3, bg='yellow', activebackground='black', cursor='hand2', font=('cylburn', 10, 'bold'), fg='black', activeforeground='darkgoldenrod', command=search_tasks)
    searchButton.grid(row=3, column=1, padx=5, pady=10)
    
    showAllButton = Button(frame1, text="SHOW ALL", bd=3, bg='yellow', activebackground='black', cursor='hand2', font=('cylburn', 10, 'bold'), fg='black', activeforeground='darkgoldenrod', command=show_all_tasks)
    showAllButton.grid(row=4, column=3, padx=5, pady=10)
    
    addButton = Button(frame1, text="ADD", bd=3, bg='yellow', activebackground='black', cursor='hand2', font=('cylburn', 10, 'bold'), fg='black', activeforeground='darkgoldenrod', command=lambda: add(email))
    addButton.grid(row=0, column=1, padx=3, pady=10)
    
    updateButton = Button(frame1, text="UPDATE", bd=3, bg='yellow', activebackground='black', cursor='hand2', font=('cylburn', 10, 'bold'), fg='black', activeforeground='darkgoldenrod', command=update_task)
    updateButton.grid(row=1, column=1, padx=3, pady=10)
    
    deleteButton = Button(frame1, text="DELETE", bd=3, bg='yellow', activebackground='black', cursor='hand2', font=('cylburn', 10, 'bold'), fg='black', activeforeground='darkgoldenrod', command=delete_task)
    deleteButton.grid(row=2, column=1, padx=3, pady=10)
    
    Button(root, text="Logout", bd=3, bg='red', activebackground='black', cursor='hand2', font=('cylburn', 10, 'bold'), fg='white', activeforeground='darkgoldenrod', command=lambda: (logout(), root.destroy())).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    email = load_session()
    if email:
        todoList(email)
    else:
        main_window = Tk()
        main_window.geometry("300x200")
        main_window.title("Welcome")

        Button(main_window, text="Sign Up", command=signup).pack(pady=10)
        Button(main_window, text="Login", command=login).pack(pady=10)

        main_window.mainloop()
