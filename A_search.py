import pygame
import heapq
import random

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước màn hình và kích thước ô
WIDTH, HEIGHT = 600, 400  # Kích thước màn hình game
CELL_SIZE = 20  # Kích thước mỗi ô vuông trong game

# Định nghĩa các màu sắc sử dụng trong game
BLACK = (0, 0, 0)    # Màu đen cho nền
WHITE = (255, 255, 255)  # Màu trắng cho mắt rắn và text
GREEN = (0, 255, 0)   # Màu xanh lá cho thân rắn

# Thiết lập cửa sổ game và đặt tiêu đề
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Durian")

# Biến lưu điểm cao nhất
high_score = 0

# Hàm tính khoảng cách Manhattan giữa 2 điểm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Thuật toán A* để tìm đường đi
def astar_search(start, goal, obstacles, grid_size):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        neighbors = [
            (current[0] + 1, current[1]),  # Phải
            (current[0] - 1, current[1]),  # Trái
            (current[0], current[1] + 1),  # Dưới
            (current[0], current[1] - 1),  # Trên
        ]

        for neighbor in neighbors:
            if (
                0 <= neighbor[0] < grid_size[0]
                and 0 <= neighbor[1] < grid_size[1]
                and neighbor not in obstacles
            ):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

# Thiết lập các thông số ban đầu của game
grid_size = (WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)
snake = [(5, 5)]
snake_dir = (1, 0)
food = (10, 10)
obstacles = set()
clock = pygame.time.Clock()
score = 0

# Tải hình ảnh quả sầu riêng
durian_img = pygame.image.load("durian.png")
durian_img = pygame.transform.scale(durian_img, (CELL_SIZE * 2, CELL_SIZE * 2))  # Tăng gấp đôi  # Thay đổi kích thước cho phù hợp

# Thiết lập font chữ để hiển thị điểm
font = pygame.font.Font(None, 36)

# Vòng lặp chính của game
running = True
while running:
    screen.fill(BLACK)

    # Vẽ rắn và mắt rắn
    for i, segment in enumerate(snake):
        pygame.draw.rect(
            screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )
        if i == 0:
            pygame.draw.circle(screen, WHITE, 
                (int(segment[0] * CELL_SIZE + CELL_SIZE//4), 
                 int(segment[1] * CELL_SIZE + CELL_SIZE//4)), 3)
            pygame.draw.circle(screen, WHITE,
                (int(segment[0] * CELL_SIZE + 3*CELL_SIZE//4),
                 int(segment[1] * CELL_SIZE + CELL_SIZE//4)), 3)

    # Vẽ thức ăn (quả sầu riêng)
    screen.blit(durian_img, (food[0] * CELL_SIZE, food[1] * CELL_SIZE))

    # Hiển thị điểm số và điểm cao nhất
    score_text = font.render(f'Score: {score}', True, WHITE)
    high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (WIDTH - 200, 10))

    pygame.display.flip()

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        # Tìm đường đi đến thức ăn bằng A*
        path = astar_search(snake[0], food, set(snake[1:]) | obstacles, grid_size)

        if path:
            next_step = path[0]
            snake.insert(0, next_step)

            if next_step == food:
                score += 10
                if score > high_score:
                    high_score = score
                attempts = 0
                while attempts < 100:
                    food = (random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1))
                    if food not in snake:
                        break
                    attempts += 1
                if attempts >= 100:
                    print("You Win!")
                    running = False
            else:
                snake.pop()
        else:
            print("Game Over!")
            if score > high_score:
                high_score = score
            snake = [(5, 5)]
            food = (10, 10)
            score = 0

    except Exception as e:
        print(f"Error: {e}")
        snake = [(5, 5)]
        food = (10, 10)
        score = 0

    clock.tick(10)

pygame.quit()
