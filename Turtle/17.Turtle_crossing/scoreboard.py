from turtle import Turtle

FONT = ("Courier", 16, "normal")


class Scoreboard(Turtle):
    
    def __init__(self):
        super().__init__()
        self.level = 1
        self.color("black")
        self.penup()
        self.hideturtle()
        self.setposition(-290, 270)
        self.update_scoreboard()
    
    def update_scoreboard(self):
        self.write(f"Level: {self.level}", align="left", font=FONT)
    
    def refresh_score(self):
        self.level += 1
        self.clear()
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write(f"Game Over.", align="center", font=FONT)
        
