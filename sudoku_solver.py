import tkinter as tk
from tkinter import Menu, Entry, Button, Label
import random

def generate_initial_board():
    board = [[0]*9 for _ in range(9)]
    for _ in range(random.randint(22, 26)):
        row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
        while not is_valid(board, num, (row, col)):
            row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
        board[row][col] = num
    return board

def is_valid(board, num, pos):
    row, col = pos
    return not (num in board[row] or num in [board[i][col] for i in range(9)] 
            or num in [board[i][j] for i in range(row//3*3, row//3*3+3) for j in range(col//3*3, col//3*3+3)])

def solve_sudoku(board):
    empty_spot = find_empty(board)
    if not empty_spot:
        return True
    row, col = empty_spot
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_step():
    for i in range(9):
        for j in range(9):
            board[i][j] = int(entries[i][j].get()) if entries[i][j].get() else 0
    if solve_sudoku(board):
        update_gui()
    else:
        label.configure(text="No solution exists", fg="darkred", bg="white")

def is_valid_input():
    for i in range(9):
        for j in range(9):
            entry = entries[i][j]
            value = entry.get()
            if value != '':
                if not value.isdigit() or int(value) < 1 or int(value) > 9:
                    return False

                for k in range(9):
                    if k != i and board[k][j] == int(value):
                        return False
                    if k != j and board[i][k] == int(value):
                        return False

                box_x = j // 3
                box_y = i // 3
                for x in range(box_y*3, box_y*3 + 3):
                    for y in range(box_x*3, box_x*3 + 3):
                        if (x != i or y != j) and board[x][y] == int(value):
                            return False

    return True

def solve():
    solve_button.configure(state="disabled")
    if not is_valid_input():
        label.configure(text="Invalid input!!", fg="darkred")
        return
    for i in range(9):
        for j in range(9):
            board[i][j] = int(entries[i][j].get()) if entries[i][j].get() else 0
    if solve_sudoku(board):
        update_gui()
    else:
        label.configure(text="No solution exists", fg="darkred", bg="white")

def update_gui():
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(board[i][j]) if board[i][j] != 0 else '')

def play_again():
    global board
    board = generate_initial_board()
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(board[i][j]) if board[i][j] != 0 else '')
    label.configure(text="")
    solve_button.configure(state='normal')

def generate_level_board(min_count, max_count):
    board = [[0]*9 for _ in range(9)]
    for _ in range(random.randint(min_count, max_count)):  
        row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
        while not is_valid(board, num, (row, col)):
            row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
        board[row][col] = num
    return board

def choose_level(difficulty):
    if difficulty == 'beginner':
        min_count, max_count = 20, 30
    elif difficulty == 'intermediate':
        min_count, max_count = 15, 20
    elif difficulty == 'expert':
        min_count, max_count = 5, 10
    else:
        raise ValueError("Invalid difficulty level")

    global board
    board = generate_level_board(min_count, max_count)
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(board[i][j]) if board[i][j] != 0 else '')
    label.configure(text="")
    solve_button.configure(state='normal')

root = tk.Tk()
root.title("Sudoku Solver")
root.configure(bg='lightblue') 

board = generate_initial_board()
entries = [[Entry(root, width=2, font=('Arial', 20), justify='center',highlightthickness=2) for _ in range(9)] for _ in range(9)]

for i in range(9):
    for j in range(9):
        entries[i][j].grid(row=i, column=j)
        entries[i][j].insert(0, str(board[i][j]) if board[i][j] != 0 else '')
        if i % 3 == 0:
            entries[i][j].grid(pady=(2,0))
        if j % 3 == 0:
            entries[i][j].grid(padx=(2,0))

solve_button = Button(root, text="Solve", command=solve)
solve_button.grid(row=10, columnspan=9)

play_again_button = Button(root, text="Play Again", command=play_again)
play_again_button.grid(row=11, columnspan=9)

exit_button = Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=12, columnspan=14)

label = Label(root, text="")
label.grid(row=9, columnspan=9)

m = Menu(root)
root.config(menu=m)

lev = Menu(m)
m.add_cascade(label="Level", menu=lev)
lev.add_command(label="Beginner", command=lambda: choose_level('beginner'))
lev.add_command(label="Intermediate", command=lambda: choose_level('intermediate'))
lev.add_command(label="Expert", command=lambda: choose_level('expert'))

root.mainloop()
