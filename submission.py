from runnable import Runnable


class Submission(Runnable):
    def __init__(self, file_path, name, id, question_number, group_number):
        """
        Submission module class.
        Submission contains submitted code by student which will be tested against the solution by a Solution object.
        
        param: file_path: Full path of .py file.
        param: question_number: The corresponding question in the assessment with this Solution file.
        param: group_number: The corresponding group in the assessment with this Solution file.
        param: name: Full name of author of the Submission.
        param: id: Student ID of author of the Submission.
        """
        super().__init__(file_path, question_number, group_number)

        self.fullname = name
        self.id = id

        self.marked = False
        self.score = 0
    
    def __repr__(self) -> str:
        return f"{self.fullname} ({self.id}) - Group {self.group_number}: Question {self.question_number}" if not self.marked else f"{self.fullname} ({self.id}) - Group {self.group_number}: Question {self.group_number}. Score = {self.score}" 