import os
import glob
import time
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image

class ImageViewer(object):
    def __init__(self):

        self.N = 3                          # Number of images
        self.x0, self.y0 = 10, 150          # Coordinates of upper left corner

        self.root = tk.Tk()
        self.root.state('zoomed')
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.canvas_part = self.width // self.N    # Horizontal part taken up by image

        self.main_dir = None
        self.iter = 0
        self.num_files = None
        self.skip_length = 2

        input_img, optflow_img, bbox_img, wh, ht = self.open_file()
        self.canvas = tk.Canvas(self.root, width=wh, height=ht)
        self.canvas.pack()   

        self.image1_on_canvas = self.canvas.create_image(self.x0, self.y0, anchor='nw', image=input_img)
        self.image2_on_canvas = self.canvas.create_image(self.x0 + self.canvas_part, self.y0, anchor='nw', image=optflow_img)
        self.image3_on_canvas = self.canvas.create_image(self.x0 + 2*self.canvas_part, self.y0, anchor='nw', image=bbox_img)

        self.canvas.create_text(240, self.y0 - 20, 
                                text="Input image", 
                                fill="black", font=('Helvetica 17 bold'))

        self.canvas.create_text(240 + self.canvas_part, self.y0 - 20, 
                                text="Optical flow", 
                                fill="black", font=('Helvetica 17 bold'))

        self.canvas.create_text(240 + 2*self.canvas_part, self.y0 - 20, 
                                text="Detected elements", fill="black", font=('Helvetica 17 bold'))

        self.canvas.create_text(self.width//2, self.height//2 + 80, 
                                text="Press the buttons above or arrows for the next and previous image", 
                                fill="black", font=('Helvetica 16 bold'), anchor='center')

        self.skip_text = self.canvas.create_text(self.width//2, self.height//2 + 110, 
                                text="Press space to skip "+str(self.skip_length)+" images", 
                                fill="black", font=('Helvetica 16 bold'), anchor='center')     
                     

        self.canvas.create_text(self.width//2, self.height//2 + 140, 
                                text="Press Q to quit", 
                                fill="black", font=('Helvetica 16 bold'), anchor='center')
        
        self.next = tk.Button(self.root, text='Next image', command=self.next_image)
        self.next.place(relx=0.5, rely=0.6, anchor='center')

        self.prev = tk.Button(self.root, text='Previous image', command=self.prev_image)
        self.prev.place(relx=0.4, rely=0.6, anchor='center')

        self.skip = tk.Button(self.root, text='Skip', command=self.skip_image)
        self.skip.place(relx=0.58, rely=0.6, anchor='center')

        self.skip_input = tk.Text(self.root, height=1, width=5, borderwidth=1, relief="solid")
        self.skip_input.place(relx=0.83, rely=0.6, anchor='center')

        self.skip_input_btn = tk.Button(self.root, text='Change skip-length', command=self.change_skip_length)
        self.skip_input_btn.place(relx=0.83, rely=0.65, anchor='center')

        self.root.bind('<Right>', self.next_image)
        self.root.bind('<Left>', self.prev_image)
        self.root.bind('<space>', self.skip_image)
        self.root.bind('q', self.quit)

        self.root.mainloop()
  
    def open_file(self):

        self.main_dir = filedialog.askdirectory()
        input_file = self.main_dir + "/input_images/input"+str(self.iter)+".png"
        optflow_file = self.main_dir + "/optflow_images/optflow"+str(self.iter)+".png"
        bbox_file = self.main_dir + "/bbox_images/bbox"+str(self.iter)+".png"

        input_files = os.listdir(self.main_dir + "/input_images")
        if '.DS_Store' in input_files:
            input_files.pop(input_files.index('.DS_Store'))
        self.num_files = len(input_files)

        self.input_images = glob.glob(os.path.dirname(input_file) + '/*.png')
        self.optflow_images = glob.glob(os.path.dirname(optflow_file) + '/*.png')
        self.bbox_images = glob.glob(os.path.dirname(bbox_file) + '/*.png')

        self.root.title("Graphical User Interface")

        input_img = Image.open(input_file)
        optflow_img = Image.open(optflow_file)
        bbox_img = Image.open(bbox_file)

        input_img = self.resize_img(input_img)
        optflow_img = self.resize_img(optflow_img)
        bbox_img = self.resize_img(bbox_img)

        return input_img, optflow_img, bbox_img, self.width, self.height

    def next_image(self, event: 'tk.Event' = None):

        if self.iter < self.num_files - 1:
            self.iter += 1

        input_image = self.main_dir + "/input_images/input"+str(self.iter)+".png"
        optflow_image = self.main_dir + "/optflow_images/optflow"+str(self.iter)+".png"
        bbox_image = self.main_dir + "/bbox_images/bbox"+str(self.iter)+".png"
        self.root.title("Graphical User Interface")
        input_img = Image.open(input_image)
        optflow_img = Image.open(optflow_image)
        bbox_img = Image.open(bbox_image)

        input_img = self.resize_img(input_img)
        optflow_img = self.resize_img(optflow_img)
        bbox_img = self.resize_img(bbox_img)

        self.canvas.itemconfigure(self.image1_on_canvas, image=input_img)
        self.canvas.itemconfigure(self.image2_on_canvas, image=optflow_img)
        self.canvas.itemconfigure(self.image3_on_canvas, image=bbox_img)

        self.canvas.config(width=self.width, height=self.height)
        try:
            self.canvas.wait_visibility()
        except tk.TclError:
            pass
    
    def prev_image(self, event: 'tk.Event' = None):
        if self.iter >= 1:
            self.iter -= 2
            self.next_image()
    
    def skip_image(self, event: 'tk.Event' = None):
        if self.num_files > self.iter + self.skip_length:
            self.iter += self.skip_length - 1
            self.next_image()

    def change_skip_length(self):
        if self.skip_input.get("1.0", "end") is not '\n':
            self.skip_length = int(self.skip_input.get("1.0", "end"))
            self.canvas.itemconfig(self.skip_text, 
                                   text="Press space to skip "+str(self.skip_length)+" images")

    def resize_img(self, img: 'Image') -> 'ImageTk.PhotoImage':
        width, height = img.size
        width //= 4.2
        height //= 4.2
        resized_image = img.resize((int(width), int(height)), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)

    def quit(self, event: 'tk.Event' = None):
        self.root.destroy()

ImageViewer()