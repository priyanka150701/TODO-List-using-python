# -*- coding: utf-8 -*-
"""
Created on Sun May  5 03:16:18 2024

@author: nabanita
"""


from tkinter import*
from tkinter import messagebox

from PIL import ImageTk

#Functionality part
''''
def forget_pass():
    def change_password():
        if user_entry.get()==''or newpass_entry.get()=='' or confirmpass_entry.get()=='':
            messagebox.showerror('Error','All Fields Are Requied',parent=window)
        elif newpass_entry.get()!=confirmpass_entry.get():
            messagebox.showerror('Error','Password and confirm password are not matching',parent=window)
  '''        
def username_enter(event):
    if user_entry.get()=='Username':
        user_entry.delete(0,END) 
               
def newpass_enter(event):
    if newpass_entry.get()=='New Password':
        newpass_entry.delete(0,END) 
        
def confirmpass_enter(event):
    if confirmpass_entry.get()=='Confirm Password':
        confirmpass_entry.delete(0,END) 
                
        
window= Tk()#new window top level class
window.geometry("724x408")
window.resizable(0,0)
window.title('Change Password')

#background image on top level window
bgpic = ImageTk.PhotoImage(file='bgResetPswrd.jpg')
bglable=Label(window,image=bgpic)
bglable.grid()
#heading lable 
heading_label=Label(window,text='RESET PASSWORD',font=('arial','18','bold'),bg='white',fg='magenta2')
#heading_label place
heading_label.place(x=250,y=60)
'''

#User Lable window
userLabel=Label(window,text='Username',font=('arial','12','bold'),bg='white',fg='magenta2')
userLabel.place(x=250,y=130)

'''
#User Entry Filed
user_entry=Entry(window,width=25,fg='magenta2',font=('arial',10,'bold'),bd=0)
user_entry.place(x=250,y=120)
user_entry.insert(0,'Username')
user_entry.bind('<FocusIn>',username_enter)

frame1=Frame(window,width=140,height=2,bg='black')



'''
#password Lable window
newpassLabel=Label(window, text='New Password',font=('arial',12,'bold'),bg='white', fg='magenta2')
newpassLabel.place(x=250,y=190)
'''

newpass_entry=Entry(window,width=25,fg='magenta2',font=('arial',10,'bold'),bd=0)
newpass_entry.place(x=250,y=170)
newpass_entry.insert(0,'New Password')
newpass_entry.bind('<FocusIn>',newpass_enter)

frame1=Frame(window,width=190,height=2,bg='black')


'''
#Confirmpassword Label Window
confirmpassLabel =Label(window, text='  ',font=('arial',12,'bold'),bg='white', fg='orchid1')
confirmpassLabel.place(x=250,y=260)
'''
confirmpass_entry=Entry(window, width=25, fg='magenta2',font=('arial',11,'bold'),bd=0)
confirmpass_entry.place(x=250,y=230)
confirmpass_entry.insert(0,'Confirm Password')
confirmpass_entry.bind('<FocusIn>',confirmpass_enter)
frame1=Frame(window,width=240,height=2,bg='black')



loginButton=Button(window,text="Submit",bd=3,bg='darkgoldenrod',activebackground='black',cursor='hand2',font=('cylburn',10,'bold'),fg='black',activeforeground='darkgoldenrod')
loginButton.place(x=250,y=270)


window.mainloop()
 
        

        
       
       
       

