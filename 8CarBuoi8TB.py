import tkinter as tk
from PIL import Image, ImageTk
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

        self.whiteX = ImageTk.PhotoImage(Image.open("whiteC.png").resize((60, 60)))
        self.blackX = ImageTk.PhotoImage(Image.open("blackC.png").resize((60, 60)))
        self.img_null = tk.PhotoImage(width=1, height=1)

        self.buttons_left = self.create_board(frame_left)
        self.buttons_right = self.create_board(frame_right)

        control_frame = tk.Frame(self.root, bg="lightgray")
        control_frame.grid(row=1, column=0, columnspan=2, pady=20)

        tk.Button(control_frame, text="Interactive DLS (Cars)", command=self.run_dls, width=18)\
            .grid(row=0, column=0, padx=10)
        tk.Button(control_frame, text="Greedy (Cars)", command=self.greedy_search, width=18)\
            .grid(row=0, column=1, padx=10)
        tk.Button(control_frame, text="A* (Cars)", command=self.a_star_search, width=18)\
            .grid(row=0, column=2, padx=10)

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
    def interactive_dls(self):
        depth =0
        while True:
            result = self.depth_limited_search(limit=depth)
            if result != "cutoff":
                return result
            depth += 1

    def run_dls(self):
        sol = self.interactive_dls()
        if sol not in ("failure", "cutoff"):
            self.drawxe(sol, self.buttons_right)

# bai tuan 5: Informed Search
# best first search
# a star search
# heuristic function: số xe bị tấn công

    # dem so xe bi tan cong trung hang hoac trung cot
    # dem so hang cot dang duoc dat r
    # dem so quan can di chuyen
    # -------- Heuristic: số quân xe bị tấn công --------
    def heuristic(self, state):
        attacks = 0
        attacks = 0
        used_cols = set()
        for col in state:
            if col in used_cols:
                attacks += 1
            used_cols.add(col)
        return attacks

    # -------- Greedy Best-First Search --------
    def greedy_search(self):
        frontier = []
        heapq.heappush(frontier, Node([], 0))
        explored = set()

        while frontier:
            node = heapq.heappop(frontier)
            state = node.state

            if len(state) == 8:
                if self.heuristic(state) == 0:  # không bị tấn công
                    self.drawxe(state, self.buttons_right)
                    return state

            explored.add(tuple(state))
            row = len(state)

            for col in range(8):
                if col not in state:  # tránh trùng cột
                    new_state = state + [col]
                    if tuple(new_state) not in explored:
                        h = self.heuristic(new_state)
                        heapq.heappush(frontier, Node(new_state, h))
        return None

    # -------- A* Search với 3 loại cost --------
    def a_star_search(self):
        frontier = []
        # Start node: g=0, h=0, f=0
        start_g = 0
        start_h = self.heuristic([])
        start_f = start_g + start_h
        start_node = Node([], start_f, start_g, start_h)
        heapq.heappush(frontier, start_node)
        explored = set()

        while frontier:
            node = heapq.heappop(frontier)
            state = node.state
            g_cost = node.g_cost    # g(n) - Actual cost from start
            h_cost = node.h_cost    # h(n) - Heuristic cost to goal
            f_cost = node.f_cost    # f(n) - Total cost = g(n) + h(n)

            if len(state) == 8:
                if self.heuristic(state) == 0:  # No attacks
                    self.drawxe(state, self.buttons_right)
                    return state

            state_tuple = tuple(state)
            if state_tuple in explored:
                continue
            explored.add(state_tuple)

            row = len(state)
            if row < 8:  # chưa đặt đủ 8 xe
                for col in range(8):
                    if col not in state:  # Tránh trùng cột
                        new_state = state + [col]
                        new_tuple = tuple(new_state)
                        if new_tuple not in explored:
                            #  tinh cost A*
                            new_g_cost = g_cost + 1                    # g(n) = g(parent) + step_cost
                            new_h_cost = self.heuristic(new_state)     # h(n) = heuristic estimate
                            new_f_cost = new_g_cost + new_h_cost       # f(n) = g(n) + h(n)
                            
                            # tao node moi va them vao hang doi
                            new_node = Node(new_state, new_f_cost, new_g_cost, new_h_cost)
                            heapq.heappush(frontier, new_node)
        
        print("A* search failed")
        return None

class Node:
    def __init__(self, state, f_cost, g_cost=0, h_cost=0):
        self.state = state      # state = [cột đặt xe mỗi hàng]
        self.f_cost = f_cost    # f(n) = g(n) + h(n) - Total cost
        self.g_cost = g_cost    # g(n) = Actual cost from start
        self.h_cost = h_cost    # h(n) = Heuristic cost to goal

    def __lt__(self, other):  # so sánh cho heapq
        return self.f_cost < other.f_cost
    
if __name__ == "__main__":
    root = tk.Tk()
    app = EightCarQueen(root)
    root.mainloop()
