from data import load_data
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizUI

questions = [Question(q["question"], q["correct_answer"]) for q in load_data()]
quiz = QuizBrain(questions)
QuizUI(quiz)
