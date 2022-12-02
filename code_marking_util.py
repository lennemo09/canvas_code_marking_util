import tkinter
from tkinter import filedialog, Button, Label, StringVar, IntVar, Frame, Text
from tkinter.scrolledtext import ScrolledText
from filename_helper import FilenameHelper
from submission import Submission
from solution import Solution

filename_helper = FilenameHelper()
window = tkinter.Tk()
window.resizable(False, False)
window.geometry('1700x850')
window.title('Canvas Code Marking Utility')

current_question_index = IntVar()
current_question_index.set(0)
loaded_submissions = []

file_content = StringVar()
test_content = StringVar()

def update_question_label():
    current_question = current_question_index.get()
    loaded_question_label_text.set(f"Student: {loaded_submissions[current_question].fullname} \nID: {loaded_submissions[current_question].id}\nGroup: {loaded_submissions[current_question].group_number} | Question: {loaded_submissions[current_question].question_number}")

def update_file_content():
    current_file = loaded_submissions[current_question_index.get()]
    content = current_file.load_content_string()

    file_content.set(content)
    content_text.delete('1.0', tkinter.END)
    content_text.insert(tkinter.END, file_content.get())


def select_files():
    submission_directory = filedialog.askdirectory(title='Load submission files',
        initialdir='./')

    print(f"Loaded directory: {submission_directory}")

    global loaded_submissions
    loaded_submissions = filename_helper.create_submissions_from_directory(submission_directory)
    update_question_label()
    update_file_content()
    

def next_question():
    current_question_index.set((current_question_index.get() + 1) % len(loaded_submissions))
    update_question_label()
    update_file_content()

def previous_question():
    current_question_index.set((current_question_index.get() - 1) % len(loaded_submissions))
    update_question_label()
    update_file_content()
    
top_frame = Frame(window)
top_frame.grid(row = 0, column = 0, columnspan=10)

open_button = Button(
    top_frame,
    text='Load Submission Files',
    command=select_files
)

open_button.grid(row = 0, column = 0, columnspan=2, pady = 5, padx = 5, sticky="nswe")

loaded_question_label_text = StringVar()
loaded_question_label_text.set("No submissions loaded.")
loaded_question_label = Label(top_frame, textvariable=loaded_question_label_text, justify=tkinter.LEFT, anchor="w")
loaded_question_label.grid(row = 0, column = 2, pady = 5, padx = 5, rowspan=2)

previous_question_button = Button(
    top_frame,
    text='Previous question',
    command=previous_question
)

previous_question_button.grid(row = 1, column = 0, pady = 5, padx = 5, sticky="nswe")

next_question_button = Button(
    top_frame,
    text='Next question',
    command=next_question
)

next_question_button.grid(row = 1, column = 1, pady = 5, padx = 5, sticky="nswe")

body_frame = Frame(window)
body_frame.grid(row=1,column=0,columnspan=10,rowspan=9)

content_text = ScrolledText(body_frame, wrap=tkinter.WORD, width=100, height=45)
content_text.insert(tkinter.END, "No file loaded.")
content_text.grid(row=0,column=0,pady = 5, padx = 5, sticky="nswe")

test_text = ScrolledText(body_frame, wrap=tkinter.WORD, width=100, height=45)
test_text.insert(tkinter.END, "No file loaded.")
test_text.grid(row=0,column=1,pady = 5, padx = 5, sticky="nswe")

window.mainloop()