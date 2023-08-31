import customtkinter
import webbrowser

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("800x800")
app.title("DFS and BFS")

def open_url(url):
   webbrowser.open_new_tab(url)

def switch_event():
    print("switch toggled, current value:", switch_var.get())

content_frame = customtkinter.CTkFrame(master=app)
content_frame.pack(fill=customtkinter.BOTH, expand=True, padx=10, pady=10)

switch_frame = customtkinter.CTkFrame(master=content_frame)
switch_frame.pack(side=customtkinter.TOP, pady=10)

switch_label_dfs = customtkinter.CTkLabel(master=switch_frame, text="Depth-first")
switch_label_dfs.pack(side=customtkinter.LEFT, padx=(20,5))

switch_var = customtkinter.StringVar(value="DFS")
switch = customtkinter.CTkSwitch(master=switch_frame, command=switch_event, text="Breadth-first", variable=switch_var, onvalue="DFS", offvalue="BFS", switch_width=40)
switch.pack(side=customtkinter.LEFT, pady=10, padx=(5,20))







# Bottom bar frame
navbar = customtkinter.CTkFrame(master=app, height=50)
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