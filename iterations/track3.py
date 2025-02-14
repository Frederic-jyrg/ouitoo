import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("360x800")

canvas = tk.Canvas(root, background="navajo white")
canvas.pack(expand=True, fill=tk.BOTH)

# Store PhotoImage objects in a list to prevent garbage collection
image_refs = []  # <--- This is the crucial change
Nb_points=50

def main():
    for i in range(Nb_points):
        HorCoord = i * 360 / Nb_points
        VertCoord = i * 800 / Nb_points

        try:  # Handle potential file errors
            WidthAndHeight_photo=30
            image = Image.open("D:\DATA\_Newfolder\ouitoo\mqweorkjfweirkhgfvoerktgworgqerffgfgt245rehy563333.png")
            resized_image = image.resize((30, 30))
            photo = ImageTk.PhotoImage(resized_image)


            image_top = Image.open("D:\DATA\_Newfolder\ouitoo\place.png")
            resized_image_top = image_top.resize((100, 100)) # or what size you want
            photo_top = ImageTk.PhotoImage(resized_image_top)

            image_pointer = Image.open("D:\DATA\_Newfolder\ouitoo\pointer.png")
            resized_image_pointer = image_pointer.resize((50, 50)) # or what size you want
            photo_pointer = ImageTk.PhotoImage(resized_image_pointer)

            item = canvas.create_image(
                HorCoord, VertCoord,
                anchor='center',
                image=photo
            )



            if i==Nb_points/2:
                item2 = canvas.create_image(
                    HorCoord, VertCoord, # a little offset
                    anchor='center',
                    image=photo_top
                )
                canvas.itemconfigure(item2, image=photo_top) # This is crucial to show the image
                item3 = canvas.create_image(
                    HorCoord, VertCoord, # a little offset
                    anchor='nw',
                    image=photo_pointer
                )
                canvas.itemconfigure(item3, image=photo_pointer) # This is crucial to show the image

            canvas.itemconfigure(item, image=photo) # This is crucial to show the image

            # Keep references to PhotoImage objects
            image_refs.append(photo) # <--- This is the crucial change
            image_refs.append(photo_top) # <--- This is the crucial change
            image_refs.append(photo_pointer)

        except FileNotFoundError:
            print(f"Error: Image file not found for i = {i}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

root.mainloop()