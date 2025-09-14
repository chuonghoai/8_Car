import tkinter as tk
from PIL import Image, ImageTk
from collections import deque
import random
import heapq


class EightCarQueen:
    def __init__(self, root):
        self.root = root
        self.root.title("Cars(DFS) & Queens")
        self.root.configure(bg="lightgray")

        frame_left = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_left.grid(row=0, column=0, padx=10, pady=10)

        frame_right = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_right.grid(row=0, column=1, padx=10, pady=10)

        self.whiteX = ImageTk.PhotoImage(Image.open("whiteX.png").resize((60, 60)))
        self.blackX = ImageTk.PhotoImage(Image.open("blackX.png").resize((60, 60)))
        self.img_null = tk.PhotoImage(width=1, height=1)

        self.buttons_left = self.create_board(frame_left)
        self.buttons_right = self.create_board(frame_right)

        tk.Button(self.root, text="Solve dls(Cars)", command=self.run_dls)\
            .grid(row=1, column=1, pady=10)
        tk.Button(self.root, text="Solve cot (Cars)", command=self.ucs_cot)\
            .grid(row=1, column=0, pady=10)
        tk.Button(self.root, text="Solve dong (Cars)", command=self.ucs_dong)\
            .grid(row=2, column=0, pady=10)

    def create_board(self, frame):
        buttons = []
        for i in range(8):
            row = []
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                btn = tk.Button(frame, image=self.img_null,
                                width=60, height=60,
                                bg=color, relief="flat", 
                                borderwidth=0)
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            buttons.append(row)
        return buttons  
         
    def drawxe(self, solution, board):
        for i in range(8):
            for j in range(8):
                board[i][j].configure(image=self.img_null)
        for r, c in enumerate(solution):
            color = "white" if (r + c) % 2 == 0 else "black"
            img = self.whiteX if color == "black" else self.blackX
            board[r][c].configure(image=img)
    
    def ucs_dong(self):
        frontier = []
        heapq.heappush(frontier, Node([], 0))
        explored = set()

        while frontier:
            node = heapq.heappop(frontier)
            state, cost = node.state, node.cost

            if len(state) == 8:
                self.drawxe(state, self.buttons_left)
                print("Solution:", state, "Cost:", cost)
                return

            explored.add(tuple(state))
            row = len(state)

            for col in range(8):
                if col not in state:
                    new_state = state + [col]
                    new_cost = cost + row
                    if tuple(new_state) not in explored:
                        heapq.heappush(frontier, Node(new_state, new_cost))
        return None

    def ucs_cot(self):
        col_cost = [7, 6, 5, 4, 3, 2, 1, 0]

        frontier = []
        heapq.heappush(frontier, Node([], 0))
        explored = set()

        while frontier:
            node = heapq.heappop(frontier)
            state, cost = node.state, node.cost

            if len(state) == 8:
                self.drawxe(state, self.buttons_left)
                print("UCS Solution:", state, "Cost:", cost)
                return

            explored.add(tuple(state))
            row = len(state)

            for col in range(8):
                if col not in state:
                    new_state = state + [col]
                    new_cost = cost + col_cost[col]
                    if tuple(new_state) not in explored:
                        heapq.heappush(frontier, Node(new_state, new_cost))
        return None

    def depth_limited_search(self, limit=8):
        def recursive_dls(state, row, limit):
            if len(state) == 8: return state
            if limit == 0: return "cutoff"
            cutoff = False
            for col in range(8):
                if col not in state:
                    result = recursive_dls(state + [col], row + 1, limit - 1)
                    if result == "cutoff": cutoff = True
                    elif result != "failure": return result
            return "cutoff" if cutoff else "failure"
        return recursive_dls([], 0, limit)

    def run_dls(self):
        sol = self.depth_limited_search()
        if sol not in ("failure", "cutoff"):
            self.drawxe(sol, self.buttons_right)

class Node:
    def __init__(self, state, cost):
        self.state = state  # state = [cột đặt xe mỗi hàng]
        self.cost = cost    # tổng chi phí đến state này

    def __lt__(self, other):  # so sánh cho heapq
        return self.cost < other.cost 
    

if __name__ == "__main__":
    root = tk.Tk()
    app = EightCarQueen(root)
    root.mainloop()
