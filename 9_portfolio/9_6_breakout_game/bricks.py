import turtle

BRICK_WIDTH = 75
BRICK_HEIGHT = 20
ROWS = 7
COLS = 10
START_Y = 250
START_X = -370
BRICK_COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "white"]


def setup_bricks():
    bricks = []
    for row in range(ROWS):
        for col in range(COLS):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.color(BRICK_COLORS[row % len(BRICK_COLORS)])
            brick.shapesize(stretch_wid=BRICK_HEIGHT / 20, stretch_len=BRICK_WIDTH / 20)  # 預設形狀是 20x20
            brick.penup()
            x = START_X + col * (BRICK_WIDTH + 5)  # 5 像素的間隔
            y = START_Y - row * (BRICK_HEIGHT + 5)
            brick.goto(x, y)
            bricks.append(brick)
    return bricks