import tkinter as tk
from tkinter import messagebox
import random
from functools import partial

class MinesweeperGUI:
    def __init__(self, width=10, height=10, num_mines=15):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.buttons = []
        self.flags = 0
        self.mines_left = num_mines
        
        # Initialize game state
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flags = [[False for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.victory = False
        
        # Create main window
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.window.configure(bg='white')
        
        # Create mine counter label
        self.mine_label = tk.Label(self.window, text=f"Mines Left: {self.mines_left}", 
                                 font=('Arial', 12), bg='white')
        self.mine_label.grid(row=0, column=0, columnspan=self.width, pady=5)
        
        # Create game board
        self.create_board()
        
        # Place mines
        self.place_mines()
        self.calculate_numbers()
        
    def create_board(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                button = tk.Button(self.window, width=2, height=1, 
                                 command=partial(self.click_button, x, y))
                button.grid(row=y+1, column=x, padx=1, pady=1)
                button.bind('<Button-3>', partial(self.right_click, x, y))
                row.append(button)
            self.buttons.append(row)
            
    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == 0:
                self.board[y][x] = -1
                mines_placed += 1
                
    def calculate_numbers(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    continue
                self.board[y][x] = self.count_adjacent_mines(x, y)
                
    def count_adjacent_mines(self, x, y):
        count = 0
        for i in range(max(0, y-1), min(y+2, self.height)):
            for j in range(max(0, x-1), min(x+2, self.width)):
                if self.board[i][j] == -1:
                    count += 1
        return count
                
    def click_button(self, x, y):
        if self.game_over or self.revealed[y][x]:
            return
        if self.flags[y][x]:
            return
            
        self.revealed[y][x] = True
        
        if self.board[y][x] == -1:
            self.game_over = True
            self.victory = False
            self.show_all_mines()
            messagebox.showinfo("Game Over", "You hit a mine!")
            self.window.quit()
            return
            
        self.update_button(x, y)
        
        if self.board[y][x] == 0:
            self.reveal_adjacent(x, y)
            
        self.check_victory()
            
    def reveal_adjacent(self, x, y):
        for i in range(max(0, y-1), min(y+2, self.height)):
            for j in range(max(0, x-1), min(x+2, self.width)):
                if not self.revealed[i][j]:
                    self.click_button(j, i)
                    
    def right_click(self, x, y, event):
        if self.game_over or self.revealed[y][x]:
            return
            
        if self.flags[y][x]:
            self.flags[y][x] = False
            self.mines_left += 1
            self.buttons[y][x].config(text="")
        else:
            self.flags[y][x] = True
            self.mines_left -= 1
            self.buttons[y][x].config(text="F")
            
        self.mine_label.config(text=f"Mines Left: {self.mines_left}")
        self.check_victory()
        
    def update_button(self, x, y):
        button = self.buttons[y][x]
        if self.board[y][x] == -1:
            button.config(text="*", bg="red")
        elif self.board[y][x] == 0:
            button.config(text="", bg="light gray")
        else:
            button.config(text=str(self.board[y][x]), bg="light gray")
            
    def show_all_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    self.buttons[y][x].config(text="*", bg="red")
                elif not self.revealed[y][x]:
                    self.buttons[y][x].config(bg="light gray")
                    
    def check_victory(self):
        self.victory = True
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    self.victory = False
                    return
                    
        if self.victory:
            self.game_over = True
            self.show_all_mines()
            messagebox.showinfo("Victory!", "Congratulations! You've won!")
            self.window.quit()
            
    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = MinesweeperGUI()
    game.start()