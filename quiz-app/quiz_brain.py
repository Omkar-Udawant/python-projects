import html

class QuizBrain:
    def __init__(self, questions):
        self.questions = questions
        self.index = 0
        self.score = 0

    def has_next(self):
        return self.index < len(self.questions)

    def next_question(self):
        q = self.questions[self.index]
        self.index += 1
        return f"Q{self.index}. {html.unescape(q.text)}"

    def check(self, answer):
        correct = self.questions[self.index - 1].answer == answer
        if correct:
            self.score += 1
        return correct
