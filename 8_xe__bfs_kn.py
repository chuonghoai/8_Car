import time
import tkinter as tk
import random
from collections import deque

class eight_rooks:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Rooks")
        self.root.config(bg="lightgray")
        self.n = 8
        self.pos_rook = [[0] * self.n for _ in range(self.n)]

        frame_left = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_left.grid(row=0, column=0, padx=10, pady=10)
        frame_right = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_right.grid(row=0, column=1, padx=10, pady=10)

        self.buttons_l = self.create_widget(frame_left, False)
        self.bfs(random.randint(0, 7), random.randint(0, 7))
        self.buttons_r = self.create_widget(frame_right, True)

    def create_widget(self, frame, show_rook):
        buttons = []
        for i in range(self.n):
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "lightpink"
                text = "R" if show_rook and self.pos_rook[i][j] == 1 else ""
                btn = tk.Label(frame, width=4, height=2, bg=color, text=text,
                               font=("Arial", 20), borderwidth=1, relief="flat")
                btn.grid(row=i, column=j, padx=1, pady=1)
                buttons.append(btn)
        return buttons

    def bfs(self, row_start, col_start):
        q = deque()
        q.append([(row_start, col_start)])
        
        while q:
            state = q.popleft()
            if len(state) == self.n: 
                for r, c in state:
                    self.pos_rook[r][c] = 1
                return

            for row in range(self.n):
                if all(r != row for r, c in state):
                    for col in range(self.n):
                        if all(c != col for r, c in state):
                            q.append(state + [(row, col)])
                            
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = eight_rooks(root)
    root.mainloop()
