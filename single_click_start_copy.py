import pickle
import subprocess
import tkinter as tk


def save_inputs():
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


def load_inputs():
    try:
        with open('user_inputs.pkl', 'rb') as file:
            data = pickle.load(file)
            for i in range(1, 6):
                entry_list[i].insert(0, data[f'input_{i}'])
                select_vars[i].set(data[f'select_{i}'])
    except (FileNotFoundError, IOError):
        pass


def run_powershell_command(command, directory):
    try:
        print(f"running 'cd {directory}; {command}'")
        subprocess.run(["powershell", "-Command",
                       f"Start-Process powershell -Verb RunAs -ArgumentList '-NoExit', '-Command', 'cd {directory}; {command}'"])
    except subprocess.SubprocessError as e:
        print(f"Error running subprocess: {e}")


def run_script():
    commands = ["npm test", "npm start",
                "npm run start-dev", "npm run dev", "npm run dev"]
    directories = [entry_list[i].get()
                   for i in range(1, 6) if select_vars[i].get()]
    for cmd, directory in zip(commands, directories):
        run_powershell_command(cmd, directory)


def create_entry_label(parent, text, row):
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

# Create labels, entries, and checkboxes
for i, label_text in enumerate(["Enter path for NodeLayer", "Enter path for UI", "Enter path for Mock Server", "Enter path for Server", "Enter path for Client"], start=1):
    entry, select_var = create_entry_label(root, label_text, i - 1)
    entry_list[i] = entry
    select_vars[i] = select_var

load_inputs()

run_button = tk.Button(root, text="run", command=run_script)
run_button.grid(row=5, column=1, columnspan=2, padx=5, pady=20)

root.protocol("WM_DELETE_WINDOW", save_inputs)
root.mainloop()
