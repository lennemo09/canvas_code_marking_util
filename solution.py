from runnable import Runnable


class Solution(Runnable):
    def __init__(self, file_path, question_number, group_number, functions_to_test = [], inputs_to_test = []):
        """
        Solution module class.
        A Solution object is used to test submissions against its own test cases and expected output.

        param: file_path: Full path of .py file.
        param: question_number: The corresponding question in the assessment with this Solution file.
        param: group_number: The corresponding group in the assessment with this Solution file.
        param: functions_to_test: List of functions to be called while testing.
        param: inputs_to_test: List of inputs to be passed to each function while testing.
                               can be a nested list, with each list corresponding to multiple 
                               calls of each function in functions_to_test list.
        """
        super().__init__(file_path, question_number, group_number)

        self.functions_to_test = functions_to_test
        self.inputs_to_test = inputs_to_test
    
