from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

question_bank=[]
for i in range (0, len(question_data)):
    question_bank.append(Question(question_data[i]['text'], question_data[i]['answer']))

quiz = QuizBrain(question_bank)
quiz.next_question()

while quiz.still_has_questions():
    quiz.next_question()

print("You'have completed the quiz")
print(f"Your final score was: {quiz.score}/{len(question_bank)}")