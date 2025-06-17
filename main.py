import time
from maze_generator import MazeGenerator
from pathfinding import PathFinder

def compare_algorithms(maze_size=15):
    # Tạo mê cung
    generator = MazeGenerator(maze_size, maze_size)
    maze = generator.generate_maze()
    
    print("Mê cung ban đầu:")
    generator.print_maze()
    print("\n")

    # Khởi tạo pathfinder
    pathfinder = PathFinder(maze)
    
    # Danh sách các thuật toán cần so sánh
    algorithms = [
        ("A*", pathfinder.a_star),
        ("BFS", pathfinder.bfs),
        ("DFS", pathfinder.dfs),
        ("Dijkstra", pathfinder.dijkstra)
    ]
    
    # So sánh các thuật toán
    results = []
    for name, algo in algorithms:
        print(f"Đang chạy thuật toán {name}...")
        start_time = time.time()
        path, _, _ = algo()
        end_time = time.time()
        
        if path:
            path_length = len(path)
            time_taken = (end_time - start_time) * 1000  # Chuyển đổi sang milliseconds
            results.append((name, path_length, time_taken))
            
            # Hiển thị đường đi trên mê cung
            maze_copy = maze.copy()
            for y, x in path:
                if maze_copy[y, x] not in [2, 3]:  # Không ghi đè lên điểm bắt đầu và kết thúc
                    maze_copy[y, x] = 4  # Đánh dấu đường đi
            
            print(f"\nKết quả của thuật toán {name}:")
            for row in maze_copy:
                for cell in row:
                    if cell == 1:  # Tường
                        print('█', end='')
                    elif cell == 0:  # Đường trống
                        print(' ', end='')
                    elif cell == 2:  # Điểm bắt đầu
                        print('S', end='')
                    elif cell == 3:  # Điểm kết thúc
                        print('E', end='')
                    elif cell == 4:  # Đường đi
                        print('·', end='')
                print()
            print(f"Do dai duong di: {path_length}")
            print(f"Thoi gian thuc thi: {time_taken:.2f}ms\n")
        else:
            print(f"Khong tim thay đuong đi cho thuật toan {name}\n")
    
    # Hiển thị bảng so sánh
    print("\nBảng so sánh các thuật toán:")
    print("-" * 50)
    print(f"{'Thuật toán':<15}{'Độ dài đường đi':<20}{'Thời gian (ms)':<15}")
    print("-" * 50)
    for name, path_length, time_taken in results:
        print(f"{name:<15}{path_length:<20}{time_taken:.2f}")

if __name__ == "__main__":
    maze_size = int(input("Nhập kích thước mê cung (ví dụ: 15): "))
    compare_algorithms(maze_size)