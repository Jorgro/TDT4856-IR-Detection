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
        self.image_texts = [
            "Input",
            "Moving objects",
            "Classified objects",
            "Thresholded optical flow",
            "Object filtering",
        ]

        self.N = len(self.image_paths) // 2  # Number of images
        self.x0, self.y0 = 10, 80  # Coordinates of upper left corner

        self.root = tk.Tk()
        self.root.state("zoomed")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.canvas_part = self.width // 3  # Horizontal part taken up by image

        self.main_dir = "./data/GUI_images"
        self.iter = 0
        self.num_files = None
        self.skip_length = 2

        images = self.open_file()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.canvas_images = []

        print(self.canvas_part)

        for i, img in enumerate(images):
            if i > 2:
                y0 = self.y0 + 400
                x0 = self.x0 + (i - 3) * self.canvas_part
            else:
                y0 = self.y0
                x0 = self.x0 + i * self.canvas_part
            self.canvas_images.append(
                self.canvas.create_image(x0, y0, anchor="nw", image=img)
            )
        for i, txt in enumerate(self.image_texts):
            if i > 2:
                y0 = self.y0 + 380
                x0 = self.canvas_part // 2 + (i - 3) * self.canvas_part
            else:
                y0 = self.y0 - 20
                x0 = self.canvas_part // 2 + i * self.canvas_part

            self.canvas.create_text(
                x0, y0, text=txt, fill="black", font=("Helvetica 17 bold"),
            )

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
        width = self.canvas_part
        height = height // (width / self.canvas_part)
        resized_image = img.resize((int(width), int(height)), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)

    def quit(self, event: "tk.Event" = None):
        self.root.destroy()


if __name__ == "__main__":
    img = ImageViewer()
