import os
import pickle
import subprocess
import tkinter as tk
from datetime import datetime


def save_inputs():
    """
    The function `save_inputs` saves user inputs to a file named 'user_inputs.pkl' using the pickle
    module in Python.
    """
    try:
        with open('user_inputs.pkl', 'wb') as file:
            data = {
                f'input_{i}': entry_list[i].get() for i in range(1, 6)
            }
            data.update(
                {f'select_{i}': select_vars[i].get() for i in range(1, 6)}
            )
            data.update(
                {f'select_command_{i}': select_command[f"select_{i}"].get(
                )for i in range(1, 6)}
            )
            pickle.dump(data, file)
    except IOError as e:
        print(f"Error saving data: {e}")
    root.destroy()


def validate_paths():
    """
    The function `validate_paths` checks if the paths entered in `entry_list` exist and updates the text
    color of the corresponding entry widget accordingly.
    """
    for i in range(1, 6):
        path = entry_list[i].get()
        if path:
            if not os.path.exists(path):
                entry_list[i].config(fg='red')
            else:
                entry_list[i].config(fg='black')


def load_inputs():
    """
    The function `load_inputs` loads user inputs from a file and populates the corresponding entry
    fields and select variables.
    """
    try:
        with open('user_inputs.pkl', 'rb') as file:
            data = pickle.load(file)
            for i in range(1, 6):
                entry_list[i].insert(0, data[f'input_{i}'])
                select_vars[i].set(data[f'select_{i}'])
                select_command[f'select_{i}'].set(data[f'select_command_{i}'])
    except (FileNotFoundError, IOError):
        pass


def run_powershell_command(command, directory):
    """
    The function `run_powershell_command` runs a PowerShell command in a specified directory.

    :param command: The `command` parameter is a string that represents the PowerShell command you want
    to run. It can be any valid PowerShell command or script
    :param directory: The directory parameter is the path to the directory where you want to run the
    PowerShell command
    """
    try:
        print(f"running 'cd {directory}; {command}'")
        subprocess.run(["powershell", "-Command",
                       f"Start-Process powershell -Verb RunAs -ArgumentList '-NoExit', '-Command', 'cd {directory}; {command}'"])
    except subprocess.SubprocessError as e:
        print(f"Error running subprocess: {e}")


def run_script():
    """
    The `run_script` function creates a dictionary of selected directories and their corresponding
    commands, executes the commands using PowerShell, and logs the execution status in a file.
    """
    directories = {
        i: entry_list[i].get() for i in range(1, 6) if select_vars[i].get()
    }
    for option in directories:
        log_file = 'command_log.txt'
        run_cmd = False
        directory = directories[option]
        if len(directory) > 0 and os.path.exists(directory):
            run_powershell_command(
                select_command[f"select_{option}"].get(), directory)
            run_cmd = True
        with open(log_file, "a") as file:
            file.write(
                f'[{datetime.now()}] - {directory +" ; "+ select_command[f"select_{option}"].get() } - executed command ? {run_cmd}\n')


def create_entry_label(parent, text, row, options):
    """
    The function creates a label, entry field, checkbox, and dropdown menu in a tkinter parent widget
    and returns the entry field, checkbox variable, and selected option.

    :param parent: The parent parameter refers to the parent widget or container where the entry label
    will be placed. It could be a frame, a window, or any other widget that can contain other widgets
    :param text: The text parameter is the label text that will be displayed next to the entry field
    :param row: The `row` parameter specifies the row number in which the entry label should be placed
    in the parent widget
    :param options: The "options" parameter is a list of options that can be selected from the dropdown
    menu
    :return: The function `create_entry_label` returns three values: `entry`, `select_var`, and
    `selected_option`.
    """
    label = tk.Label(parent, text=text)
    entry = tk.Entry(parent)
    select_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(parent, text="Select", variable=select_var)

    selected_option = tk.StringVar(parent)
    selected_option.set(options[0])  # Set default option

    dropdown = tk.OptionMenu(parent, selected_option, *options)
    label.grid(row=row, column=0, padx=5, pady=5)
    entry.grid(row=row, column=1, padx=5, pady=5)
    checkbox.grid(row=row, column=3, padx=5, pady=5)
    dropdown.grid(row=row, column=2, padx=5, pady=5)
    dropdown.config(width=20)
    return entry, select_var, selected_option


root = tk.Tk()
root.title("Run apps")
root.geometry("575x280")  # Width x Height

entry_list = {}
select_vars = {}
select_command = {}

label_names = ["Enter path for NodeLayer", "Enter path for UI",
               "Enter path for Mock Server", "Enter path for Server", "Enter path for Client"]

drop_down_options = [
    ["npm run dev", "npm run test", "npm run coverage"],
    ["npm start", "npm run test", "npm run coverage"],
    ["npm run start-dev"],
    ["npm run dev"],
    ["npm run dev"],
]


# This code block is creating a set of entry labels, checkboxes, and dropdown menus in a tkinter
# window.
for i, label_text in enumerate(label_names, start=1):
    entry, select_var, selected_option = create_entry_label(
        parent=root,
        text=label_text,
        row=i - 1,
        options=drop_down_options[i - 1])
    entry_list[i] = entry
    select_vars[i] = select_var
    select_command[f"select_{i}"] = selected_option

load_inputs()


validate_button = tk.Button(
    root, text="Validate Paths", command=validate_paths, bg='red')
validate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

run_button = tk.Button(root, text="run", command=run_script, bg='green')
run_button.grid(row=5, column=1, columnspan=2, padx=5, pady=20)

root.protocol("WM_DELETE_WINDOW", save_inputs)
root.mainloop()
