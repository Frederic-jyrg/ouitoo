import tkinter as tk
from PIL import Image, ImageTk
import functools


LAT_REF=40.81147001
LONG_REF=-96.68791604
LAT_PT2=40.81908576
LONG_PT2=-96.69120128
DISTANCE=890.73
SCALE=4000.0
ROTATION_ANGLE=4.0
NORTH_MODE="P"

root = tk.Tk()
root.geometry("360x800")


def handle_input(Myvar):
    global count, main_canvas, return_button, entry1, entry2, entry3, entry4
    count=Myvar
    if count==1:
        Lat = entry1.get()
        Long = entry2.get()
        print(f"Lat: {Lat}, Long: {Long}")
        count += 1
        main(count)
    elif count==2:
        Lat = entry1.get()
        Long = entry2.get()
        print(f"Lat: {Lat}, Long: {Long}")
        count += 1
        main(count)
    elif count==3:
        d = entry1.get()
        sc = entry2.get()
        ra = entry3.get()
        nm = entry4.get()
        print(f"d: {d}, sc: {sc}, ra: {ra}, nm: {nm}")
        count += 1

    if count > 3: # Exit condition
        root.destroy()  # Close the window
        return

def main(Myvar):
    global count, main_canvas, return_button, entry1, entry2, entry3, entry4

    count=Myvar
    print("main",count)
    j=count
    smiley_icon = Image.open("D:\DATA\_Newfolder\ouitoo\happy.png")

    if count==1:

        j=count
        # Main canvas
        main_canvas = tk.Canvas(root, width=250, height=300, bg="blue")
        main_canvas.pack()
        main_canvas.place(x=50, y=300)

        # Create labels and entry fields directly on the canvas
        main_canvas.create_text(125, 50, text="Latitude pt1, (ref):", font=("Arial", 15) , fill="white")
        main_canvas.create_text(125, 150, text="Longitude pt1, (ref):", font=("Arial", 15), fill="white")
        entry1 = tk.Entry(main_canvas)
        entry2 = tk.Entry(main_canvas)
        main_canvas.create_window(125, 100, window=entry1)
        main_canvas.create_window(125, 200, window=entry2)

        LATREF=LAT_REF
        LONGREF=LONG_REF

        content1 = tk.StringVar()
        content2 = tk.StringVar()
        content1.set(LATREF)
        content2.set(LONGREF)
        entry1["textvariable"] = content1
        entry2["textvariable"] = content2

        resize_smiley = smiley_icon.resize((100, 100))
        return_button_icon = ImageTk.PhotoImage(resize_smiley)
        return_button = tk.Button(root, text="enter", image=return_button_icon, command = lambda i=j: handle_input(i))
    ##        return_button = tk.Button(root, text="enter", image=return_button_icon, command=functools.partial(handle_input, count))
    ##        return_button = tk.Button(root, text="enter", image=return_button_icon, command = handle_input)
        return_button.image = return_button_icon
        return_button.pack()
        return_button.place(x=250, y=0)

    elif count==2:

        if main_canvas: # Destroy previous canvas
            main_canvas.destroy()
        if return_button: # Destroy previous button
            return_button.destroy()
        ##    entry1 = None
        ##    entry2 = None
        ##    entry3 = None
        ##    entry4 = None

        j=count
        # Main canvas
        main_canvas = tk.Canvas(root, width=250, height=140, bg="blue")
        main_canvas.pack()
        main_canvas.place(x=50, y=300) # Position at coordinates (50, 50)

        # Create labels and entry fields directly on the canvas
        main_canvas.create_text(125, 20, text="Latitude pt2 (DEC):", font=("Arial", 15) , fill="white")
        main_canvas.create_text(125, 80, text="Longitude pt2 (DEC):", font=("Arial", 15), fill="white")
        entry1 = tk.Entry(main_canvas,font=("Arial", 15))
        entry2 = tk.Entry(main_canvas,font=("Arial", 15))
        main_canvas.create_window(125, 50, window=entry1)
        main_canvas.create_window(125, 110, window=entry2)

        LAT2=LAT_PT2
        LONG2=LONG_PT2

        content1 = tk.StringVar()
        content2 = tk.StringVar()
        content1.set(LAT2)
        content2.set(LONG2)
        entry1["textvariable"] = content1
        entry2["textvariable"] = content2

        resize_smiley = smiley_icon.resize((85, 85))
        return_button_icon = ImageTk.PhotoImage(resize_smiley)
        return_button = tk.Button(root, text="enter", image=return_button_icon, command = lambda i=j: handle_input(i))
    ##    return_button = tk.Button(root, text="enter", image=return_button_icon, command=functools.partial(handle_input, count))
    ##    return_button = tk.Button(root, text="enter", image=return_button_icon, command = handle_input)
        return_button.image = return_button_icon
        return_button.pack()
        return_button.place(x=275, y=0)

    elif count==3:

        if main_canvas: # Destroy previous canvas
            main_canvas.destroy()
        if return_button: # Destroy previous button
            return_button.destroy()
        ##    entry1 = None
        ##    entry2 = None
        ##    entry3 = None
        ##    entry4 = None

        j=count
        # Main canvas
        main_canvas = tk.Canvas(root, width=260, height=260, bg="blue")
        main_canvas.pack()
        main_canvas.place(x=50, y=300) # Position at coordinates (50, 50)

        # Create labels and entry fields directly on the canvas
        main_canvas.create_text(130, 20, text="DISTANCE REF TO pt2 (m):", font=("Arial", 15) , fill="white")
        entry1 = tk.Entry(main_canvas,font=("Arial", 15))
        main_canvas.create_window(130, 50, window=entry1)

        main_canvas.create_text(130, 80, text="SCALE 1/__ ):", font=("Arial", 15), fill="white")
        entry2 = tk.Entry(main_canvas,font=("Arial", 15))
        main_canvas.create_window(125, 110, window=entry2)

        main_canvas.create_text(125, 140, text="ROTATION ANGLE (DEC):", font=("Arial", 15), fill="white")
        entry3 = tk.Entry(main_canvas,font=("Arial", 15))
        main_canvas.create_window(130, 170, window=entry3)

        main_canvas.create_text(130, 200, text="NORTH MODE (P) (M):", font=("Arial", 15), fill="white")
        entry4 = tk.Entry(main_canvas,font=("Arial", 15))
        main_canvas.create_window(130, 230, window=entry4)

        DIST=DISTANCE
        SCAL=SCALE
        ROTANG=ROTATION_ANGLE
        NORTHMOD=NORTH_MODE

        content1 = tk.StringVar()
        content2 = tk.StringVar()
        content3 = tk.StringVar()
        content4 = tk.StringVar()
        content1.set(DIST)
        content2.set(SCAL)
        content3.set(ROTANG)
        content4.set(NORTHMOD)
        entry1["textvariable"] = content1
        entry2["textvariable"] = content2
        entry3["textvariable"] = content3
        entry4["textvariable"] = content4

        resize_smiley = smiley_icon.resize((85, 85))
        return_button_icon = ImageTk.PhotoImage(resize_smiley)
        return_button = tk.Button(root, text="enter", image=return_button_icon, command = lambda i=j: handle_input(i))
    ##    return_button = tk.Button(root, text="enter", image=return_button_icon, command=functools.partial(handle_input, count))
    ##    return_button = tk.Button(root, text="enter", image=return_button_icon, command = handle_input)
        return_button.image = return_button_icon
        return_button.pack()
        return_button.place(x=275, y=0)

count = 1
main_canvas = None  # Initialize canvas outside the loop
return_button = None # Initialize button outside the loop
entry1 = None
entry2 = None
entry3 = None
entry4 = None
main(count)

root.mainloop()


##import tkinter as tk
##
##def my_command():
##    print("Button was clicked!")
##
##def change_command():
##    global button
##    button.config(command=new_command)
##
##def new_command():
##    print("New command executed!")
##
##root = tk.Tk()
##
##button = tk.Button(root, text="Click Me", command=my_command)
##button.pack()
##
##change_button = tk.Button(root, text="Change Command", command=change_command)
##change_button.pack()
##
##root.mainloop()

##import tkinter as tk

##root = tk.Tk()
##
##current_button = None  # Keep track of the current button
##
##def create_button():
##    global current_button  # Access the global variable
##
##    if current_button:  # If a button exists, destroy it
##        current_button.destroy()
##
##    current_button = tk.Button(root, text="New Button")  # Create new button
##    current_button.pack()
##
### Example usage (e.g., in a loop or in response to an event):
##for i in range(5):
##    create_button()
##    root.update() # This will update the window, otherwise you will not see the button change
##    root.after(5000) # This will create a delay of 500ms so you can see the button change
##
##root.mainloop()
