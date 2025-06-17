from collections import deque
import heapq
import numpy as np

class PathFinder:
    def __init__(self, maze):
        self.maze = maze
        self.height, self.width = maze.shape
        self.start = None
        self.end = None
        self._find_start_end()
        
        # Khởi tạo các biến lưu trữ trạng thái tìm kiếm
        self.bfs_queue = None
        self.dfs_stack = None
        self.astar_pq = None
        self.dijkstra_pq = None
        self.gbfs_pq = None
        
        # Khởi tạo visited nodes
        self.visited = {}
        self.current_node = None

    def reset_state(self):
        self.bfs_queue = None
        self.dfs_stack = None
        self.astar_pq = None
        self.dijkstra_pq = None
        self.visited = {}
        self.current_node = None

    def _find_start_end(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y, x] == 2:  # Start point
                    self.start = (y, x)
                elif self.maze[y, x] == 3:  # End point
                    self.end = (y, x)

    def _get_neighbors(self, pos):
        y, x = pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for dy, dx in directions:
            new_y, new_x = y + dy, x + dx
            if (0 <= new_y < self.height and 0 <= new_x < self.width 
                and self.maze[new_y, new_x] != 1):  # Not a wall
                neighbors.append((new_y, new_x))
        return neighbors

    def _manhattan_distance(self, pos):
        return abs(pos[0] - self.end[0]) + abs(pos[1] - self.end[1])

    def bfs(self):
        """
        Thuật toán Breadth-First Search (BFS) để tìm đường đi ngắn nhất trong mê cung.
        BFS khám phá tất cả các nút lân cận ở độ sâu hiện tại trước khi chuyển sang các nút ở độ sâu tiếp theo.
        Nó đảm bảo tìm thấy đường đi ngắn nhất (theo số bước) trong mê cung không trọng số.
        """
        # Khởi tạo lần đầu
        if self.bfs_queue is None:
            self.visited = {self.start: 0}
            self.bfs_queue = deque([(self.start, [self.start])])
            self.current_node = self.start
            return None, self.visited, self.current_node

        # Xử lý 5 bước
        for _ in range(5):
            if not self.bfs_queue:
                return None, self.visited, self.current_node
            
            self.current_node, path = self.bfs_queue.popleft()
            if self.current_node == self.end:
                return path, self.visited, self.current_node

            for neighbor in self._get_neighbors(self.current_node):
                new_cost = self.visited[self.current_node] + 1
                if neighbor not in self.visited or new_cost < self.visited[neighbor]:
                    self.visited[neighbor] = new_cost
                    self.bfs_queue.append((neighbor, path + [neighbor]))
        
        return None, self.visited, self.current_node

    def greedy_best_first_search(self):
        """
        Thuật toán Greedy Best-First Search (GBFS) để tìm đường đi trong mê cung.
        GBFS mở rộng nút có chi phí heuristic thấp nhất (gần đích nhất).
        Nó không đảm bảo tìm thấy đường đi ngắn nhất hoặc tối ưu, nhưng thường nhanh hơn A*.
        """
        # Khởi tạo lần đầu
        if not hasattr(self, 'gbfs_pq') or self.gbfs_pq is None:
            self.visited = {self.start: 0}
            # Hàng đợi ưu tiên: (heuristic_cost, current_node, path)
            self.gbfs_pq = [(self._manhattan_distance(self.start), self.start, [self.start])]
            self.current_node = self.start
            return None, self.visited, self.current_node

        # Xử lý 5 bước
        for _ in range(5):
            if not self.gbfs_pq:
                return None, self.visited, self.current_node
            
            h_cost, self.current_node, path = heapq.heappop(self.gbfs_pq)

            if self.current_node == self.end:
                return path, self.visited, self.current_node

            for neighbor in self._get_neighbors(self.current_node):
                if neighbor not in self.visited:
                    self.visited[neighbor] = 0 # Cost doesn't matter for visited in GBFS, just mark as visited
                    h = self._manhattan_distance(neighbor)
                    heapq.heappush(self.gbfs_pq, (h, neighbor, path + [neighbor]))
        
        return None, self.visited, self.current_node
        
    def dfs(self):
        """
        Thuật toán Depth-First Search (DFS) để tìm đường đi trong mê cung.
        DFS khám phá càng sâu càng tốt theo mỗi nhánh trước khi quay lui.
        Nó không đảm bảo tìm thấy đường đi ngắn nhất.
        """
        # Khởi tạo lần đầu
        if self.dfs_stack is None:
            self.visited = {self.start: 0}
            self.dfs_stack = [(self.start, [self.start])]
            self.current_node = self.start
            return None, self.visited, self.current_node

        # Xử lý 5 bước
        for _ in range(5):
            if not self.dfs_stack:
                return None, self.visited, self.current_node
            self.current_node, path = self.dfs_stack.pop()
            if self.current_node == self.end:
                return path, self.visited, self.current_node

            for neighbor in self._get_neighbors(self.current_node):
                new_cost = self.visited[self.current_node] + 1
                if neighbor not in self.visited or new_cost < self.visited[neighbor]:
                    self.visited[neighbor] = new_cost
                    self.dfs_stack.append((neighbor, path + [neighbor]))
        
        return None, self.visited, self.current_node

    def a_star(self):
        """
        Thuật toán A* (A-star) để tìm đường đi ngắn nhất trong mê cung.
        A* là một thuật toán tìm kiếm đồ thị và duyệt đồ thị hiệu quả, được sử dụng rộng rãi trong tìm đường và duyệt đồ thị.
        Nó sử dụng hàm heuristic (khoảng cách Manhattan trong trường hợp này) để ước tính chi phí từ nút hiện tại đến đích,
        giúp ưu tiên các đường đi có vẻ hứa hẹn hơn.
        """
        # Khởi tạo lần đầu
        if self.astar_pq is None:
            self.visited = {self.start: 0}
            self.astar_pq = [(0, self.start, [self.start])]
            self.current_node = self.start
            return None, self.visited, self.current_node

        # Xử lý 5 bước
        for _ in range(5):
            if not self.astar_pq:
                return None, self.visited, self.current_node
            f, self.current_node, path = heapq.heappop(self.astar_pq)
            if self.current_node == self.end:
                return path, self.visited, self.current_node

            for neighbor in self._get_neighbors(self.current_node):
                new_cost = self.visited[self.current_node] + 1
                if neighbor not in self.visited or new_cost < self.visited[neighbor]:
                    self.visited[neighbor] = new_cost
                    f = new_cost + self._manhattan_distance(neighbor)
                    heapq.heappush(self.astar_pq, (f, neighbor, path + [neighbor]))
        
        return None, self.visited, self.current_node

    def dijkstra(self):
        """
        Thuật toán Dijkstra để tìm đường đi ngắn nhất từ điểm bắt đầu đến tất cả các điểm khác trong mê cung.
        Dijkstra hoạt động bằng cách khám phá các nút theo thứ tự tăng dần của chi phí đường đi từ điểm bắt đầu.
        Nó đảm bảo tìm thấy đường đi ngắn nhất trong mê cung không có cạnh âm.
        """
        # Khởi tạo lần đầu
        if self.dijkstra_pq is None:
            self.visited = {self.start: 0}
            self.dijkstra_pq = [(0, self.start, [self.start])]
            self.current_node = self.start
            return None, self.visited, self.current_node

        # Xử lý 5 bước
        for _ in range(5):
            if not self.dijkstra_pq:
                return None, self.visited, self.current_node
            cost, self.current_node, path = heapq.heappop(self.dijkstra_pq)
            if self.current_node == self.end:
                return path, self.visited, self.current_node

            for neighbor in self._get_neighbors(self.current_node):
                new_cost = self.visited[self.current_node] + 1
                if neighbor not in self.visited or new_cost < self.visited[neighbor]:
                    self.visited[neighbor] = new_cost
                    heapq.heappush(self.dijkstra_pq, (new_cost, neighbor, path + [neighbor]))
        
        return None, self.visited, self.current_node