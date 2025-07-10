from tkinter import *
import copy
from time import sleep

# Board and knight settings
N = 8
size_square = 80
delay_ = 0.5
Letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Allowed knight moves
allowedMoves = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

# Globals
lookahead = 1
previous_positions = []


def create_gui_root():
    global root, canvas
    root = Tk()
    root.title("Group 2 - Knight’s Tour Problem")

    frame = Frame(root)
    frame.pack()

    # Title and buttons
    title_label = Label(frame, text="Welcome to the Knight’s Tour\nPick an Option:", font=("Arial", 16))
    title_label.pack()

    step1_button = Button(frame, text='One step ahead', command=set_depth_one)
    step1_button.pack(side=TOP, padx=10, pady=5)

    step2_button = Button(frame, text='Two steps ahead', command=set_depth_two)
    step2_button.pack(side=TOP, padx=10, pady=10)

    # Canvas for chessboard and graphics
    canvas = Canvas(frame, width=N * size_square + 250, height=N * size_square + 50)
    canvas.pack(expand=True, fill="both", padx=(250, 0))

    return root, canvas, step1_button, step2_button


# Step depth control
def set_depth_one():
    global lookahead
    lookahead = 1


def set_depth_two():
    global lookahead
    lookahead = 2


def handle_click(event):
    x, y = event.x, event.y
    if 0 < x < N * size_square and 0 < y < N * size_square:
        start_knight_tour(y // size_square, x // size_square)


def create_board_canvas(canvas):
    for i in range(N):
        for j in range(N):
            color = "#EEEED2" if (i + j) % 2 == 0 else "#769656"
            canvas.create_rectangle(size_square * j, size_square * i,
                                    size_square * (j + 1), size_square * (i + 1), fill=color)
    canvas.update_idletasks()


def update_board_display(board, canvas):
    newly_created_items = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                continue
            if board[i][j] in Letters:
                a, b = highlight_square(canvas, j * size_square, i * size_square, 'red', board[i][j])
                newly_created_items += [a, b]
            elif type(board[i][j]) == int:
                a, b = draw_circle_with_number(canvas, board[i][j], j * size_square, i * size_square)
                newly_created_items += [a, b]
            elif len(str(board[i][j])) == 2 and board[i][j][0] in Letters:
                a, b = highlight_square(canvas, j * size_square, i * size_square, 'yellow', board[i][j])
                newly_created_items += [a, b]
    draw_arrows(canvas)
    canvas.update_idletasks()


def draw_arrows(canvas):
    canvas.delete('arrow')
    if len(previous_positions) < 2:
        return
    (x1, y1), (x2, y2) = previous_positions[-2], previous_positions[-1]
    start_x = y1 * size_square + size_square // 2
    start_y = x1 * size_square + size_square // 2
    mid_x = y2 * size_square + size_square // 2
    mid_y = x2 * size_square + size_square // 2

    if abs(x2 - x1) == 2:
        corner_y = start_y
        corner_x = mid_x
    else:
        corner_x = start_x
        corner_y = mid_y

    canvas.create_line(start_x, start_y, corner_x, corner_y, fill='red', width=2, tags='arrow')
    canvas.create_line(corner_x, corner_y, mid_x, mid_y, fill='red', width=2, arrow=LAST, tags='arrow')


def highlight_square(canvas, x, y, color, text):
    square = canvas.create_rectangle(x, y, x + size_square, y + size_square, fill=color)
    text = canvas.create_text(x + (size_square / 2), y + (size_square / 8),
                              text=text, font=("Arial", int(size_square / 2)), anchor="n")
    return square, text


def draw_circle_with_number(canvas, number, x, y):
    oval = canvas.create_oval(x, y, x + size_square, y + size_square, fill='#4A4747')
    text = canvas.create_text(x + (size_square / 2), y + (size_square / 8), text=str(number),
                              font=("Arial", int(size_square / 2)), anchor="n", fill='white')
    return oval, text


def find_valid_moves(board, knight_x, knight_y):
    valid_moves = []
    for direction in allowedMoves:
        n_x, n_y = knight_x + direction[0], knight_y + direction[1]
        if 0 <= n_x < N and 0 <= n_y < N and board[n_x][n_y] == 0:
            valid_moves.append([n_x, n_y])
    return valid_moves


def update_moves_list(display_moves):
    global canvas
    canvas.create_text(605, 10, text="Number of available moves:", font=("Arial", 12))
    for index, move in enumerate(display_moves):
        x = 680
        y = 50 + index * 20
        canvas.create_text(x, y, text=move, font=("Arial", 12), justify="center")


def calculate_next_moves_one_step(board):
    display_moves = []
    x, y, largest_number = 0, 0, 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > largest_number:
                x, y = i, j
                largest_number = board[i][j]
    valid_moves = find_valid_moves(board, x, y)
    for i in range(len(valid_moves)):
        board[valid_moves[i][0]][valid_moves[i][1]] = Letters[i]
    for i in range(len(valid_moves)):
        move_text = f"{Letters[i]}: {len(find_valid_moves(board, valid_moves[i][0], valid_moves[i][1]))}"
        display_moves.append(move_text)
    if lookahead == 1:
        update_moves_list(display_moves)
    return board


def calculate_next_moves_two_steps(board):
    display_moves = []
    depth_one_board = calculate_next_moves_one_step(board)
    all_moves = []
    for i in range(len(depth_one_board)):
        for j in range(len(depth_one_board[i])):
            if depth_one_board[i][j] in Letters:
                altered_board = copy.deepcopy(depth_one_board)
                altered_board[i][j] = 65
                all_moves.append([depth_one_board[i][j]] + find_valid_moves(altered_board, i, j))
    for i in range(len(all_moves)):
        for j in range(1, len(all_moves[i])):
            if depth_one_board[all_moves[i][j][0]][all_moves[i][j][1]] == 0:
                depth_one_board[all_moves[i][j][0]][all_moves[i][j][1]] = str(all_moves[i][0] + str(j))
    for i in range(len(depth_one_board)):
        for j in range(len(depth_one_board[i])):
            if not isinstance(depth_one_board[i][j], int) and depth_one_board[i][j] not in Letters:
                available_moves = len(find_valid_moves(depth_one_board, i, j))
                move = f"{depth_one_board[i][j]}: {available_moves}\n"
                display_moves.append(move)
    update_moves_list(display_moves)
    return depth_one_board


def make_best_move(board):
    largest_number = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if isinstance(board[i][j], int) and board[i][j] > largest_number:
                largest_number = board[i][j]
    one_step_moves, two_step_moves = [], []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if isinstance(board[i][j], str) and len(board[i][j]) == 2:
                two_step_moves.append(board[i][j])
            elif board[i][j] in Letters:
                one_step_moves.append(board[i][j])
    if not one_step_moves:
        return False
    max_moves = -1
    best_letter = ''
    if two_step_moves:
        move_count = {letter: 0 for letter in Letters}
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] in two_step_moves:
                    moves = len(find_valid_moves(board, i, j))
                    letter = board[i][j][0]
                    move_count[letter] += moves
                    if move_count[letter] > max_moves:
                        max_moves = move_count[letter]
                        best_letter = letter
    else:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] in one_step_moves:
                    moves = len(find_valid_moves(board, i, j))
                    if moves > max_moves:
                        max_moves = moves
                        best_letter = board[i][j]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == best_letter:
                board[i][j] = largest_number + 1
                previous_positions.append((i, j))
            elif isinstance(board[i][j], str):
                board[i][j] = 0
    return board


def start_knight_tour(start_x, start_y):
    global previous_positions
    previous_positions = [(start_x, start_y)]
    canvas.delete('all')
    create_board_canvas(canvas)
    board = [[0 for _ in range(N)] for _ in range(N)]
    board[start_x][start_y] = 1
    while board:
        if lookahead == 1:
            board = calculate_next_moves_one_step(copy.deepcopy(board))
        else:
            board = calculate_next_moves_two_steps(copy.deepcopy(board))
        update_board_display(board, canvas)
        sleep(delay_)
        board = make_best_move(copy.deepcopy(board))
        if board is not False:
            canvas.delete('all')
            create_board_canvas(canvas)
            update_board_display(board, canvas)
        else:
            print('No more valid moves!')
            sleep(delay_)


# Run the application
root, canvas, step1_button, step2_button = create_gui_root()
create_board_canvas(canvas)
canvas.bind("<Button-1>", handle_click)
root.mainloop()
