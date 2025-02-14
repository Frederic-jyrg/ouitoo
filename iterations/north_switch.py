import tkinter as tk
from PIL import Image, ImageTk
import time
import random

## needs to add a rotate transform to fit rotate_angle values

def simulate_api_call():
    """Simulates an API call and returns north_direction condition."""
    return random.choice(["M", "P"])

def update_north_direction_and_rotate():
    global rotate_angle, button, north_mag_image, north_polaris_image, north_direction_label

    north_direction = simulate_api_call()
    if north_direction == "M":
        rotate_angle = 0
        button.config(image=north_mag_image)
        north_direction_label.config(text="Magnetic North!")
    elif north_direction == "P":
        rotate_angle = 180
        button.config(image=north_polaris_image)
        north_direction_label.config(text="Polaris!")

    root.after(500, update_north_direction_and_rotate)

root = tk.Tk()

# Load images
north_mag_image = tk.PhotoImage(file="D:\DATA\_Newfolder\ouitoo\Mag.png")
north_polaris_image = tk.PhotoImage(file="D:\DATA\_Newfolder\ouitoo\polaris.png")

rotate_angle = 0

button = tk.Button(
    root,
    image=north_mag_image,
    compound=tk.CENTER,
    command=None
)
button.pack()

# Create and pack the label with side=TOP and pady=10
north_direction_label = tk.Label(root, text="Loading...")
north_direction_label.pack(side=tk.TOP, pady=10)

update_north_direction_and_rotate()

root.mainloop()