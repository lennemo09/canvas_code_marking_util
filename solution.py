from runnable import Runnable
from submission import Submission
import random, subprocess, sys, os
import traceback
from func_timeout import func_timeout, FunctionTimedOut

random.seed(1337)
RUNTIME_LIMIT = 1 # Seconds

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

        self.function_to_test = function_to_test
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
                    if type(test_input) == list:
                        copy_test_input = test_input[:]
                    else:
                        copy_test_input = test_input

                    solution_output_string += "####################################"
                    solution_output_string += f"\nTesting with inputs:\n{copy_test_input}"                    
                    solution_subprocess = subprocess.run(['python', self.file_path], text=True, timeout=RUNTIME_LIMIT, capture_output=True, input=copy_test_input)
                    solution_output_string += "\n\nOutput from solution:\n"
                    solution_output_string += solution_subprocess.stdout +"\n"

                    if type(test_input) == list:
                        copy_test_input = test_input[:]
                    else:
                        copy_test_input = test_input

                    submission_output_string += "####################################"
                    submission_output_string += f"\nTesting with inputs:\n{copy_test_input}"
                    submission_subprocess = subprocess.run(['python', submission.file_path], text=True, timeout=RUNTIME_LIMIT, capture_output=True, input=copy_test_input)
                    submission_output_string += f"\nOutput match solution: {submission_subprocess.stdout == solution_subprocess.stdout}".upper()
                    submission_output_string += "\n\nOutput from submission:\n"
                    submission_output_string += submission_subprocess.stdout +"\n"

            else: # When the question module's content is wrapped in a function.
                submission_module = func_timeout(RUNTIME_LIMIT, submission.load_module)
                solution_module = self.load_module()

                solution_function = getattr(solution_module, self.function_to_test)
                submission_function = getattr(submission_module, self.function_to_test)

                for test_input in self.inputs_to_test:
                    if type(test_input) == list:
                        copy_test_input = test_input[:]
                    else:
                        copy_test_input = test_input
                    if suppress_stdout:
                        sys.stdout = open(os.devnull, 'w') # Suppresses stdout from loaded module.
                    
                    solution_output_string += "####################################"
                    solution_output_string += f"\nTesting with inputs:\n{copy_test_input}"

                    if not self.multi_input: # If the function only takes 1 argument
                        solution_output = solution_function(copy_test_input)
                    else: # If the function takes in multiple arguments -> unpack the list of inputs
                        solution_output = solution_function(*copy_test_input)

                    solution_output_string += "\n\nOutput from solution:\n"
                    solution_output_string += solution_output.__repr__() +"\n"

                    if type(test_input) == list:
                        copy_test_input = test_input[:]
                    else:
                        copy_test_input = test_input

                    submission_output_string += "####################################"
                    submission_output_string += f"\nTesting with inputs:\n{copy_test_input}"

                    if not self.multi_input: # If the function only takes 1 argument
                        submission_output = func_timeout(RUNTIME_LIMIT, submission_function, args=(copy_test_input,))
                    else: # If the function takes in multiple arguments -> unpack the list of inputs
                        submission_output = func_timeout(RUNTIME_LIMIT, submission_function, args=tuple(copy_test_input))

                    submission_output_string += f"\nOutput match solution: {submission_output == solution_output}".upper()
                    submission_output_string += "\n\nOutput from submission:\n"
                    submission_output_string += submission_output.__repr__() +"\n"

                    if suppress_stdout:
                        sys.stdout = sys.__stdout__# Unsuppresses stdout from loaded module.
        except FunctionTimedOut:
            if suppress_stdout:
                sys.stdout = sys.__stdout__# Unsuppresses stdout from loaded module.

            submission_output_string += "\n\nSubmission timeout! Took too long to run.\n\n"
            submission_output_string += traceback.format_exc()
        except subprocess.TimeoutExpired:
            if suppress_stdout:
                sys.stdout = sys.__stdout__# Unsuppresses stdout from loaded module.

            submission_output_string += "\n\nSubmission timeout! Took too long to run.\n\n"
            submission_output_string += traceback.format_exc()
        except Exception as e:
            if suppress_stdout:
                sys.stdout = sys.__stdout__# Unsuppresses stdout from loaded module.

            submission_output_string += "\n\nERROR encountered while testing submission.\n\n"
            submission_output_string += traceback.format_exc()
        finally:
            return submission_output_string, solution_output_string