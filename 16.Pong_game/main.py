# imported modules
from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard



# screen setup
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor('black')
screen.title('Pong')
screen.tracer(0)



# Construct paddle
player = Paddle(350, 0)
computer = Paddle(-350, 0)
ball = Ball()
scoreboard = Scoreboard()



# Screen key listen

screen.listen()
screen.onkeypress(player.move_up, "Up")
screen.onkeypress(player.move_down, "Down")
screen.onkeypress(computer.move_up, "w")
screen.onkeypress(computer.move_down, "s")

# flag
game_is_on = True
print(ball.xcor())
while game_is_on:
    screen.update()
    ball.move_ball()
    
    
    # Detect collision with wall
    if ball.ycor() >= 290 or ball.ycor() <= -290 :
        ball.bounce_y()

    # Detect collision with wall
    if ball.xcor() > 320 and ball.distance(player) < 50 or ball.distance(computer) < 50 and ball.xcor() > -320:
        ball.bounce_x()

    # Detect R paddle misses
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()
    
    # Detect L paddle misses
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()
    
    



screen.exitonclick()