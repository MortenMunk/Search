from tkinter import filedialog
import customtkinter
import webbrowser
# from algo import *

from exceptions import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


EMPTY = 0
START = "A"
GOAL = "B"
ROUTE = 1

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # reduce the minimum size of the application window, because I am too lazy for responsiveness
        self.minsize(600,600)
        self.geometry("800x800")
        self.title("DFS and BFS")

        # Content Frame
        self.content_frame = ContentFrame(self)
        self.content_frame.pack(fill=customtkinter.BOTH, expand=True, padx=10, pady=10)

        # Bottom Navbar Frame
        self.navbar = NavbarFrame(self)
        self.navbar.pack(fill=customtkinter.X, side=customtkinter.BOTTOM, pady=10, padx=10)



class ContentFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.maze_state = {}
        self.is_start_placed = False
        self.is_goal_placed = False
        self.grid_frame = None
        self.columns = None
        self.rows = None
        self.save_maze_frame = False

        self.entry_frame = EntryFrame(self)
        self.entry_frame.pack(side=customtkinter.TOP, pady=10, padx=10)

        # Switch frame
        self.switch_frame = SwitchFrame(self)
        self.switch_frame.pack(side=customtkinter.BOTTOM, pady=10)

        # Load Maze Frame
        self.load_maze_frame = LoadMazeFrame(self)
        self.load_maze_frame.pack(side=customtkinter.BOTTOM, pady=10, padx=10)

        # Components
       # node = Node
       # stack_frontier = StackFrontier
       # queue_frontier = QueueFrontier
       # maze = Maze


        self.grid_frame = None

    def create_grid(self, columns, rows):
        if self.grid_frame is not None:
            self.grid_frame.destroy()
        
        self.maze_state.clear()
        self.is_goal_placed = False
        self.is_start_placed = False

        self.grid_frame = customtkinter.CTkFrame(self)
        self.grid_frame.pack(side=customtkinter.TOP, pady=10, padx=10)

        for row in range(rows):
            for col in range(columns):
                self.maze_state[(row, col)] = EMPTY
                cell = customtkinter.CTkFrame(self.grid_frame, border_width=1, border_color="lightblue", width=30, height=30, corner_radius=0, fg_color="black")
                cell.grid(row=row, column=col, padx=0, pady=0)
                cell.bind("<Button-1>", self.change_cell_state)
                cell.bind("<Button-3>", self.change_cell_state)

        if self.save_maze_frame is False:
            save_maze_frame = customtkinter.CTkFrame(self)
            save_maze_frame.pack(side=customtkinter.BOTTOM)

            save_maze_btn = customtkinter.CTkButton(master=save_maze_frame, text="Save maze", command=self.save_maze)
            save_maze_btn.pack(side=customtkinter.LEFT, padx=20, pady=10)
            self.save_maze_frame = True


    def save_maze(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        values = list(self.maze_state.values())
        text = str(values)[1:-1].replace(",", "").replace(" ", "").replace("'", "")

        if values and text:
            with open(file_path, 'w') as file:
                file.write(f"{self.columns}x{self.rows}\n")
                file.write(text)
                file.close()


    def change_cell_state(self, event):
        widget = event.widget
        row = widget.master.grid_info()["row"]
        col = widget.master.grid_info()["column"]
        if event.num == 1:
            if self.maze_state.get((row, col), EMPTY) == EMPTY:
                self.maze_state[(row, col)] = ROUTE
                widget.master.configure(fg_color="white")
                print("Route placed")
            elif self.maze_state.get((row, col), EMPTY) == ROUTE:
                self.maze_state[(row, col)] = EMPTY
                widget.master.configure(fg_color="black")
                print("Route removed")
            elif self.maze_state.get((row, col), EMPTY) == START or self.maze_state.get((row, col), EMPTY) == GOAL:
                print("Cannot place route on goal or start")
            else:
                print("Undefined error")
        elif event.num == 3:
            if self.maze_state.get((row, col), EMPTY) == EMPTY or self.maze_state.get((row, col), ROUTE) == ROUTE:
                if self.is_start_placed and not self.is_goal_placed:
                    self.maze_state[(row, col)] = GOAL
                    widget.master.configure(fg_color="green")
                    self.is_goal_placed = True
                    print("Goal placed")
                elif not self.is_start_placed and self.is_goal_placed:
                    self.maze_state[(row, col)] = START
                    widget.master.configure(fg_color="yellow")
                    self.is_start_placed = True
                    print("Start placed")
                elif not self.is_start_placed and not self.is_goal_placed:
                    self.maze_state[(row, col)] = START
                    self.is_start_placed = True
                    widget.master.configure(fg_color="yellow")
                    print("Start placed")
                elif self.is_goal_placed and self.is_start_placed:
                    print("Both start and goal placed")
            elif self.maze_state.get((row, col), START) == START:
                self.maze_state[(row, col)] = EMPTY
                self.is_start_placed = False
                widget.master.configure(fg_color="black")
                print("Start removed")
            elif self.maze_state.get((row, col), GOAL) == GOAL:
                self.maze_state[(row, col)] = EMPTY
                self.is_goal_placed = False
                widget.master.configure(fg_color="black")
                print("Goal removed")
            else:
                print("Undefined error")


    def generate_grid(self):
        columns = self.entry_frame.x_axis_entry.get()
        rows = self.entry_frame.y_axis_entry.get()
        try:
            if not columns and not rows:
                raise TypeError

            if not columns.isdigit() and not rows.isdigit():
                raise InvalidGridValue

            columns = int(columns)
            rows = int(rows)

            if columns < 3 or rows < 3:
                raise InvalidGridDimension
            elif columns > 10 or rows > 10:
                raise InvalidGridDimension

            if self.grid_frame is not None:
                self.grid_frame.destroy()

            self.create_grid(columns, rows)
            self.columns = columns
            self.rows = rows
        
        except TypeError as e:
            print(e)
            return
        except InvalidGridValue as e:
            print(e.message)
            return
        except InvalidGridDimension as e:
            print(e.message)
            return


class EntryFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.x_axis_entry = customtkinter.CTkEntry(self, placeholder_text="Columns", width=75)
        self.x_axis_entry.pack(side=customtkinter.LEFT, padx=(20,5), pady=10)

        self.times_label = customtkinter.CTkLabel(self, text="X")
        self.times_label.pack(side=customtkinter.LEFT)

        self.y_axis_entry = customtkinter.CTkEntry(self, placeholder_text="Rows", width=75)
        self.y_axis_entry.pack(side=customtkinter.LEFT, padx=(5,20))

        self.grid_btn = customtkinter.CTkButton(self, text="Generate grid", command=self.master.generate_grid)
        self.grid_btn.pack(side=customtkinter.LEFT, padx=(0,20)) 


class SwitchFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.switch_label_dfs = customtkinter.CTkLabel(self, text="Depth-first", cursor="hand2")
        self.switch_label_dfs.pack(side=customtkinter.LEFT, padx=(20,5))

        self.switch_var = customtkinter.StringVar(value="DFS")
        self.switch = customtkinter.CTkSwitch(self, command=self.switch_event, text="Breadth-first", variable=self.switch_var, onvalue="DFS", offvalue="BFS", switch_width=40)
        self.switch.pack(side=customtkinter.LEFT, pady=10, padx=(5,20))

    def switch_event(self):
        print("switch toggled, current value:", self.switch_var.get())



class LoadMazeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.load_maze_btn = customtkinter.CTkButton(self, text="Load maze", cursor="hand2", command=self.load_maze)
        self.load_maze_btn.pack(side=customtkinter.LEFT, padx=10, pady=10)


    def load_maze(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        # read from file, and split into lines
        with open(file_path, "r") as file:
            maze_lines = file.readlines()

        # if less than 2 lines, then the file does not follow correct format
        try:
            if len(maze_lines) < 2:
                raise NotEnoughLinesInFile
        except NotEnoughLinesInFile as e:
            print(e.message)
            return

        # Checks if there is x and y values that are numeric
        try:
            dimensions = maze_lines[0].strip().split('x')
            if len(dimensions) != 2 or not dimensions[0].isdigit() or not dimensions[1].isdigit():
                raise InvalidGridDimension
        except InvalidGridDimension as e:
            print(e.message)
            return

        x_axis = int(dimensions[0])
        y_axis = int(dimensions[1])

        # checks the maze data has enough coordinates
        try:
            if len(maze_lines[1].strip()) != x_axis * y_axis:
                raise InvalidGridValue
        except InvalidGridValue as e:
            print(e.message)
            return

        # save second line of file as maze data
        maze_data = maze_lines[1].strip()

        maze_state = self.master.maze_state
        maze_state.clear()
        self.master.is_start_placed = False
        self.master.is_goal_placed = False

        self.master.create_grid(x_axis, y_axis)

        for row in range(y_axis):
            for col in range(x_axis):
                index = row * x_axis + col
                char = maze_data[index]

                if char == 'A':
                    maze_state[(row, col)] = START
                elif char == 'B':
                    maze_state[(row, col)] = GOAL
                elif char == '1':
                    maze_state[(row, col)] = ROUTE
                elif char == '0':
                    maze_state[(row, col)] = EMPTY

        # Redraw the maze based on the updated maze_state
        for row in range(y_axis):
            for col in range(x_axis):
                cell_value = maze_state.get((row, col), EMPTY)
                cell = self.master.grid_frame.grid_slaves(row=row, column=col)[0]
                if cell_value == ROUTE:
                    cell.configure(fg_color="white")
                elif cell_value == START:
                    cell.configure(fg_color="yellow")
                elif cell_value == GOAL:
                    cell.configure(fg_color="green")
                elif cell_value == EMPTY:
                    cell.configure(fg_color="black")

        self.is_start_placed = any(val == START for val in maze_state.values())
        self.is_goal_placed = any(val == GOAL for val in maze_state.values())


class NavbarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.navbar_btns = NavbarBtns(self)
        self.navbar_btns.pack(side=customtkinter.TOP, pady=10)

        self.github_link = customtkinter.CTkLabel(self, text="Made by Morten Munk", cursor="hand2", text_color="grey")
        self.github_link.pack(side=customtkinter.BOTTOM, pady=10)
        self.github_link.bind("<Button-1>", lambda e:self.open_url("https://github.com/MortenMunk"))

    def open_url(url):
        webbrowser.open_new_tab(url)



class NavbarBtns(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.source_btn = customtkinter.CTkButton(self, text="Source Code", cursor="hand2")
        self.source_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)
        self.source_btn.bind("<Button-1>", lambda e:self.open_url("https://github.com/MortenMunk/Search/tree/main"))

        self.help_btn = customtkinter.CTkButton(self, text="Documentation", cursor="hand2")
        self.help_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)

        self.contact_btn = customtkinter.CTkButton(self, text="Contact", cursor="hand2")
        self.contact_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)

    def open_url(url):
        webbrowser.open_new_tab(url)


app = App()
app.mainloop()