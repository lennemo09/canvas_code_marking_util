import tkinter
from tkinter import filedialog, Button, Label, StringVar, IntVar
from filename_helper import FilenameHelper

filename_helper = FilenameHelper()
window = tkinter.Tk()
window.resizable(False, False)
window.geometry('900x750')
window.title('Canvas Code Marking Utility')

current_question_index = IntVar()
current_question_index.set(0)
loaded_submissions = []


def update_question_label():
    current_question = current_question_index.get()
    loaded_question_label_text.set(f"Student: {loaded_submissions[current_question].fullname} \n ID: {loaded_submissions[current_question].id}\n Group: {loaded_submissions[current_question].group_number} | Question: {loaded_submissions[current_question].question_number}")

def select_files():
    submission_directory = filedialog.askdirectory(title='Load submission files',
        initialdir='./')

    print(f"Loaded directory: {submission_directory}")

    global loaded_submissions
    loaded_submissions = filename_helper.create_submissions_from_directory(submission_directory)
    update_question_label()
    

def next_question():
    current_question_index.set((current_question_index.get() + 1) % len(loaded_submissions))
    update_question_label()

def previous_question():
    current_question_index.set((current_question_index.get() - 1) % len(loaded_submissions))
    update_question_label()


open_button = Button(
    window,
    text='Load Submission Files',
    command=select_files
)

open_button.pack(expand=True)

next_question_button = Button(
    window,
    text='Next question',
    command=next_question
)

next_question_button.pack()

loaded_question_label_text = StringVar()
loaded_question_label_text.set("No submissions loaded.")
loaded_question_label = Label(window, textvariable=loaded_question_label_text)
loaded_question_label.pack()



window.mainloop()