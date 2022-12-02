import os
import importlib.util
import sys


class Runnable:
    def __init__(self, file_path, question_number, group_number):
        """
        Base class for runnable .py files related to the assessment.

        param: file_path: Full path of .py file.
        param: question_number: The corresponding question in the assessment with this runnable file.
        param: group_number: The corresponding group in the assessment with this runnable file.
        """
        self.file_path = file_path
        self.question_number = question_number
        self.group_number = group_number

        self.content = self.load_content_string()

    def load_module(self, module_name = "runnable_module"):
        """
        Import the assigned Python module and return it as a callable object.

        param: module_name: name in scope for the module being imported.
        """
        spec = importlib.util.spec_from_file_location(module_name, self.file_path)
        runnable_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = runnable_module
        spec.loader.exec_module(runnable_module)
        return runnable_module

    def load_content_string(self):
        """
        Return the file content as a string.
        """
        if os.path.isfile(self.file_path):
            # Open Python file as text file
            code_file = open(self.file_path, "r", encoding="utf8")

            # Read file content as string
            code_string = code_file.read()

            code_file.close()

            return code_string
        else:
            print(f"Cannot find file with path: {self.file_path}")

    def show_content(self):
        """
        Print the module text content.
        """
        print(self.content)