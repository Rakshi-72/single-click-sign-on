import pickle
import subprocess
import tkinter as tk


def save_inputs():
    with open('user_inputs.pkl', 'wb') as file:
        pickle.dump({
            'input_1': entry_1.get(),
            'input_2': entry_2.get(),
            'input_3': entry_3.get(),
            'input_4': entry_4.get(),
            'input_5': entry_5.get(),
            'select_1': select_var_1.get(),
            'select_2': select_var_2.get(),
            'select_3': select_var_3.get(),
            'select_4': select_var_4.get(),
            'select_5': select_var_5.get(),
        }, file)


def load_inputs():
    try:
        with open('user_inputs.pkl', 'rb') as file:
            data = pickle.load(file)
            entry_1.insert(0, data['input_1'])
            entry_2.insert(0, data['input_2'])
            entry_3.insert(0, data['input_3'])
            entry_4.insert(0, data['input_4'])
            entry_5.insert(0, data['input_5'])
            select_var_1.set(data['select_1'])
            select_var_2.set(data['select_2'])
            select_var_3.set(data['select_3'])
            select_var_4.set(data['select_4'])
            select_var_5.set(data['select_5'])
    except FileNotFoundError:
        pass


def run_script():
    commands = []
    directories = []
    if select_var_1.get():
        commands.append("npm test")
        directories.append(entry_1.get())
    if select_var_2.get():
        commands.append("npm start")
        directories.append(entry_2.get())
    if select_var_3.get():
        commands.append("npm run start-dev")
        directories.append(entry_3.get())
    if select_var_4.get():
        commands.append("npm run dev")
        directories.append(entry_4.get())
    if select_var_5.get():
        commands.append("npm run dev")
        directories.append(entry_5.get())

    def run_powershell_command(command, directory):
        print(f"running 'cd {directory}; {command}'")
        subprocess.run(["powershell", "-Command",
                        f"Start-Process powershell -Verb RunAs -ArgumentList '-NoExit', '-Command', 'cd {directory}; {command}'"])

    for cmd, directory in zip(commands, directories):
        run_powershell_command(cmd, directory)


root = tk.Tk()
root.title("Run apps")
root.geometry("400x250")  # Width x Height

label_1 = tk.Label(root, text="Enter path for NodeLayer")
label_2 = tk.Label(root, text="Enter path for UI")
label_3 = tk.Label(root, text="Enter path for Mock Server")
label_4 = tk.Label(root, text="Enter path for Server")
label_5 = tk.Label(root, text="Enter path for Client")

entry_1 = tk.Entry(root)
entry_2 = tk.Entry(root)
entry_3 = tk.Entry(root)
entry_4 = tk.Entry(root)
entry_5 = tk.Entry(root)

select_var_1 = tk.BooleanVar()
select_var_2 = tk.BooleanVar()
select_var_3 = tk.BooleanVar()
select_var_4 = tk.BooleanVar()
select_var_5 = tk.BooleanVar()

select_1 = tk.Checkbutton(root, text="Select", variable=select_var_1)
select_2 = tk.Checkbutton(root, text="Select", variable=select_var_2)
select_3 = tk.Checkbutton(root, text="Select", variable=select_var_3)
select_4 = tk.Checkbutton(root, text="Select", variable=select_var_4)
select_5 = tk.Checkbutton(root, text="Select", variable=select_var_5)

label_1.grid(row=0, column=0, padx=5, pady=5)
entry_1.grid(row=0, column=1, padx=5, pady=5)
select_1.grid(row=0, column=2, padx=5, pady=5)

label_2.grid(row=1, column=0, padx=5, pady=5)
entry_2.grid(row=1, column=1, padx=5, pady=5)
select_2.grid(row=1, column=2, padx=5, pady=5)

label_3.grid(row=2, column=0, padx=5, pady=5)
entry_3.grid(row=2, column=1, padx=5, pady=5)
select_3.grid(row=2, column=2, padx=5, pady=5)

label_4.grid(row=3, column=0, padx=5, pady=5)
entry_4.grid(row=3, column=1, padx=5, pady=5)
select_4.grid(row=3, column=2, padx=5, pady=5)

label_5.grid(row=4, column=0, padx=5, pady=5)
entry_5.grid(row=4, column=1, padx=5, pady=5)
select_5.grid(row=4, column=2, padx=5, pady=5)

load_inputs()

run_button = tk.Button(root, text="run", command=run_script)
run_button.grid(row=5, column=1, columnspan=2, padx=5, pady=20)

root.protocol("WM_DELETE_WINDOW", save_inputs)
root.mainloop()
