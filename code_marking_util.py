import tkinter
from tkinter import filedialog, Button, Label, StringVar, IntVar, Frame, Text
from tkinter.scrolledtext import ScrolledText
from filename_helper import FilenameHelper
from submission import Submission
from solution import Solution
from predefined_solutions_earlyfinal import solution_dict

filename_helper = FilenameHelper()
window = tkinter.Tk()
window.resizable(False, False)
window.geometry('1800x950')
window.title('Canvas Code Marking Utility')
window.iconphoto(False, tkinter.PhotoImage(file='./icon.png'))

current_question_index = IntVar()
current_question_index.set(0)
loaded_submissions = []

file_content = StringVar()
solution_content = StringVar()
test_submission_content = StringVar()
test_solution_content = StringVar()
current_submission_filename = StringVar()
current_submission_filename.set("No file loaded.")
current_solution_filename = StringVar()
current_solution_filename.set("No file loaded.")

def update_question_label():
    current_question = current_question_index.get()
    loaded_question_label_text.set(f"Student: {loaded_submissions[current_question].fullname} \nID: {loaded_submissions[current_question].id}\nGroup: {loaded_submissions[current_question].group_number} | Question: {loaded_submissions[current_question].question_number}")

def update_file_content():
    current_file : Submission = loaded_submissions[current_question_index.get()]
    submission_content_string = current_file.load_content_string()

    question_num = current_file.question_number
    group_num = current_file.group_number
    current_solution : Solution = solution_dict[(question_num,group_num)]
    solution_content_string = current_solution.load_content_string()

    current_submission_filename.set(current_file.file_path)
    current_solution_filename.set(current_solution.file_path)

    file_content.set(submission_content_string)
    submission_text.delete('1.0', tkinter.END)
    submission_text.insert(tkinter.END, file_content.get())

    solution_content.set(solution_content_string)
    solution_text.delete('1.0', tkinter.END)
    solution_text.insert(tkinter.END, solution_content.get())
    test_file()

def test_file():
    current_submission : Submission = loaded_submissions[current_question_index.get()]
    question_num = current_submission.question_number
    group_num = current_submission.group_number

    current_solution : Solution = solution_dict[(question_num,group_num)]
    sub_out, sol_out = current_solution.test_submission(current_submission)
    
    test_submission_content.set(sub_out)
    test_submission_text.delete('1.0', tkinter.END)
    test_submission_text.insert(tkinter.END, test_submission_content.get())

    test_solution_content.set(sol_out)
    test_solution_text.delete('1.0', tkinter.END)
    test_solution_text.insert(tkinter.END, test_solution_content.get())

def select_files():
    submission_directory = filedialog.askdirectory(title='Load submission files',
        initialdir='./')

    print(f"Loaded directory: {submission_directory}")

    global loaded_submissions
    loaded_submissions = filename_helper.create_submissions_from_directory(submission_directory)
    current_question_index.set(0)
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
top_frame.grid(row = 0, column = 0, columnspan=10, sticky="w")

open_button = Button(
    top_frame,
    text='Load Submission Files',
    command=select_files
)

open_button.grid(row = 0, column = 0, columnspan=2, pady = 5, padx = 5, sticky="nswe")

loaded_question_label_text = StringVar()
loaded_question_label_text.set("No submissions loaded.")
loaded_question_label = Label(top_frame, textvariable=loaded_question_label_text, justify=tkinter.LEFT, anchor="e")
loaded_question_label.grid(row = 0, column = 2, pady = 5, padx = 5, rowspan=2, columnspan=8, sticky="e")

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

submission_title_label = Label(body_frame, text="Submission Code:", wraplength=700, justify=tkinter.LEFT, anchor="w")
submission_title_label.grid(row = 0, column = 0, pady = 1, padx = 1, sticky="w")

submission_text_label = Label(body_frame, textvariable=current_submission_filename, wraplength=700, justify=tkinter.LEFT, anchor="w")
submission_text_label.grid(row = 1, column = 0, pady = 1, padx = 1, sticky="w")

submission_text = ScrolledText(body_frame, wrap=tkinter.WORD, width=70, height=30)
submission_text.insert(tkinter.END, "No file loaded.")
submission_text.grid(row=2,column=0,pady = 5, padx = 5, rowspan=3, sticky="nswe")

solution_title_label = Label(body_frame, text="Solution Code:", wraplength=700, justify=tkinter.LEFT, anchor="w")
solution_title_label.grid(row = 0, column = 1, pady = 1, padx = 1, sticky="w")

solution_text_label = Label(body_frame, textvariable=current_solution_filename, wraplength=700, justify=tkinter.LEFT, anchor="w")
solution_text_label.grid(row = 1, column = 1, pady = 1, padx = 1, sticky="w")

solution_text = ScrolledText(body_frame, wrap=tkinter.WORD, width=70, height=30)
solution_text.insert(tkinter.END, "No file loaded.")
solution_text.grid(row=2,column=1,pady = 5, padx = 5, rowspan=3, sticky="nswe")

test_submission_label = Label(body_frame, text="Submission Test Output:", wraplength=700, justify=tkinter.LEFT, anchor="w")
test_submission_label.grid(row = 1, column = 2, pady = 1, padx = 1, sticky="w")

test_submission_text = ScrolledText(body_frame, wrap=tkinter.WORD, width=72, height=23)
test_submission_text.insert(tkinter.END, "No file loaded.")
test_submission_text.grid(row=2,column=2,pady = 5, padx = 5, sticky="nswe")

test_solution_label = Label(body_frame, text="Solution Test Output:", wraplength=700, justify=tkinter.LEFT, anchor="w")
test_solution_label.grid(row = 3, column = 2, pady = 1, padx = 1, sticky="sw")

test_solution_text = ScrolledText(body_frame, wrap=tkinter.WORD, width=72, height=23)
test_solution_text.insert(tkinter.END, "No file loaded.")
test_solution_text.grid(row=4,column=2,pady = 5, padx = 5, sticky="nswe")

window.mainloop()