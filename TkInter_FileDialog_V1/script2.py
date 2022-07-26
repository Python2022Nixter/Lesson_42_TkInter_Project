import os
from textwrap import fill
from tkinter import *
from sys import platform
from tkinter import filedialog

if platform == 'darwin':
    from tkmacosx import *

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_TYPES = [("Text files", "*.txt"),
              ("Python files", "*.py"),
              ("CSV files", "*.csv")]

headers = ""
students_list = []


def open_file():
    file_path = filedialog.askopenfilename(
        title="Your Choise",
        filetypes=FILE_TYPES,
        initialdir=PROJECT_FOLDER)
    print(file_path)
    info.configure(text=file_path.split('/')[-1])

    global headers
    global students_list

    with open(file_path, 'r', encoding='utf-8') as f:
        headers = f.readline()
        students_list = f.readlines()

    pass


def display_students():
    print("list box: ", students_list_box.size())
    students_list_box.delete(0, END)
    students_list_box.insert(0, *students_list)
    info.config(text=f"headers:\n {headers}")
    pass

def get_selected_student(e):
    print(e.widget.get(ANCHOR)) # get the selected student from the list box
    info.config(text=e.widget.get(ANCHOR))
    pass


root_window = Tk()
root_window.title("Folder Maker")
root_window.geometry("600x500")

# Root frames
info_frame = Frame(root_window)
buttons_frame = Frame(root_window)
list_frame = Frame(root_window)

info_frame.pack(fill=X, padx=10, pady=10)
buttons_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)
list_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

# info_frame widgets
info = Label(info_frame)
info.pack(expand=True, fill=BOTH)

# buttons_frame widgets
Button(buttons_frame, text="Open file", command=open_file).grid(row=0, padx=5, pady=5, sticky=(W, E))
Button(buttons_frame, text="Display students list",
       command=display_students).grid(row=1, padx=5, pady=5, sticky=(W, E))

# list_frame: configuration, widgets
list_frame.columnconfigure(0, weight=1)
list_frame.rowconfigure(0, weight=1)
list_y_scroll = Scrollbar(list_frame, orient=VERTICAL)
list_x_scroll = Scrollbar(list_frame, orient=HORIZONTAL)

students_list_box = Listbox(list_frame, yscrollcommand=list_y_scroll.set, xscrollcommand=list_x_scroll.set)
students_list_box.grid(row=0, column=0, sticky=NSEW)
students_list_box.bind("<<ListboxSelect>>",  get_selected_student)
list_y_scroll.config(command=students_list_box.yview)
list_x_scroll.config(command=students_list_box.xview)
list_y_scroll.grid(row=0, column=1, sticky=NS)
list_x_scroll.grid(row=1, column=0, sticky=EW, columnspan=2)


root_window.mainloop()
