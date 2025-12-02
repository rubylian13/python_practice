from turtle import Turtle


class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.penup()
        self.goto(0, -300)
        self.dx = 3  # x 軸移動速度
        self.dy = 3  # y 軸移動速度

    def move(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_wall(self):
        # 頂部碰撞
        if self.ycor() > 290:
            self.sety(290)
            self.dy *= -1
        # 左右兩側碰撞
        if self.xcor() > 390 or self.xcor() < -390:
            self.dx *= -1

    def bounce_paddle(self, paddle):
        if self.distance(paddle) < 60 and self.ycor() < -260 and self.dy < 0:
            self.sety(-260)
            self.dy *= -1

    def is_out_of_bounds(self):
        return self.ycor() < -300
