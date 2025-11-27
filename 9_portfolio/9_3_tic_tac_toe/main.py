"""
Build a GUI version of the Tic Tac Toe game.
"""
import tkinter as tk
from tkinter import messagebox

def draw_board(canvas):
    """在 Canvas 上繪製 3x3 的網格線"""
    # 繪製垂直線：1/3 處的線 & 2/3 處的線 (x1, y1, x2, x2, 寬度, 線條顏色)
    canvas.create_line(CELL_SIZE, 0, CELL_SIZE, CANVAS_SIZE, width=2, fill=LINE_COLOR)
    canvas.create_line(CELL_SIZE * 2, 0, CELL_SIZE * 2, CANVAS_SIZE, width=2, fill=LINE_COLOR)

    # 繪製水平線：1/3 處的線 & 2/3 處的線 (x1, y1, x2, x2, 寬度, 線條顏色)
    canvas.create_line(0, CELL_SIZE, CANVAS_SIZE, CELL_SIZE, width=2, fill=LINE_COLOR)
    canvas.create_line(0, CELL_SIZE * 2, CANVAS_SIZE, CELL_SIZE * 2, width=2, fill=LINE_COLOR)

def draw_move(canvas, row, col, player):
    # 計算格子邊界
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    # XO和線條的邊距
    padding = 10

    if player == "X":
        # 繪製 X (兩條斜線)
        canvas.create_line(x1 + padding, y1 + padding, x2 - padding, y2 - padding,
                           width=7, fill=PLAYER_X_COLOR)
        canvas.create_line(x1 + padding, y2 - padding, x2 - padding, y1 + padding,
                           width=7, fill=PLAYER_X_COLOR)
    elif player == "O":
        # 繪製 O (一個圓形/橢圓)
        canvas.create_oval(x1 + padding, y1 + padding, x2 - padding, y2 - padding,
                           width=7, outline=PLAYER_O_COLOR)

def handle_click(event):
    global current_player

    # 根據點擊座標 (event.x, event.y) 計算 row 和 col
    col = int(event.x // CELL_SIZE)
    row = int(event.y // CELL_SIZE)

    # 檢查是否在有效的 3x3 範圍內
    if 0 <= row < 3 and 0 <= col < 3:
        # 檢查該格子是否為空
        if board[row][col] == "":
            board[row][col] = current_player
            # 繪製棋子
            draw_move(canvas, row, col, current_player)
            # 繪製最後X或O
            window.update()

            # 檢查遊戲狀態
            if check_win(current_player):
                messagebox.showinfo("Game Over", f"{current_player} Win！")
            elif check_draw():
                messagebox.showinfo("Game Over", "Draw！")
            else:
                # 切換玩家並更新label
                current_player = "O" if current_player == "X" else "X"
                label_status.config(text=f"輪到玩家: {current_player}")

def reset_game():
    global current_player, board

    current_player = "X"
    board = [[""] * 3 for _ in range(3)]
    canvas.delete("all")
    draw_board(canvas)
    canvas.bind("<Button-1>", handle_click)

def check_win(player):
    # 檢查行
    for r in range(3):
        if all(board[r][c] == player for c in range(3)):
            return True

    # 檢查列
    for c in range(3):
        if all(board[r][c] == player for r in range(3)):
            return True

    # 檢查對角線
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

def check_draw():
    return all(board[r][c] != "" for r in range(3) for c in range(3))


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Tic Tac Toe")
window.config(padx=50, pady=50)

CANVAS_SIZE = 350
canvas = tk.Canvas(height=CANVAS_SIZE, width=CANVAS_SIZE, bg='#7FFFD4')
CELL_SIZE = CANVAS_SIZE / 3
canvas.grid(row=1, column=1)
LINE_COLOR = "grey"
PLAYER_X_COLOR = "black"
PLAYER_O_COLOR = "white"

current_player = "X"
label_status = tk.Label(window, text=f"Player: {current_player}", font=('Arial', 14))
label_status.grid(row=0, column=0, columnspan=2, pady=10)
board = [[""] * 3 for _ in range(3)]  # 3x3 的空棋盤資料

# 繪製初始棋盤
draw_board(canvas)
canvas.bind("<Button-1>", handle_click)

# Buttons
reset_button = tk.Button(text="Reset", width=36, command=reset_game)
reset_button.grid(row=4, column=1, columnspan=2)

window.mainloop()