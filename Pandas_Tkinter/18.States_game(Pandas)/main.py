#  imported modules
import turtle 
import pandas

# Screen setup
screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.setup(width=730, height=495)
screen.addshape(image)
turtle.shape(image)


# reading csv file by pandas
data = pandas.read_csv("50_states.csv")
data_state_list = data["state"].to_list()

guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct", prompt="What's another state name?").title()
    
    if answer_state == "Exit":
        missing_states = []
        for state in data_state_list:
            if state not in guessed_states:
                missing_states.append(state)
        # creating new DataFrame pandas and creating csv file with exported data
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break

# Verifying correctness of answer
    if answer_state in data_state_list:
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == answer_state]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(answer_state)

