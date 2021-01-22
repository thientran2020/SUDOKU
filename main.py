from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from itertools import product
import sys
import os
import numpy as np


class SDK_MainWindow(object):
    def __init__(self):
        # Central Widget
        self.centralWidget = QtWidgets.QWidget(MainWindow)

        # Menu Bar
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.exitAction = QtWidgets.QAction(MainWindow)
        self.loadAction = QtWidgets.QAction(MainWindow)

        # Grid Layout
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        # Buttons, Level label
        self.buttons = [QtWidgets.QPushButton(self.centralWidget) for _ in range(5)]
        self.lvLabel = QtWidgets.QLabel(self.centralWidget)

        # Default Style for The Sudoku
        self.styleDef = "color: red;\
                    font-family: Times New Roman; font-size: 41px;\
                    font-weight: bold; background-color: white"

        # @length: puzzle length = 9
        # @boxes: 2D list QTextEdit objects - stands for 9x9 positions of the puzzle
        # @puzzle: main puzzle
        # @bool: boolean puzzle (True: empty positions - False: others)
        self.boxes = []
        self.length = 9
        self.puzzle = None
        self.bool = None
        self.level = "EASY"
        self.solution = None

        # Load Dataset
        self.dataset = self.load_sudoku_data()

    # TODO: Load puzzle problems from sudoku_dataset.txt file
    def load_sudoku_data(self):
        data = {}
        with open("sudoku_dataset.txt") as file:
            num = int(file.readline())
            for idx in range(num):
                level = file.readline().strip()
                p = []
                for _ in range(self.length):
                    row = file.readline().strip()
                    p.append([int(c) for c in row])
                data[idx] = (level, p)
        return data

    # TODO: Create a GridLayOutWidget to place the 9x9 sudoku
    def setupGridLayout(self):
        self.centralWidget.setStyleSheet("background-color: black")
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 540, 540))
        self.gridLayoutWidget.setStyleSheet(self.styleDef)
        self.gridLayoutWidget.setAutoFillBackground(False)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(1)

        for row in range(self.length):
            rows = []
            for col in range(self.length):
                box = QtWidgets.QTextEdit(self.centralWidget)
                rows.append(box)
                self.gridLayout.addWidget(box, row, col, 1, 1)
            self.boxes.append(rows)

    # TODO: Create Menu File
    def setupMenuBar(self, MyWindow):
        MyWindow.setCentralWidget(self.centralWidget)
        MyWindow.setMenuBar(self.menuBar)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1120, 28))
        self.menuBar.setStyleSheet("font-size: 20px; color: yellow; background-color:black")

        # Set up Menu File with 2 separators:
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.setTitle("File")
        self.menuFile.addAction(self.loadAction)
        self.menuFile.addAction(self.exitAction)

        # Set up Exit separator
        self.exitAction.triggered.connect(lambda: sys.exit(app.exec_()))
        self.exitAction.setText("Exit")
        self.exitAction.setShortcut('Ctrl+Q')

        # Set up Load separator
        self.loadAction.triggered.connect(lambda: os.startfile("about.txt"))
        self.loadAction.setText("About Game")
        self.loadAction.setShortcut('Ctrl+A')

    # TODO: Set up buttons list: NEW, CHECK, REMOVE, CLEAR, SOLVE
    def setupButtons(self):
        btStyle = "color: red;\
                    font-family: Book Antigua; font-size: 24px;\
                    font-weight: bold; background-color: white"
        labels = ["NEW", "CHECK", "REMOVE", "CLEAR", "SOLVE"]
        x_pos = 550
        y_pos = 25
        btWidth = 135
        btHeight = 70
        for idx in range(len(labels)):
            button = self.buttons[idx]
            button.setGeometry(QtCore.QRect(x_pos, y_pos, btWidth, btHeight))
            button.setStyleSheet(btStyle)
            button.setText(labels[idx])
            y_pos += 100
            if idx == 0:
                button.clicked.connect(lambda: self.setupPuzzle())
            elif idx == 1:
                button.clicked.connect(lambda: self.checkClicked())
            elif idx == 2:
                button.clicked.connect(lambda: self.removeClicked())
            elif idx == 3:
                button.clicked.connect(lambda: self.clearClicked())
            else:
                button.clicked.connect(lambda: self.solveClicked())

    # TODO: Display level of sudoku
    # 4 levels: easy, medium, hard, fiendish
    def setupLevel(self):
        self.lvLabel.setGeometry(QtCore.QRect(50, 570, 540, 70))
        self.lvLabel.setText(f"LEVEL: {self.level}")
        self.lvLabel.setStyleSheet("color: yellow;\
               font-family: Times New Roman; font-size: 54px;\
               font-style: italic; font-weight: bold;")

    # TODO: Set up the main gui sudoku, take a random puzzle and assign to GridLayout
    def setupPuzzle(self):
        horizontal_border_style = "border-bottom-style: outset;\
                                border-bottom-color: blue;\
                                border-bottom-width: 3px;"
        vertical_border_style = "border-right-style: outset;\
                                border-right-color: blue;\
                                border-right-width: 3px;"

        self.level, self.puzzle = self.dataset[np.random.randint(len(self.dataset))]
        self.bool = (np.array(self.puzzle) == 0).tolist()
        self.setupLevel()

        # helper function to create border for a grid widget object
        # @(r,c) == (row, col)
        # @s1, s2 == stylesheet1, stylesheet2
        def create_border(r, c, s1, s2):
            if r in [2, 5] and c in [2, 5]:
                self.boxes[r][c].setStyleSheet(s1 + s2)
            elif r in [2, 5]:
                self.boxes[r][c].setStyleSheet(s1)
            elif c in [2, 5]:
                self.boxes[r][c].setStyleSheet(s2)

        # Loop through GridLayout to set up border for the sudoku
        for row in range(self.length):
            for col in range(self.length):
                if self.puzzle[row][col] != 0:
                    defColor = "color: red;"
                    self.boxes[row][col].setText(str(self.puzzle[row][col]))
                    self.boxes[row][col].setReadOnly(True)
                    if row not in [2, 5] and col not in [2, 5]:
                        self.boxes[row][col].setStyleSheet(defColor)
                    else:
                        create_border(row, col, horizontal_border_style, vertical_border_style)
                else:
                    self.boxes[row][col].setText("")
                    userColor = "color: black;"
                    self.boxes[row][col].setReadOnly(False)
                    if row not in [2, 5] and col not in [2, 5]:
                        self.boxes[row][col].setStyleSheet(userColor)
                    else:
                        create_border(row, col, horizontal_border_style + userColor, vertical_border_style + userColor)
        self.solution = self.solveClicked(False, False)

    # TODO: after CHECK button is clicked - Display message
    def checkClicked(self):
        solved = self.solveClicked(False, False)
        wrong = False
        for row in range(self.length):
            for col in range(self.length):
                tmp = self.boxes[row][col].toPlainText()
                if self.bool[row][col] and tmp != "" and str(solved[row][col]) != tmp:
                    wrong = True
                    break
            else:
                continue
            break
        error_msg = "There are some wrong numbers filled.\n1. Press REMOVE to delete them.\n2. Press CLEAR to play again."
        not_error_msg = "You've been right so far. Keep going...!"
        msg = QMessageBox()
        if wrong:
            msg.setWindowTitle("ERROR")
            msg.setText(error_msg)
        else:
            msg.setWindowTitle("GREAT")
            msg.setText(not_error_msg)
        msg.exec_()

    # TODO: after REMOVE button is clicked - remove incorrect numbers filled by players
    def removeClicked(self):
        for row in range(self.length):
            for col in range(self.length):
                if self.bool[row][col] and \
                        self.boxes[row][col].toPlainText() != str(self.solution[row][col]):
                    self.boxes[row][col].setText("")

    # TODO: after CLEAR button is clicked - restore the initial status of the current sudoku
    def clearClicked(self):
        for row in range(self.length):
            for col in range(self.length):
                if self.bool[row][col]:
                    self.boxes[row][col].setText("")

    # TODO: after SOLVE button is clicked - Solve and Return solution
    # @printSolution: bool value (True: display solution, False: no)
    # @clearPuzzle: bool value (True: restore the initial status of the current sudoku)
    def solveClicked(self, printSolution=True, clearPuzzle=True):
        # Check if a value is valid when assigned to a specific position
        # @(x,y): the position in the puzzle @p
        # @value: number from 1-9
        def isValid(x, y, puz, value):
            for i in range(0, 9):
                if puz[x][i] == value or puz[i][y] == value:
                    return False
            for (i, j) in product(range(0, 3), repeat=2):
                if puz[x - x % 3 + i][y - y % 3 + j] == value:
                    return False
            return True

        # Solve a puzzle using backtracking method
        # Loop through each row and column - assign each box to a possible number from 1-9
        # Recursively do it until cant continue, go back and set puzzle[r][c] = 0
        # @(r,c) = (row, col)
        def solve(puzzle):
            for (r, c) in product(range(0, 9), repeat=2):
                if puzzle[r][c] == 0:
                    for number in range(1, 10):
                        if isValid(r, c, puzzle, number):
                            puzzle[r][c] = number
                            if trial := solve(puzzle):
                                return trial
                            else:
                                puzzle[r][c] = 0
                    return False
            return puzzle

        p = list(map(list, self.puzzle))
        solved = solve(p)
        if clearPuzzle:
            self.clearClicked()
        if printSolution:
            for row in range(self.length):
                for col in range(self.length):
                    self.boxes[row][col].setText(str(solved[row][col]))
        return solved

    # TODO: set up the main  SUDOKU Window
    def setupUI(self, MyWindow):
        MyWindow.setFixedSize(700, 700)
        MyWindow.setWindowTitle("SUDOKU SOLVER")
        self.setupMenuBar(MyWindow)
        self.setupGridLayout()
        self.setupPuzzle()
        self.setupButtons()
        QtCore.QMetaObject.connectSlotsByName(MyWindow)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    sudoku = SDK_MainWindow()
    sudoku.setupUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
