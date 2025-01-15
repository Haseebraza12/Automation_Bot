import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading

class PasswordDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Password Required")
        self.geometry("300x150")

        self.label = ttk.Label(self, text="Enter Password:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.password_entry = ttk.Entry(self, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        self.submit_button = ttk.Button(self, text="Submit", command=self.check_password)
        self.submit_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def check_password(self):
        if self.password_entry.get() == "josh":
            self.destroy()  # Close the dialog if the password is correct
            self.master.run_script()
        else:
            messagebox.showerror("Error", "Incorrect password. Please try again.")

    def on_closing(self):
        self.master.destroy()  # Close the main application if the dialog is closed

class BotRunnerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bot Runner")
        self.geometry("400x300")

        # Create a canvas for the gradient background
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.pack(fill="both", expand=True)

        # Create the gradient background
        self.create_gradient(400, 300)

        # Bind the resize event to the resize_canvas function
        self.canvas.bind("<Configure>", self.resize_canvas)

        # Create a frame for the UI elements
        self.frame = tk.Frame(self, bg='white', bd=2, relief='groove')
        self.frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=200)

        # Add the welcome text above the dropdown
        self.welcome_label = tk.Label(self.frame, text="Welcome to Bot Runner", bg='white', font=("Arial", 16, "bold"))
        self.welcome_label.pack(pady=(10, 0))

        # Create a variable to hold the selected script
        self.script_var = tk.StringVar()

        # Create a label
        self.label = tk.Label(self.frame, text="Select a Bot Script to Run:", bg='white', font=("Arial", 12))
        self.label.pack(pady=10)

        # Create a dropdown menu
        self.script_options = ["code violations.py", "fire.py", "water.py"]
        self.script_menu = tk.OptionMenu(self.frame, self.script_var, *self.script_options)
        self.script_menu.config(bg='lightgray', font=("Arial", 10))
        self.script_menu.pack(pady=10)

        # Create a button to run the selected script
        self.run_button = tk.Button(self.frame, text="Run Selected Script", command=self.on_run_button_click, bg='lightgray', fg='black', font=("Arial", 10))
        self.run_button.pack(pady=10)

    def create_gradient(self, width, height):
        # Clear the canvas
        self.canvas.delete("all")
        # Create a gradient background
        for i in range(height):
            grey_value = int(200 - (i * 100 / height))  # Adjust the range for grey
            # Fill the canvas with light grey color
            self.canvas.create_rectangle(0, 0, width, height, fill='grey', outline='grey')
            color = f'#{grey_value:02x}{grey_value:02x}{grey_value:02x}'  # Define the color as a shade of grey
            self.canvas.create_line(0, i, width, i, fill=color)

    def resize_canvas(self, event):
        # Redraw the gradient when the window is resized
        self.create_gradient(event.width, event.height)

    def run_script(self):
        selected_script = self.script_var.get()
        if selected_script:
            # Run the script in a separate thread
            threading.Thread(target=self._run_script_thread, args=(selected_script,)).start()
        else:
            messagebox.showwarning("Warning", "Please select a script to run.")

    def _run_script_thread(self, script_name):
        try:
            # Run the selected script
            subprocess.run(['python', script_name], check=True)
            messagebox.showinfo("Success", f"{script_name} executed successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error executing {script_name}: {e}")

    def on_run_button_click(self):
        PasswordDialog(self)

if __name__ == "__main__":
    app = BotRunnerApp()
    app.mainloop()