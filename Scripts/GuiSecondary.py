

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo




def select_file(filetypes:list,check=False)->str:
    filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
    if check:
        showinfo(title='Selected File',message=filename)
    return filename


def select_folder(check=False,Title="")->str:
    folderPath=fd.askdirectory(initialdir=r"F:\python\pythonProject",title="Select folder for "+Title)
    if check:
        showinfo(title='Selected File',message=folderPath)
    return folderPath


if __name__=="__main__":
    ListFileTypes = (('text files', '*.txt'),('All files', '*.*'))
    P=select_file(filetypes=ListFileTypes)
    print("FIle is here!!!!!!!!!!!!!!!!!!!!!!",P)

    Folder=select_folder()
    print("Folder",Folder)