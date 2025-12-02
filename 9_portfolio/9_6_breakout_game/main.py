"""
Using Python Turtle, build a clone of the 80s hit game Breakout.
"""
import turtle
from turtle import Screen
from paddle import Paddle
from ball import Ball
from bricks import setup_bricks
import time

screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Breakout Game")
screen.tracer(0)

paddle = Paddle()
ball = Ball()
bricks = setup_bricks()
score = 0
screen.listen()
screen.onkeypress(paddle.go_left, "Left")
screen.onkeypress(paddle.go_right, "Right")

game_is_on = True
while game_is_on:
    time.sleep(0.01)  # 控制遊戲速度
    screen.update()

    ball.move()
    ball.bounce_wall()
    ball.bounce_paddle(paddle)

    for brick in bricks[:]:
        if ball.distance(brick) < 30:
            # 球反彈
            ball.dy *= -1

            brick.clear()
            brick.hideturtle()
            bricks.remove(brick)
            score += 10  # 增加分數

    # 檢查球是否出界
    if ball.is_out_of_bounds():
        game_is_on = False
        # 顯示遊戲結束訊息
        score_display = turtle.Turtle()
        score_display.hideturtle()
        score_display.color("white")
        score_display.write(f"Game Over. Score: {score}", align="center", font=("Courier", 24, "normal"))

    # 檢查是否所有磚塊都被清除
    if not bricks:
        game_is_on = False

        score_display = turtle.Turtle()
        score_display.hideturtle()
        score_display.color("white")
        score_display.write(f"You Win! Final Score: {score}", align="center", font=("Courier", 24, "normal"))

screen.exitonclick()