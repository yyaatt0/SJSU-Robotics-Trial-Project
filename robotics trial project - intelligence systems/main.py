import pygame
import random
import heapq

# Constants
WIDTH = 800  # Width of the grid
HEIGHT = 600  # Height of the grid
GRID_SIZE = 20  # Size of each grid cell
NUM_ROWS = HEIGHT // GRID_SIZE  # y-axis
NUM_COLS = WIDTH // GRID_SIZE  # x-axis

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Attributes of the Rover object
class Rover:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Attributes of the Obstacle object
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Endpoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Data structure that represents each point in the grid
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

# Define a heuristic function (Manhattan distance) for A*
def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

# A* algorithm
def astar(start, goal, obstacles):
    open_list = []
    closed_set = set()

    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])

    start_node.g = 0
    start_node.h = heuristic(start_node, goal_node)
    start_node.f = start_node.g + start_node.h

    heapq.heappush(open_list, start_node)

    steps = 0
    collisions = 0

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.x == goal_node.x and current_node.y == goal_node.y:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1], steps, collisions

        closed_set.add((current_node.x, current_node.y))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = current_node.x + dx, current_node.y + dy

            if (
                0 <= new_x < NUM_COLS
                and 0 <= new_y < NUM_ROWS
                and (new_x, new_y) not in closed_set
                and not any(obstacle.x == new_x and obstacle.y == new_y for obstacle in obstacles)
            ):
                neighbor_node = Node(new_x, new_y)
                neighbor_node.parent = current_node
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = heuristic(neighbor_node, goal_node)
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                heapq.heappush(open_list, neighbor_node)
                steps += 1

                if any(obstacle.x == new_x and obstacle.y == new_y for obstacle in obstacles):
                    collisions += 1

    return None, steps, collisions

# Creates a visible grid
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

# Draw obstacles on the grid
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle.draw()

# Draw the path on the grid
def draw_path(path):
    for node in path:
        pygame.draw.rect(screen, BLACK, (node[0] * GRID_SIZE, node[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Animates the path on the grid
def animate_path(path, rover, obstacles, endpoint):
    for i in range(len(path)):
        new_x, new_y = path[i]
        dx = new_x - rover.x
        dy = new_y - rover.y

        if 0 <= new_x < NUM_COLS and 0 <= new_y < NUM_ROWS and not is_collision(Rover(new_x, new_y), obstacles):
            rover.move(dx, dy)

        screen.fill(WHITE)
        draw_grid()
        draw_obstacles(obstacles)
        rover.draw()
        endpoint.draw()
        draw_path(path[:i+1])
        pygame.display.flip()
        clock.tick(10)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# Generate obstacles
def generate_obstacles(num_obstacles):
    obstacles = []
    for _ in range(num_obstacles):
        x = random.randint(0, NUM_COLS - 1)
        y = random.randint(0, NUM_ROWS - 1)
        obstacles.append(Obstacle(x, y))
    return obstacles

# Check if a point is an endpoint
def is_endpoint(rover, endpoint):
    return rover.x == endpoint.x and rover.y == endpoint.y

# Check for collisions with obstacles
def is_collision(rover, obstacles):
    for obstacle in obstacles:
        if rover.x == obstacle.x and rover.y == obstacle.y:
            return True
    return False

def main():
    numOfSteps = 0
    numOfCollisions = 0

    numOfObs = int(input("Enter the number of obstacles: "))

    rover = Rover(0, 0)
    obstacles = generate_obstacles(numOfObs)

    x = random.randint(NUM_COLS // 2, NUM_COLS - 1)
    y = random.randint(NUM_ROWS // 2, NUM_ROWS - 1)

    start = (0, 0)
    end = (x, y)
    endpoint = Endpoint(x, y)

    path, steps, collisions = astar(start, end, obstacles)
    success = True

    selection = int(input("Enter '1' for manual movement. Enter '2' for autonomous navigation. "))

    if selection == 1:
        while success:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -1
            elif keys[pygame.K_RIGHT]:
                dx = 1
            elif keys[pygame.K_UP]:
                dy = -1
            elif keys[pygame.K_DOWN]:
                dy = 1

            new_x = rover.x + dx
            new_y = rover.y + dy

            if 0 <= new_x < NUM_COLS and 0 <= new_y < NUM_ROWS and not is_collision(Rover(new_x, new_y), obstacles):
                rover.move(dx, dy)
                numOfSteps += 1

            if is_collision(Rover(new_x, new_y), obstacles):
                numOfCollisions += 1

            screen.fill(WHITE)
            draw_grid()
            draw_obstacles(obstacles)
            rover.draw()
            endpoint.draw()

            if is_endpoint(Rover(new_x, new_y), endpoint):
                success = False

            pygame.display.flip()
            clock.tick(15)
    elif selection == 2:
        while success:
            numOfSteps += steps
            numOfCollisions += collisions

            if path:
                animate_path(path, rover, obstacles, endpoint)
                if is_endpoint(Rover(rover.x, rover.y), endpoint):
                    success = False

    print("Number of Collisions: ", numOfCollisions)
    print("Number of Steps: ", numOfSteps)

    print("SUCCESS\nThe rover has reached the endpoint")

if __name__ == '__main__':
    main()