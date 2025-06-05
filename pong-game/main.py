from turtle import Screen
from paddle import Paddle
from constants import PADDLE_POSITION, WALL_COORDINATE, SCOREBOARD_POSITION
import time
from ball import Ball
from score import Scoreboard

screen = Screen()
screen.title("Pong Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

paddle_1 = Paddle(PADDLE_POSITION)
paddle_2 = Paddle((-PADDLE_POSITION[0], PADDLE_POSITION[1]))
ball = Ball()
score_1 = Scoreboard(SCOREBOARD_POSITION)
score_2 = Scoreboard((-SCOREBOARD_POSITION[0], SCOREBOARD_POSITION[1]))

screen.listen()
screen.onkey(paddle_1.move_up, "Up")
screen.onkey(paddle_1.move_down, "Down")
screen.onkey(paddle_2.move_up, "w")
screen.onkey(paddle_2.move_down, "s")

screen.update()

game_on = True
while game_on:
    score_1 = 0
    score_2 = 0
    time.sleep(0.1)
    screen.update()


    paddle_1.limit_movement()
    paddle_2.limit_movement()

    ball.move()

    if ball.ycor() > WALL_COORDINATE or ball.ycor() < -WALL_COORDINATE:
        ball.bounce_y()

    if ball.xcor() > PADDLE_POSITION[0]:
        ball.bounce_x()
        score_1.update_score()
        ball.reset_position()
    if ball.xcor() < -PADDLE_POSITION[0]:
        ball.bounce_x()
        score_2.update_score()
        ball.reset_position()

screen.exitonclick()