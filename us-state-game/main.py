import turtle
import pandas as pd
import os

data = pd.read_csv("us-state-game/50_states.csv")
all_states = data["state"].to_list()
# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

screen = turtle.Screen()
screen.title("U.S. States Game")
# Use absolute path to the image file
image = os.path.join(script_dir, "blank_states_img.gif")
screen.addshape(image)
turtle.shape(image)


guessed_states = []

while len(guessed_states) < 50:
    answer = screen.textinput(title=f"{len(guessed_states)}/50 States Correct", prompt="What's another state's name?").title()


    if answer in all_states:
        guessed_states.append(answer)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data["state"] == answer]   
        t.goto(state_data.x.item(), state_data.y.item())
        t.write(answer)

    if answer == "Exit":
        missing_states = [state for state in all_states if state not in guessed_states]
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv("us-state-game/states_to_learn.csv")
        break



screen.exitonclick()


# we need to see if the answer is a corresponds to any of the states in the data frame

