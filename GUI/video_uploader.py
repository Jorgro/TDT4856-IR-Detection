from tkinter import filedialog
import tkinter as tk

class VideoUploader(object):
    def __init__(self):

        # Change size of window
        self.root = tk.Tk()
        self.width = 500
        self.height = 200
        self.root.geometry(str(self.width)+"x"+str(self.height))

        self.dir = None
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()   

        self.canvas.create_text(self.width//2, self.height//2 + 30, text="Press the button to upload file", fill="black", font=('Helvetica 16 bold'), anchor='center')
        self.canvas.create_text(self.width//2, self.height//2 + 60, text="Press Q to quit", fill="black", font=('Helvetica 15 bold'), anchor='center')
        
        b = tk.Button(self.root, text='Select file', command=self.open_file)
        b.place(relx=0.5, rely=0.3, anchor='center')

        self.root.bind('q', self.quit)

        self.root.mainloop()
  
    def open_file(self):
        self.dir = filedialog.askopenfile()
        self.canvas.create_text(self.width//2, self.height//2, text="Upload complete!", fill="green", font=('Helvetica 15 bold'), anchor='center')

    def get_dir(self):
        return self.dir.name if self.dir else ""
    
    def quit(self, event: 'tk.Event' = None):
        self.root.destroy()

path = VideoUploader().get_dir()
print(path)