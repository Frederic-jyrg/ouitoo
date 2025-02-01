import tkinter as tk
from PIL import Image, ImageTk  # Install Pillow: pip install Pillow
import math
import numpy as np

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.master.title("ouitoo trackplotter")
        self.master.geometry('360x800')
        self.master.resizable(False, False)
        tk.Label(self.master, text = "non-resizable").pack()

        self.create_widgets()
        self.pil_image = None
        self.image_point = None  # Store the last valid image point


    def create_widgets(self):
        self.label_image_pixel = tk.Label(self, text="(--, --)")  # Initialize label
        self.label_image_pixel.pack()
        # Canvas
        self.canvas = tk.Canvas(self.master, background="black")
        self.canvas.pack(expand=True,  fill=tk.BOTH)
#        self.canvas = tk.Canvas(self)  # Add a canvas to be able to bind to it
#        self.canvas.pack()
        self.canvas.bind("<Motion>", self.handle_mouse_motion)  # Bind to mouse motion
##
#        self.master.bind("<Button-1>", self.mouse_down_left)                   # MouseDown
#        self.master.bind("<B1-Motion>", self.mouse_move_left)                  # MouseDrag（ボタンを押しながら移動）
##        self.master.bind("<Motion>", self.mouse_move)                          # MouseMove
##       self.master.bind("<Double-Button-1>", self.mouse_double_click_left)    # MouseDoubleClick
#        self.master.bind("<MouseWheel>", self.mouse_wheel)                     # MouseWheel


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
            self.master.iconbitmap("simple2.ico")
#            self.pil_image = Image.open(filepath)
            self.pil_image = Image.open(filepath)
            self.tk_image = ImageTk.PhotoImage(self.pil_image)  # Make it Tk-compatible
#
#            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image) #Display on canvas
#            self.canvas.config(width=self.pil_image.width, height=self.pil_image.height) #Set canvas size
            print("in load image",self.pil_image.width,self.pil_image.height)
#
            self.zoom_fit(self.pil_image.width, self.pil_image.height)
            print("zooming")
            self.draw_image(self.pil_image)
#

        except FileNotFoundError:
            print(f"Error: Image file not found at {filepath}")
        except Exception as e:
            print(f"Error loading image: {e}")
#        except Exception as e2:
#            print(f"Error setting window icon: {e2}")
# ===============
    def reset_transform(self):
        self.mat_affine = np.eye(3)

    def translate(self, offset_x, offset_y):
        mat = np.eye(3)
        mat[0, 2] = float(offset_x)
        mat[1, 2] = float(offset_y)

        self.mat_affine = np.dot(mat, self.mat_affine)

    def scale(self, scale:float):
        mat = np.eye(3)
        mat[0, 0] = scale
        mat[1, 1] = scale

        self.mat_affine = np.dot(mat, self.mat_affine)


    def zoom_fit(self, image_width, image_height):

##        canvas_width = self.canvas.winfo_width()
##        canvas_height = self.canvas.winfo_height()
        canvas_width = 360
        canvas_height = 800

        print("in zoom_fit", canvas_width, canvas_height, image_width, image_height)

        if (image_width * image_height <= 0) or (canvas_width * canvas_height <= 0):
            return

        self.reset_transform()

        scale = 1.0
        offsetx = 0.0
        offsety = 0.0

        if (canvas_width * image_height) > (image_width * canvas_height):
            scale = canvas_height / image_height
            offsetx = (canvas_width - image_width * scale) / 2
        else:
            scale = canvas_width / image_width
            offsety = (canvas_height - image_height * scale) / 2

        print("in zoom_fit",scale,offsetx,offsety)

        self.scale(scale)
        self.translate(offsetx, offsety)

    def draw_image(self, pil_image):

        if pil_image == None:
            return

        self.pil_image = pil_image

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        print("in draw_image",canvas_width,canvas_height)

        mat_inv = np.linalg.inv(self.mat_affine)

        # numpy array
        affine_inv = (
            mat_inv[0, 0], mat_inv[0, 1], mat_inv[0, 2],
            mat_inv[1, 0], mat_inv[1, 1], mat_inv[1, 2]
            )

##        # PIL
##        dst = self.pil_image.transform(
##                    (canvas_width, canvas_height),
##                    Image.AFFINE,
##                    affine_inv,
##                    Image.NEAREST
##                    )

        # PIL
        dst = self.pil_image.transform(
                    (360, 800),
                    Image.AFFINE,
                    affine_inv,
                    Image.NEAREST
                    )

        im = ImageTk.PhotoImage(image=dst)

        #
#            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image) #Display on canvas
#            self.canvas.config(width=self.pil_image.width, height=self.pil_image.height) #Set canvas size
        item = self.canvas.create_image(
                0, 0,
                anchor='nw',
                image=im
                )

        self.image = im


root = tk.Tk()
app = Application(master=root)

# ***REPLACE THIS WITH THE ACTUAL PATH TO YOUR IMAGE FILE***
# image_path = "path/to/your/image.jpg"  # Example: "images/my_image.png"
image_path = "union-plaza-ocad-4000-04-09-2021.png"  # Example: "images/my_image.png"
app.load_image(image_path)

root.mainloop()
