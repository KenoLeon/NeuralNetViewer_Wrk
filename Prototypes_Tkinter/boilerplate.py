import tkinter as tk


root = tk.Tk()
root.title('HW')

# Screen position, size:

screenRatio = 1.2
screenWidth = root.winfo_screenwidth()
sreenHeight = root.winfo_screenheight()
width = int(screenWidth / screenRatio)
height = int(sreenHeight / screenRatio)
screenX = (screenWidth / 2) - (width / 2)
screenY = (sreenHeight / 2) - (height / 2)
root.geometry('%dx%d+%d+%d' % (width, height, screenX, screenY))
root.configure(background='black')

# Widgets:

w = tk.Label(root, text="Hello Tkinter!")
w.configure(background='black')
w.configure(foreground='white')
w.pack()

# Loop
root.mainloop()
