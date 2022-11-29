class Submission:
    def __init__(self, path, name, id, question_number, group_number):
        self.file_path = path
        self.fullname = name
        self.id = id
        self.question_number = question_number
        self.group_number = group_number

        self.marked = False
        self.score = 0

    def __repr__(self) -> str:
        return f"{self.fullname} ({self.id}) - Group {self.group_number}: Question {self.question_number}" if not self.marked else f"{self.fullname} ({self.id}) - Group {self.group_number}: Question {self.group_number}. Score = {self.score}" 