import datetime
from PIL import Image, ImageDraw
from exceptions import *

def contains_start_and_goal(maze):
    print(maze)
    try:
        if maze.count("A") != 1 and maze.count("B") != 1:
            raise MazeNeedsStartAndGoal
    except MazeNeedsStartAndGoal as e:
        print(e.message)
        return


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():

    def __init__(self, maze_state):

        self.height = len(maze_state)
        self.width = max(len(line) for line in maze_state)
        self.walls = []

        # Validate start and goal
        contains_start_and_goal(maze_state)
        
        # Keep track of walls  
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    print(maze_state[i][j])
                    if maze_state[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif maze_state[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif maze_state[i][j] == 1:
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def generate_frames(self, show_solution=True, show_explored=True):
        frames = []
        cell_size = 50
        cell_border = 2
    
        for step in range(len(self.solution[1])):
            img = Image.new(
                "RGBA",
                (self.height * cell_size, self.width * cell_size),
                "black"
            )
            draw = ImageDraw.Draw(img)
    
            current_state = self.solution[1][step]
    
            for i, row in enumerate(self.walls):
                for j, col in enumerate(row):
                    if col:
                        fill = (40, 40, 40)
                    elif (i, j) == self.start:
                        fill = (255, 0, 0)
                    elif (i, j) == self.goal:
                        fill = (0, 171, 28)
                    elif show_solution and (i, j) == current_state:
                        fill = (220, 235, 113)
                    elif show_explored and (i, j) in self.explored:
                        fill = (212, 97, 85)
                    else:
                        fill = (237, 240, 252)
    
                    draw.rectangle(
                        ([(j * cell_size + cell_border, i * cell_size + cell_border),
                          ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                        fill=fill
                    )
    
            # Append the current image to the frames list
            frames.append(img)
    
        return frames




    def save_gif(self, show_solution=True, show_explored=True):
        frames = self.generate_frames(show_solution, show_explored)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"maze_{timestamp}.gif"
        frames[0].save(
            filename,
            save_all=True,
            append_images=frames[1:],
            duration=200,  # Adjust the duration between frames as needed
            loop=0  # 0 means an infinite loop
        )
    

