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
## if window has size 360 x 800, canvas has size W=360-2x2 (pix right, and left)
## and H=800-2x2
## plus a 30 px header above
## a label is 20 px height
        self.master.resizable(False, False)
##        tk.Label(self.master, text = "non-resizable").pack()

        self.create_widgets()
        self.pil_image = None
        self.image_point = None  # Store the last valid image point
##
        self.image_top = None
        self.item_top = None

    def create_widgets(self):
## The following line adds a 20 height label as a header
        self.label_image_pixel = tk.Label(self, text="(--, --)")  # Initialize label
##        self.label_image_pixel.pack()
        # Canvas
        self.canvas = tk.Canvas(self.master, background="grey75")
        self.canvas.pack(expand=True,  fill=tk.BOTH)
#        self.canvas = tk.Canvas(self)  # Add a canvas to be able to bind to it
#        self.canvas.pack()
        self.canvas.bind("<Motion>", self.handle_mouse_motion)  # Bind to mouse motion
##
        self.master.bind("<Button-1>", self.mouse_down_left)                   # MouseDown
        self.master.bind("<B1-Motion>", self.mouse_move_left)                  # MouseDrag
##        self.master.bind("<Motion>", self.mouse_move)                          # MouseMove
##       self.master.bind("<Double-Button-1>", self.mouse_double_click_left)    # MouseDoubleClick
        self.master.bind("<MouseWheel>", self.mouse_wheel)                     # MouseWheel


    def to_image_point(self, x, y):
        if self.pil_image is not None:
            width, height = self.pil_image.size
            if 0 <= x < width and 0 <= y < height:
                return (x, y)  # Or your converted image coordinates
            else:
                return None
        else:
            return None

    def load_image(self, filepath):
        try:
            self.master.iconbitmap("simple2.ico")
#            self.pil_image = Image.open(filepath)
            self.pil_image = Image.open(filepath)
            self.tk_image = ImageTk.PhotoImage(self.pil_image)  # Make it Tk-compatible
#
##            self.canvas.create_image(0, 100, anchor=tk.NW, image=self.tk_image) #Display on canvas
##            self.canvas.config(width=self.pil_image.width, height=self.pil_image.height) #Set canvas size
            print("in load image",self.pil_image.width,self.pil_image.height)
            print("in load image",self.tk_image.width,self.tk_image.height)
#
            self.zoom_fit(self.pil_image.width, self.pil_image.height)
            self.draw_image(self.pil_image)

        except FileNotFoundError:
            print(f"Error: Image file not found at {filepath}")
        except Exception as e:
            print(f"Error loading image: {e}")
#        except Exception as e2:
#            print(f"Error setting window icon: {e2}")

    def load_pointer(self, MyCanvas):

        # ============
        # ====== adds a pointer
        root.update_idletasks()  # Make sure the window is fully rendered
        ##pil_image.width,self.pil_image.height)
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        print( window_width, window_height )

        # center coordinates
        c_x=window_width*0.5
        c_y=window_height*0.5
        print( c_x , c_y )

        # Load the image
        self.image_top = ImageTk.PhotoImage(Image.open("D:\DATA\_Newfolder\ouitoo\pointer.png"))
        photo_width = self.image_top.width()
        photo_height = self.image_top.height()

        ### Make the root window transparent
        ##root.wm_attributes('-transparentcolor', 'red')

        self.item_top = MyCanvas.create_image(
        c_x, c_y,
        anchor='nw',
        image=self.image_top
        )

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

    def scale_at(self, scale:float, cx:float, cy:float):
        self.translate(-cx, -cy)
        self.scale(scale)
        self.translate(cx, cy)

    def rotate(self, deg:float):
        mat = np.eye(3) # 単位行列
        mat[0, 0] = math.cos(math.pi * deg / 180)
        mat[1, 0] = math.sin(math.pi * deg / 180)
        mat[0, 1] = -mat[1, 0]
        mat[1, 1] = mat[0, 0]

        self.mat_affine = np.dot(mat, self.mat_affine)

    def rotate_at(self, deg:float, cx:float, cy:float):
        self.translate(-cx, -cy)
        self.rotate(deg)
        self.translate(cx, cy)
## ================

    def zoom_fit(self, image_width, image_height):

##        canvas_width = self.canvas.winfo_width()
##        canvas_height = self.canvas.winfo_height()
        canvas_width = self.master.winfo_width()
        canvas_height = self.master.winfo_height()
##      Q&D fix
##        canvas_width = 360
##        canvas_height = 800


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
        print("in zoom_fit, factor to zoom 100% is:",1/scale,math.log(1/scale)/math.log(1.25))

        self.scale(scale)
        self.translate(offsetx, offsety)

    def draw_image(self, pil_image):
        if pil_image == None:
            return

        self.pil_image = pil_image
        Mywidth, Myheight = self.pil_image.size
        print("in draw image",Mywidth,Myheight)

##        canvas_width = self.canvas.winfo_width()
##        canvas_height = self.canvas.winfo_height()
        canvas_width = self.master.winfo_width()
        canvas_height = self.master.winfo_height()

        mat_inv = np.linalg.inv(self.mat_affine)

        # numpy array
        affine_inv = (
            mat_inv[0, 0], mat_inv[0, 1], mat_inv[0, 2],
            mat_inv[1, 0], mat_inv[1, 1], mat_inv[1, 2]
            )

        # PIL
        dst = self.pil_image.transform(
                    (canvas_width, canvas_height),
                    Image.AFFINE,
                    affine_inv,
                    Image.NEAREST
                    )

##        # PIL
##        dst = self.pil_image.transform(
##                    (360, 800),
##                    Image.AFFINE,
##                    affine_inv,
##                    Image.NEAREST
##                    )

        im = ImageTk.PhotoImage(image=dst)
        print("in draw image",self.pil_image.width,self.pil_image.height)
        #
#            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image) #Display on canvas
#            self.canvas.config(width=self.pil_image.width, height=self.pil_image.height) #Set canvas size
        item = self.canvas.create_image(
                0, 0,
                anchor='nw',
                image=im
                )
##
##
        self.load_pointer(self.canvas)
##
##
        self.image = im

    def redraw_image(self):
        if self.pil_image == None:
            return
        self.draw_image(self.pil_image)

    # -------------------------------------------------------------------------------
    # mice events
    # -------------------------------------------------------------------------------
    def mouse_down_left(self, event):
        self.__old_event = event

    def mouse_move_left(self, event):
        if (self.pil_image == None):
            return
        self.translate(event.x - self.__old_event.x, event.y - self.__old_event.y)
        self.redraw_image()
        self.__old_event = event

##    def mouse_move(self, event):
##        if (self.pil_image == None):
##            return
##
##        image_point = self.to_image_point(event.x, event.y)
##        if image_point != []:
##            self.label_image_pixel["text"] = (f"({image_point[0]:.2f}, {image_point[1]:.2f})")
##        else:
##            self.label_image_pixel["text"] = ("(--, --)")

    def handle_mouse_motion(self, event):
        image_point = self.to_image_point(event.x, event.y)
        if image_point is not None:
            self.image_point = image_point
            self.label_image_pixel["text"] = (f"({image_point[0]:.2f}, {image_point[1]:.2f})")
        elif self.image_point is not None:
            self.label_image_pixel["text"] = (f"({self.image_point[0]:.2f}, {self.image_point[1]:.2f})")
        else:
            self.label_image_pixel["text"] = ("(--, --)")  # Keep the "out of bounds" message

##    def mouse_double_click_left(self, event):
##        if self.pil_image == None:
##            return
##        self.zoom_fit(self.pil_image.width, self.pil_image.height)
##        self.redraw_image()

    def mouse_wheel(self, event):
        if self.pil_image == None:
            return

## event.state enforced to block the image rotating shift+MouseWheel
        event.state=10
        if event.state != 9:
            if (event.delta < 0):
                self.scale_at(1.25, event.x, event.y)
            else:
                self.scale_at(0.8, event.x, event.y)
        else:
            if (event.delta < 0):
                self.rotate_at(-5, event.x, event.y)
            else:
                self.rotate_at(5, event.x, event.y)
        self.redraw_image()

root = tk.Tk()
app = Application(master=root)

# ***REPLACE THIS WITH THE ACTUAL PATH TO YOUR IMAGE FILE***
# image_path = "path/to/your/image.jpg"  # Example: "images/my_image.png"
image_path = "union-plaza-ocad-4000-04-09-2021.png"  # Example: "images/my_image.png"
##image_path = "pointer.png"  # Example: "images/my_image.png"
app.load_image(image_path)

root.mainloop()