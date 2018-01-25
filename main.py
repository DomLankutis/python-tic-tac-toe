from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox


class App(Frame):
    def __init__(self, master=None):
        """Initialises the program launching the pre requisites and initialising necessary global variables."""
        super().__init__(master)
        self.masterframe = Frame(self.master)
        self.masterframe.pack()
        self.grid = Grid(3)
        self.canvasSize = 100
        self.mX = 0
        self.mY = 0
        self.working = True
        # True is Player 1 and False is Player 2
        self.turn = True
        self.createCanvas()


    def createCanvas(self):
        """Creates the canvas (Display that is used to play the game) and returns the variable: self.canvas"""
        self.screen = self.grid.gridSize * self.canvasSize
        self.canvas = Canvas(self.masterframe,width=self.screen, height=self.screen)
        self.canvas.create_rectangle(0,0, self.screen, self.screen, fill="white")
        # Create a visual grid for the canvas. This provides a good visual indication of where the items can go.
        for x in range(self.grid.gridSize):
            self.canvas.create_line(x * self.canvasSize, 0, x * self.canvasSize, self.screen, width=2)
            self.canvas.create_line(0, x * self.canvasSize, self.screen, x * self.canvasSize, width=2)
        self.canvas.bind("<Button-1>", self.updateCanvas)
        self.canvas.pack()


    def updateCanvas(self, event):
        """Logic of the canvas. Processes each frame """
        mX = event.x // self.canvasSize
        mY = event.y // self.canvasSize
        RECTSIZE = self.screen / self.grid.gridSize

        try:
            self.canvas.delete(self.canvastext)
        except:
            pass

        if self.grid.grid[mX][mY] == ".":
            if self.turn:
                # Draw Player 1 on screen and set text that the other player is up
                self.grid.grid[mX][mY] = "P1"
                self.canvas.create_rectangle(mX * RECTSIZE, mY * RECTSIZE, (mX + 1) * RECTSIZE,
                                         (mY + 1) * RECTSIZE, fill="blue")
                self.canvastext = self.canvas.create_text(0, 0, font="Arial 12", text="Player 2's turn", anchor="nw")
            else:
                # Draw player 2 on screen and set the text that the opposing player is up
                self.grid.grid[mX][mY] = "P2"
                self.canvas.create_rectangle(mX * RECTSIZE, mY * RECTSIZE, (mX + 1) * RECTSIZE,
                                             (mY + 1) * RECTSIZE, fill="red")
                self.canvastext = self.canvas.create_text(0, 0, font="Arial 12", text="Player 1's turn", anchor="nw")
            self.turn = not self.turn
        # Perform the check from the grid class
        winner = self.grid.check()
        if winner:
            if winner == "Tie":
                messagebox.showinfo("Tie", "You have tied the game")
            else:
                messagebox.showinfo("Winner", "{} is the winner".format(winner))
            self.masterframe.destroy()
            self.__init__(master=self.master)


class Grid:
    def __init__(self, gridSize):
        """Initialises main variables to work with the grid of the game"""
        self.grid = []
        self.player1Pos = []
        self.player2Pos = []
        self.winner = None
        self.gridSize = gridSize
        self.generate()

    def generate(self):
        """Generates the grid with the size given in the __init__ returns: self.grid"""
        self.grid = [["." for x in range(self.gridSize)] for y in range(self.gridSize)]

    def checkval(self, P1, P2, winningval):
        """Checks if the points earned by the players meet the winning number
        Returns: Winner if there is any. Otherwise it returns None as there is no winner"""
        if P1 == winningval:
            return "Player 1"
        elif P2 == winningval:
            return "Player 2"

    def check(self):
        """Performs the logical check for the grid itself.
        Returns: The winning condition.
                    Tie
                    Player 1
                    Player 2"""
        winner = None
        count = 0

        for y in range(self.gridSize):
            if winner != None:
                return winner
            P1, P2 = 0, 0
            for item in self.grid[y]:
                # Check row of the grid
                if item == "P1":
                    P1 += 1
                elif item == "P2":
                    P2 += 1
            winner = self.checkval(P1, P2, self.gridSize)
            if winner != None:
                return winner
            P1, P2 = 0, 0
            for x in range(self.gridSize):
                # Check column of the grid
                if self.grid[x][y] == "P1":
                    P1 += 1
                elif self.grid[x][y] == "P2":
                    P2 += 1
            winner = self.checkval(P1, P2, self.gridSize)
        if winner != None:
            return winner
        P1, P2 = 0, 0
        for y in range(self.gridSize):
            # Check right top to left bottom across the grid
            for x in range(self.gridSize):
                if x == y:
                    if self.grid[x][y] == "P1":
                        P1 += 1
                    elif self.grid[x][y] == "P2":
                        P2 += 1
        winner = self.checkval(P1, P2, self.gridSize)
        if winner != None:
            return winner
        P1, P2 = 0, 0
        for y in range(self.gridSize):
            # Check the left top to the right bottom across the grid
            for x in range(self.gridSize - 1, -1, -1):
                # Check how many filled spaces there are
                if "." not in self.grid[y][x]:
                    count += 1
                if x + y == self.gridSize - 1:
                    if self.grid[y][x] == "P1":
                        P1 += 1
                    elif self.grid[y][x] == "P2":
                        P2 += 1
        winner = self.checkval(P1, P2, self.gridSize)
        # Check if there is a winner if so return the winner
        if winner != None:
            return winner
        # Check if the fields that are filled are equal to the possible spaces to be filled in the grid
        if count == self.gridSize**2:
            return "Tie"


app = App(master=Tk())
# Launch the app itself
app.mainloop()





