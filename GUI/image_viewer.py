import os
import glob
import tkinter as tk
from PIL import ImageTk, Image


class ImageViewer(object):
    """
    This class assumes the following folder structure:
    -> data
        -> GUI_images
            -> input_images     : contains input0.png, input1.png, ..., inputn.png
            -> optflow_images   : contains optflow0.png, optflow1.png, ..., optflown.png
            -> bbox_images      : contains bbox0.png, bbox1.png, ..., bboxn.png
    """

    def __init__(self):

        self.image_paths = [
            "/input/",
            "/moving_bbxs/",
            "/classified_bbxs/",
            "/thresholded/",
            "/object_merger/",
        ]

        self.N = len(self.image_paths)  # Number of images
        self.x0, self.y0 = 10, 150  # Coordinates of upper left corner

        self.root = tk.Tk()
        self.root.state("zoomed")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.canvas_part = self.width // self.N  # Horizontal part taken up by image

        self.main_dir = "./data/GUI_images"
        self.iter = 0
        self.num_files = None
        self.skip_length = 2

        images = self.open_file()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.canvas_images = []

        for i, img in enumerate(images):
            self.canvas_images.append(
                self.canvas.create_image(
                    self.x0 + i * self.canvas_part, self.y0, anchor="nw", image=img
                )
            )

        self.canvas.create_text(
            240,
            self.y0 - 20,
            text="Input image",
            fill="black",
            font=("Helvetica 17 bold"),
        )

        self.canvas.create_text(
            240 + self.canvas_part,
            self.y0 - 20,
            text="Optical flow",
            fill="black",
            font=("Helvetica 17 bold"),
        )

        self.canvas.create_text(
            240 + 2 * self.canvas_part,
            self.y0 - 20,
            text="Detected elements",
            fill="black",
            font=("Helvetica 17 bold"),
        )

        self.image_text = self.canvas.create_text(
            self.width // 2 + 5,
            50,
            text="Frame " + str(self.iter + 1),
            fill="black",
            font=("Helvetica 18 bold"),
            anchor="center",
        )

        self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 80,
            text="Press the buttons above or arrows for the next and previous frame",
            fill="black",
            font=("Helvetica 16 bold"),
            anchor="center",
        )

        self.skip_text = self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 110,
            text="Press space to skip " + str(self.skip_length) + " frames",
            fill="black",
            font=("Helvetica 16 bold"),
            anchor="center",
        )

        self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 140,
            text="Press Q to quit",
            fill="black",
            font=("Helvetica 16 bold"),
            anchor="center",
        )

        self.next = tk.Button(self.root, text="Next frame", command=self.next_image)
        self.next.place(relx=0.51, rely=0.6, anchor="center")

        self.prev = tk.Button(self.root, text="Previous frame", command=self.prev_image)
        self.prev.place(relx=0.41, rely=0.6, anchor="center")

        self.skip = tk.Button(self.root, text="Skip", command=self.skip_image)
        self.skip.place(relx=0.59, rely=0.6, anchor="center")

        self.skip_input = tk.Text(
            self.root, height=1, width=5, borderwidth=1, relief="solid"
        )
        self.skip_input.place(relx=0.83, rely=0.6, anchor="center")

        self.skip_input_btn = tk.Button(
            self.root, text="Change skip-length", command=self.change_skip_length
        )
        self.skip_input_btn.place(relx=0.83, rely=0.65, anchor="center")

        self.root.bind("<Right>", self.next_image)
        self.root.bind("<Left>", self.prev_image)
        self.root.bind("<space>", self.skip_image)
        self.root.bind("q", self.quit)

        self.root.mainloop()

    def open_file(self):

        images = []

        for path in self.image_paths:
            file_path = f"{self.main_dir}{path}image{self.iter}.png"
            img = Image.open(file_path)
            img = self.resize_img(img)
            images.append(img)

        input_files = os.listdir(self.main_dir + self.image_paths[0])

        if ".DS_Store" in input_files:
            input_files.pop(input_files.index(".DS_Store"))

        self.num_files = len(input_files)

        self.root.title("Image viewer")

        return images

    def next_image(self, event: "tk.Event" = None):

        if self.iter < self.num_files - 1:
            self.iter += 1

        images = []

        for path in self.image_paths:
            file_path = f"{self.main_dir}{path}image{self.iter}.png"
            img = Image.open(file_path)
            img = self.resize_img(img)
            images.append(img)

        for canvas_img, img in zip(self.canvas_images, images):
            self.canvas.itemconfigure(canvas_img, image=img)

        self.canvas.config(width=self.width, height=self.height)
        self.update_image_text()
        try:
            self.canvas.wait_visibility()
        except tk.TclError:
            pass

    def prev_image(self, event: "tk.Event" = None):
        if self.iter >= 1:
            self.iter -= 2
            self.next_image()
            self.update_image_text()

    def skip_image(self, event: "tk.Event" = None):
        if self.num_files > self.iter + self.skip_length:
            self.iter += self.skip_length - 1
            self.next_image()
            self.update_image_text()

    def change_skip_length(self):
        if self.skip_input.get("1.0", "end") != "\n":
            self.skip_length = int(self.skip_input.get("1.0", "end"))
            self.canvas.itemconfig(
                self.skip_text,
                text="Press space to skip " + str(self.skip_length) + " frames",
            )

    def update_image_text(self):
        self.canvas.itemconfig(self.image_text, text="Frame " + str(self.iter + 1))

    def resize_img(self, img: "Image") -> "ImageTk.PhotoImage":
        width, height = img.size
        width //= 4.2
        height //= 4.2
        resized_image = img.resize((int(width), int(height)), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)

    def quit(self, event: "tk.Event" = None):
        self.root.destroy()
