import tkinter as tk
from PIL import Image, ImageTk  # Install Pillow: pip install Pillow

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.pil_image = None
        self.image_point = None  # Store the last valid image point

    def create_widgets(self):
        self.label_image_pixel = tk.Label(self, text="(--, --)")  # Initialize label
        self.label_image_pixel.pack()
        self.canvas = tk.Canvas(self)  # Add a canvas to be able to bind to it
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.handle_mouse_motion)  # Bind to mouse motion

    def to_image_point(self, x, y):
        if self.pil_image is not None:
            width, height = self.pil_image.size
            if 0 <= x < width and 0 <= y < height:
                return (x, y)  # Or your converted image coordinates
            else:
                return None
        else:
            return None

    def handle_mouse_motion(self, event):
        image_point = self.to_image_point(event.x, event.y)
        if image_point is not None:
            self.image_point = image_point
            self.label_image_pixel["text"] = (f"({image_point[0]:.2f}, {image_point[1]:.2f})")
        elif self.image_point is not None:
            self.label_image_pixel["text"] = (f"({self.image_point[0]:.2f}, {self.image_point[1]:.2f})")
        else:
            self.label_image_pixel["text"] = ("(--, --)")  # Keep the "out of bounds" message

    def load_image(self, filepath):
        try:
#            self.pil_image = Image.open(filepath)
            self.master.iconbitmap("simple.ico")
            self.master.title("ouitoo trackplotter")
            self.pil_image = Image.open("union-plaza-ocad-4000-04-09-2021.png")
            self.tk_image = ImageTk.PhotoImage(self.pil_image)  # Make it Tk-compatible
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image) #Display on canvas
            self.canvas.config(width=self.pil_image.width, height=self.pil_image.height) #Set canvas size
        except FileNotFoundError:
            print(f"Error: Image file not found at {filepath}")
        except Exception as e:
            print(f"Error loading image: {e}")
        except Exception as e2:
            print(f"Error setting window icon: {e2}")


root = tk.Tk()
app = Application(master=root)

# ***REPLACE THIS WITH THE ACTUAL PATH TO YOUR IMAGE FILE***
# image_path = "path/to/your/image.jpg"  # Example: "images/my_image.png"
image_path = "union-plaza-ocad-4000-04-09-2021.png"  # Example: "images/my_image.png"
app.load_image(image_path)

root.mainloop()
