from turtle import Turtle


MOVE = 20



class Paddle(Turtle):

    def __init__(self, positionx, positiony):
        super().__init__()
        self.shape('square')
        self.shapesize(5.0, 1.0, 1)
        self.color('white')
        self.penup()
        self.goto(positionx, positiony)

    def move_up(self):
        new_y = self.ycor() + MOVE
        self.goto(self.xcor(), new_y)

    def move_down(self):
        new_y = self.ycor() - MOVE
        self.goto(self.xcor(), new_y)

        