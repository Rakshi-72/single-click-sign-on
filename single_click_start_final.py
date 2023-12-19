import os
import pickle
import subprocess
import tkinter as tk
from datetime import datetime


def save_inputs():
    """
    The function `save_inputs` saves user inputs and selections to a file named 'user_inputs.pkl' using
    pickle, and then closes the window.
    """
    try:
        with open('user_inputs.pkl', 'wb') as file:
            data = {
                f'input_{i}': entry_list[i].get() for i in range(1, 6)
            }
            data.update(
                {f'select_{i}': select_vars[i].get() for i in range(1, 6)})
            pickle.dump(data, file)
    except IOError as e:
        print(f"Error saving data: {e}")
    root.destroy()


def validate_paths():
    """
    The function `validate_paths` checks if the paths entered in `entry_list` exist, and if not, it
    marks them as invalid.
    """
    for i in range(1, 6):
        path = entry_list[i].get()
        if path and not os.path.exists(path):
            entry_list[i].config(fg='red')
            entry_list[i].delete(0, tk.END)


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
    The `run_script` function runs a series of npm commands in specified directories using PowerShell.
    """
    commands = {"select_1": "npm test", "select_2": "npm start",
                "select_3": "npm run start-dev", "select_4": "npm run dev", "select_5": "npm run dev"}
    # directories = [entry_list[i].get()
    #                for i in range(1, 6) if select_vars[i].get()]

    directories = {
        f'select_{i}': entry_list[i].get() for i in range(1, 6) if select_vars[i].get()
    }
    for key in directories.keys():
        log_file = 'command_log.txt'
        run_cmd = False
        directory = directories[key]
        if len(directory) > 0 and os.path.exists(directory):
            run_powershell_command(commands[key], directory)
            run_cmd = True
        with open(log_file, "a") as file:
            file.write(
                f'[{datetime.now()}] - {directory +" ; "+ commands[key] } - executed command ? {run_cmd}\n')


def create_entry_label(parent, text, row):
    """
    The function `create_entry_label` creates a label, an entry field, and a checkbox in a given parent
    widget, and returns the entry field and the checkbox variable.

    :param parent: The parent parameter refers to the parent widget or container where the label, entry,
    and checkbox will be placed. It could be a frame, a window, or any other widget that can contain
    other widgets
    :param text: The "text" parameter is the text that will be displayed on the label. It is a string
    value
    :param row: The `row` parameter is used to specify the row number in which the label, entry, and
    checkbox will be placed in the parent widget
    :return: The function `create_entry_label` returns two values: `entry` and `select_var`.
    """
    label = tk.Label(parent, text=text)
    entry = tk.Entry(parent)
    select_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(parent, text="Select", variable=select_var)

    label.grid(row=row, column=0, padx=5, pady=5)
    entry.grid(row=row, column=1, padx=5, pady=5)
    checkbox.grid(row=row, column=2, padx=5, pady=5)

    return entry, select_var


root = tk.Tk()
root.title("Run apps")
root.geometry("400x250")  # Width x Height

entry_list = {}
select_vars = {}

for i, label_text in enumerate(["Enter path for NodeLayer", "Enter path for UI", "Enter path for Mock Server", "Enter path for Server", "Enter path for Client"], start=1):
    entry, select_var = create_entry_label(root, label_text, i - 1)
    entry_list[i] = entry
    select_vars[i] = select_var

load_inputs()

validate_button = tk.Button(
    root, text="Validate Paths", command=validate_paths, bg='red')
validate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

run_button = tk.Button(root, text="run", command=run_script, bg='green')
run_button.grid(row=5, column=1, columnspan=2, padx=5, pady=20)

root.protocol("WM_DELETE_WINDOW", save_inputs)
root.mainloop()
