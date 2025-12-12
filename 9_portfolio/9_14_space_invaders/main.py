import turtle
import math
import random
import time

screen = turtle.Screen()
screen.title("Space Invaders: Shapes & Lives Version")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

score = 0
player_lives = 3

# 分數
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(-380, 260)

# 生命值
lives_pen = turtle.Turtle()
lives_pen.speed(0)
lives_pen.color("green")
lives_pen.penup()
lives_pen.hideturtle()
lives_pen.goto(280, 260)

# Game Over
game_over_pen = turtle.Turtle()
game_over_pen.speed(0)
game_over_pen.color("red")
game_over_pen.penup()
game_over_pen.hideturtle()
game_over_pen.goto(0, 0)

# Player
player = turtle.Turtle()
player.speed(0)
player.shape("triangle")
player.color("yellow")
player.penup()
player.setheading(90)
player.goto(0, -250)
player_speed = 20

# Enemies
number_of_enemies = 10
enemies = []
for _ in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.speed(0)
    enemy.shape("circle")
    enemy.color("red")
    enemy.penup()
    x = random.randint(-200, 200)
    y = random.randint(150, 250)
    enemy.goto(x, y)

enemy_speed = 1.5

# Bullet
bullet = turtle.Turtle()
bullet.speed(0)
bullet.shape("triangle")
bullet.color("white")
bullet.shapesize(0.5, 0.5)
bullet.penup()
bullet.setheading(90)
bullet.goto(0, -400)
bullet.hideturtle()

bullet_speed = 25
bullet_state = "ready"


def update_scoreboard():
    score_pen.clear()
    score_pen.write("Score: {}".format(score), align="left", font=("Courier", 14, "bold"))


def update_livesboard():
    lives_pen.clear()
    if player_lives == 1:
        lives_pen.color("red")
    else:
        lives_pen.color("green")
    lives_pen.write("Lives: {}".format(player_lives), align="right", font=("Courier", 14, "bold"))


def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -380:
        x = -380
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x > 380:
        x = 380
    player.setx(x)


def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.goto(x, y)
        bullet.showturtle()


def is_collision(t1, t2):
    # 距離
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 25:
        return True
    else:
        return False


def reset_positions():
    player.goto(0, -250)
    bullet.hideturtle()
    global bullet_state
    bullet_state = "ready"

    for enemy in enemies:
        x = random.randint(-200, 200)
        y = random.randint(150, 250)
        enemy.goto(x, y)

    screen.update()
    time.sleep(1)


screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# 初始顯示
update_scoreboard()
update_livesboard()

game_is_on = True
while game_is_on:
    screen.update()

    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"

    hit_edge = False
    for enemy in enemies:
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        if enemy.xcor() > 380 or enemy.xcor() < -380:
            hit_edge = True

        if is_collision(bullet, enemy):
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.goto(0, -400)

            x = random.randint(-200, 200)
            y = random.randint(150, 250)
            enemy.goto(x, y)

            score += 10
            update_scoreboard()

        if is_collision(player, enemy) or enemy.ycor() < -240:
            player_lives -= 1
            update_livesboard()

            if player_lives > 0:
                print(f"哎呀！被擊中了。剩餘生命: {player_lives}")
                reset_positions()  # 呼叫重置函數
                break
            else:
                game_is_on = False
                game_over_pen.write("GAME OVER", align="center", font=("Courier", 30, "bold"))
                break

    if hit_edge:
        enemy_speed *= -1
        for e in enemies:
            y = e.ycor()
            y -= 40
            e.sety(y)

screen.mainloop()