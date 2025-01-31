import tkinter as tk

root = tk.Tk()
root.title('NNV')

# Screen position, size:

screenRatio = 1.14
screenWidth = root.winfo_screenwidth()
sreenHeight = root.winfo_screenheight()
width = int(screenWidth / screenRatio)
height = int(sreenHeight / screenRatio)
screenX = (screenWidth / 2) - (width / 2)
screenY = (sreenHeight / 2) - (height / 2)
root.geometry('%dx%d+%d+%d' % (width, height, screenX, screenY))
root.configure(background='black')


# Screen split:

sidebar = tk.Frame(root, width=300, bg='#212121', height=500, relief='flat', borderwidth=1, padx =10)
sidebar.pack(expand=False, fill='both', side='right', anchor='nw')

# main content area
mainarea = tk.Frame(root, bg='#101010', width=400, height=500)
mainarea.pack(expand=True, fill='both', side='left')

# Widgets:

def callback():
    print("click!")


# w = tk.Button(sidebar, text="Play", command=callback)
# w.pack(fill=tk.X, pady = 2, padx = 4 )

w = tk.Label(sidebar, text="FPS", background='#2b2b2b', fg="lightgrey")
w.pack(fill=tk.X, pady = 2, padx = 4)
w = tk.Label(sidebar, text="Place Neurons", background='#2b2b2b', fg="lightgrey")
w.pack(fill=tk.X, pady = 2, padx = 4)

# Loop
root.mainloop()
