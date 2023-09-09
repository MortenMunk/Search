from tkinter import filedialog
import customtkinter
import webbrowser
from algo import *
import functools
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

        # Empty 2D array
        self.maze_state = []
        self.is_start_placed = False
        self.is_goal_placed = False
        self.grid_frame = None
        self.columns = None
        self.rows = None

        self.entry_frame = EntryFrame(self)
        self.entry_frame.pack(side=customtkinter.TOP, pady=10, padx=10)

        # Switch frame
        self.switch_cont_frame = SwitchContainerFrame(self)
        self.switch_cont_frame.pack(side=customtkinter.BOTTOM, padx=20, fill=customtkinter.X, pady=20)

        # Load Maze Frame
        self.load_maze_frame = LoadMazeFrame(self)
        self.load_maze_frame.pack(side=customtkinter.BOTTOM, pady=10, padx=10)

        self.grid_frame = None

    def create_grid(self, columns, rows):
        if self.grid_frame is not None:
            self.grid_frame.destroy()
        
        self.maze_state = [[EMPTY for _ in range(columns)] for _ in range(rows)]
        self.is_goal_placed = False
        self.is_start_placed = False

        if self.grid_frame is None:
            save_maze_frame = customtkinter.CTkFrame(self)
            save_maze_frame.pack(side=customtkinter.BOTTOM)

            save_maze_btn = customtkinter.CTkButton(master=save_maze_frame, text="Save maze", command=self.save_maze)
            save_maze_btn.pack(side=customtkinter.LEFT, padx=20, pady=10)

            search_frame = customtkinter.CTkFrame(self.switch_cont_frame)
            search_frame.pack(side=customtkinter.BOTTOM, padx=20, pady=(0,10))

            search_btn = customtkinter.CTkButton(search_frame, text="Search", command=functools.partial(self.search))
            search_btn.pack(side=customtkinter.BOTTOM, padx=20, pady=10)
        

        self.grid_frame = customtkinter.CTkFrame(self)
        self.grid_frame.pack(side=customtkinter.TOP, pady=10, padx=10)

        for row in range(rows):
            for col in range(columns):
                self.maze_state[row][col] = EMPTY
                cell = customtkinter.CTkFrame(self.grid_frame, border_width=1, border_color="lightblue", width=30, height=30, corner_radius=0, fg_color="black")
                cell.grid(row=row, column=col, padx=0, pady=0)
                cell.bind("<Button-1>", self.change_cell_state)
                cell.bind("<Button-3>", self.change_cell_state)


    
    def search(self):
        print(self.rows)
        print(self.columns)
        m = Maze(self.maze_state, self.rows, self.columns)
        m.solve()
        m.output_image("maze.png", show_explored=True)


    def save_maze(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if self.maze_state:
            with open(file_path, 'w') as file:
                for row in range(self.rows):
                    for col in range(self.columns):
                        file.write(str(self.maze_state[row][col]))
                    file.write("\n")
                file.close()


    def change_cell_state(self, event):
        widget = event.widget
        row = widget.master.grid_info()["row"]
        col = widget.master.grid_info()["column"]
        if event.num == 1:
            if self.maze_state[row][col] == EMPTY:
                self.maze_state[row][col] = ROUTE
                widget.master.configure(fg_color="white")
                print("Route placed")
            elif self.maze_state[row][col] == ROUTE:
                self.maze_state[row][col] = EMPTY
                widget.master.configure(fg_color="black")
                print("Route removed")
            elif self.maze_state[row][col] == START or self.maze_state[row][col] == GOAL:
                print("Cannot place route on goal or start")
            else:
                print("Undefined error")
        elif event.num == 3:
            if self.maze_state[row][col] == EMPTY or self.maze_state[row][col] == ROUTE:
                if self.is_start_placed and not self.is_goal_placed:
                    self.maze_state[row][col] = GOAL
                    widget.master.configure(fg_color="green")
                    self.is_goal_placed = True
                    print("Goal placed")
                elif not self.is_start_placed and self.is_goal_placed:
                    self.maze_state[row][col] = START
                    widget.master.configure(fg_color="yellow")
                    self.is_start_placed = True
                    print("Start placed")
                elif not self.is_start_placed and not self.is_goal_placed:
                    self.maze_state[row][col] = START
                    self.is_start_placed = True
                    widget.master.configure(fg_color="yellow")
                    print("Start placed")
                elif self.is_goal_placed and self.is_start_placed:
                    print("Both start and goal placed")
            elif self.maze_state[row][col] == START:
                self.maze_state[row][col] = EMPTY
                self.is_start_placed = False
                widget.master.configure(fg_color="black")
                print("Start removed")
            elif self.maze_state[row][col] == GOAL:
                self.maze_state[row][col] = EMPTY
                self.is_goal_placed = False
                widget.master.configure(fg_color="black")
                print("Goal removed")
            else:
                print("Undefined error")
        print(str(self.maze_state))


    def generate_grid(self):
        self.columns = self.entry_frame.x_axis_entry.get()
        self.rows = self.entry_frame.y_axis_entry.get()
        try:
            if not self.columns and not self.rows:
                raise TypeError

            if not self.columns.isdigit() and not self.rows.isdigit():
                raise InvalidGridValue

            self.columns = int(self.columns)
            self.rows = int(self.rows)

            if self.columns < 3 or self.rows < 3:
                raise InvalidGridDimension
            elif self.columns > 10 or self.rows > 10:
                raise InvalidGridDimension

            if self.grid_frame is not None:
                self.grid_frame.destroy()

            for _ in range(self.rows):
                row = []
                for _ in range(self.columns):
                    row.append(None)
                    self.maze_state.append(row)

            self.create_grid(self.columns, self.rows)
        
        except TypeError as e:
            print(e)
            return
        except InvalidGridValue as e:
            print(e.message)
            return
        except InvalidGridDimension as e:
            print(e.message)
            return
        

class SwitchContainerFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
       
        self.switch_frame = SwitchFrame(self)
        self.switch_frame.pack(side=customtkinter.TOP, pady=10)


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
            content = file.read().splitlines()

        try:
            start_count = sum(row.count('A') for row in content)
            goal_count = sum(row.count('B') for row in content)
            if start_count != 1 or goal_count != 1:
                raise MazeNeedsStartAndGoal
        except MazeNeedsStartAndGoal as e:
            print(e.message)
            return
    
        rows = len(content)
        columns = len(content[0])

        try:
            # if less than 3 rows or columns throw error
            if columns < 3 or rows < 3:
                raise NotEnoughLinesInFile
            # if more than 10 rows or columns throw error
            elif columns > 10 or rows > 10:
                raise InvalidGridDimension
        except NotEnoughLinesInFile as e:
            print(e.message)
            return
        except InvalidGridDimension as e:
            print(e.message)
            return


        # save second line of file as maze data
        self.master.maze_state.clear()
        self.master.is_start_placed = False
        self.master.is_goal_placed = False

        self.master.create_grid(columns, rows)

        for row in range(rows):
            for col in range(columns):
                if content[row][col] == 'A':
                    self.master.maze_state[row][col] = START
                elif content[row][col] == 'B':
                    self.master.maze_state[row][col] = GOAL
                elif content[row][col] == '1':
                    self.master.maze_state[row][col] = ROUTE
                elif content[row][col] == '0':
                    self.master.maze_state[row][col] = EMPTY

        # Redraw the maze based on the updated maze_state
        for row in range(rows):
            for col in range(columns):
                cell_value = self.master.maze_state[row][col]
                cell = self.master.grid_frame.grid_slaves(row=row, column=col)[0]
                if cell_value == ROUTE:
                    cell.configure(fg_color="white")
                elif cell_value == START:
                    cell.configure(fg_color="yellow")
                elif cell_value == GOAL:
                    cell.configure(fg_color="green")
                elif cell_value == EMPTY:
                    cell.configure(fg_color="black")

        self.is_start_placed = True
        self.is_goal_placed = True
        print(self.master.maze_state)


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