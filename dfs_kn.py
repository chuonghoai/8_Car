import tkinter as tk

class eight_rooks:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Rooks")
        self.root.config(bg="lightgray")
        self.n = 8
        self.pos_rook = [[0] * self.n for _ in range(self.n)]

        # Khung trái và phải
        frame_left = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_left.grid(row=0, column=0, padx=10, pady=10)
        frame_right = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_right.grid(row=0, column=1, padx=10, pady=10)

        # Nút bấm Next
        btn_next = tk.Button(self.root, text="Next Solution", command=self.show_next_solution)
        btn_next.grid(row=1, column=0, columnspan=2, pady=10)

        # Tạo bàn cờ trống (trái) và bàn cờ có quân (phải)
        self.buttons_l = self.create_widget(frame_left, False)
        self.buttons_r = self.create_widget(frame_right, True)

        # Tìm tất cả lời giải bằng DFS
        self.solutions = []
        self.dfs([])
        self.current_index = 0

        # Hiển thị lời giải đầu tiên ngay khi mở
        self.show_next_solution()

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

    def dfs(self, state, row=0):
        if row == self.n:
            self.solutions.append(state.copy())  # copy chỉ ở thời điểm leaf
            return
        for col in range(self.n):
            if all(c != col for r, c in state):
                state.append((row, col))
                self.dfs(state, row + 1)
                state.pop()  # thu hồi để thử col tiếp theo


    def show_next_solution(self):
        if not self.solutions:
            return

        # Reset bàn cờ
        self.pos_rook = [[0] * self.n for _ in range(self.n)]
        solution = self.solutions[self.current_index]

        # Đặt quân xe theo lời giải
        for r, c in solution:
            self.pos_rook[r][c] = 1

        # Cập nhật giao diện (bàn cờ bên phải)
        for i in range(self.n):
            for j in range(self.n):
                idx = i * self.n + j
                text = "R" if self.pos_rook[i][j] == 1 else ""
                self.buttons_r[idx].config(text=text)

        # Sang lời giải tiếp theo
        self.current_index = (self.current_index + 1) % len(self.solutions)



if __name__ == "__main__":
    root = tk.Tk()
    app = eight_rooks(root)
    root.mainloop()



