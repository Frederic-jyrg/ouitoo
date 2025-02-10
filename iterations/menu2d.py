import tkinter as tk
from PIL import Image, ImageTk

def handle_input():
    Lat = entry1.get()
    Long = entry2.get()
    print(f"Lat: {Lat}, Long: {Long}")

root = tk.Tk()
root.geometry("360x800")

# Main canvas
main_canvas = tk.Canvas(root, width=250, height=300, bg="blue")
main_canvas.pack()
main_canvas.place(x=50, y=300) # Position at coordinates (50, 50)

# Create labels and entry fields directly on the canvas
main_canvas.create_text(125, 50, text="Latitude pt1, (ref):", font=("Arial", 15) , fill="white")
main_canvas.create_text(125, 150, text="Longitude pt1, (ref):", font=("Arial", 15), fill="white")
entry1 = tk.Entry(main_canvas)
entry2 = tk.Entry(main_canvas)
main_canvas.create_window(125, 100, window=entry1)
main_canvas.create_window(125, 200, window=entry2)

content1 = tk.StringVar()
content2 = tk.StringVar()
content1.set("40.81147001")
content2.set("-96.68791604")
entry1["textvariable"] = content1
entry2["textvariable"] = content2


smiley_icon = Image.open("D:\DATA\_Newfolder\ouitoo\happy.png")
resize_smiley = smiley_icon.resize((100, 100))
return_button_icon = ImageTk.PhotoImage(resize_smiley)
## return_button_icon = tk.PhotoImage(file="happy.png")
return_button = tk.Button(root, text="enter", image=return_button_icon, command=handle_input)
return_button.pack()
return_button.place(x=250, y=0)

root.mainloop()




