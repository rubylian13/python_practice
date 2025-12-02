from turtle import Turtle


class Paddle(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=5)  # 伸展寬度為 1, 長度為 5
        self.penup()
        self.goto(0, -280)  # 放置在螢幕底部

    def go_left(self):
        new_x = self.xcor() - 20
        if new_x > -380:
            self.setx(new_x)

    def go_right(self):
        new_x = self.xcor() + 20
        if new_x < 360:
            self.setx(new_x)
