import os
import importlib.util
import sys

from submission import Submission

SRC_DIR = ".\submissions"
NEW_DIR = ".\submissions_renamed"
LATE_STRING = "_LATE"
EXTENSION = ".py"


def clean_submission_filename(filename):
    # Remove [ and ] from string
    new_filename = filename.replace("[","")
    new_filename = new_filename.replace("]","")

    # Remove redundant underscores
    new_filename = new_filename.replace("__","_")

    # Remove _LATE from string
    new_filename = new_filename.replace("_LATE","")

    # Remove extension from string
    new_filename = new_filename[:-3]

    return new_filename


def get_filename_parts(filename):
    # Split string into list of components
    # [fullname, ID, question number, group number]
    parts = filename.split('_')
    parts[-2] = parts[-2][1::]
    parts[-1] = parts[-1][1:2]
    del parts[1:3]

    # Checks for missing ID
    if parts[1] == 'ID':
        parts[1] = 'MISSING ID'

    return parts


def rename_file(filename, fileparts):
    old_path = SRC_DIR + "\\" + filename

    if fileparts[1] != 'MISSING ID':
        new_filename = "_".join(fileparts[1:]) + EXTENSION
        new_path = NEW_DIR + "\\" + fileparts[1]
    else:
        new_filename = fileparts[0] + "_" + "_".join(fileparts[2:]) + EXTENSION
        new_path = NEW_DIR + "\\" + fileparts[0]

    os.makedirs(new_path, exist_ok=True)
    new_path += "\\"  + new_filename

    # New file will be named:
    # ID_Question_Group.py
    # If ID missing, use fullname of student instead.
    try:
        os.rename(old_path, new_path)
        print(f"Old file: {old_path} -> New file: {new_path}")
    except FileExistsError:
        print(f"Cleaned file exists for {fileparts[0]} - Q{fileparts[2]}")

    return new_path


def create_submission(path, parts):
    return Submission(path, name = parts[0], 
                            id = parts[1], 
                            question_number = parts[2],
                            group_number = parts[3])

def create_submissions_from_directory(dir):
    submissions_list = []

    for filename in os.listdir(SRC_DIR):
        clean_name = clean_submission_filename(filename=filename)
        parts = get_filename_parts(clean_name)
        new_path = rename_file(filename, parts)
        submissions_list.append(create_submission(new_path, parts))
    
    return submissions_list


def import_module_from_path(path):
    """
    Import .py module using given path.
    """
    spec = importlib.util.spec_from_file_location("submission_module", path)
    submission_module = importlib.util.module_from_spec(spec)
    sys.modules["submission_module"] = submission_module
    spec.loader.exec_module(submission_module)
    return submission_module


def main():
    submissions = create_submissions_from_directory(SRC_DIR)
    for sub in submissions:
        print(sub)
    

        
if __name__ == "__main__":
    main()

    