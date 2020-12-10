# imported modules
from turtle import Turtle, Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time
import keyboard






MAX_PLUS_POSITION = 280
MAX_MINUS_POSITION = -280

# screen setup
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My snake game")
screen.tracer(0)



def game():
    
    
    # Flags
    game_is_on = True

    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()

        

    screen.listen()
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")
    

    while game_is_on:
        screen.update()
        time.sleep(0.05)
        snake.move()

        # Detect collision with food.
        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()
            scoreboard.refresh_score()

        
        # Detect collision with wall.
        if snake.head.xcor() > MAX_PLUS_POSITION or snake.head.xcor() < MAX_MINUS_POSITION or snake.head.ycor() > MAX_PLUS_POSITION or snake.head.ycor() < MAX_MINUS_POSITION:
            game_is_on = False
            scoreboard.game_over()

            
            

        # Detect collision with tail.
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < 10:
                game_is_on = False
                scoreboard.game_over()
    while True:
        try:
            if keyboard.is_pressed('space'):
                food.visib()
                snake.visib()
                scoreboard.visib()
                break     
        except:
            break
    
                
                
game()
screen.listen()
screen.onkey(game, 'space')
screen.exitonclick()