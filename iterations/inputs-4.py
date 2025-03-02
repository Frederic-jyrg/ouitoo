import os
import tkinter as tk

##global mapname,entrystep

MyVar = os.environ.get('OS')
if ('win' in MyVar) or ('Win' in MyVar) or ('windows' in MyVar) or ('Windows' in MyVar): print("Windows System")


dirmap = "photos"
dirinput = "inputfiles"

current_dir = os.getcwd()
##print(current_dir)
print(f"Current directory: {current_dir}")

# Change the current working directory
new_dir = "D:\DATA\_Newfolder\ouitoo"  # Replace with the desired path
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

def show_popup(event):
    popup_menu.post(event.x_root, event.y_root)

def name_selection(varname):
    global mapname,entrystep
    mapname=varname
    print(mapname)
    entrystep=2
    contents.set(os.path.splitext(mapname)[0])
    # Tell the entry widget to watch this variable.
    entrythingy["textvariable"] = contents

def print_contents(event):
    global mapname,entrystep
    if (entrystep==1):
        print("Hi. The current entry content is:",
              contents.get())
    elif (entrystep==2):
        print(mapname)
        main(mapname)

def read_data_from_file(filename):
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
##    print(f"Error: File '{filename}' not found.")
    contents.set("Error: File '{filename}' not found.")

    return []
##
def main(varname):
    global mapname

    # Files usage
    ##mapname = "union-plaza-ocad-4000-04-09-2021.PNG"
    inputname = mapname + ".input"
    inputfilename = "./" + dirinput + "/" + inputname
    mapfilename =  "./" + dirmap + "/"  + mapname

    if os.path.isfile(mapfilename):
      try:
        print(f"Map '{mapfilename}' exists")
        print(f"Reading input File '{inputfilename}' ")
        data = read_data_from_file(inputfilename)
      except FileNotFoundError:
        print(f"Error: File '{mapfilename}' not found.")

    if data:
        print("Data read from file:")
        for item in data:
            print(item)
        # Further processing based on data type:
        for item in data:
            try:
              number = float(item)
              print(f"Found a number: {number}")
            except ValueError:
              print(f"Found a non-numeric value: {item}")
        print(data[0])
        print(float(data[0].split(",")[0]),float(data[0].split(",")[1]))
        print(data[1])
        print(float(data[1].split(",")[0]),float(data[1].split(",")[1]))
        print(str(data[5]))
        LAT1=float(data[0].split(",")[0])
        LONG1=float(data[0].split(",")[1])
        LAT2=float(data[1].split(",")[0])
        LONG2=float(data[1].split(",")[1])
        DISTANCE=data[2]
        SCALE=data[3]
        ROTATION_ANGLE=data[4]
        NORTH_MODE=str(data[5])

##
##
##

root = tk.Tk()

popup_menu = tk.Menu(root, tearoff=0)

entrythingy = tk.Entry(root, width=100)
entrythingy.pack()

# Create the application variable.
contents = tk.StringVar()
# Set it to some value.
contents.set("Map Name (right click for list)")
# Tell the entry widget to watch this variable.
entrythingy["textvariable"] = contents

entrystep=1


MyDir = os.path.join(new_dir, dirmap)
print(f"Files in the directory: {MyDir}")
files = os.listdir(MyDir)
print(MyDir)

# Filtering only the files.
##files = [f for f in files if os.path.isfile(MyDir+'/'+f)]
##files = [f for f in os.listdir(MyDir) if f.endswith(".png") or f.endswith(".PNG")]
##print(*files, sep="\n")


# List all files and directories within the 'photos' directory
all_entries = os.listdir(MyDir)

# Filter to keep only files (not directories)
files = [f for f in all_entries if os.path.isfile(os.path.join(MyDir, f))]

# Filter to keep only PNG files
png_files = [f for f in files if f.endswith(".png") or f.endswith(".PNG")]

print(png_files)


# Filtering only the PNG
for x in png_files:
    if (x.endswith(".png") or x.endswith(".PNG")):
##        ext_name=os.path.splitext(x)[1]
        # Prints only text file present in the folder
        base_name=x.split(".")[0]
        print(x)
        popup_menu.add_command(label=base_name, command = lambda item=x: name_selection(item))

##mapname=x
root.bind("<Button-3>", show_popup)
##root.bind("<Button-1>", show_popup)

# Define a callback for when the user hits return.
# It prints the current value of the variable.
entrythingy.bind('<Key-Return>',
                     print_contents)

root.mainloop()

##import os
##print(os.environ)
##
##user_name = os.environ.get('USERDOMAIN')
##print(user_name)
##### or
##user_name = os.environ['WINDIR']
##print(user_name)
##
##api_key = os.environ.get('API_KEY', 'default_api_key')
##print(api_key)
##
##os.environ['NEW_VARIABLE'] = 'new_value'
##print(os.environ['NEW_VARIABLE'])
##
##MyVar = os.environ.get('PROCESSOR_ARCHITECTURE')
##print(MyVar)
##
##MyVar = os.environ.get('PROCESSOR_IDENTIFIER')
##print(MyVar)
##
##MyVar = os.environ.get('OS')
##print(MyVar)
##if ('win' in MyVar) or ('Win' in MyVar) or ('windows' in MyVar) or ('Windows' in MyVar): print("Windows System")


