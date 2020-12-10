from turtle import Turtle
import time

ALIGNMENT = "center"
FONT = ("Courier", 16, "normal")

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.goto(0, 260)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    
    def refresh_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write(f"Game Over.", align=ALIGNMENT, font=FONT)
        self.goto(0, -25)
        self.write(f"Press space to play again", align=ALIGNMENT, font=FONT)
    
    def visib(self):
        self.hideturtle()
        self.clear()

        
