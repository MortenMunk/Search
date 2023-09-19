import datetime
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from exceptions import *

def contains_start_and_goal(maze):
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


    def solve(self, search_type):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        try:
            if search_type == "dfs":
                frontier = StackFrontier()
            elif search_type == "bfs":
                frontier = QueueFrontier()
            else:
                raise InvalidSearchType
        except InvalidSearchType as e:
            print(e.message)
            return    
            
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

      # Provide the path to your own font file (.ttf)
      relative_path = os.getcwd()
      font_path = "VCR_OSD_MONO_1.001.ttf"
      font_path = relative_path + '\\' + font_path
      font_size = 16  # Adjust the font size as needed
      font = ImageFont.truetype(font_path, font_size)

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

                  # Draw the step number inside the rectangle
                  if (i, j) == current_state:
                      text = str(step + 1)  # Step numbers start from 1

                      # Calculate text size and position using textsize
                      text_box = draw.textbbox((j * cell_size, i * cell_size), text, font=font)
                      text_width = text_box[2] - text_box[0]
                      text_height = text_box[3] - text_box[1]
                      
                      text_x = (j * cell_size + (cell_size - text_width) // 2)
                      text_y = (i * cell_size + (cell_size - text_height) // 2)

                      # Draw text on the image
                      draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

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
    

