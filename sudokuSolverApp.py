from tkinter import *
import random, numpy as np


class TTT(Tk):
    def __init__(self):
        res = [600,600]
        self.parent = Tk.__init__(self)
        self.lablist = []
        self.helpmsg = \
            "Overview - This program doubles as a sudoku game and a solver.\n\n " \
            "To insert a number onto the board you must first\n " \
            "click the spot on the board and then enter a digit from 1-9\n " \
            "if the number 0 is input this clears that spot on the board\n\n" \
            "Quit - Quits the program\t\t\t\t\t\t\n" \
            "Reset - Resets the board\t\t\t\t\t\t\n" \
            "Solve - Solves the current board and if its unsolvable it will display an error message\n" \
            "Help - Displays a help message\t\t\t\t\t\n"
        self.victorymsg = \
            "VICTORY\n press the reset button to play again\n"
        canvas = Canvas(bg="white", height=75, width=600)
        canvas.create_text(300, 37, text="Sudoku Player", font=("Helvetica", 30))
        canvas.pack()
        canvas = Canvas(bg="white", height=res[0], width=res[1])
        canvas.pack()
        for row in range(9):
            self.labrow = []
            for col in range(9):
                lab = Label(text=" ", width=2, font=("Helvetica", 30), relief="sunken",bd= 4, background = "white")
                canvas.create_window(((row*res[1]//10)+42)+(row//3*19), ((col*res[1]//10)+42)+(col//3*19), window=lab)
                lab.bind("<Button-1>", self.setfocus)
                lab.num = [row, col]  # the integer that identifies the label
                self.labrow.append(lab)
            self.lablist.append(self.labrow)
            
        # Creating the grid
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

        canvas = Canvas(bg="white", height=170, width=600)
        canvas.pack()

        self.quitButton = Button(text=" Quit ", font=("Helvetica", 20),
                           relief="groove", command=self.quit)
        canvas.create_window(500, 125, window=self.quitButton)

        self.resetButton = Button(text="Reset", font=("Helvetica", 20),
                           relief="groove", command=self.reset)
        canvas.create_window(300, 125, window=self.resetButton)

        self.solveButton = Button(text="Solve", font=("Helvetica", 20),
                           relief="groove", command=self.solve)
        canvas.create_window(100, 50, window=self.solveButton)

        self.helpButton = Button(text=" Help ", font=("Helvetica", 20),
                           relief="groove", command= lambda: self.displaypopup(" Help ", self.helpmsg))
        canvas.create_window(500, 50, window=self.helpButton)

        self.randomBoardButton = Button(text=" Random Board ", font=("Helvetica", 20),
                           relief="groove", command=self.randomBoard)
        canvas.create_window(300, 50, window=self.randomBoardButton)


    def reset(self):
        for labrow in self.lablist:
            for lab in labrow:
                lab.configure(text=" ")
        self.board = np.zeros((9, 9), dtype=np.int8)

    
    def displaypopup(self, title, msg):
        popup = Tk()
        popup.wm_title(title)
        label = Label(popup, text=msg, font="helvetica")
        label.pack(side="top", fill="x", pady=10)
        popup.mainloop()
        
        
    def done(self, board, coords):
        # checks if the board is done if it finds a spot with a zero then we are not
        # done and this zero space is filled with a hopefully valid number
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    coords[0] = i
                    coords[1] = j
                    return 0
        return 1


    def sudokusolve(self, board):
        coords = [0, 0]
        if self.isvalid(board) == 0:
            return 0
        if self.done(board, coords):
            return 1
        else:
            for i in range(1, 10):
                board[coords[0]][coords[1]] = i
                lab = self.lablist[coords[1]][coords[0]]  # which label was clicked
                lab.configure(text=str(i))  # make mark on the graphical board
                lab.update()
                if self.sudokusolve(board):
                    return 1
                board[coords[0]][coords[1]] = 0
                lab.configure(background="white")
                lab.update()

    def isvalid(self, board):
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                for k in range(1, 10):
                    if np.sum(board[j:j + 3, i:i + 3] == k) > 1:
                        return 0

        for i in range(len(board)):
            for j in range(1, 10):
                if np.sum(board[i, :] == j) > 1 or np.sum(board[:, i] == j) > 1:
                    return 0
        return 1

    def randomBoard(self):
        def generateBoard(board):
            coords = [0, 0]
            if self.isvalid(board) == 0:
                return 0
            if self.done(board, coords):
                return 1
            else:
                for i in range(1, 10):
                    i = random.randint(1, 9)
                    board[coords[0]][coords[1]] = i
                    lab = self.lablist[coords[1]][coords[0]]  # which label was clicked
                    lab.configure(text=str(i))  # make mark on the graphical board
                    lab.update()
                    if generateBoard(board):
                        return 1
                    board[coords[0]][coords[1]] = 0
                    lab.configure(background="white")
                    lab.update()
        def removeSquares(board):
            for i in range(len(board)):
                for j in range(len(board)):
                    if random.randint(0, 1):
                        board[i][j] = 0
                        lab = self.lablist[j][i]  # which label was clicked
                        lab.configure(text="")  # make mark on the graphical board
                        lab.update()
                    
            return
        generateBoard(self.board)
        removeSquares(self.board)

    def setfocus(self, event):  # sets keyboard focus onto the pressed label
        global lastlab
        n = event.widget.num
        lab = self.lablist[n[0]][n[1]]
        lab.configure(background="yellow")
        lab.update()
        event.widget.focus_set()
        event.widget.bind('<Key>', self.keypress)  # binds the key event to the label to take keyboard input
        if lastlab != 0:
            lab = self.lablist[lastlab[0]][lastlab[1]]
            lab.configure(background="white")
            lab.update()
        lastlab = n

    def keypress(self, event):
        n = event.widget.num  # n is the x,y of the clicked label
        lab = self.lablist[n[0]][n[1]]  # which label was clicked
        num = int(event.char)
        if num == 0:
            lab.configure(text="")
        else:
            lab.configure(text=str(num))
        self.board[n[1]][n[0]] = int(num)
        if self.isvalid(self.board) == 1:
            self.displaypopup("", self.victorymsg);

    def solve(self):
        if not self.sudokusolve(self.board):
            print("Board is unsolvable")
            print(self.board)
        else:
            print("SUCCESS!")
            print(self.board)


if __name__ == "__main__":
    game = TTT()
    lastlab = [0, 0]
    game.title("Sudoku Solver")
    game.configure(background='white')
    game.mainloop()
