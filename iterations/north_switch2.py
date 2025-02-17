import tkinter as tk
from PIL import Image, ImageTk
import time
import random


def simulate_api_call():
    """Simulates an API call and returns north_direction condition."""
    return random.choice(["M", "P"])

def update_north_direction_and_rotate():
    global rotang, rotation_angle, button, north_mag_image_pil, north_polaris_image_pil, north_direction_label, north_mode, north_mag_image, north_polaris_image

    north_direction = simulate_api_call()
    print(north_direction, north_mode)

    if (north_direction == north_mode):
        rotang=rotation_angle
    else:
        rotang = random.choice([-15,-10,-5,0,5,10,15])
    print(rotang)
    if north_direction == "M":
##        rotang = 0
        rotated_img_pil = north_mag_image_pil.rotate(rotang)
##        button.config(image=north_mag_image)
        rotated_img = ImageTk.PhotoImage(rotated_img_pil)
        button.config(image=rotated_img)
        button.image = rotated_img
        north_direction_label.config(text="Magnetic North!")

    elif north_direction == "P":
##        rotang = 180
        rotated_img_pil = north_polaris_image_pil.rotate(rotang)
##        button.config(image=north_polaris_image)
        rotated_img = ImageTk.PhotoImage(rotated_img_pil)
        button.config(image=rotated_img)
        button.image = rotated_img
        north_direction_label.config(text="Polaris!")

##    root.after(500, update_north_direction_and_rotate)

root = tk.Tk()

# Load images

north_mag_image_pil = Image.open("D:\DATA\_Newfolder\ouitoo\Mag.png")
north_polaris_image_pil = Image.open("D:\DATA\_Newfolder\ouitoo\polaris.png")
north_mag_image = ImageTk.PhotoImage(north_mag_image_pil)
north_polaris_image = ImageTk.PhotoImage(north_polaris_image_pil)


north_mode = "P"
rotation_angle = -4

rotang=rotation_angle

button = tk.Button(
    root,
    image=north_mag_image,
    compound=tk.CENTER,
##    command=None
    command=update_north_direction_and_rotate
)
button.pack()

# Create and pack the label with side=TOP and pady=10
north_direction_label = tk.Label(root, text="Loading...")
north_direction_label.pack(side=tk.TOP, pady=10)

update_north_direction_and_rotate()

root.mainloop()

##from PIL import Image
##
### Open the image
####img = Image.open("D:\DATA\_Newfolder\ouitoo\MagJPEg.jpg")
##
##
### Rotate the image by 45 degrees counterclockwise
##rotated_img = img.rotate(45)
##
### To rotate clockwise, use a negative angle:
### rotated_img = img.rotate(-45)
##
### Save the rotated image
##rotated_img.save("./rotated_MagJPEg.jpg")
##
### Display the rotated image (optional, may require additional setup)
##rotated_img.show()


##def tk_image_to_pil(tk_image):
##    """Converts a Tkinter PhotoImage object to a PIL Image object.
##
##    Args:
##        tk_image: The Tkinter PhotoImage object to convert.
##
##    Returns:
##        A PIL Image object representing the image in the Tkinter PhotoImage.
##    """
##    # Use the "data" attribute to get the image data in base64 format
##    data = tk_image.data
##
##    # Decode the base64 data
##    image_data = base64.b64decode(data)
##
##    # Use BytesIO to handle the image data as a file-like object
##    image_stream = io.BytesIO(image_data)
##
##    # Open the image with PIL
##    pil_image = Image.open(image_stream)
##    return pil_image
##
##if __name__ == '__main__':
##    # Create a Tkinter window
##    root = Tk()
##
##    # Load an image using PhotoImage
##    image_path = "path/to/your/image.png"  # Replace with the actual path to your image
##    tk_image = PhotoImage(file=image_path)
##
##    # Create a Label to display the Tkinter image (optional, for verification)
##    label = Label(root, image=tk_image)
##    label.pack()
##
##    # Convert the Tkinter image to a PIL image
##    pil_image = tk_image_to_pil(tk_image)
##
##    # Display or process the PIL image as needed
##    pil_image.show()  # Example: Display the PIL image
##
##    # Keep the window open until closed manually
##    root.mainloop()

