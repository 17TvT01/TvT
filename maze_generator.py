import random
import numpy as np

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = np.ones((height, width), dtype=int)  # 1 represents walls

    def generate_maze(self):
        # Start from cell (1,1)
        self.recursive_backtracker(1, 1)
        # Set start point at (1,1) and end point at bottom-right corner
        self.maze[1, 1] = 2  # Start point
        self.maze[self.height-2, self.width-2] = 3  # End point
        return self.maze

    def recursive_backtracker(self, x, y):
        self.maze[y, x] = 0  # Mark current cell as path

        # Define possible directions (up, right, down, left)
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            # Check if the new position is within bounds and unvisited
            if (0 < new_x < self.width-1 and 0 < new_y < self.height-1 
                and self.maze[new_y, new_x] == 1):
                # Create a path by setting the cell between current and new position to 0
                self.maze[y + dy//2, x + dx//2] = 0
                self.recursive_backtracker(new_x, new_y)

    def get_maze(self):
        return self.maze.copy()

    def print_maze(self):
        for row in self.maze:
            for cell in row:
                if cell == 1:  # Wall
                    print('█', end='')
                elif cell == 0:  # Path
                    print(' ', end='')
                elif cell == 2:  # Start
                    print('S', end='')
                elif cell == 3:  # End
                    print('E', end='')
            print()