from runnable import Runnable
from submission import Submission
import random, subprocess, sys, os
import traceback

random.seed(1337)


class Solution(Runnable):
    def __init__(self, file_path, question_number, group_number, function_to_test = None, inputs_to_test = [], run_from_main=False, multi_input=False):
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
        param: run_from_main: Whether the question module's content have code that's supposed to be run in global scope (run in main).
        param: multi_input: Whether the function in the question module requires more than 1 argument.
        """
        super().__init__(file_path, question_number, group_number)

        self.functions_to_test = function_to_test
        self.inputs_to_test = inputs_to_test
        
        self.run_from_main = run_from_main
        self.multi_input = multi_input

    def test_submission(self, submission : Submission, suppress_stdout = True):
        """
        Test a given submission against the solution provided.

        If the question module's content have code that's supposed to be run in global scope (run in main), 
        then self.run_from_main must be True for this to work.

        Else, if the question module's content have code that's wrapped in a function, 
        self.multi_input must be set to True if the function takes in more than 1 input as arguments.

        param: submission: Submission object containing the submission corresponding to the same question as this Solution.
        param: supress_stdout: Supress output such as print statements from the loaded modules.
        """
        try:
            submission_output_string = ""
            solution_output_string = ""
            if self.run_from_main: # When the question module's content is not wrapped in a function.
                for test_input in self.inputs_to_test:
                    solution_output_string += "\n####################################"
                    solution_output_string += f"\nTesting with inputs:\n{test_input}"                    
                    solution_subprocess = subprocess.run(['python', self.file_path], text=True, capture_output=True, input=test_input)
                    solution_output_string += "\n\nOutput from solution:\n"
                    solution_output_string += solution_subprocess.stdout

                    submission_output_string += "\n####################################"
                    submission_output_string += f"\nTesting with inputs:\n{test_input}"
                    submission_subprocess = subprocess.run(['python', submission.file_path], text=True, capture_output=True, input=test_input)
                    submission_output_string += f"\nOutput match solution: {submission_subprocess.stdout == solution_subprocess.stdout}"
                    submission_output_string += "\n\nOutput from submission:\n"
                    submission_output_string += submission_subprocess.stdout

            else: # When the question module's content is wrapped in a function.
                submission_module = submission.load_module()
                solution_module = self.load_module()

                solution_function = getattr(solution_module, self.functions_to_test)
                submission_function = getattr(submission_module, self.functions_to_test)

                for test_input in self.inputs_to_test:
                    if suppress_stdout:
                        sys.stdout = open(os.devnull, 'w') # Suppresses stdout from loaded module.
                    
                    solution_output_string += "\n####################################"
                    solution_output_string += f"\nTesting with inputs:\n{test_input}"

                    if not self.multi_input: # If the function only takes 1 argument
                        solution_output = solution_function(test_input)
                    else: # If the function takes in multiple arguments -> unpack the list of inputs
                        solution_output = solution_function(*test_input)

                    solution_output_string += "\n\nOutput from solution:\n"
                    solution_output_string += solution_output.__repr__()


                    submission_output_string += "\n####################################"
                    submission_output_string += f"\nTesting with inputs:\n{test_input}"

                    if not self.multi_input: # If the function only takes 1 argument
                        submission_output = submission_function(test_input)
                    else: # If the function takes in multiple arguments -> unpack the list of inputs
                        submission_output = submission_function(*test_input)

                    submission_output_string += f"\nOutput match solution: {submission_output == solution_output}"
                    submission_output_string += "\n\nOutput from submission:\n"
                    submission_output_string += submission_output.__repr__()

                    if suppress_stdout:
                        sys.stdout = sys.__stdout__# Unsuppresses stdout from loaded module.
                    
        except Exception as e:
            if suppress_stdout:
                sys.stdout = sys.__stdout__# Unsuppresses stdout from loaded module.

            submission_output_string += "\n\nERROR encountered while testing submission.\n\n"
            submission_output_string += traceback.format_exc()
        finally:
            return submission_output_string, solution_output_string


if __name__ == "__main__":
    submission_g1_q1 = Submission(file_path=".\submissions_renamed\doquynhtrang\doquynhtrang_1_1.py",
    name="doquynhtrang",id="doquynhtrang",question_number="1",group_number=1)

    submission_g1_q2 = Submission(file_path=".\submissions_renamed\doquynhtrang\doquynhtrang_2_1.py",
    name="doquynhtrang",id="doquynhtrang",question_number="2",group_number=1)

    submission_g1_q3a = Submission(file_path=".\submissions_renamed\doquynhtrang\doquynhtrang_3a_1.py",
    name="doquynhtrang",id="doquynhtrang",question_number="3a",group_number=1)

    submission_g1_q4 = Submission(file_path=".\submissions_renamed\doquynhtrang\doquynhtrang_4_1.py",
    name="doquynhtrang",id="doquynhtrang",question_number="4",group_number=1)

    solution_g1_q1 = Solution(file_path=".\solution\g1-q1.py", question_number="1", group_number=1, run_from_main=True)
    solution_g1_q1.inputs_to_test = ["VinUni is a young institution\nand elite\n", "Hi my name is Jack\nthe reaper\n","I really really like pancakes\nwith bacon\n"]

    solution_g1_q2 = Solution(file_path=".\solution\g1-q2.py", question_number="2", group_number=1, run_from_main=True)
    solution_g1_q2.inputs_to_test = ["5\n20\n80\n100\n90\n50\n"]

    solution_g1_q3a = Solution(file_path=".\solution\g1-q3a.py", question_number="3a", group_number=1, run_from_main=False)
    solution_g1_q3a.functions_to_test = "odds_sum"
    solution_g1_q3a.inputs_to_test = [[1,3,4,5],[-2,0,2,4,6,8],[1,-3,3,7]]

    solution_g1_q4 = Solution(file_path=".\solution\g1-q4.py", question_number="4", group_number=1, run_from_main=False, multi_input=True)
    solution_g1_q4.functions_to_test = "add_matrix"
    solution_g1_q4.inputs_to_test = [[[[1,2,3], [1,5,1], [1,2,2]], [[3,1,0], [1,1,2], [2,1,0]]],
                                [[[4, 3, 3], [2, 6, 3], [3, 3, 2]], [[1,2,3], [1,5,1], [1,2,2]]],
                                [[[1,2],[2,3],[3,4]], [[5,6],[7,8],[9,10]]]]

    sub_out, sol_out = solution_g1_q3a.test_submission(submission_g1_q3a)
    print(sub_out)