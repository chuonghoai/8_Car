import tkinter as tk
import random
import copy
from PIL import Image, ImageTk
from collections import deque

class eight_queen:
    def __init__(self, root):
        self.root = root
        self.root.title("8 queen")
        self.root.config(bg="lightgray")
        self.n = 8

        self.frame_left = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        self.frame_left.grid(row=0, column=0, padx=10, pady=5)

        self.frame_right = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        self.frame_right.grid(row=0, column=1, padx=10, pady=5)

        white_xa = Image.open("./whiteX.png").resize((60, 60))
        black_xa = Image.open("./blackX.png").resize((60, 60))
        self.whiteX = ImageTk.PhotoImage(white_xa)
        self.blackX = ImageTk.PhotoImage(black_xa)
        
        self.img_null = tk.PhotoImage(width=1, height=1)

        #Tạo ma trận các tọa độ sắp xếp ngẫu nhiên
        self.pos_random = [[(i, j) for j in range(self.n)] for i in range(self.n)]
        _ = [pos for row in self.pos_random for pos in row]
        random.shuffle(_)
        self.pos_random = [_[i*self.n:(i+1)*self.n] for i in range(self.n)]

        #Đặt xe vào ma trận với các tọa độ từ node
        node = self.set_xa_DFS()
        self.pos_xa = [[0] * self.n for _ in range(self.n)]
        for x, y in node:
            self.pos_xa[x][y] = 1

        cost = self.cost_cal(node)
        cost_txt = tk.Label(self.root, bg="lightgray", text=f"Chi phí: {cost}", font=("Arial", 15))
        cost_txt.grid(row=1, column=0, columnspan=2, pady=5)
        
        #Vẽ lên giao diện
        self.buttons_left = self.create_widget(self.frame_left, False)
        self.buttons_right = self.create_widget(self.frame_right, True)

    def create_widget(self, frame, draw_xa):
        buttons = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "black"
                
                if draw_xa and self.pos_xa[i][j] == 1:
                    img = self.whiteX if color == "black" else self.blackX
                else:
                    img = self.img_null
                
                btn = tk.Button(frame, image=img, width=60, height=60, bg=color,
                                relief="flat", borderwidth=0, highlightthickness=0)
                    
                btn.grid(row = i, column = j, padx=1, pady=1)
                row.append(btn)
            buttons.append(row)
        
        return buttons
    
    #Hàm đặt xe bằng DFS
    def set_xa_DFS(self):
        #Stack và các biến ban đầu
        frontier = deque([])    #stack
        xst, yst = self.pos_random[0][0][0], self.pos_random[0][0][1]
        node = [(xst, yst)]
        if self.check_goal(node):
            return node
        frontier.append((node))
        explored = []
        
        while True:
            if not frontier:
                return None
            node = frontier.pop()
            explored.append(node)

            #Duyệt từng tọa độ x, y trong ma trận tọa độ random ban đầu
            for _ in self.pos_random:
                for x, y in _:
                    can_set = True
                    for node_x, node_y in node:     #Kiểm tra mỗi tọa độ x, y hiện tại có khắc quân cờ nào trong node ko
                        if node_x == x or node_y == y:
                            can_set = False
                            break
                    if can_set:
                        child = self.child_node(node, x, y)     #Tạo nhánh cây con child 
                        if child not in frontier and child not in explored:
                            if self.check_goal(child):
                                return child
                            if len(node) < self.n:      #Giới hạn lại số lượng quân cờ
                                frontier.append(child)
    
    def check_goal(self, node):     #Kiểm tra điều kiện đạt goal: số lượng đã đủ và ko 2 quân nào khắc nhau
        if len(node) != self.n:
            return False
        else:
            for i in range(len(node)):
                for j in range(i + 1, len(node)):
                    if node[i][0] == node[j][0] or node[i][1] == node[j][1]:
                        return False
        return True
    
    def child_node(self, node, x, y):       #Sinh ra nhánh con child
        child = []
        child = copy.deepcopy(node)
        child.append((x, y))
        return child  

    #Chi phí = các ô đã bị hạn chế = tổng số ô - số ô trống    
    def cost_cal(self, node):
        row = {x for (x, _) in node}
        col = {y for (_, y) in node}

        free_pos = 0
        for i in range(self.n):
            if i not in row:
                for j in range(self.n):
                    if j not in col:
                        free_pos += 1

        return self.n * self.n - free_pos
    
if __name__ == "__main__":
    root = tk.Tk()
    game = eight_queen(root)
    root.mainloop()