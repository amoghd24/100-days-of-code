import random
from turtle import Turtle, Screen
import random

is_race_on = False

screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
## starting point needs to be -60
y_positions = [(i * 30) - 90 for i in range(len(colors))] ###lets add first y position as -60


all_turtles = []

for turtle_index in range(len(colors)):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_index])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=y_positions[turtle_index])
    all_turtles.append(new_turtle)

if user_bet:
    is_race_on = True
while is_race_on:
    for turtle in all_turtles:
       ###the turtle moves forward by random number between 0 and 10
       random_distance = random.randint(0, 10)
       turtle.forward(random_distance)
       if turtle.xcor() > 230:
           is_race_on = False
           winner_color = turtle.pencolor()
           if winner_color == user_bet:
               print(f"You've won! The {winner_color} turtle is the winner!")
           else:
               print(f"You've lost! The {winner_color} turtle is the winner!")
           



def move_forwards():
    for turtle in all_turtles:
        turtle.forward(10)

def move_backwards():
    for turtle in all_turtles:
        turtle.backward(10)

def turn_left():
    for turtle in all_turtles:
        new_heading = turtle.heading() + 10
        turtle.setheading(new_heading)

def turn_right():
    for turtle in all_turtles:
        new_heading = turtle.heading() - 10
        turtle.setheading(new_heading)


def clear():
    for turtle in all_turtles:
        turtle.clear()
        turtle.penup()
        turtle.home()
        turtle.pendown()

screen.listen()
screen.onkey(key="w", fun=move_forwards)
screen.onkey(key="s", fun=move_backwards)
screen.onkey(key="a", fun=turn_left)
screen.onkey(key="d", fun=turn_right)
screen.onkey(key="c", fun=clear)
#screen.exitonclick()

