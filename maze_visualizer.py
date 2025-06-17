import pygame
import sys
import time
from maze_generator import MazeGenerator
from pathfinding import PathFinder
import pygame

class MazeVisualizer:
    def __init__(self, maze_size=15):
        pygame.init()
        self.maze_size = maze_size
        self.cell_size = 30
        self.padding = 20
        self.info_height = 60
        
        # Kích thước cửa sổ
        self.window_width = (self.maze_size * self.cell_size + self.padding) * 2 + self.padding
        self.window_height = (self.maze_size * self.cell_size + self.padding + self.info_height) * 2 + self.padding
        
        # Màu sắc
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)
        
        # Khởi tạo cửa sổ
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('So sánh thuật toán tìm đường')
        
        # Font chữ
        self.font = pygame.font.Font(None, 24)
        
        # Tạo mê cung
        self.generator = MazeGenerator(maze_size, maze_size)
        self.maze = self.generator.generate_maze()
        self.pathfinder = PathFinder(self.maze)
        
        # Trạng thái các thuật toán
        self.algorithms = {
            'A*': {'path': None, 'visited': set(), 'current': None, 'time': 0},
            'BFS': {'path': None, 'visited': set(), 'current': None, 'time': 0},
            'DFS': {'path': None, 'visited': set(), 'current': None, 'time': 0},
            'Dijkstra': {'path': None, 'visited': set(), 'current': None, 'time': 0}
        }
        
        # Vị trí hiển thị từng thuật toán
        self.positions = {
            'A*': (self.padding, self.padding),
            'BFS': (self.padding * 2 + maze_size * self.cell_size, self.padding),
            'DFS': (self.padding, self.padding * 2 + maze_size * self.cell_size + self.info_height),
            'Dijkstra': (self.padding * 2 + maze_size * self.cell_size, 
                        self.padding * 2 + maze_size * self.cell_size + self.info_height)
        }
        
        self.animation_speed = 50  # ms delay
        self.paused = False
    
    def draw_maze(self, pos_x, pos_y, visited, current, path):
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                rect = pygame.Rect(
                    pos_x + x * self.cell_size,
                    pos_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                # Vẽ các ô
                if self.maze[y, x] == 1:  # Tường
                    pygame.draw.rect(self.screen, self.BLACK, rect)
                elif (y, x) in visited:  # Ô đã duyệt
                    pygame.draw.rect(self.screen, self.GRAY, rect)
                else:  # Đường đi
                    pygame.draw.rect(self.screen, self.WHITE, rect)
                
                # Vẽ điểm bắt đầu và kết thúc
                if self.maze[y, x] == 2:  # Điểm bắt đầu
                    pygame.draw.rect(self.screen, self.GREEN, rect)
                elif self.maze[y, x] == 3:  # Điểm kết thúc
                    pygame.draw.rect(self.screen, self.RED, rect)
                
                # Vẽ đường đi tìm được
                if path and (y, x) in path:
                    pygame.draw.rect(self.screen, self.YELLOW, rect)
                
                # Vẽ vị trí hiện tại
                if current and (y, x) == current:
                    pygame.draw.rect(self.screen, self.BLUE, rect)
    
    def draw_info(self, pos_x, pos_y, algo_name, algo_data):
        info_rect = pygame.Rect(
            pos_x,
            pos_y + self.maze_size * self.cell_size,
            self.maze_size * self.cell_size,
            self.info_height
        )
        pygame.draw.rect(self.screen, self.WHITE, info_rect)
        
        # Hiển thị thông tin
        text_y = pos_y + self.maze_size * self.cell_size + 10
        
        # Tên thuật toán
        algo_text = self.font.render(f'Thuật toán: {algo_name}', True, self.BLACK)
        self.screen.blit(algo_text, (pos_x + 10, text_y))
        
        # Số ô đã duyệt
        visited_text = self.font.render(
            f'Số ô đã duyệt: {len(algo_data["visited"])}',
            True, self.BLACK
        )
        self.screen.blit(visited_text, (pos_x + 10, text_y + 20))
        
        # Thời gian thực thi
        time_text = self.font.render(
            f'Thời gian: {algo_data["time"]:.2f}ms',
            True, self.BLACK
        )
        self.screen.blit(time_text, (pos_x + 10, text_y + 40))
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_UP:
                        self.animation_speed = max(10, self.animation_speed - 10)
                    elif event.key == pygame.K_DOWN:
                        self.animation_speed = min(200, self.animation_speed + 10)
                    elif event.key == pygame.K_n:
                        self.maze = self.generator.generate_maze()
                        self.pathfinder = PathFinder(self.maze)
                        self.pathfinder.reset_state()
                        self.reset_algorithms()
                    elif event.key == pygame.K_r:
                        self.maze = self.generator.generate_maze()
                        self.pathfinder = PathFinder(self.maze)
                        self.pathfinder.reset_state()
                        self.reset_algorithms()
            
            if not self.paused:
                self.screen.fill(self.WHITE)
                
                # Cập nhật và vẽ từng thuật toán
                for algo_name, algo_data in self.algorithms.items():
                    pos_x, pos_y = self.positions[algo_name]
                    
                    # Thực hiện một bước của thuật toán
                    start_time = time.time()
                    if algo_name == 'A*':
                        path, visited, current = self.pathfinder.a_star()
                    elif algo_name == 'BFS':
                        path, visited, current = self.pathfinder.bfs()
                    elif algo_name == 'DFS':
                        path, visited, current = self.pathfinder.dfs()
                    else:  # Dijkstra
                        path, visited, current = self.pathfinder.dijkstra()
                    
                    algo_data['path'] = path
                    algo_data['visited'] = visited
                    algo_data['current'] = current
                    algo_data['time'] = (time.time() - start_time) * 1000
                    
                    # Vẽ mê cung và thông tin
                    self.draw_maze(
                        pos_x, pos_y,
                        algo_data['visited'],
                        algo_data['current'],
                        algo_data['path']
                    )
                    self.draw_info(pos_x, pos_y, algo_name, algo_data)
                
                pygame.display.flip()
                clock.tick(1000 / self.animation_speed)
        
        pygame.quit()
        sys.exit()

    def reset_algorithms(self):
        for algo_name in self.algorithms:
            self.algorithms[algo_name] = {'path': None, 'visited': set(), 'current': None, 'time': 0}

if __name__ == "__main__":
    maze_size = int(input("Nhập kích thước mê cung (ví dụ: 15): "))
    visualizer = MazeVisualizer(maze_size)
    visualizer.run()