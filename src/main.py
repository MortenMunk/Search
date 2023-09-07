from tkinter import filedialog
import customtkinter
import webbrowser

from exceptions import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Globals
save_maze_frame = None
maze_state = {}
is_goal_placed = False
is_start_placed = False
grid_frame = None


# Maze cell states
EMPTY = 0
START = "A"
GOAL = "B"
ROUTE = 1

def occurs_once(list, item):
    return list.count(item) == 1

def open_url(url):
   webbrowser.open_new_tab(url)


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
        navbar.pack(fill=customtkinter.X, side=customtkinter.BOTTOM, pady=10, padx=10)



class ContentFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Entry frame
        self.entry_frame = EntryFrame(self)
        self.entry_frame.pack(side=customtkinter.TOP, pady=10, padx=10)

        # Switch frame
        self.switch_frame = SwitchFrame(self)
        self.switch_frame.pack(side=customtkinter.BOTTOM, pady=10)

        # Load Maze Frame
        self.load_maze_frame = LoadMazeFrame(self)
        self.load_maze_frame.pack(side=customtkinter.BOTTOM, pady=10, padx=10)


class SwitchFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        switch_label_dfs = customtkinter.CTkLabel(self, text="Depth-first", cursor="hand2")
        switch_label_dfs.pack(side=customtkinter.LEFT, padx=(20,5))

        switch_var = customtkinter.StringVar(value="DFS")
        switch = customtkinter.CTkSwitch(self, command=switch_event, text="Breadth-first", variable=switch_var, onvalue="DFS", offvalue="BFS", switch_width=40)
        switch.pack(side=customtkinter.LEFT, pady=10, padx=(5,20))

        def switch_event():
            print("switch toggled, current value:", switch_var.get())


class EntryFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        x_axis_entry = customtkinter.CTkEntry(self, placeholder_text="Columns", width=75)
        x_axis_entry.pack(side=customtkinter.LEFT, padx=(20,5), pady=10)

        times_label = customtkinter.CTkLabel(self, text="X")
        times_label.pack(side=customtkinter.LEFT)

        y_axis_entry = customtkinter.CTkEntry(self, placeholder_text="Rows", width=75)
        y_axis_entry.pack(side=customtkinter.LEFT, padx=(5,20))

        grid_btn = customtkinter.CTkButton(self, text="Generate grid", command=generate_grid)
        grid_btn.pack(side=customtkinter.LEFT, padx=(0,20))


class LoadMazeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        load_maze_btn = customtkinter.CTkButton(self, text="Load maze", cursor="hand2", command=load_maze)
        load_maze_btn.pack(side=customtkinter.LEFT, padx=10, pady=10)


def change_cell_state(event):
    global maze_state, is_start_placed, is_goal_placed
    widget = event.widget
    row = widget.master.grid_info()["row"]
    col = widget.master.grid_info()["column"]
    if event.num == 1:
        if maze_state.get((row, col), EMPTY) == EMPTY:
            maze_state[(row, col)] = ROUTE
            widget.master.configure(fg_color="white")
            print("Route placed")
        elif maze_state.get((row, col), EMPTY) == ROUTE:
            maze_state[(row, col)] = EMPTY
            widget.master.configure(fg_color="black")
            print("Route removed")
        elif maze_state.get((row, col), EMPTY) == START or maze_state.get((row, col), EMPTY) == GOAL:
            print("Cannot place route on goal or start")
        else:
            print("undefined error")
    elif event.num == 3:
        if maze_state.get((row, col), EMPTY) == EMPTY or maze_state.get((row, col), ROUTE) == ROUTE:
            if is_start_placed and not is_goal_placed:
                maze_state[(row, col)] = GOAL
                widget.master.configure(fg_color="green")
                is_goal_placed = True
                print("goal placed")
            elif not is_start_placed and is_goal_placed:
                maze_state[(row, col)] = START
                widget.master.configure(fg_color="yellow")
                is_start_placed = True
                print("start placed")
            elif not is_start_placed and not is_goal_placed:
                maze_state[(row, col)] = START
                is_start_placed = True
                widget.master.configure(fg_color="yellow")
                print("start placed")
            elif is_goal_placed and is_start_placed:
                print("both start and goal placed")
        elif maze_state.get((row, col), START) == START:
            maze_state[(row, col)] = EMPTY
            is_start_placed = False
            widget.master.configure(fg_color="black")
            print("start removed")
        elif maze_state.get((row, col), GOAL) == GOAL:
            maze_state[(row, col)] = EMPTY
            is_goal_placed = False
            widget.master.configure(fg_color="black")
            print("goal removed")
        else: 
            print("undefined error")
            

def handle_grid():
    global maze_state, grid_frame, is_start_placed, is_goal_placed, x_axis, y_axis, save_maze_frame
    if grid_frame is not None:
        if save_maze_frame is not None:
            save_maze_frame.destroy()
        maze_state.clear()
        is_goal_placed = False
        is_start_placed = False
        for widget in grid_frame.winfo_children():
            widget.destroy()
        grid_frame.pack_forget()


    # Creating 2d grid
    if x_axis is not None and y_axis is not None:
        grid_frame = customtkinter.CTkFrame(master=content_frame)
        grid_frame.pack(side=customtkinter.TOP, pady=10)

        for row in range(y_axis):
            for col in range(x_axis):
                maze_state[(row, col)] = EMPTY
                cell = customtkinter.CTkFrame(master=grid_frame, border_width=1, border_color="lightblue", width=30, height=30, corner_radius=0, fg_color="black")
                cell.grid(row=row, column=col, padx=0, pady=0,)
                cell.bind("<Button-1>", change_cell_state)
                cell.bind("<Button-3>", change_cell_state)

        # save maze button
        save_maze_frame = customtkinter.CTkFrame(master=content_frame)
        save_maze_frame.pack(side=customtkinter.TOP)

        save_maze_btn = customtkinter.CTkButton(master=save_maze_frame, text="Save maze", command=save_maze)
        save_maze_btn.pack(side=customtkinter.LEFT, padx=20, pady=10)


    
def generate_grid():
    global maze_state, grid_frame, is_start_placed, is_goal_placed, x_axis, y_axis
    
    try:
        if x_axis_entry.get() is None or y_axis_entry.get() is None:
            raise TypeError
        elif y_axis_entry.get().isnumeric() is False or x_axis_entry.get().isnumeric is False:
            raise InvalidGridValue
        elif int(y_axis_entry.get()) > 10 or int(x_axis_entry.get()) > 10:
            raise InvalidGridDimension
        elif int(y_axis_entry.get()) < 3 or int(x_axis_entry.get()) < 3:
            raise InvalidGridDimension
        else:
            x_axis = int(x_axis_entry.get())
            y_axis = int(y_axis_entry.get())
    except InvalidGridDimension as e:
        print(e.message)
        x_axis = None
        y_axis = None
    except InvalidGridValue as e:
        print(e.message)
        x_axis = None
        y_axis = None
    except TypeError as e:
        print(e)
        x_axis = None
        y_axis = None
    
    handle_grid()


def save_maze():
    global x_axis, y_axis
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    values = list(maze_state.values())
    text = str(values)[1:-1].replace(",", "").replace(" ", "").replace("'", "")

    with open(file_path, 'w') as file:
        file.write(f"{x_axis}x{y_axis}\n")
        file.write(text)
        file.close()


def load_maze():
    global x_axis, y_axis, maze_state, grid_frame, is_start_placed, is_goal_placed
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

    handle_grid()

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
            cell = grid_frame.grid_slaves(row=row, column=col)[0]
            if cell_value == ROUTE:
                cell.configure(fg_color="white")
            elif cell_value == START:
                cell.configure(fg_color="yellow")
            elif cell_value == GOAL:
                cell.configure(fg_color="green")
            elif cell_value == EMPTY:
                cell.configure(fg_color="black")

    is_start_placed = any(val == START for val in maze_state.values())
    is_goal_placed = any(val == GOAL for val in maze_state.values())



# content_frame = customtkinter.CTkFrame(master=app, border_width=1, border_color="grey")











# Bottom bar frame
navbar = customtkinter.CTkFrame(master=app, height=50, border_width=1, border_color="grey")


# navbar buttons
navbar_btns = customtkinter.CTkFrame(master=navbar)
navbar_btns.pack(side=customtkinter.TOP, pady=10)

source_btn = customtkinter.CTkButton(master=navbar_btns, text="Source Code", cursor="hand2")
source_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)
source_btn.bind("<Button-1>", lambda e:open_url("https://github.com/MortenMunk/Search/tree/main"))

help_btn = customtkinter.CTkButton(master=navbar_btns, text="Documentation", cursor="hand2")
help_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)

contact_btn = customtkinter.CTkButton(master=navbar_btns, text="Contact", cursor="hand2")
contact_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)

# bottom link
github_link = customtkinter.CTkLabel(master=navbar, text="Made by Morten Munk", cursor="hand2", text_color="grey")
github_link.pack(side=customtkinter.BOTTOM, pady=10)
github_link.bind("<Button-1>", lambda e:open_url("https://github.com/MortenMunk"))

app = App()
app.mainloop()