from tkinter import filedialog
import customtkinter
import webbrowser

from exceptions import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


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

        self.switch_label_dfs = customtkinter.CTkLabel(self, text="Depth-first", cursor="hand2")
        self.switch_label_dfs.pack(side=customtkinter.LEFT, padx=(20,5))

        self.switch_var = customtkinter.StringVar(value="DFS")
        self.switch = customtkinter.CTkSwitch(self, command=self.switch_event, text="Breadth-first", variable=self.switch_var, onvalue="DFS", offvalue="BFS", switch_width=40)
        self.switch.pack(side=customtkinter.LEFT, pady=10, padx=(5,20))

    def switch_event(self):
        print("switch toggled, current value:", self.switch_var.get())


class EntryFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.x_axis_entry = customtkinter.CTkEntry(self, placeholder_text="Columns", width=75)
        self.x_axis_entry.pack(side=customtkinter.LEFT, padx=(20,5), pady=10)

        self.times_label = customtkinter.CTkLabel(self, text="X")
        self.times_label.pack(side=customtkinter.LEFT)

        self.y_axis_entry = customtkinter.CTkEntry(self, placeholder_text="Rows", width=75)
        self.y_axis_entry.pack(side=customtkinter.LEFT, padx=(5,20))

        self.grid_btn = customtkinter.CTkButton(self, text="Generate grid", command=self.generate_grid)
        self.grid_btn.pack(side=customtkinter.LEFT, padx=(0,20))

    def generate_grid(self):
        column = self.x_axis_entry.get()
        rows = self.y_axis_entry.get()

        try:
            if not column and not rows:
                raise TypeError
            
            if not column.isdigit() and not rows.isdigit():
                raise InvalidGridValue
            
            column = int(column)
            rows = int(rows)

            if column < 3 or rows < 3:
                raise InvalidGridDimension
            elif column > 10 or rows > 10:
                raise InvalidGridDimension
            
            if hasattr(self.master, 'maze_frame'):
                self.master.maze_frame.destroy()

        except TypeError as e:
            print(e)
            return
        except InvalidGridValue as e:
            print(e.message)
            return
        except InvalidGridDimension as e:
            print(e.message)
            return
        


class LoadMazeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.load_maze_btn = customtkinter.CTkButton(self, text="Load maze", cursor="hand2", command=self.load_maze)
        self.load_maze_btn.pack(side=customtkinter.LEFT, padx=10, pady=10)

    def load_maze():
        return


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

# content_frame = customtkinter.CTkFrame(master=app, border_width=1, border_color="grey")


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