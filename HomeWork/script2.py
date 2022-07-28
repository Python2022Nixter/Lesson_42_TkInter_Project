import os
from tkinter import *
from sys import platform
from tkinter import filedialog

if platform == 'darwin':
    from tkmacosx import *

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FOLDERS = os.path.join(PROJECT_FOLDER, "students")
FILE_TYPES = [("CSV files", "*.csv")]

headers = ""
students_list = []
selected_students = []
create_folder_button = None


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
    # print(e.widget.get(ANCHOR))  # get the selected student from the list box
    info.config(text=e.widget.get(ANCHOR))
    global selected_students
    selected_students = []
    for i in e.widget.curselection():
        selected_students.append(e.widget.get(i).split(';'))
    # selected_student = e.widget.get(ANCHOR).strip().split(',') # get the selected student from the list box
    # print(selected_students)

    # create new button -> create folders
    add_remove_button(e)
    pass


def create_folders():
    global selected_students
    print("create folders------------------------------------------------------")
    create_studetns_folders()
    count = 0

    for next_stud in selected_students:
        # print("---",next_stud)

        # create folder for each student
        name_of_folder = (next_stud[0].strip().split(','))[3]
        name_of_course = (next_stud[0].strip().split(','))[7]
        create_folder(name_of_folder)
        create_folder(name_of_folder + "/" + name_of_course)
        count += 1
        pass

    students_list_box.selection_clear(0, END)
    info.config(text=f"{count} folders created")
    count = 0
    pass


def add_remove_button(e):
    global create_folder_button
    # create new button -> create folders
    print(f"add remove button: {len (e.widget.curselection())}")
    print(buttons_frame.winfo_children())

    if len(e.widget.curselection()) == 0:
        # remove button
        if create_folder_button is not None:
            print("remove button")
            create_folder_button.destroy()
            create_folder_button = None
        pass
    else:
        # create button if not exist
        if create_folder_button is None:
            print("create button")
            create_folder_button = Button(
                buttons_frame, text="Create Folders", command=create_folders, image=icon2, compound=RIGHT)
            create_folder_button.grid(row=2, padx=5, pady=5, sticky=(W, E))
            # if buttons_frame.winfo_exists():
            # print(buttons_frame.winfo_children()[2])
        pass


def create_studetns_folders():
    if not os.path.exists(STUDENTS_FOLDERS):
        os.mkdir(STUDENTS_FOLDERS)
    pass


def create_folder(name_of_folder):
    if not os.path.exists(os.path.join(STUDENTS_FOLDERS, name_of_folder)):
        os.mkdir(os.path.join(STUDENTS_FOLDERS, name_of_folder))
    pass


root_window = Tk()
root_window.title("Folder Maker")
root_window.geometry("600x500")

IMG1 = PhotoImage(file=PROJECT_FOLDER + "/" + "f.png")
icon1 = IMG1.subsample(5, 5)
IMG2 = PhotoImage(file=PROJECT_FOLDER + "/" + "f2.png")
icon2 = IMG2.subsample(5, 5)

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
Button(buttons_frame, text="Open file", image=icon1, compound=RIGHT, command=open_file).grid(
    row=0, padx=5, pady=5, sticky=(W, E))
Button(buttons_frame, text="Display students list",
       command=display_students).grid(row=1, padx=5, pady=5, sticky=(W, E))

# list_frame: configuration, widgets
list_frame.columnconfigure(0, weight=1)
list_frame.rowconfigure(0, weight=1)
list_y_scroll = Scrollbar(list_frame, orient=VERTICAL)
list_x_scroll = Scrollbar(list_frame, orient=HORIZONTAL)

students_list_box = Listbox(list_frame,
                            yscrollcommand=list_y_scroll.set,
                            xscrollcommand=list_x_scroll.set,
                            selectmode=MULTIPLE)
"""
selectmode=EXTENDED
BROWSE - default
SINGLE - only one item can be selected at a time
MULTIPLE - multiple items can be selected
"""


students_list_box.grid(row=0, column=0, sticky=NSEW)
students_list_box.bind("<<ListboxSelect>>",  get_selected_student)
# students_list_box.bind("<<ListboxSelect>>",  add_remove_button)
list_y_scroll.config(command=students_list_box.yview)
list_x_scroll.config(command=students_list_box.xview)
list_y_scroll.grid(row=0, column=1, sticky=NS)
list_x_scroll.grid(row=1, column=0, sticky=EW, columnspan=2)


root_window.mainloop()
