import os
from submission import Submission

SRC_DIR = ".\submissions"
NEW_DIR = ".\submissions_renamed"
SOLUTIION_DIR = ".\solution"
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
    parts[-1] = int(parts[-1][1:2]) # Group number will be int
    del parts[1:3]

    # Checks for missing ID
    if parts[1] == 'ID':
        parts[1] = 'MISSING ID'

    return parts


def rename_file(filename, fileparts, source_directory, new_directory):
    old_path = source_directory + "\\" + filename

    if fileparts[1] != 'MISSING ID':
        new_filename = "_".join(fileparts[1:]) + EXTENSION
        new_path = new_directory + "\\" + fileparts[1]
    else:
        new_filename = fileparts[0] + "_" + "_".join(fileparts[2:]) + EXTENSION
        new_path = new_directory + "\\" + fileparts[0]

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

def create_submissions_from_directory(source_dir, new_dir):
    submissions_list = []

    for filename in os.listdir(source_dir):
        clean_name = clean_submission_filename(filename=filename)
        parts = get_filename_parts(clean_name)
        new_path = rename_file(filename, parts, source_dir, new_dir)
        submissions_list.append(create_submission(new_path, parts))
    
    return submissions_list

def main():
    submissions = create_submissions_from_directory(SRC_DIR, NEW_DIR)
    for sub in submissions:
        print(sub.content)
    

        
if __name__ == "__main__":
    main()

    