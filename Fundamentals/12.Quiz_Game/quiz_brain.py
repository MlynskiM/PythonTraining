class QuizBrain:

    def __init__(self, questions_list):
        self.question_number = 0
        self.questions_list = questions_list
        self.score = 0

    def still_has_questions(self):
        """Checking question availability returning True or False"""
        return self.question_number < len(self.questions_list)
        
       

    def next_question(self):
        """Printing question from the list in range 1 to len(list)"""
        current_question = self.questions_list[self.question_number]
        self.question_number += 1
        player_answer = input(f"Q.{self.question_number} {current_question.text} (True/False): ")
        self.check_answer(player_answer, current_question.answer)
        

    
    def check_answer(self, user_answer, correct_answer):
        """Checking answer is it correct or not?"""
        if user_answer.lower() == correct_answer.lower():
            print("You got it right!")
            self.score += 1
        else:
            print("That's wrong.")
        print(f"The correct answer was: {correct_answer}.")
        print(f"Your current score is: {self.score}/{self.question_number} ")
        print("\n")