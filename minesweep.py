import random
from colorama import init, Fore, Back, Style

init()  # Initialize colorama

class Minesweeper:
    def __init__(self, width=10, height=10, num_mines=15):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flags = [[False for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.victory = False
        
        self.place_mines()
        self.calculate_numbers()
        
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
                
    def reveal(self, x, y):
        if self.game_over or self.revealed[y][x]:
            return
            
        if self.flags[y][x]:
            return
            
        self.revealed[y][x] = True
        
        if self.board[y][x] == -1:
            self.game_over = True
            self.victory = False
            return
            
        if self.board[y][x] == 0:
            self.reveal_adjacent(x, y)
            
        self.check_victory()
            
    def reveal_adjacent(self, x, y):
        for i in range(max(0, y-1), min(y+2, self.height)):
            for j in range(max(0, x-1), min(x+2, self.width)):
                if not self.revealed[i][j]:
                    self.reveal(j, i)
                    
    def toggle_flag(self, x, y):
        if self.game_over or self.revealed[y][x]:
            return
        self.flags[y][x] = not self.flags[y][x]
        
    def check_victory(self):
        self.victory = True
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    self.victory = False
                    return
                    
    def print_board(self):
        print("  " + " ".join(str(i) for i in range(self.width)))
        print("  " + "-" * (self.width * 2 - 1))
        
        for y in range(self.height):
            row = str(y) + "|"
            for x in range(self.width):
                if self.revealed[y][x]:
                    if self.board[y][x] == -1:
                        row += Fore.RED + "M" + Style.RESET_ALL
                    else:
                        color = Fore.WHITE
                        if self.board[y][x] == 1: color = Fore.BLUE
                        elif self.board[y][x] == 2: color = Fore.GREEN
                        elif self.board[y][x] == 3: color = Fore.RED
                        elif self.board[y][x] == 4: color = Fore.MAGENTA
                        elif self.board[y][x] == 5: color = Fore.YELLOW
                        elif self.board[y][x] == 6: color = Fore.CYAN
                        row += color + str(self.board[y][x]) + Style.RESET_ALL
                elif self.flags[y][x]:
                    row += Fore.YELLOW + "F" + Style.RESET_ALL
                else:
                    row += " "
                row += "|"
            print(row)
            
    def play(self):
        while not self.game_over:
            self.print_board()
            action = input("\nEnter action (r for reveal, f for flag), followed by coordinates (e.g., r 3 4): ").strip().lower()
            
            try:
                if action[0] == 'r':
                    x, y = map(int, action[2:].split())
                    self.reveal(x, y)
                elif action[0] == 'f':
                    x, y = map(int, action[2:].split())
                    self.toggle_flag(x, y)
                else:
                    print("Invalid action. Use 'r' to reveal or 'f' to flag.")
                    continue
            except:
                print("Invalid input. Please enter coordinates in the format: r x y or f x y")
                continue
                
        self.print_board()
        if self.victory:
            print("Congratulations! You've won!")
        else:
            print("Game Over! You hit a mine.")

if __name__ == "__main__":
    game = Minesweeper()
    game.play()