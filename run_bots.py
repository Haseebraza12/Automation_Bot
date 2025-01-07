import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import threading
import time
from tqdm import tqdm

class TkinterTqdm(tqdm):
    def __init__(self, *args, **kwargs):
        self.progress_var = kwargs.pop('progress_var', None)
        self.root = kwargs.pop('root', None)
        super().__init__(*args, **kwargs)

    def update(self, n=1):
        super().update(n)
        if self.progress_var:
            self.progress_var.set(self.n)
            if self.root:
                self.root.update_idletasks()

def run_script(script_name):
    try:
        # Run the selected script with a progress bar
        for _ in TkinterTqdm(range(100), desc=f"Running {script_name}", progress_var=progress_var, root=root):
            subprocess.run(['python', script_name], check=True)
            time.sleep(0.1)  # Simulate progress
        messagebox.showinfo("Success", f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error executing {script_name}: {e}")
    finally:
        progress_var.set(0)
        root.update_idletasks()  # Reset the progress bar

def on_run_button_click():
    selected_script = script_var.get()
    if selected_script:
        threading.Thread(target=run_script, args=(selected_script,)).start()
    else:
        messagebox.showwarning("Warning", "Please select a script to run.")

def create_gradient(canvas, width, height):
    # Clear the canvas
    canvas.delete("all")
    # Create a gradient background
    for i in range(height):
        color = f'#{int(255 - (i * 255 / height)):02x}99ff'  # Light purple to white
        canvas.create_line(0, i, width, i, fill=color)

def resize_canvas(event):
    # Redraw the gradient when the window is resized
    create_gradient(canvas, event.width, event.height)

# Create the main window
root = tk.Tk()
root.title("Bot Runner")
root.geometry("400x300")

# Create a canvas for the gradient background
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack(fill="both", expand=True)

# Create the gradient background
create_gradient(canvas, 400, 300)

# Bind the resize event to the resize_canvas function
canvas.bind("<Configure>", resize_canvas)

# Create a frame for the UI elements
frame = tk.Frame(root, bg='white', bd=2, relief='groove')
frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=200)

# Create a variable to hold the selected script
script_var = tk.StringVar()

# Create a label
label = tk.Label(frame, text="Select a Bot Script to Run:", bg='white', font=("Arial", 12))
label.pack(pady=10)

# Create a dropdown menu
script_options = ["bot1.py", "bot2.py", "bot3.py"]
script_menu = tk.OptionMenu(frame, script_var, *script_options)
script_menu.config(bg='lightgray', font=("Arial", 10))
script_menu.pack(pady=10)

# Create a button to run the selected script
run_button = tk.Button(frame, text="Run Selected Script", command=on_run_button_click, bg='purple', fg='white', font=("Arial", 10))
run_button.pack(pady=10)

# Create a progress bar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame, orient="horizontal", length=100, mode="determinate", maximum=1, variable=progress_var)
progress_bar.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()