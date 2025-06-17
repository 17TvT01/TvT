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
        self.window_width = self.maze_size * self.cell_size + self.padding * 2
        self.window_height = self.maze_size * self.cell_size + self.padding * 2 + self.info_height
        
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
        pygame.display.set_caption('Mê cung - Tìm đường')
        
        # Font chữ
        self.font = pygame.font.Font(None, 24)
        
        # Tạo mê cung
        self.generator = MazeGenerator(maze_size, maze_size)
        self.maze = self.generator.generate_maze()
        self.pathfinder = PathFinder(self.maze)
        
        # Thuật toán hiện tại
        self.current_algorithm = None
        self.algorithm_data = {
            'path': None,
            'visited': {},
            'current': None,
            'time': 0
        }
        
        # Danh sách thuật toán
        self.algorithms = ['A*', 'BFS', 'DFS', 'Dijkstra', 'Greedy Best-First Search']
        self.selected_index = 0
        
        self.animation_speed = 200  # ms delay
        self.paused = False
        self.algorithm_selected = False
        

    
    def draw_algorithm_selection(self):
        self.screen.fill(self.WHITE)
        
        title = self.font.render('Chọn thuật toán:', True, self.BLACK)
        title_rect = title.get_rect(center=(self.window_width // 2, self.padding * 2))
        self.screen.blit(title, title_rect)
        
        for i, algo in enumerate(self.algorithms):
            color = self.BLUE if i == self.selected_index else self.BLACK
            text = self.font.render(algo, True, color)
            text_rect = text.get_rect(
                center=(self.window_width // 2,
                       self.padding * 4 + i * 30)
            )
            self.screen.blit(text, text_rect)
    
    def draw_maze(self):
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                rect = pygame.Rect(
                    self.padding + x * self.cell_size,
                    self.padding + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                # Vẽ các ô
                if self.maze[y, x] == 1:  # Tường
                    pygame.draw.rect(self.screen, self.BLACK, rect)
                elif (y, x) in self.pathfinder.visited:  # Ô đã duyệt
                    pygame.draw.rect(self.screen, self.GRAY, rect)
                else:  # Đường đi
                    pygame.draw.rect(self.screen, self.WHITE, rect)
                
                # Vẽ điểm bắt đầu và kết thúc
                if self.maze[y, x] == 2:  # Điểm bắt đầu
                    pygame.draw.rect(self.screen, self.GREEN, rect)
                elif self.maze[y, x] == 3:  # Điểm kết thúc
                    pygame.draw.rect(self.screen, self.RED, rect)
                
                # Vẽ đường đi tìm được
                if self.algorithm_data['path'] and (y, x) in self.algorithm_data['path']:
                    pygame.draw.rect(self.screen, self.YELLOW, rect)
                
                # Vẽ vị trí hiện tại
                if self.algorithm_data['current'] and (y, x) == self.algorithm_data['current']:
                    pygame.draw.rect(self.screen, self.BLUE, rect)
    
    def draw_info(self):
        info_rect = pygame.Rect(
            self.padding,
            self.padding + self.maze_size * self.cell_size,
            self.maze_size * self.cell_size,
            self.info_height
        )
        pygame.draw.rect(self.screen, self.WHITE, info_rect)
        
        # Hiển thị thông tin
        text_y = self.padding + self.maze_size * self.cell_size + 10
        
        # Tên thuật toán
        algo_text = self.font.render(
            f'Thuật toán: {self.current_algorithm}',
            True, self.BLACK
        )
        self.screen.blit(algo_text, (self.padding + 10, text_y))
        
        # Số ô đã duyệt
        visited_text = self.font.render(
            f'Số ô đã duyệt: {len(self.pathfinder.visited)}',
            True, self.BLACK
        )
        self.screen.blit(visited_text, (self.padding + 10, text_y + 20))
        
        # Thời gian thực thi
        time_text = self.font.render(
            f'Thời gian: {self.algorithm_data["time"]:.2f}ms',
            True, self.BLACK
        )
        self.screen.blit(time_text, (self.padding + 10, text_y + 40))
        
        # Hướng dẫn phím
        if self.algorithm_data['path']:
            help_text = self.font.render(
                'Nhấn N để tìm đường mới, R để tạo mê cung mới',
                True, self.BLACK
            )
            self.screen.blit(help_text, (self.padding + 10, text_y + 60))
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.algorithm_selected:
                        if event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % len(self.algorithms)
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % len(self.algorithms)
                        elif event.key == pygame.K_RETURN:
                            self.current_algorithm = self.algorithms[self.selected_index]
                            self.algorithm_selected = True
                            self.pathfinder.reset_state() # Reset visited nodes and other states
                    else:
                        if event.key == pygame.K_SPACE:
                            self.paused = not self.paused
                        elif event.key == pygame.K_UP:
                            self.animation_speed = max(10, self.animation_speed - 10)
                        elif event.key == pygame.K_DOWN:
                            self.animation_speed = min(200, self.animation_speed + 10)
                        elif event.key == pygame.K_r:
                            # Reset
                            self.algorithm_selected = False
                            self.algorithm_data = {
                                'path': None,
                                'visited': {},
                                'current': None,
                                'time': 0
                            }
                            self.maze = self.generator.generate_maze()
                            self.pathfinder = PathFinder(self.maze)
                            self.pathfinder.reset_state()
                        elif event.key == pygame.K_n and self.algorithm_data['path']:
                            # Tìm đường mới sau khi đã tìm thấy đường đi
                            self.algorithm_data['path'] = None
                            self.pathfinder.reset_state() # Reset visited nodes and other states
                            self.algorithm_data['current'] = None
            
            self.screen.fill(self.WHITE)
            
            if not self.algorithm_selected:
                self.draw_algorithm_selection()
            else:
                if not self.paused:
                    start_time = time.time()
                    
                    # Thực hiện một bước của thuật toán nếu chưa tìm được đường đi hoàn chỉnh
                    if not self.algorithm_data['path'] or (self.algorithm_data['path'] and self.algorithm_data['path'][-1] != self.pathfinder.end):
                        if self.current_algorithm == 'A*':
                            path, visited, current = self.pathfinder.a_star()
                        elif self.current_algorithm == 'BFS':
                            path, visited, current = self.pathfinder.bfs()
                        elif self.current_algorithm == 'DFS':
                            path, visited, current = self.pathfinder.dfs()
                        elif self.current_algorithm == 'Dijkstra':
                            path, visited, current = self.pathfinder.dijkstra()
                        elif self.current_algorithm == 'Greedy Best-First Search':
                            path, visited, current = self.pathfinder.greedy_best_first_search()
                        
                        self.algorithm_data['path'] = path
                        self.pathfinder.visited = visited # Update the pathfinder's visited set
                        self.pathfinder.current_node = current # Update the pathfinder's current node
                        self.algorithm_data['current'] = current

                    
                    # Cập nhật vị trí hiện tại
                    if not self.algorithm_data['path']:
                        for y in range(self.maze_size):
                            for x in range(self.maze_size):
                                if (y, x) in self.algorithm_data['visited'] and (y, x) != self.algorithm_data['current']:
                                    self.algorithm_data['current'] = (y, x)
                                    break
                    
                    self.algorithm_data['time'] = (time.time() - start_time) * 1000
                
                # Vẽ mê cung và thông tin
                self.draw_maze()
                self.draw_info()
            
            pygame.display.flip()
            clock.tick(1000 / self.animation_speed)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    maze_size = int(input("Nhập kích thước mê cung (ví dụ: 15): "))
    visualizer = MazeVisualizer(maze_size)
    visualizer.run()