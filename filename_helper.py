import os
from submission import Submission

SRC_DIR = ".\submissions"
NEW_DIR = ".\submissions_renamed"
SOLUTIION_DIR = ".\solution"
LATE_STRING = "_LATE"
EXTENSION = ".py"

class FilenameHelper:
    def clean_submission_filename(self, filename):
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


    def get_filename_parts(self, filename, cleaned=False, keep_name=True):

        if not cleaned:
            # Split string into list of components
            # [fullname, ID, question number, group number]
            parts = filename.split('_')
            parts[-2] = parts[-2][1::]
            parts[-1] = parts[-1][1:2]
            del parts[1:3]

            # Checks for missing ID
            if parts[1] == 'ID':
                parts[1] = 'MISSING ID'

        else:
            parts = filename.split('_')

        if not keep_name:
            parts = parts[1:]

        return parts


    def rename_file(self, filename, fileparts, source_directory, new_directory, keep_name=True):
        old_path = source_directory + "\\" + filename

        if fileparts[1] != 'MISSING ID':
            if keep_name:
                new_filename = "_".join(fileparts) + EXTENSION
            else:
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


    def create_submission(self, path, parts):
        if len(parts) == 4:
            return Submission(path, name = parts[0], 
                                    id = parts[1], 
                                    question_number = parts[2],
                                    group_number = parts[3])
        else:
            return Submission(path, name = parts[0], 
                                    id = parts[0], 
                                    question_number = parts[1],
                                    group_number = parts[2])


    def create_submissions_from_raw_directory(self, source_dir, new_dir):
        submissions_list = []

        for filename in os.listdir(source_dir):
            if filename[-2:] == '.py':
                clean_name = self.clean_submission_filename(filename=filename)
                parts = self.get_filename_parts(clean_name)
                new_path = self.rename_file(filename, parts, source_dir, new_dir)
                submissions_list.append(self.create_submission(new_path, parts))
        
        return submissions_list

    def create_submissions_from_directory(self, source_dir, keep_name=True):
        submissions_list = []

        for filepath in os.listdir(source_dir):
            if filepath[-3:] == '.py':
                # Remove extension from string
                filepath_no_extension = filepath[:-3]
                parts = self.get_filename_parts(filepath_no_extension, cleaned=True, keep_name=keep_name)
                submissions_list.append(self.create_submission(f'{source_dir}\{filepath}', parts))

        return submissions_list
    
    def clean_submissions_directory(self, source_dir, new_dir):
        for filename in os.listdir(source_dir):
            clean_name = self.clean_submission_filename(filename)
            parts = self.get_filename_parts(clean_name)
            new_path = self.rename_file(filename, parts, source_dir, new_dir)

            print(f"Successfully renamed file to {new_path}")

if __name__ == "__main__":
    filename_helper = FilenameHelper()
    filename_helper.clean_submissions_directory(SRC_DIR, NEW_DIR)