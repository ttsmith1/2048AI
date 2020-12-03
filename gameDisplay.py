from tkinter import Frame, Label, CENTER

import gameAI
import gameFunction

EDGE_LENGTH = 400
CELL_COUNT = 4
CELL_PAD = 10

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY= "'d'"
AI_KEY = "'q'"
AI_PLAY_KEY = "'p'"

LABEL_FONT = ("Verdana", 40, "bold")

GAME_COLOR = "#a39489"

EMPTY_COLOR = "#c2b3a9"

TILE_COLORS = {2: "#fcefe6", 4: "#f2e8cb", 8: "#f5b682", 16: "#f29446",
                   32: "#ff775c", 64: "#e64c2e", 128: "#ede291",
                   256: "#fce130", 512: "#ffdb4a", 1024: "#f0b922",
                   2048: "#fad74d", 4096: "#000000", 8192: "#000000",}

LABEL_COLORS = {2: "#011c08", 4: "#011c08", 8: "#011c08", 16: "#011c08",
                   32: "#011c08", 64: "#f2f2f0", 128: "#f2f2f0",
                   256: "#f2f2f0", 512: "#f2f2f0", 1024: "#f2f2f0",
                   2048: "#f2f2f0", 4096: "#f2f2f0", 8192: "#f2f2f0",}

class Display(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_press)

        self.commands = {UP_KEY: gameFunction.move_up, 
                         DOWN_KEY: gameFunction.move_down,
                         LEFT_KEY: gameFunction.move_left, 
                         RIGHT_KEY: gameFunction.move_right,
                         AI_KEY: gameAI.ai_move,
                         }
        
        self.grid_cells = []
        self.build_grid()
        self.init_matrix()
        self.draw_grid_cells()

        self.mainloop()

    def build_grid(self):
        background = Frame(self, bg=GAME_COLOR,
                           width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid()

        for row in range(CELL_COUNT):
            grid_row = []
            for col in range(CELL_COUNT):
                cell = Frame(background, bg=EMPTY_COLOR,
                             width=EDGE_LENGTH / CELL_COUNT,
                             height=EDGE_LENGTH / CELL_COUNT)
                cell.grid(row=row, column=col, padx=CELL_PAD,
                          pady=CELL_PAD)
                t = Label(master=cell, text="",
                          bg=EMPTY_COLOR,
                          justify=CENTER, font=LABEL_FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = gameFunction.initialize_game()

    def draw_grid_cells(self):
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    self.grid_cells[row][col].configure(
                        text="", bg=EMPTY_COLOR)
                else:
                    self.grid_cells[row][col].configure(text=str(
                        tile_value), bg=TILE_COLORS[tile_value],
                        fg=LABEL_COLORS[tile_value])
        self.update_idletasks()
    
    def key_press(self, event):
        valid_game = True
        key = repr(event.char)
        if key == AI_PLAY_KEY:
            move_count = 0
            while valid_game:
                self.matrix, valid_game = gameAI.ai_move(self.matrix,40, 30)
                if valid_game:
                    self.matrix = gameFunction.add_new_tile(self.matrix)
                    self.draw_grid_cells()
                move_count += 1
        if key == AI_KEY:
            self.matrix, move_made = gameAI.ai_move(self.matrix, 20, 30)
            if move_made:
                self.matrix = gameFunction.add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_made = False

        elif key in self.commands:
            self.matrix, move_made, _ = self.commands[repr(event.char)](self.matrix)
            if move_made:
                self.matrix = gameFunction.add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_made = False
gamegrid = Display()