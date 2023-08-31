import customtkinter
import webbrowser

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()

maze_state = {}
is_goal_placed = False
is_start_placed = False
EMPTY = 1
START = "A"
GOAL = "B"
ROUTE = 0

# reduce the minimum size of the application window, because I am too lazy for responsiveness
app.minsize(600,600)
app.geometry("800x800")
app.title("DFS and BFS")

def open_url(url):
   webbrowser.open_new_tab(url)


def switch_event():
    print("switch toggled, current value:", switch_var.get())


def change_cell_state(event):
    global is_start_placed
    global is_goal_placed
    widget = event.widget
    row = widget.master.grid_info()["row"]
    col = widget.master.grid_info()["column"]
    if event.num == 1:
        if maze_state.get((row, col), EMPTY) == EMPTY:
            maze_state[(row, col)] = ROUTE
            print("Route placed")
        elif maze_state.get((row, col), EMPTY) == ROUTE:
            maze_state[(row, col)] = EMPTY
            print("Route removed")
        elif maze_state.get((row, col), EMPTY) == START or maze_state.get((row, col), EMPTY) == GOAL:
            print("Cannot place route on goal or start")
        else:
            print("undefined error")
    elif event.num == 3:
        if maze_state.get((row, col), EMPTY) == EMPTY or maze_state.get((row, col), ROUTE) == ROUTE:
            if is_start_placed and not is_goal_placed:
                maze_state[(row, col)] = GOAL
                is_goal_placed = True
                print("goal placed")
            elif not is_start_placed and is_goal_placed:
                maze_state[(row, col)] = START
                is_start_placed = True
                print("start placed")
            elif not is_start_placed and not is_goal_placed:
                maze_state[(row, col)] = START
                is_start_placed = True
                print("start placed")
            elif is_goal_placed and is_start_placed:
                print("both start and goal placed")
        elif maze_state.get((row, col), START) == START:
            maze_state[(row, col)] = EMPTY
            is_start_placed = False
            print("start removed")
        elif maze_state.get((row, col), GOAL) == GOAL:
            maze_state[(row, col)] = EMPTY
            print("goal removed")
        else: 
            print("undefined error")
            

    

def generate_grid():
    x_axis = int(x_axis_entry.get())
    y_axis = int(y_axis_entry.get())
    
    # clear existing grid, if any
    if "grid-frame" in globals():
        grid_frame.destroy()

    grid_frame= customtkinter.CTkFrame(master=content_frame)
    grid_frame.pack(side=customtkinter.TOP, pady=10)

    # Creating 2d grid
    for row in range(y_axis):
        for col in range(x_axis):
            cell = customtkinter.CTkFrame(master=grid_frame, border_width=1, border_color="lightblue", width=30, height=30, corner_radius=0, fg_color="black")
            cell.grid(row=row, column=col, padx=0, pady=0,)
            cell.bind("<Button-1>", change_cell_state)
            cell.bind("<Button-3>", change_cell_state)


content_frame = customtkinter.CTkFrame(master=app, border_width=1, border_color="grey")
content_frame.pack(fill=customtkinter.BOTH, expand=True, padx=10, pady=10)

# x and y axis entries
entry_frame = customtkinter.CTkFrame(master=content_frame)
entry_frame.pack(side=customtkinter.TOP, pady=10, padx=10)

x_axis_entry = customtkinter.CTkEntry(master=entry_frame, placeholder_text="x axis cells", width=75)
x_axis_entry.pack(side=customtkinter.LEFT, padx=(20,5), pady=10)

times_label = customtkinter.CTkLabel(master=entry_frame, text="X")
times_label.pack(side=customtkinter.LEFT)

y_axis_entry = customtkinter.CTkEntry(master=entry_frame, placeholder_text="y axis cells", width=75)
y_axis_entry.pack(side=customtkinter.LEFT, padx=(5,20))

grid_btn = customtkinter.CTkButton(master=entry_frame, text="Generate grid", command=generate_grid)
grid_btn.pack(side=customtkinter.LEFT, padx=(0,20))


# switch frame

switch_frame = customtkinter.CTkFrame(master=content_frame)
switch_frame.pack(side=customtkinter.BOTTOM, pady=10)

switch_label_dfs = customtkinter.CTkLabel(master=switch_frame, text="Depth-first")
switch_label_dfs.pack(side=customtkinter.LEFT, padx=(20,5))

switch_var = customtkinter.StringVar(value="DFS")
switch = customtkinter.CTkSwitch(master=switch_frame, command=switch_event, text="Breadth-first", variable=switch_var, onvalue="DFS", offvalue="BFS", switch_width=40)
switch.pack(side=customtkinter.LEFT, pady=10, padx=(5,20))




# Bottom bar frame
navbar = customtkinter.CTkFrame(master=app, height=50, border_width=1, border_color="grey")
navbar.pack(fill=customtkinter.X, side=customtkinter.BOTTOM, pady=10, padx=10)

# navbar buttons
navbar_btns = customtkinter.CTkFrame(master=navbar)
navbar_btns.pack(side=customtkinter.TOP, pady=10)

source_btn = customtkinter.CTkButton(master=navbar_btns, text="Source Code")
source_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)
source_btn.bind("<Button-1>", lambda e:open_url("https://github.com/MortenMunk/Search/tree/main"))

help_btn = customtkinter.CTkButton(master=navbar_btns, text="Documentation")
help_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)

contact_btn = customtkinter.CTkButton(master=navbar_btns, text="Contact")
contact_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)

# bottom link
github_link = customtkinter.CTkLabel(master=navbar, text="Made by Morten Munk", cursor="hand2", text_color="grey")
github_link.pack(side=customtkinter.BOTTOM, pady=10)
github_link.bind("<Button-1>", lambda e:open_url("https://github.com/MortenMunk"))

app.mainloop()