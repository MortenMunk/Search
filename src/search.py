import customtkinter
import webbrowser

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()

# reduce the minimum size of the application window, because I am too lazy for responsiveness
app.minsize(600,600)
app.geometry("800x800")
app.title("DFS and BFS")

def open_url(url):
   webbrowser.open_new_tab(url)

def switch_event():
    print("switch toggled, current value:", switch_var.get())

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

help_btn = customtkinter.CTkButton(master=navbar_btns, text="Documentation")
help_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)

contact_btn = customtkinter.CTkButton(master=navbar_btns, text="Contact")
contact_btn.pack(side=customtkinter.LEFT, pady=15, padx=20)

# navbar link
github_link = customtkinter.CTkLabel(master=navbar, text="Made by Morten Munk", cursor="hand2", text_color="grey")
github_link.pack(side=customtkinter.BOTTOM, pady=10)
github_link.bind("<Button-1>", lambda e:open_url("https://github.com/MortenMunk"))

app.mainloop()