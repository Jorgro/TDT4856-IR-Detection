from fileinput import filename
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
import time

filename = ""

ws = Tk()
ws.title('File upload')
ws.geometry('350x100')  

def open_file():
    file_path = askopenfile(mode='r', filetypes=[('Video Files', '*mov'), 
                                                 ('Video Files', '*mp4'),
                                                 ('Image Files', '*png')])
    if file_path is not None:
        Label(ws, text='File Uploaded Successfully!', foreground='green').grid(row=4, columnspan=3, pady=10)
        global filename
        filename = file_path.name

def upload_file():
    upload_label = Label(
                ws, 
                text='Upload video file (.mp4, .mov) '
    )
    upload_label.grid(row=0, column=0, padx=10)

    upload_button = Button(
                    ws, 
                    text ='Choose File', 
                    command = lambda:open_file()
    ) 
    upload_button.grid(row=0, column=1)

    exit_button = Button(
                    ws, 
                    text ='Exit window', 
                    command = lambda:ws.destroy()
    ) 
    exit_button.grid(row=1, column=1)

    ws.mainloop()

def get_filename():
    global filename
    upload_file()
    if len(filename):
        return filename