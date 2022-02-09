import tkinter as tk
from PIL import Image,ImageTk
#from tkVideoPlayer import TkinterVideo

# Defines
N = 3                                       # Number of images
canvas_width, canvas_height = 1400, 400     # Dimensions of window

# Function for resizing images
def resize_img(img: 'Image') -> 'ImageTk.PhotoImage':
    width, height = img.size
    width //= 5
    height //= 5
    resized_image = img.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized_image)

def display_images(file1: 'str', file2: 'str', file3: 'str'):

    # create top-level widget as main window of application
    root = tk.Tk()      

    # create layout with specified width and height
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)

    # connect canvas to main window
    canvas.pack()      

    # load images from folder
    img1 = Image.open(file1)    
    img2 = Image.open(file2)
    img3 = Image.open(file3)

    # Resize images
    img1 = resize_img(img1)
    img2 = resize_img(img2)
    img3 = resize_img(img3)

    # Image constants
    x0, y0 = 20, 100
    canvas_part = canvas_width // N

    canvas.create_image(x0, y0, anchor='nw', image=img1)      
    canvas.create_image(x0 + canvas_part, y0, anchor='nw', image=img2)
    canvas.create_image(x0 + 2*canvas_part, y0, anchor='nw', image=img2)

    canvas.create_text(220, y0 - 20, text="Input image", fill="black", font=('Helvetica 15 bold'))
    canvas.create_text(220 + canvas_part, y0 - 20, text="Optical flow", fill="black", font=('Helvetica 15 bold'))
    canvas.create_text(220 + 2*canvas_part, y0 - 20, text="Detected elements", fill="black", font=('Helvetica 15 bold'))

    # start the program      
    tk.mainloop()  

display_images('test.png', 'testing.png', 'testing.png')

#Scaling video
#videoplayer = TkinterVideo(master=root, scaled=True, pre_load=False)

#load video from foldeer
#videoplayer.load(r"samplevideo.mp4")
#videoplayer.pack(expand=True, fill="both")

# play the video
#videoplayer.play() 