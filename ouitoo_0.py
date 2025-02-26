## ouitoo trackplotter version for laptop/desktop milestone
##
## Reads a png file representing a terrain
## Orientates to north
## Plots a set of a moving user positions
##
import tkinter as tk
from PIL import Image, ImageTk  # Install Pillow: pip install Pillow
import math
import numpy as np
import os
import functools

############################################################################
# remove this block once load_image() is moved to count==2 step of the GUI menus
PointCyc=True
###############################################################################

## Test for system check
## continuing if Intel architecture

MyVar = os.environ.get('OS')
if ('win' in MyVar) or ('Win' in MyVar) or ('windows' in MyVar) or ('Windows' in MyVar):
    print("Windows System")
    Machine="PC"

if (Machine=="PC"):
    print("continue, no other option")

## Anticipating mobile folders
##

dirmap = "photos"
dirinput = "inputfiles"

tempdir= "D:\DATA\_Newfolder\ouitoo" # Replace with the desired path

##
## Changing working directory

current_dir = os.getcwd()
##print(current_dir)
print(f"Current directory: {current_dir}")

# Change the current working directory
##new_dir = "D:\DATA\_Newfolder\ouitoo"  # Replace with the desired path
## or
new_dir=tempdir
try:
    os.chdir(new_dir)
    print(f"Directory changed to: {os.getcwd()}")
except FileNotFoundError:
    print(f"Error: Directory not found: {new_dir}")
except PermissionError:
    print(f"Error: Permission denied to access: {new_dir}")
except Exception as e:
    print(f"An error occurred: {e}")

##
##
##
##

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

        self.count = 1
        self.X0=None
        self.Y0=None
        self.X2=None
        self.Y2=None
##
##
##
##

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

        self.popup_menu = tk.Menu(self.master, tearoff=0)


## GUI menus
##
##
    def GUI_menus(self):

##        MAP_NAME="my map name"
##        LAT_REF=40.81147001
##        LONG_REF=-96.68791604
##        LAT_PT2=40.81908576
##        LONG_PT2=-96.69120128
##        DISTANCE=890.73
##        SCALE=4000.0
##        ROTATION_ANGLE=4.0
##        NORTH_MODE="P"

        MAP_NAME=None
        LAT_REF=None
        LONG_REF=None
        LAT_PT2=None
        LONG_PT2=None
        DISTANCE=None
        SCALE=None
        ROTATION_ANGLE=None
        NORTH_MODE=None


        self.Set_Inputs()


        def handle_input(Myvar):
            global main_canvas, return_button, entry1, entry2, entry3, entry4
            self.count=Myvar
            if self.count==1:
                MName = entry1.get()
                print(f"Map Name: {MName}")
                self.count += 1
                handle_input_main(self.count)
            elif self.count==2:
                Lat = entry1.get()
                Long = entry2.get()
                print(f"Lat: {Lat}, Long: {Long}")
                self.count += 1
                handle_input_main(self.count)
            elif self.count==3:
                self.count += 1
                handle_input_main(self.count)
            elif self.count==4:
                Lat = entry1.get()
                Long = entry2.get()
                print(f"Lat: {Lat}, Long: {Long}")
                self.count += 1
                handle_input_main(self.count)
            elif self.count==5:
                self.count += 1
                handle_input_main(self.count)
            elif self.count==6:
                d = entry1.get()
                sc = entry2.get()
                ra = entry3.get()
                nm = entry4.get()
                print(f"d: {d}, sc: {sc}, ra: {ra}, nm: {nm}")
                self.count += 1
                print(self.count)
                handle_input_main(self.count)

            if self.count > 7: # Exit condition
                root.destroy()  # Close the window
                return

        def handle_input_main(Myvar):
            global main_canvas, return_button, entry1, content1, entry2, entry3, entry4
            global mapname, datamap, PointCyc
            global LAT_REF,LONG_REF,LAT_PT2,LONG_PT2,DISTANCE,SCALE,ROTATION_ANGLE,NORTH_MODE, MAP_NAME

            PointCyc=True
            print(" in handle_input_main ")
            self.count=Myvar
            print(self.count)
            print("main",self.count)
            j=self.count
            smiley_icon = Image.open("D:\DATA\_Newfolder\ouitoo\.icons\happy.png")

            if self.count==1:

                j=self.count
                # Main canvas
                main_canvas = tk.Canvas(root, width=250, height=300, bg="blue")
                main_canvas.pack()
                main_canvas.place(x=50, y=300)

                # Create labels and entry fields directly on the canvas
                main_canvas.create_text(125, 50, text="Map Name", font=("Arial", 15) , fill="white")
                entry1 = tk.Entry(main_canvas)
                main_canvas.create_window(125, 100, window=entry1)

                MName="Map Name (right click for list)"

                content1 = tk.StringVar()
                content1.set(MName)
                entry1["textvariable"] = content1

                resize_smiley = smiley_icon.resize((100, 100))
                return_button_icon = ImageTk.PhotoImage(resize_smiley)
                return_button = tk.Button(root, text="enter", image=return_button_icon, command = lambda i=j: handle_input(i))
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=250, y=0)

            elif self.count==2:

                self.popup_menu.destroy()

                self.set_map_data(mapname)
                LAT_REF=float(datamap[0].split(",")[0])
                LONG_REF=float(datamap[0].split(",")[1])
                LAT_PT2=float(datamap[1].split(",")[0])
                LONG_PT2=float(datamap[1].split(",")[1])
                DISTANCE=float(datamap[2])
                SCALE=float(datamap[3])
                ROTATION_ANGLE=float(datamap[4])
                NORTH_MODE=str(datamap[5])
                print(LAT_REF,LONG_REF,LAT_PT2,LONG_PT2,DISTANCE,SCALE,ROTATION_ANGLE,NORTH_MODE)

                self.load_pointer(self.canvas, False)

                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None

                j=self.count
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
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=250, y=0)

            elif self.count==3:

                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None
                print(LAT_REF,LONG_REF,LAT_PT2,LONG_PT2,DISTANCE,SCALE,ROTATION_ANGLE,NORTH_MODE)

                self.load_pointer(self.canvas, True)

                j=self.count
                resize_smiley = smiley_icon.resize((100, 100))
                return_button_icon = ImageTk.PhotoImage(resize_smiley)
                return_button = tk.Button(root, text="enter", image=return_button_icon, command = lambda i=j: handle_input(i))
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=250, y=0)

            elif self.count==4:

                self.load_pointer(self.canvas, False)
                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None

                j=self.count
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
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=275, y=0)

            elif self.count==5:

                self.load_pointer(self.canvas, False)
                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None

                self.load_pointer(self.canvas, True)

                j=self.count
                resize_smiley = smiley_icon.resize((100, 100))
                return_button_icon = ImageTk.PhotoImage(resize_smiley)
                return_button = tk.Button(root, text="enter", image=return_button_icon, command = lambda i=j: handle_input(i))
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=250, y=0)

            elif self.count==6:

#   Therefore the pointer becomes useless, the map has been being referenced (including this case)
                self.load_pointer(self.canvas, False)
                PointCyc=False


                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None

                j=self.count
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
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=275, y=0)

            elif self.count==7:

##                self.load_pointer(self.canvas, False)
                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None
                    print(self.X0, self.Y0, self.X2, self.Y2)
##                self.TrackPlot()


        main_canvas = None  # Initialize canvas outside the loop
        return_button = None # Initialize button outside the loop
        entry1 = None
        entry2 = None
        entry3 = None
        entry4 = None
        handle_input_main(self.count)




## inputs
##
    def Set_Inputs(self): ## change all the objects to self.

        def show_popup(event):

##            global count
            if self.count==1:
                self.popup_menu.post(event.x_root, event.y_root)

        def name_selection(varname):
            global mapname,entry1,content1

            mapname=varname
            print("in name selection:", mapname)
            content1.set(os.path.splitext(mapname)[0])
            entry1["textvariable"] = content1


        # Filtering only the PNG
        print("in set_inputs:", png_files)
        for x in png_files:
            if (x.endswith(".png") or x.endswith(".PNG")):
                ext_name=os.path.splitext(x)[1]
                # Prints only text file present in the folder
                base_name=x.split(".")[0]
                print(x)
                self.popup_menu.add_command(label=base_name, command = lambda item=x: name_selection(item))


        root.bind("<Button-3>", show_popup)
        return

# gets data in the companion .input file of the map if existing
#

    def set_map_data(self,varname):
        global mapname, datamap

        mapname=varname
        # Files usage
        inputname = mapname + ".input"
        inputfilename = "./" + dirinput + "/" + inputname
        mapfilename =  "./" + dirmap + "/"  + mapname
        print("in set map", mapname)
        if os.path.isfile(mapfilename):
          try:
            print(f"Map '{mapfilename}' exists")
            print(f"Reading input File '{inputfilename}' ")
            datamap = self.read_data_from_file(inputfilename)
          except FileNotFoundError:
            print(f"Error: File '{mapfilename}' not found.")

        if datamap:
##            print("Data read from file:")
##            for item in datamap:
##                print(item)
            # Further processing based on data type:
            for item in datamap:
                try:
                  number = float(item)
                  print(f"Found a number: {number}")
                except ValueError:
                  print(f"Found a non-numeric value: {item}")
##            print(datamap[0])
##            print(float(datamap[0].split(",")[0]),float(datamap[0].split(",")[1]))
##            print(datamap[1])
##            print(float(datamap[1].split(",")[0]),float(datamap[1].split(",")[1]))
##            print(str(datamap[5]))
##            LAT1=float(datamap[0].split(",")[0])
##            LONG1=float(datamap[0].split(",")[1])
##            LAT2=float(datamap[1].split(",")[0])
##            LONG2=float(datamap[1].split(",")[1])
##            DISTANCE=datamap[2]
##            SCALE=datamap[3]
##            ROTATION_ANGLE=datamap[4]
##            NORTH_MODE=str(datamap[5])


# called by set_map_data()
#
    def read_data_from_file(self,filename):
        """
        Reads data from a file with potentially mixed data types.

        Args:
        filename: The name of the file containing the data.

        Returns:
        A list of data items read from the file.
        """
        try:
            with open(filename, 'r') as file:
                data = []
                lcount=0
                for line in file:
                    lcount+=1
                    line = line.strip()  # Remove leading/trailing whitespace
                    if line:  # Skip empty lines
                        data.append(line)
                print("Lines in file:")
                print(lcount)
            return data
        except FileNotFoundError:
##                    print(f"Error: File '{filename}' not found.")
            contents.set("Error: File '{filename}' not found.")
            # Filter to keep only files (not directories)
            data = ["0,0" for elem in [0,1,2,3,4,5]]
            return data

# picking a position on the image
#

    def to_image_point(self, x, y):
        if self.pil_image is not None:
            width, height = self.pil_image.size
            if 0 <= x < width and 0 <= y < height:
                return (x, y)  # Or your converted image coordinates
            else:
                return None
        else:
            return None

## initial loading from first call
##

    def load_image(self, filepath):
        try:
            self.master.iconbitmap(".icons/simple2.ico")
#            self.pil_image = Image.open(filepath)
            self.pil_image = Image.open(filepath)
            self.tk_image = ImageTk.PhotoImage(self.pil_image)  # Make it Tk-compatible
#
#
            self.zoom_fit(self.pil_image.width, self.pil_image.height)
            self.draw_image(self.pil_image)
            self.GUI_menus()

        except FileNotFoundError:
            print(f"Error: Image file not found at {filepath}")
        except Exception as e:
            print(f"Error loading image: {e}")
#        except Exception as e2:
#            print(f"Error setting window icon: {e2}")

# pointer used as a visual locator to pin the map to the GPS world
#

    def load_pointer(self, MyCanvas, PointerCyc):

        # ============
        # ====== adds a pointer if PointerCyc True

        if (PointerCyc):
            root.update_idletasks()  # Make sure the window is fully rendered
            ##pil_image.width,self.pil_image.height)
            window_width = root.winfo_width()
            window_height = root.winfo_height()

            # center coordinates
            c_x=window_width*0.5
            c_y=window_height*0.5

            # Load the image
            self.image_top = ImageTk.PhotoImage(Image.open("D:\DATA\_Newfolder\ouitoo\.icons\pointer.png"))
            photo_width = self.image_top.width()
            photo_height = self.image_top.height()

            self.item_top = MyCanvas.create_image(
            c_x, c_y,
            anchor='nw',
            image=self.image_top
            )
        else:
            if self.image_top: # Check if it is not None
                MyCanvas.delete(self.item_top) # Delete the item
                self.image_top = None # Reset the image
                self.item_top = None # Reset the item
        # ===============

#
#
#
#
# following: a few functions defined in relation to the mice events
#
#

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
        print(scale)
        self.scale(scale)
        self.translate(cx, cy)

    def rotate(self, deg:float):
        mat = np.eye(3)
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

# initial fitting of the map to the window
#

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

##        print("in zoom_fit",scale,offsetx,offsety)
##        print("in zoom_fit, factor to zoom 100% is:",1/scale,math.log(1/scale)/math.log(1.25))

        self.scale(scale)
        self.translate(offsetx, offsety)

# displaying map
#

    def draw_image(self, pil_image):
        global PointCyc, ROTATION_ANGLE

        if pil_image == None:
            return

        self.pil_image = pil_image
        Mywidth, Myheight = self.pil_image.size


##        canvas_width = self.canvas.winfo_width()
##        canvas_height = self.canvas.winfo_height()
        canvas_width = self.master.winfo_width()
        canvas_height = self.master.winfo_height()

        affine_= (
            self.mat_affine[0, 0], self.mat_affine[0, 1], self.mat_affine[0, 2],
            self.mat_affine[1, 0], self.mat_affine[1, 1], self.mat_affine[1, 2]
            )

        mat_inv = np.linalg.inv(self.mat_affine)

        # numpy array
        affine_inv = (
            mat_inv[0, 0], mat_inv[0, 1], mat_inv[0, 2],
            mat_inv[1, 0], mat_inv[1, 1], mat_inv[1, 2]
            )
        print("draw_image",self.count)
        if (self.count<4):
            self.X0 = mat_inv[0, 2]
            self.Y0 = mat_inv[1, 2]
            print("status: scale",mat_inv[0, 0]," c x: ", self.X0," c y: ", self.Y0)
        elif (self.count<6):
            self.X2 = mat_inv[0, 2]
            self.Y2 = mat_inv[1, 2]
            print("status: scale",mat_inv[0, 0]," c x: ", self.X2," c y: ", self.Y2)

        # PIL
        dst = self.pil_image.transform(
                    (canvas_width, canvas_height),
                    Image.AFFINE,
                    affine_inv,
                    Image.NEAREST
                    )

        dst_lanczos = dst.resize(
            (canvas_width, canvas_height),
            Image.LANCZOS
            )

##        print(ROTATION_ANGLE)
##    if (ROTATION_ANGLE != 0.0):
        rotated_dst = dst_lanczos.rotate(angle=ROTATION_ANGLE)  # Rotate ROTANG degrees counter-clockwise
        im = ImageTk.PhotoImage(image=rotated_dst)
##    else:
##        im = ImageTk.PhotoImage(image=dst)

##        # PIL
##        dst = self.pil_image.transform(
##                    (360, 800),
##                    Image.AFFINE,
##                    affine_inv,
##                    Image.NEAREST
##                    )


        #
#            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image) #Display on canvas
#            self.canvas.config(width=self.pil_image.width, height=self.pil_image.height) #Set canvas size
##        dst.show()
        item = self.canvas.create_image(
                0, 0,
                anchor='nw',
                image=im
                )
##
##
## Called only at GUI step PointCyc == True
##
        self.load_pointer(self.canvas, PointCyc)
##
##
        self.image = im

# ----------------- here ends draw_image()

# calling this due to mouse events
#

    def redraw_image(self):
        if self.pil_image == None:
            return
        self.draw_image(self.pil_image)

#
# -------------------------------------------------------------------------------
# mice events (functions above more than below)
# -------------------------------------------------------------------------------
#


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
                print("event.delta",event.delta)
                self.scale_at(1.25, event.x, event.y)
            else:
                print("event.delta",event.delta)
                self.scale_at(0.8, event.x, event.y)
        else:
            if (event.delta < 0):
                self.rotate_at(-5, event.x, event.y)
            else:
                self.rotate_at(5, event.x, event.y)
        self.redraw_image()

    def GPS_to_screen(self, current_LAT, current_LONG):
        global LAT_REF,LONG_REF,LAT_PT2,LONG_PT2,DISTANCE,SCALE,ROTATION_ANGLE,NORTH_MODE, MAP_NAME
    ##LONG0=-96.68791604
    ##LAT0=40.81147001
    ##LONG2=-96.69120128
    ##LAT2=40.81908576
        LONG0=LONG_REF
        LAT0=LAT_REF
        LONG2=LONG_PT2
        LAT2=LAT_PT2

        self.X0 = 63.84
        self.Y0 = 336.144
        self.X2 = -187.776
        self.Y2 = -460.848

        a_LONG = (X0-X2)/(LONG0-LONG2);
        b_LONG = X0 - a_LONG * LONG0;

        a_LAT = (Y0-Y2)/(LAT0-LAT2);
        b_LAT = Y0 - a_LAT * LAT0;

        x_LONG=current_LONG
        y_LAT=current_LAT


        x_transformed = a_LONG * x_LONG + b_LONG
        y_transformed = a_LAT * y_LAT + b_LAT

        ##// to screen frame of reference
        x_screen = x_transformed
        y_screen = y_transformed
        ##
        ##// Print the transformed point
        print(f"Transformed point: ({x_screen}, {y_screen})")


    def API_GPS(self):
##Example of track (from start to post #1)
##	latitude (DEC)	longitude (DEC)
##	40.8104943	-96.6891308
##	40.8105471	-96.6891375
##	40.8106354	-96.6891563
##	40.8107095	-96.6891643
##	40.8108211	-96.6891563
##	40.8109013	-96.6891295
##	40.8109353	-96.689112
##	40.8109714	-96.6890651
##	40.8109978	-96.688996
##	40.8110181	-96.6889417
##	40.8110348	-96.6888921
##	40.8110516	-96.6887995
##	40.811084	-96.6887311
##	40.81115	-96.6886909
##	40.8112495	-96.6886855
##	40.8112952	-96.688648
##	40.8113652	-96.6885836
##	40.8114363	-96.6885742
##	40.8115206	-96.6886089
##	40.8115663	-96.6886666
##	40.8115947	-96.6887175
##	40.8116739	-96.6887752
##	40.8117195	-96.6887792
##	40.8118134	-96.6887357
##	40.8118992	-96.6887162
##	40.8119438	-96.6886921
##	40.8119926	-96.6886733
##	40.8120332	-96.6886371
##	40.8120474	-96.6885794
##	40.8120403	-96.6884989
##	40.812021	-96.6883997
##	40.8119916	-96.6883313
##	40.8119763	-96.688228
##	40.8119642	-96.6881422
##	40.8119611	-96.6880644
##	40.8119565	-96.6880141
        return current_LAT, current_LONG


    def TrackPlot(self):
        print("plotting track")
        print("status is:")
        ## while double click on north button

## end of class Application()
##

def get_screen_resolution():
    rootin = tk.Tk()
    rootin.withdraw()  # Hide the main window
    screen_width = rootin.winfo_screenwidth()
    screen_height = rootin.winfo_screenheight()
    rootin.destroy()
    return screen_width, screen_height

##
##
##
##

## getting screen resolution with tkinter package
##
print("Screen Resolution:",get_screen_resolution())


## starting tk interface
##

root = tk.Tk()

## getting all images in "current directory"/Photos
##

MyDir = os.path.join(new_dir, dirmap)
##print(f"Files in the directory: {MyDir}")
files = os.listdir(MyDir)
# List all files and directories within the 'photos' directory
all_entries = os.listdir(MyDir)
# Filter to keep only files (not directories)
files = [f for f in all_entries if os.path.isfile(os.path.join(MyDir, f))]
# Filter to keep only PNG files
png_files = [f for f in files if f.endswith(".png") or f.endswith(".PNG")]

### Filtering only the PNG
### Setting popmenu lines
###
##for x in png_files:
##    if (x.endswith(".png") or x.endswith(".PNG")):
####        ext_name=os.path.splitext(x)[1]
##        # Prints only text file present in the folder
##        base_name=x.split(".")[0]
##        print(x)
##        popup_menu.add_command(label=base_name, command = lambda item=x: name_selection(item))

##
##
##
##
# calling and assigning Application()
app = Application(master=root)

# ***REPLACE THIS WITH THE ACTUAL PATH TO YOUR IMAGE FILE***
# image_path = "path/to/your/image.jpg"  # Example: "images/my_image.png"
image_path = "photos/union-plaza-ocad-4000-04-09-2021.png"  # Example: "images/my_image.png"
##image_path = "pointer.png"  # Example: "images/my_image.png"
ROTATION_ANGLE=0.0

app.load_image(image_path) # this has to be changed once mapname can be used instead of image_path

root.mainloop()
