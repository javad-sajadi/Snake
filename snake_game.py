"""
snake_game.py - Interactive Graphical Snake Game with Dynamic Boards & Multi-Level Difficulty
Author: Javad Sajadi
Repository: javad-sajadi/Snake

Features:
  - Customizable board dimensions (X, Y > 4)
  - 10 progressive difficulty and speed levels
  - Real-time sprite rendering using Tkinter and PIL
  - Save/Load game state functionality (savefile.txt)
  - In-game pause, score tracking, and victory conditions
"""

import os
import sys
import random
import numpy as np
from tkinter import Tk, Frame, Canvas, Label, Entry, Button, ALL, NW, N, CENTER, S
from PIL import Image, ImageTk


def action(X, Y, Z):
    """Calculates next coordinate based on direction vector."""
    if Z == "R":
        return [X + 1, Y]
    if Z == "L":
        return [X - 1, Y]
    if Z == "U":
        return [X, Y - 1]
    if Z == "D":
        return [X, Y + 1]
    return [X, Y]


class Apple:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def Location(self):
        return [self.X, self.Y]


class Snake:
    def __init__(self, X, Y, Z):
        self.length = 2
        A = action(X, Y, Z)
        self.location = [(A[0], A[1], 0), (X, Y, 1)]

    def Head(self):
        head = []
        for a, b, c in self.location:
            if c == 0 or c == 1:
                head.append([a, b])
        return head

    def Move(self, Z, apple):
        head = self.Head()
        next_move = action(head[0][0], head[0][1], Z)
        ate_apple = False
        if next_move != head[1]:
            new_location = [(next_move[0], next_move[1], 0)]
            for a, b, c in self.location:
                if c != self.length - 1 or next_move == apple:
                    new_location.append((a, b, c + 1))
            self.location = new_location
            if next_move == apple:
                self.length += 1
                ate_apple = True
        return ate_apple

    def In_Snake(self, A):
        for a, b, _ in self.location:
            if a == A[0] and b == A[1]:
                return True
        return False

    def Hit(self, X, Y):
        head = self.Head()
        # Wall collision check
        if head[0][0] >= X or head[0][0] <= 0 or head[0][1] >= Y or head[0][1] <= 0:
            return True
        # Self collision check
        for a, b, c in self.location:
            if a == head[0][0] and b == head[0][1] and c != 0:
                return True
        return False

    def Score(self):
        return (self.length - 2) * 10


class Board:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.Over = False
        rand_x = np.random.randint(2, max(3, X - 2))
        rand_y = np.random.randint(2, max(3, Y - 2))
        rand_dir = random.choice(["R", "L", "D", "U"])
        self.snake = Snake(rand_x, rand_y, rand_dir)
        self.apple_maker()

    def apple_maker(self):
        pos = [random.randint(1, self.X - 1), random.randint(1, self.Y - 1)]
        while self.snake.In_Snake(pos):
            pos = [random.randint(1, self.X - 1), random.randint(1, self.Y - 1)]
        self.apple = Apple(pos[0], pos[1])

    def Board_size(self):
        return self.X, self.Y

    def Snake_move(self, Z):
        ate = self.snake.Move(Z, self.apple.Location())
        if ate:
            self.apple_maker()
        if self.snake.Hit(self.X, self.Y):
            self.Over = True
        return ate

    def Game_Over(self):
        return self.Over

    def Snake_Location(self):
        return np.array([(a, b) for a, b, _ in self.snake.location])

    def set_snake_location(self, A):
        self.snake.location = [(a, b, j) for j, (a, b) in enumerate(A)]
        self.snake.length = len(A)

    def set_apple_location(self, A):
        self.apple = Apple(A[0], A[1])

    def Apple_Location(self):
        return self.apple.Location()

    def Score(self):
        return self.snake.Score()


class Config:
    BOARD_WIDTH = 550
    BOARD_HEIGHT = 550
    BASE_DELAY = 300


class SnakeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game - Interactive Python Edition")
        self.root.resizable(width=False, height=False)

        self.canvas = Canvas(root, width=Config.BOARD_WIDTH, height=Config.BOARD_HEIGHT,
                             background="#1a1a1a", highlightthickness=0)
        self.canvas.pack()

        self.A, self.B, self.C = 16, 16, 3
        self.pause = False
        self.key_move = "R"
        self.board = None

        self.load_images()
        self.init_menu()

    def load_images(self):
        """Loads game sprites or generates clean colored fallback shapes."""
        def load_or_placeholder(filename, color):
            if os.path.exists(filename):
                try:
                    img = Image.open(filename).resize((20, 20), Image.Resampling.LANCZOS)
                    return ImageTk.PhotoImage(img)
                except Exception:
                    pass
            img = Image.new("RGBA", (20, 20), color)
            return ImageTk.PhotoImage(img)

        self.head = load_or_placeholder("bodys2.png", (46, 204, 113, 255))
        self.body = load_or_placeholder("bodys.png", (39, 174, 96, 255))
        self.apple = load_or_placeholder("bodys3.png", (231, 76, 60, 255))
        self.wall = load_or_placeholder("wall.png", (127, 140, 141, 255))

    def init_menu(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(Config.BOARD_WIDTH / 2, 100, text="S N A K E   G A M E",
                                font=("Helvetica", 24, "bold"), fill="#2ecc71")
        self.canvas.create_text(Config.BOARD_WIDTH / 2, 140, text="Designed by Javad Sajadi",
                                font=("Helvetica", 11, "italic"), fill="#95a5a6")

        self.new_game_btn = Button(self.root, text="Start New Game", font=("Helvetica", 11),
                                   bg="#2ecc71", fg="black", padx=15, pady=5, command=self.show_new_game_form)
        self.new_game_btn.place(relx=0.5, rely=0.45, anchor=CENTER)

        has_save = os.path.exists("savefile.txt")
        self.load_game_btn = Button(self.root, text="Load Saved Game", font=("Helvetica", 11),
                                    bg="#3498db" if has_save else "#7f8c8d", fg="white",
                                    padx=15, pady=5, command=self.load_game,
                                    state="normal" if has_save else "disabled")
        self.load_game_btn.place(relx=0.5, rely=0.58, anchor=CENTER)

    def show_new_game_form(self):
        self.new_game_btn.destroy()
        self.load_game_btn.destroy()
        self.canvas.delete(ALL)

        self.canvas.create_text(Config.BOARD_WIDTH / 2, 60, text="Game Settings",
                                font=("Helvetica", 20, "bold"), fill="white")

        self.l_x = Label(self.root, text="Grid Width (X > 4):", bg="#1a1a1a", fg="white")
        self.l_x.place(relx=0.5, rely=0.22, anchor=CENTER)
        self.e_x = Entry(self.root, justify="center")
        self.e_x.insert(0, "16")
        self.e_x.place(relx=0.5, rely=0.28, anchor=CENTER)

        self.l_y = Label(self.root, text="Grid Height (Y > 4):", bg="#1a1a1a", fg="white")
        self.l_y.place(relx=0.5, rely=0.36, anchor=CENTER)
        self.e_y = Entry(self.root, justify="center")
        self.e_y.insert(0, "16")
        self.e_y.place(relx=0.5, rely=0.42, anchor=CENTER)

        self.l_level = Label(self.root, text="Difficulty Level (1 - 10):", bg="#1a1a1a", fg="white")
        self.l_level.place(relx=0.5, rely=0.50, anchor=CENTER)
        self.e_level = Entry(self.root, justify="center")
        self.e_level.insert(0, "5")
        self.e_level.place(relx=0.5, rely=0.56, anchor=CENTER)

        self.start_btn = Button(self.root, text="Launch Game", bg="#2ecc71", font=("Helvetica", 11, "bold"),
                                padx=20, pady=5, command=self.start_game)
        self.start_btn.place(relx=0.5, rely=0.68, anchor=CENTER)

    def start_game(self):
        try:
            self.A = max(5, int(self.e_x.get()))
            self.B = max(5, int(self.e_y.get()))
            self.C = max(1, min(10, int(self.e_level.get())))
        except ValueError:
            self.A, self.B, self.C = 16, 16, 5

        for widget in [self.l_x, self.e_x, self.l_y, self.e_y, self.l_level, self.e_level, self.start_btn]:
            widget.destroy()

        self.key_move = "R"
        self.board = Board(self.A, self.B)
        self.bind_events()
        self.run_loop()

    def bind_events(self):
        self.root.bind_all("<Key>", self.on_key_pressed)

    def on_key_pressed(self, e):
        k = e.keysym
        if k in ("Left", "a", "A") and self.key_move != "R":
            self.key_move = "L"
        elif k in ("Right", "d", "D") and self.key_move != "L":
            self.key_move = "R"
        elif k in ("Up", "w", "W") and self.key_move != "D":
            self.key_move = "U"
        elif k in ("Down", "s", "S") and self.key_move != "U":
            self.key_move = "D"
        elif k in ("p", "P", "space"):
            self.toggle_pause()

    def toggle_pause(self):
        self.pause = not self.pause
        if not self.pause:
            self.run_loop()
        else:
            self.render_pause_menu()

    def run_loop(self):
        if self.pause:
            return
        if not self.board.Game_Over():
            self.board.Snake_move(self.key_move)
            self.render()
            if self.board.Game_Over():
                self.render_game_over()
            else:
                delay = int(Config.BASE_DELAY * (11 - self.C) / 10)
                self.canvas.after(max(40, delay), self.run_loop)
        else:
            self.render_game_over()

    def render(self):
        self.canvas.delete(ALL)
        offset_x = 30
        offset_y = 40
        cell_size = 22

        # Header Info
        self.canvas.create_text(Config.BOARD_WIDTH / 2, 20,
                                text=f"Score: {self.board.Score()}   |   Level: {self.C}   |   (P: Pause/Save)",
                                font=("Helvetica", 11, "bold"), fill="white")

        # Walls
        X, Y = self.board.Board_size()
        for i in range(X + 1):
            self.canvas.create_image(i * cell_size + offset_x, 0 * cell_size + offset_y, image=self.wall, anchor=NW)
            self.canvas.create_image(i * cell_size + offset_x, Y * cell_size + offset_y, image=self.wall, anchor=NW)
        for i in range(Y):
            self.canvas.create_image(0 * cell_size + offset_x, i * cell_size + offset_y, image=self.wall, anchor=NW)
            self.canvas.create_image(X * cell_size + offset_x, i * cell_size + offset_y, image=self.wall, anchor=NW)

        # Apple
        ax, ay = self.board.Apple_Location()
        self.canvas.create_image(ax * cell_size + offset_x, ay * cell_size + offset_y, image=self.apple, anchor=NW)

        # Snake
        snake_locs = self.board.Snake_Location()
        if len(snake_locs) > 0:
            self.canvas.create_image(snake_locs[0][0] * cell_size + offset_x,
                                     snake_locs[0][1] * cell_size + offset_y, image=self.head, anchor=NW)
            for seg in snake_locs[1:]:
                self.canvas.create_image(seg[0] * cell_size + offset_x,
                                         seg[1] * cell_size + offset_y, image=self.body, anchor=NW)

    def render_pause_menu(self):
        self.save_btn = Button(self.root, text="Save Game", bg="#3498db", fg="white", font=("Helvetica", 11),
                               padx=15, pady=5, command=self.save_game)
        self.save_btn.place(relx=0.5, rely=0.45, anchor=CENTER)

        self.resume_btn = Button(self.root, text="Resume Game", bg="#2ecc71", fg="black", font=("Helvetica", 11),
                                 padx=15, pady=5, command=self.resume_game)
        self.resume_btn.place(relx=0.5, rely=0.57, anchor=CENTER)

    def save_game(self):
        with open("savefile.txt", "w") as f:
            f.write(f"{self.A} {self.B} {self.C} ")
            for i, j in self.board.Snake_Location():
                f.write(f"{i} {j} ")
            ax, ay = self.board.Apple_Location()
            f.write(f"{ax} {ay}\n")
        print("Game state saved to savefile.txt.")
        self.resume_game()

    def resume_game(self):
        self.save_btn.destroy()
        self.resume_btn.destroy()
        self.pause = False
        self.run_loop()

    def load_game(self):
        self.new_game_btn.destroy()
        self.load_game_btn.destroy()
        with open("savefile.txt", "r") as f:
            tokens = f.read().strip().split()
        self.A, self.B, self.C = int(tokens[0]), int(tokens[1]), int(tokens[2])
        snake_coords = []
        for i in range(3, len(tokens) - 2, 2):
            snake_coords.append([int(tokens[i]), int(tokens[i + 1])])
        apple_pos = [int(tokens[-2]), int(tokens[-1])]

        self.board = Board(self.A, self.B)
        self.board.set_snake_location(snake_coords)
        self.board.set_apple_location(apple_pos)
        self.key_move = "R"
        self.bind_events()
        self.run_loop()

    def render_game_over(self):
        self.canvas.create_rectangle(Config.BOARD_WIDTH / 2 - 150, Config.BOARD_HEIGHT / 2 - 60,
                                     Config.BOARD_WIDTH / 2 + 150, Config.BOARD_HEIGHT / 2 + 60,
                                     fill="#c0392b", outline="white", width=2)
        self.canvas.create_text(Config.BOARD_WIDTH / 2, Config.BOARD_HEIGHT / 2 - 20,
                                text="GAME OVER", font=("Helvetica", 18, "bold"), fill="white")
        self.canvas.create_text(Config.BOARD_WIDTH / 2, Config.BOARD_HEIGHT / 2 + 15,
                                text=f"Final Score: {self.board.Score()}  (Level {self.C})",
                                font=("Helvetica", 12), fill="white")


if __name__ == "__main__":
    root = Tk()
    app = SnakeWindow(root)
    root.mainloop()
