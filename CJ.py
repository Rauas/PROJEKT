import os
import pathlib
import tkinter as tk

def get_folder_names():
    desktop_path = pathlib.Path.home() / "Desktop"
    folder_names = [name for name in os.listdir(desktop_path) if os.path.isdir(desktop_path / name)]
    return folder_names

def display_folder_names():
    folder_names = get_folder_names()
    output_text = "\n".join(folder_names)
    output_label.configure(text=output_text)

# create the GUI window
root = tk.Tk()
root.title("Folder Names on Desktop")

# create the output label
output_label = tk.Label(root, text="", justify="left")
output_label.pack()

# create the refresh button
refresh_button = tk.Button(root, text="Refresh", command=display_folder_names)
refresh_button.pack()

# display the initial folder names
display_folder_names()

# start the main loop
root.mainloop()
