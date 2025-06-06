from turtle import Turtle
from constants import FONT, SCOREBOARD_ALIGNMENT

class Scoreboard(Turtle):
    def __init__(self, position):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.goto(position)
        self.write(f"Score: {self.score}", align=SCOREBOARD_ALIGNMENT, font=FONT)
        
    def update_score(self):
        self.clear()
        self.score += 1
        self.write(f"Score: {self.score}", align=SCOREBOARD_ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write("Game Over", align=SCOREBOARD_ALIGNMENT, font=FONT)
        
        