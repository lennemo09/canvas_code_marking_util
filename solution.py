from runnable import Runnable
from submission import Submission
import random, subprocess, sys, os

random.seed(1337)

class Solution(Runnable):
    def __init__(self, file_path, question_number, group_number, functions_to_test = [], inputs_to_test = [], run_from_main=False, multi_input=False):
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
        
        self.run_from_main = run_from_main
        self.multi_input = multi_input

    def test_submission(self, submission : Submission):
        if self.run_from_main: # When the question module's content is not wrapped in a function.
            for test_input in self.inputs_to_test:
                print("####################################")
                print(f"Testing with inputs:\n{test_input}")
                print("Output from submission:")
                proc = subprocess.run(['python', submission.file_path], text=True, capture_output=True, input=test_input)
                print(proc.stdout)

                print()

                print("Output from solution:")
                proc = subprocess.run(['python', self.file_path], text=True, capture_output=True, input=test_input)
                print(proc.stdout)
        else: # When the question module's content is wrapped in a function.
            submission_module = submission.load_module()
            solution_module = solution.load_module()
            for function_name in self.functions_to_test:
                solution_function = getattr(solution_module, function_name)
                submission_function = getattr(submission_module, function_name)
                for test_input in self.inputs_to_test:
                    print("####################################")
                    print(f"Testing with inputs:\n{test_input}")

                    sys.stdout = open(os.devnull, 'w')
                    if not self.multi_input:
                        solution_output = solution_function(test_input)
                        submission_output = submission_function(test_input)
                    else:
                        solution_output = solution_function(*test_input)
                        submission_output = submission_function(*test_input)
                    sys.stdout = sys.__stdout__

                    print("Output match submission:", submission_output == solution_output)
                    print("Output from submission:", submission_output)
                    print("Output from solution:", solution_output)


    
if __name__ == "__main__":
    # submission = Submission(file_path=".\submissions_renamed\doquynhtrang\doquynhtrang_1_1.py",
    # name="doquynhtrang",id="doquynhtrang",question_number="1",group_number=1)

    # solution = Solution(file_path=".\solution\g1-q1.py", question_number="1", group_number=1, run_from_main=True)
    # solution.inputs_to_test = ["VinUni is a young institution\nand elite\n", "Hi my name is Jack\nthe reaper\n","I really really like pancakes\nwith bacon\n"]

    submission = Submission(file_path=".\submissions_renamed\doquynhtrang\doquynhtrang_4_1.py",
    name="doquynhtrang",id="doquynhtrang",question_number="4",group_number=1)

    solution = Solution(file_path=".\solution\g1-q4.py", question_number="4", group_number=1, run_from_main=False, multi_input=True)
    solution.functions_to_test = ["add_matrix"]
    solution.inputs_to_test = [[[[1,2,3], [1,5,1], [1,2,2]], [[3,1,0], [1,1,2], [2,1,0]]],
                                [[[4, 3, 3], [2, 6, 3], [3, 3, 2]], [[1,2,3], [1,5,1], [1,2,2]]]]

    solution.test_submission(submission)

