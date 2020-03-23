from tkinter import *
import numpy as np
import random
import time

class TTT(Tk):
    def __init__(self):
        res = [600,600]
        self.parent = Tk.__init__(self)
        self.lablist = []
        canvas = Canvas(bg="white", height=res[0], width=res[1])
        canvas.pack()
        for row in range(9):
            self.labrow = []
            for col in range(9):
                lab = Label(text=" ", width=2, font=("Helvetica", 30), relief="sunken",bd= 4)
                canvas.create_window(((row*res[1]//10)+42)+(row//3*19), ((col*res[1]//10)+42)+(col//3*19), window=lab)
                lab.bind("<Button-1>", self.callback)
                lab.num = [row, col]  # the integer that identifies the label
                self.labrow.append(lab)
            self.lablist.append(self.labrow)
            
        canvas.create_line(0, 0, res[1], 0, fill="black", width="20")
        canvas.create_line(0, 0, 0, res[1], fill="black", width="20")
        canvas.create_line(res[1], 0, res[1], res[1], fill="black", width="10")
        canvas.create_line(0, res[1], res[1], res[1], fill="black", width="10")
        canvas.create_line(0, res[1], res[1], res[1], fill="black", width="10")
        canvas.create_line(res[1]//3, 0, res[1]//3, res[1], fill="black", width="10")
        canvas.create_line((res[1]//3)*2, 0, (res[1]//3)*2, res[1], fill="black", width="10")
        canvas.create_line(0, res[1]//3, res[1], res[1]//3, fill="black", width="10")
        canvas.create_line(0, (res[1]//3)*2, res[1], (res[1]//3)*2, fill="black", width="10")

        self.board = np.zeros((9, 9), dtype=np.int8)

        canvas = Canvas(bg="white", height=100, width=600)
        canvas.pack()

        self.but1 = Button(text="Quit", font=("Helvetica", 20),
                           relief="groove", command=self.quit)
        canvas.create_window(100, 50, window=self.but1)

        self.but2 = Button(text="Reset", font=("Helvetica", 20),
                           relief="groove", command=self.reset)
        canvas.create_window(300, 50, window=self.but2)

        self.but3 = Button(text="Solve", font=("Helvetica", 20),
                           relief="groove", command=self.solve)
        canvas.create_window(500, 50, window=self.but3)

    def reset(self):
        for labrow in self.lablist:
            for lab in labrow:
                lab.configure(text=" ")
        self.board = np.zeros((9, 9), dtype=np.int8)


    def solve(self):
        def isvalid(board):
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    for k in range(1,10):
                        if np.sum(board[j:j + 3, i:i + 3] == k) > 1:
                            return 0

            for i in range(len(board)):
                for j in range(1, 10):
                    if np.sum(board[i, :] == j) > 1 or np.sum(board[:, i] == j) > 1:
                        return 0
            return 1

        def done(board, coords):  # checks if the board is done if it finds a spot with a zero then we are not done and this zero space is filled with a hopefully valid number
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == 0:
                        coords[0] = i
                        coords[1] = j
                        return 0
            return 1

        def sodokusolve(board):
            coords = [0, 0]
            if isvalid(board) == 0:
                return 0
            if done(board, coords):
                return 1
            else:
                for i in range(1, 10):
                    board[coords[0]][coords[1]] = i
                    lab = self.lablist[coords[1]][coords[0]]  # which label was clicked
                    lab.configure(text=str(i))  # make mark on the graphical board
                    lab.update()
                    if (sodokusolve(board)):
                        return 1
                    board[coords[0]][coords[1]] = 0
                time.sleep(.005)
        if not sodokusolve(self.board):
            print("Board is unsolvable")
            print(self.board)
        else:
            print("SUCCESS!")
            print(self.board)

    def randomBoard(self):
        pass

    def callback(self, event):  # function that performs an action on the label
        n = event.widget.num  # n is the x,y of the clicked label
        lab = self.lablist[n[0]][n[1]]  # which label was clicked
        num = random.randint(1,9)
        lab.configure(text=str(num))  # make mark on the graphical board

        self.board[n[1]][n[0]] = num  # mark the logical board where player moved


if __name__ == "__main__":
    game = TTT()
    game.mainloop()
