from tkinter import *
from PIL import ImageTk

root = Tk()

# Create the background image (replace 'bg.jpg' with your image path)
bgImage = ImageTk.PhotoImage(file='bg.jpg')

# Create a label and add the image
bgLabel = Label(root, image=bgImage)

# Position the label at top left corner (using grid)
bgLabel.grid(row=0, column=0)

root.mainloop()
