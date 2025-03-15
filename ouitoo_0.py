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
import time
import threading
import random
import csv # this for API_GPS simulation




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
        self.master.geometry(WWGeometry)
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
        self.mapname=None

        self.northdir=None
        self.rotateat_ang=0.0
        self.rotateat_ang_prev=0.0

        self.Plot_Pos = []
        self.plotlabel = None
        self.START_TIME = 0
        self.image_objects = []


## button demo
        self.button_demo_image = None
        self.button_id_demo = None

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
            global main_canvas, entry1, entry2, entry3, entry4
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
            elif self.count==7:
                self.count += 1
                print(self.count)
                handle_input_main(self.count)
            elif self.count==8:
                self.count += 1
                print(self.count)
                handle_input_main(self.count)

            if self.count > 9: # Exit condition
                root.destroy()  # Close the window
                return

        def handle_input_main(Myvar):
            global main_canvas, return_button, pointer_button, entry1, content1, entry2, entry3, entry4
            global mapname, datamap
            global LAT_REF,LONG_REF,LAT_PT2,LONG_PT2,DISTANCE,SCALE,ROTATION_ANGLE,NORTH_MODE, MAP_NAME

            print(" in handle_input_main ")
            self.count=Myvar
            print(self.count)
            print("main",self.count)
            j=self.count
            smiley_icon = Image.open("D:\DATA\_Newfolder\ouitoo\.icons\happy.png")
            pointer_icon = Image.open("D:\DATA\_Newfolder\ouitoo\.icons\pointer.png")
            northmag_icon = Image.open("D:\DATA\_Newfolder\ouitoo\.icons\Mag.png")
            polaris_icon = Image.open("D:\DATA\_Newfolder\ouitoo\.icons\polaris.png")

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
                return_button = tk.Button(self.canvas, image=return_button_icon, command = lambda i=j: handle_input(i))
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=250, y=0)

            elif self.count==2:

                self.popup_menu.destroy()
                self.load_image(mapname)
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
                main_canvas = tk.Canvas(self.canvas, width=250, height=300, bg="blue")
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
                return_button = tk.Button(self.canvas, image=return_button_icon, command = lambda i=j: handle_input(i))
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

                j=self.count
                resize_smiley = smiley_icon.resize((100, 100))
                return_button_icon = ImageTk.PhotoImage(resize_smiley)
                return_button = tk.Button(self.canvas, image=return_button_icon, command = lambda i=j: handle_input(i))
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=250, y=0)

##                resize_pointer = pointer_icon.resize((100, 100))
                pointer_button_icon = ImageTk.PhotoImage(pointer_icon)

                # Create a pointer canvas
##                pointer_button_canvas = tk.Canvas(self.canvas, width=pointer_button_icon.width(), height=pointer_button_icon.height(), bg=root['bg'], highlightthickness=0)
##                pointer_button_canvas.pack()
                self.pointer_icon = self.canvas.create_image(WWWidth/2.0, WWHeight/2.0, image=pointer_button_icon, anchor=tk.NW)
                self.canvas.image = pointer_button_icon # Keep a reference to prevent garbage collection
                self.canvas.tag_raise(self.pointer_icon)

            elif self.count==4:

                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None
                if self.canvas.image: # Destroy previous button
                    self.canvas.delete(self.pointer_icon)

                j=self.count
                # Main canvas
                main_canvas = tk.Canvas(self.canvas, width=250, height=140, bg="blue")
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
                return_button = tk.Button(self.canvas, text="enter", image=return_button_icon, command = lambda i=j: handle_input(i))
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=275, y=0)

            elif self.count==5:

                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None

                j=self.count
                resize_smiley = smiley_icon.resize((100, 100))
                return_button_icon = ImageTk.PhotoImage(resize_smiley)
                return_button = tk.Button(self.canvas, image=return_button_icon, command = lambda i=j: handle_input(i))
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=250, y=0)

                pointer_button_icon = ImageTk.PhotoImage(pointer_icon)
                self.pointer_icon = self.canvas.create_image(WWWidth/2.0, WWHeight/2.0, image=pointer_button_icon, anchor=tk.NW)
                self.canvas.image = pointer_button_icon # Keep a reference to prevent garbage collection
                self.canvas.tag_raise(self.pointer_icon)

##                pointer_button = tk.Button(root, image=pointer_button_icon, command = None, borderwidth=0, highlightthickness=0)
##                pointer_button.image = pointer_button_icon
##                pointer_button.place(x=WWWidth/2.0, y=WWHeight/2.0)

            elif self.count==6:

                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None
                if self.canvas.image: # Destroy previous button
                    self.canvas.delete(self.pointer_icon)

                j=self.count
                # Main canvas
                main_canvas = tk.Canvas(self.canvas, width=260, height=260, bg="blue")
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
                self.northdir = NORTH_MODE

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
                return_button = tk.Button(root, image=return_button_icon, command = lambda i=j: handle_input(i))
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=275, y=0)

            elif self.count==7:

                if main_canvas: # Destroy previous canvas
                    main_canvas.destroy()
                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None

            ## check some stuff
            ## gets height: https://www.ngs.noaa.gov/web_services/geoid.shtml
            ## https://geodesy.noaa.gov/api/geoid/ght?lat=40.0&lon=W0800000.0 ## <- crucial call
            ## gets UTM: https://www.ngs.noaa.gov/api/ncat/llh?lat=40.0&lon=-80.0&inDatum=nad83(1986)&outDatum=nad83(2011)&utmZone=16 <-- call
            ## info: https://www.ngs.noaa.gov/web_services/ncat/lat-long-height-service.shtml
##    {
##      "ID": "1741282297895",
##      "nadconVersion": "5.0",
##      "vertconVersion": "3.0",
##      "srcDatum": "NAD83(1986)",
##      "destDatum": "NAD83(2011)",
##      "srcVertDatum": "N/A",
##      "destVertDatum": "N/A",
##      "srcLat": "40.0000000000",
##      "srcLatDms": "N400000.00000",
##      "destLat": "39.9999983008",
##      "destLatDms": "N395959.99388",
##      "deltaLat": "-0.189",
##      "sigLat": "0.000263",
##      "sigLat_m": "0.0081",
##      "srcLon": "-80.0000000000",
##      "srcLonDms": "W0800000.00000",
##      "destLon": "-79.9999976143",
##      "destLonDms": "W0795959.99141",
##      "deltaLon": "0.204",
##      "sigLon": "0.000221",
##      "sigLon_m": "0.0052",
##      "heightUnits": "N/A",
##      "srcEht": "N/A",
##      "destEht": "N/A",
##      "sigEht": "N/A",
##      "srcOrthoht": "N/A",
##      "destOrthoht": "N/A",
##      "sigOrthoht": "N/A",
##      "spcZone": "PA S-3702",
##      "spcNorthing_m": "76,470.391",
##      "spcEasting_m": "407,886.681",
##      "spcNorthing_usft": "250,886.607",
##      "spcEasting_usft": "1,338,208.220",
##      "spcNorthing_ift": "250,887.109",
##      "spcEasting_ift": "1,338,210.896",
##      "spcConvergence": "-01 27 35.22",
##      "spcScaleFactor": "0.99999024",
##      "spcCombinedFactor": "N/A",
##      "utmZone": "UTM Zone 16",
##      "utmNorthing": "4,451,293.265",
##      "utmEasting": "1,097,776.886",
##      "utmConvergence": "04 30 46.22",
##      "utmScaleFactor": "1.00400201",
##      "utmCombinedFactor": "N/A",
##      "x": "N/A",
##      "y": "N/A",
##      "z": "N/A",
##      "usng": "16SBK9777751293"
##    }

##    import requests
##        url = "https://api.example.com/data"
##        response = requests.get(url)
##    if response.status_code == 200:
##        data = response.json()  # If the response is in JSON format
##        # Process the data
##        print(data)
##    else:
##        print(f"Error: {response.status_code}")
##    headers = {"Authorization": "Bearer token"}
##    params = {"query": "example"}
##    response = requests.get(url, headers=headers, params=params)
##
##    data = {"key": "value"}
##    response = requests.post(url, json=data)  # Send data as JSON

## magnetic declination: import pygeomag for the WMM
                magnetic_declination=-2.56

                print("ouitoo detects a fancy setting")
                print("starting over ?")
                starting_over="no"
                # if yes self.count =2

                if (starting_over=="yes"):
                    self.count=2
                    j=self.count
                    # Main canvas
                    main_canvas = tk.Canvas(self.canvas, width=250, height=300, bg="blue")
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
                    return_button = tk.Button(self.canvas, image=return_button_icon, command = lambda i=j: handle_input(i))
                    return_button.image = return_button_icon
                    return_button.pack()
                    return_button.place(x=250, y=0)
                else:
                    print("starting over=",starting_over)
                    handle_input(self.count)


            elif self.count==8:

                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None

                print(ROTATION_ANGLE)
                self.My_mouse_wheel(-ROTATION_ANGLE, 180-50 , 400+30 ,"C") # replace by relevant self.X and self.Y ?

                if (NORTH_MODE=='M'):
                    resize_north_icon = northmag_icon.resize((70, 70))
                elif (NORTH_MODE=='P'):
                    resize_north_icon = polaris_icon.resize((70, 70))

                return_button_icon = ImageTk.PhotoImage(resize_north_icon)
                return_button = tk.Button(self.canvas, image=return_button_icon, command = lambda i=j: handle_input(i))
                return_button.image = return_button_icon
                return_button.pack()
                return_button.place(x=275, y=700)

            elif self.count==9:

                if return_button: # Destroy previous button
                    return_button.destroy()
                    entry1 = None
                    entry2 = None
                    entry3 = None
                    entry4 = None

        ## while Ctrl Alt double click on north button, binding while launching north
##                        draw(image) ?
##        rotate plot or ? draw_plot(plot)
##
##                ouitoo_end=0
##                while (ouitoo_end<100):
                    self.trackplotstart=0
                    self.master.after(1000, self.TrackPlot())
##                    ouitoo_end+=1



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
        global mapname, datamap

        mapname=filepath
        # Files usage
        mapfilename =  "./" + dirmap + "/"  + mapname
        filepath=mapfilename
        try:
            self.master.iconbitmap(".icons/simple2.ico")
#            self.pil_image = Image.open(filepath)
            self.pil_image = Image.open(filepath)
            self.tk_image = ImageTk.PhotoImage(self.pil_image)  # Make it Tk-compatible
            # Image size
            self.ImgWidth,self.ImgHeight=self.pil_image.size
            print(f"pil image size: ({self.ImgWidth},{self.ImgHeight})")
            self.ImgWidth,self.ImgHeight=[self.tk_image.width(),self.tk_image.height()]
            print(f"tk image size: ({self.ImgWidth},{self.ImgHeight})")
#
#
            self.zoom_fit(self.pil_image.width, self.pil_image.height)
            self.draw_image(self.pil_image)
##            self.GUI_menus()

        except FileNotFoundError:
            print(f"Error: Image file not found at {filepath}")
        except Exception as e:
            print(f"Error loading image: {e}")
#        except Exception as e2:
#            print(f"Error setting window icon: {e2}")

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
        print(mat[0, 2],mat[1, 2])
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

    def rotate_at(self, deg:float, cx:float, cy:float, flag):
        print("rotate_at(self, deg:float, cx:float, cy:float):", deg, cx, cy)
        self.translate(-cx, -cy)
        self.rotate(deg)
        if flag!="C":
            self.translate(cx, cy)
        else:
            self.translate(180, 400)
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

        print("in zoom_fit",scale,offsetx,offsety)
        print("in zoom_fit, factor to zoom 100% is:",1/scale,math.log(1/scale)/math.log(1.25))

        self.scale(scale)
        self.translate(offsetx, offsety)

# displaying map
#

    def draw_image(self, pil_image):
        global ROTATION_ANGLE

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
            self.X0 = (mat_inv[0, 2]/mat_inv[0,0]+WWWidth/2.0)*mat_inv[0,0]
            self.Y0 = (mat_inv[1, 2]/mat_inv[0,0]+WWHeight/2.0)*mat_inv[0,0]
            print("status: scale",mat_inv[0, 0]," c x: ", self.X0," c y: ", self.Y0)
        elif (self.count<6):
            self.X2 = (mat_inv[0, 2]/mat_inv[0,0]+WWWidth/2.0)*mat_inv[0,0]
            self.Y2 = (mat_inv[1, 2]/mat_inv[0,0]+WWHeight/2.0)*mat_inv[0,0]
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
##        ROTATION_ANGLE=0.0
##        rotated_dst = dst_lanczos.rotate(angle=ROTATION_ANGLE)  # Rotate ROTANG degrees counter-clockwise
        im = ImageTk.PhotoImage(image=dst)
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
        self.canvas.tag_lower(item)
        self.redraw_plot()
##
##
        self.image = im

# ----------------- here ends draw_image()

# displaying plot
#

    def draw_plot(self, class_plot):
        print("displaying plot")

        # Clear previous plots
        if hasattr(self, 'plot_objects') and self.plot_objects:
            for obj_id in self.plot_objects:
                self.canvas.delete(obj_id)
            self.plot_objects = []

        if hasattr(self, 'track_objects') and self.track_objects:
            for track_id in self.track_objects:
                self.canvas.delete(track_id)
            self.track_objects = []

        if self.Plot_Pos == []:
            return

        affine_ = (
            self.mat_affine[0, 0], self.mat_affine[0, 1], self.mat_affine[0, 2],
            self.mat_affine[1, 0], self.mat_affine[1, 1], self.mat_affine[1, 2]
        )

        mat_inv = np.linalg.inv(self.mat_affine)

        affine_inv = (
            mat_inv[0, 0], mat_inv[0, 1], mat_inv[0, 2],
            mat_inv[1, 0], mat_inv[1, 1], mat_inv[1, 2]
        )

        PosMat = np.array(self.Plot_Pos)
        T_Mat = affine_
        TMat = np.array([(T_Mat[0], T_Mat[3]), (T_Mat[1], T_Mat[4])])
        CMat = np.array((T_Mat[2], T_Mat[5]))
        Arr_Pos = np.dot(PosMat, TMat) + CMat
        List_Pos = Arr_Pos.tolist()

        # Store object IDs
        if not hasattr(self, 'plot_objects'):
            self.plot_objects = []

        if not hasattr(self, 'track_objects'):
            self.track_objects = []

##        self.plot_objects.append(self.canvas.create_image(10, 10, image=self.track_icon, anchor="center"))
##        self.plot_objects.append(self.canvas.create_image(50, 50, image=self.track_icon, anchor="center"))
##        self.plot_objects.append(self.canvas.create_image(List_Pos[0][0], List_Pos[0][1], image=self.place_icon, anchor="center"))

        Pos_count = -1
        for Pos in List_Pos:
            Pos_count += 1

        if Pos_count >= 0:
            for i_count in range(Pos_count):
                x_Pos, y_Pos = List_Pos[i_count][0], List_Pos[i_count][1]
                if (i_count==Pos_count-1):
                    self.plot_objects.append(self.canvas.create_image(List_Pos[i_count][0], List_Pos[i_count][1], image=self.place_icon, anchor="center"))
                self.track_objects.append(self.canvas.create_image(x_Pos, y_Pos, anchor=tk.CENTER, image=self.track_icon))

        if self.plot_objects:
            self.canvas.tag_raise(self.plot_objects[-1]) #raise the last plot_object.

        print("plot_objects", self.plot_objects)
        print("track_objects", self.track_objects)

###

    def draw_plot2(self, class_plot):
        print("displaying plot")

        self.image_objects = []

        if self.Plot_Pos == []:
            return
        if self.plotlabel != None:
            print(self.plotlabel)
            self.canvas.delete(self.plotlabel)
            self.plotlabel = None
            return
        if self.image_objects != []:
            self.canvas.delete(self.image_objects)
            self.image_objects = []
            return

##
##        canvas_width = self.master.winfo_width()
##        canvas_height = self.master.winfo_height()

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

        PosMat=np.array(self.Plot_Pos)
        T_Mat=affine_
        TMat=np.array([(T_Mat[0],T_Mat[3]),(T_Mat[1],T_Mat[4])])
        CMat=np.array((T_Mat[2],T_Mat[5]))
        Arr_Pos=np.dot(PosMat,TMat)+CMat
        List_Pos=Arr_Pos.tolist()

##import numpy
##
##Plot_Pos=[(2,3),(2,3),(2,3),(2,3)]
##PosMat=numpy.array(Plot_Pos)
##T_Mat=(1,0.5,1,0.5,1,1)
##TMat=numpy.array([(T_Mat[0],T_Mat[3]),(T_Mat[1],T_Mat[4])])
##CMat=numpy.array((T_Mat[2],T_Mat[5]))
##print(numpy.dot(PosMat,TMat)+CMat)



        print("draw_plot",List_Pos)

##        # PIL
##        dst = self.pil_image.transform(
##                    (canvas_width, canvas_height),
##                    Image.AFFINE,
##                    affine_inv,
##                    Image.NEAREST
##                    )
##
##
##        im = ImageTk.PhotoImage(image=dst)
##
##        item = self.canvas.create_image(
##                0, 0,
##                anchor='nw',
##                image=im
##                )
##        self.canvas.tag_lower(item)



##        LAT_REF=40.81147001
##        LONG_REF=-96.68791604
##        LAT_PT2=40.81908576
##        LONG_PT2=-96.69120128

        self.plotlabel=self.canvas.create_image(10,10, image=self.track_icon, anchor="center")
        print("plotlabel",self.plotlabel)
        self.canvas.image = self.plotlabel # Keep a reference to prevent garbage collection
        self.plotlabel=self.canvas.create_image(50,50, image=self.track_icon, anchor="center")
        print("plotlabel",self.plotlabel)
        self.canvas.image = self.plotlabel # Keep a reference to prevent garbage collection
        self.plotlabel=self.canvas.create_image(List_Pos[0][0],List_Pos[0][1], image=self.place_icon, anchor="center")
        print("plotlabel",self.plotlabel)
        self.canvas.image = self.plotlabel # Keep a reference to prevent garbage collection
        Pos_count=-1
##        image_objects=[]
        for Pos in List_Pos:
            Pos_count+=1
        if Pos_count>=0:
            for i_count in range(Pos_count):
                x_Pos, y_Pos = List_Pos[i_count][0],List_Pos[i_count][1]
                self.image_objects.append(self.canvas.create_image(x_Pos, y_Pos, anchor=tk.CENTER, image=self.track_icon))
        self.canvas.tag_raise(self.plotlabel)
##        self.place_icon
##        self.track_icon
        print("plotlabel",self.plotlabel)


# calling this due to mouse events
#

    def redraw_image(self):
        if self.pil_image == None:
            return
        self.draw_image(self.pil_image)

# calling this due to mouse events
#

    def redraw_plot(self):
        if self.Plot_Pos == []:
            return
        self.draw_plot(self.Plot_Pos)

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
        self.redraw_plot()
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
        self.redraw_plot()

    def My_mouse_wheel(self, rotang, Myevent_x, Myevent_y,flag):
        if self.pil_image == None:
            return
        self.rotate_at(rotang, Myevent_x, Myevent_y, flag)
        self.redraw_image()
        self.redraw_plot()

    def GPS_to_screen(self):
        global LAT_REF,LONG_REF,LAT_PT2,LONG_PT2,DISTANCE,SCALE,ROTATION_ANGLE,NORTH_MODE, MAP_NAME
    ##LONG0=-96.68791604
    ##LAT0=40.81147001
    ##LONG2=-96.69120128
    ##LAT2=40.81908576

        """Function to be executed every second."""
        print("Function executed")
        threading.Timer(1, self.GPS_to_screen).start()
##        TimeVar = time.monotonic()%3

##        current_LAT,current_LONG = self.API_GPS(2)
        current_LAT,current_LONG = self.API_GPS(math.floor((time.monotonic()-self.START_TIME)/3))
        print(math.floor((time.monotonic()-self.START_TIME)/3),current_LAT,current_LONG)

        LONG0=LONG_REF
        LAT0=LAT_REF
        LONG2=LONG_PT2
        LAT2=LAT_PT2

        X0 = self.X0
        Y0 = self.Y0
        X2 = self.X2
        Y2 = self.Y2

        print(X0,Y0,X2,Y2,LONG0,LAT0,LONG2,LAT2)

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
        print(self.Plot_Pos)
        add_this = (float(x_screen), float(y_screen))
        self.Plot_Pos.append(add_this)

## x_xcreen and y_screen refer to the image :: change


    def API_GPS(self,GPS_count):
##Example of track (from start to post #1)
##	latitude (DEC)	longitude (DEC)
##	40.8104943	-96.6891308
##  .../...
##	40.8119565	-96.6880141
##        LAT_REF=40.81147001
##        LONG_REF=-96.68791604
##        LAT_PT2=40.81908576
##        LONG_PT2=-96.69120128

        if self.trackplotstart<1:
            print(self.trackplotstart)
            with open("D:/DATA/_Newfolder/ouitoo/urkytsk_track.csv", 'r') as file:
                csvreader = csv.reader(file)
                self.GPS_dat=list(csvreader)
##                for row in csvreader:
##                    print(row)
        ##        header = next(csvreader)
        ##        print("Header:", header)
##            print(GPS_dat)
            self.trackplotstart=1
##            time.sleep(1333.0)
        print(GPS_count,self.GPS_dat)
        current_LAT = float(np.array(self.GPS_dat)[GPS_count][0])
        current_LONG = float(np.array(self.GPS_dat)[GPS_count][1])
##        GPS_count+=1
        print(current_LAT, current_LONG)
        return current_LAT, current_LONG
#
#
#
#
    def TrackPlot(self):

        print("plotting track")
        print(self.X0, self.Y0, self.X2, self.Y2)
        print("status is:")

        place_pil = Image.open("D:\DATA\_Newfolder\ouitoo\.icons\place.png")
        track_pil = Image.open("D:\DATA\_Newfolder\ouitoo\.icons\mqweorkjfweirkhgfvoerktgworgqerffgfgt245rehy563333.png")
##        place_icon.resize(100,100)
##        track_icon.resize(20,20)
        self.place_icon=ImageTk.PhotoImage(place_pil.resize((100,100)))
        self.track_icon=ImageTk.PhotoImage(track_pil.resize((50,50)))

        self.north(-2.56)

        # Start the function for the first time

##import schedule
##import time
##
##def job():
##    print("I'm running every second...")
##
##schedule.every(1).second.do(job)
##
##while True:
##    schedule.run_pending()
##    time.sleep(1)
        self.START_TIME=time.monotonic()
        self.GPS_to_screen()
        self.draw_plot(self.Plot_Pos)


##        self.master.destroy()
        self.create_transparent_image_button(self.on_button_click)
#
#
#
    def north(self,mag_decl):
        global rotang, button, north_mag_image_pil, north_polaris_image_pil, north_direction_label, north_mag_image, north_polaris_image
##        global LAT_REF,LONG_REF,LAT_PT2,LONG_PT2,DISTANCE,SCALE,ROTATION_ANGLE,NORTH_MODE, MAP_NAME

        def simulate_magnorth_api_call():
            """Simulates an API call and returns magnorth_direction condition."""
##            return random.choice(["M", "P"])
            return random.choice([30 + random.uniform(-5,5)])


        def update_north_direction_and_rotate():
            northdirvar=self.northdir
            print(northdirvar, north_mode)

            if (northdirvar =='M'):
                rotang = simulate_magnorth_api_call()
            else:
                rotang = simulate_magnorth_api_call() - mag_decl

            print(rotang)
            self.rotateat_ang=rotang
            self.My_mouse_wheel(-(self.rotateat_ang-self.rotateat_ang_prev),180,400,"NC") # replace by relevant self.X and self.Y ?
            self.rotateat_ang_prev=self.rotateat_ang

            if self.northdir == "M":
        ##        rotang = 0
                rotated_img_pil = north_mag_image_pil.rotate(rotang)
        ##        button.config(image=north_mag_image)
                resized_img_pil = rotated_img_pil.resize((50, 50))
                rotated_img = ImageTk.PhotoImage(resized_img_pil)

                button.config(image=rotated_img)
                button.place(x=300,y=700)
                button.image = rotated_img
                north_direction_label.config(text="Magnetic North!")
                self.northdir="P"

            elif self.northdir == "P":
        ##        rotang = 180
                rotated_img_pil = north_polaris_image_pil.rotate(rotang)
        ##        button.config(image=north_polaris_image)
                resized_img_pil = rotated_img_pil.resize((50, 50))
                rotated_img = ImageTk.PhotoImage(resized_img_pil)
                button.config(image=rotated_img)
                button.place(x=300,y=700)
                button.image = rotated_img
                north_direction_label.config(text="Polaris!")
                self.northdir="M"


        ##    root.after(500, update_north_direction_and_rotate)

        # Load images

        north_mag_image_pil = Image.open("D:\DATA\_Newfolder\ouitoo\.icons/Mag.png")
        north_polaris_image_pil = Image.open("D:\DATA\_Newfolder\ouitoo\.icons/polaris.png")
        north_mag_image = ImageTk.PhotoImage(north_mag_image_pil)
        north_polaris_image = ImageTk.PhotoImage(north_polaris_image_pil)


##        north_mode = "P"
##        rotation_angle = -4

##        rotation_angle = ROTATION_ANGLE
        rotation_angle = 0.0
        north_mode = NORTH_MODE


        rotang=rotation_angle

        button = tk.Button(
            self.canvas,
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

##        return


###################################################################
# image button demo

    def create_transparent_image_button(self, command):

        pil_image = Image.open("D:\DATA\_Newfolder\ouitoo\sad.png")
        new_width = 20
        new_height = 15
        pil_resized_image = pil_image.resize((new_width, new_height))
        self.button_demo_image = ImageTk.PhotoImage(pil_resized_image)
##        self.button_demo_image = ImageTk.PhotoImage(pil_image)
        self.button_id_demo = self.canvas.create_image(100, 300, image=self.button_demo_image, anchor=tk.NW)
        self.canvas.image = self.button_demo_image # krgc, scope of Tk create_image, not necessary since method ImageTk.PhotoImage() was used
        self.canvas.image = pil_resized_image # krgc, scope of PIL resize, not necessary


        def on_click(event):
            if self.canvas.find_withtag(tk.CURRENT) == (self.button_id_demo,):
                command()

        self.canvas.tag_bind(self.button_id_demo, "<Button-1>", on_click)

        return self.button_id_demo

    ##    create_transparent_image_button(self.on_button_click)

    def on_button_click(self):
        print("Button clicked!, Hey I am sad")
        self.canvas.delete(self.button_id_demo)

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

## work window geometry for PC version
WWWidth=360
WWHeight=800
WWGeometry=str(WWWidth) + 'x' + str(WWHeight)
print("PC version work window: ", WWGeometry)


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

app = Application(master=root)

# ***REPLACE THIS WITH THE ACTUAL PATH TO YOUR IMAGE FILE***
# image_path = "path/to/your/image.jpg"  # Example: "images/my_image.png"
image_path = "photos/union-plaza-ocad-4000-04-09-2021.png"  # Example: "images/my_image.png"
##image_path = "pointer.png"  # Example: "images/my_image.png"
ROTATION_ANGLE=0.0

##app.load_image(image_path) # this has to be changed once mapname can be used instead of image_path
app.GUI_menus()

root.mainloop()
