import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading
import queue
import signal
import os
import sys

# List of packages
packages = [
    'pynput',
    'setuptools',
    'Flask',
    'pefile',
    'lief',
    'capstone',
    'keystone-engine',
    'pygame',
    'scipy',
    'numpy',
    'pydub',
    'pdfplumber',
    'transformers',
    'tqdm',
    'moviepy',
    'imageio'
]

# Initialize the main window
root = tk.Tk()
root.title("Package Installer/Uninstaller")

# Dictionary to store package variables
package_vars = {}

# Variable to store the current running process
current_process = None

# Queue to handle output from subprocess threads
output_queue = queue.Queue()

# Function to get selected packages
def get_selected_packages():
    selected = []
    for pkg, var in package_vars.items():
        if var.get() == 1:
            selected.append(pkg)
    return selected

# Function to toggle select/unselect all packages
def toggle_select_all():
    # Check if all packages are currently selected
    all_selected = all(var.get() == 1 for var in package_vars.values())
    # Toggle the selection state
    new_state = 0 if all_selected else 1
    for var in package_vars.values():
        var.set(new_state)
    # Update the button text
    select_all_btn.config(text="Unselect All" if new_state else "Select All")

# Function to update the select/unselect all button text on any change
def update_select_all_button():
    all_selected = all(var.get() == 1 for var in package_vars.values())
    select_all_btn.config(text="Unselect All" if all_selected else "Select All")

# Function to install packages
def install_packages():
    threading.Thread(target=install_packages_thread, daemon=True).start()
    status_label.config(text="Installing packages...")
    install_btn.config(state='disabled')
    uninstall_btn.config(state='disabled')
    stop_btn.config(state='normal')
    output_text.delete(1.0, tk.END)

def install_packages_thread():
    global current_process
    selected_packages = get_selected_packages()
    if not selected_packages:
        root.after(0, lambda: messagebox.showwarning("No Packages Selected", "Please select at least one package to install."))
        root.after(0, reset_ui)
        return
    pip_command = pip_var.get()
    failed_packages = []
    for pkg in selected_packages:
        cmd = [pip_command, 'install', pkg]
        try:
            # Start the subprocess
            current_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            # Read the output line by line
            for line in current_process.stdout:
                output_queue.put(line)
            current_process.wait()
            if current_process.returncode != 0:
                failed_packages.append(pkg)
        except Exception as e:
            failed_packages.append(pkg)
            output_queue.put(f"Error installing {pkg}: {e}\n")
        finally:
            current_process = None
    root.after(0, reset_ui)
    if failed_packages:
        root.after(0, lambda: messagebox.showerror("Error", f"Failed to install: {', '.join(failed_packages)}"))
    else:
        root.after(0, lambda: messagebox.showinfo("Success", "All selected packages installed successfully."))

# Function to uninstall packages
def uninstall_packages():
    threading.Thread(target=uninstall_packages_thread, daemon=True).start()
    status_label.config(text="Uninstalling packages...")
    install_btn.config(state='disabled')
    uninstall_btn.config(state='disabled')
    stop_btn.config(state='normal')
    output_text.delete(1.0, tk.END)

def uninstall_packages_thread():
    global current_process
    selected_packages = get_selected_packages()
    if not selected_packages:
        root.after(0, lambda: messagebox.showwarning("No Packages Selected", "Please select at least one package to uninstall."))
        root.after(0, reset_ui)
        return
    pip_command = pip_var.get()
    failed_packages = []
    for pkg in selected_packages:
        cmd = [pip_command, 'uninstall', '-y', pkg]
        try:
            # Start the subprocess
            current_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            # Read the output line by line
            for line in current_process.stdout:
                output_queue.put(line)
            current_process.wait()
            if current_process.returncode != 0:
                failed_packages.append(pkg)
        except Exception as e:
            failed_packages.append(pkg)
            output_queue.put(f"Error uninstalling {pkg}: {e}\n")
        finally:
            current_process = None
    root.after(0, reset_ui)
    if failed_packages:
        root.after(0, lambda: messagebox.showerror("Error", f"Failed to uninstall: {', '.join(failed_packages)}"))
    else:
        root.after(0, lambda: messagebox.showinfo("Success", "All selected packages uninstalled successfully."))

# Function to reset UI elements after operation
def reset_ui():
    status_label.config(text="")
    install_btn.config(state='normal')
    uninstall_btn.config(state='normal')
    stop_btn.config(state='disabled')

# Function to periodically check the output queue and update the Text widget
def update_output():
    try:
        while True:
            line = output_queue.get_nowait()
            output_text.insert(tk.END, line)
            output_text.see(tk.END)
    except queue.Empty:
        pass
    root.after(100, update_output)

# Function to stop the current process
def stop_process():
    global current_process
    if current_process:
        try:
            if os.name == 'nt':
                # For Windows
                current_process.terminate()
            else:
                # For Unix/Linux/Mac
                current_process.send_signal(signal.SIGINT)
            output_queue.put("Process terminated by user.\n")
        except Exception as e:
            output_queue.put(f"Error stopping process: {e}\n")
    stop_btn.config(state='disabled')

# Create frame for checkboxes and (Un)Select All button
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(anchor='w')

# Create (Un)Select All button
select_all_btn = tk.Button(checkbox_frame, text="Unselect All", command=toggle_select_all)
select_all_btn.pack(anchor='w', pady=5)

# Create checkboxes for each package
for pkg in packages:
    var = tk.IntVar(value=1)  # Selected by default
    cb = tk.Checkbutton(checkbox_frame, text=pkg, variable=var, command=update_select_all_button)
    cb.pack(anchor='w')
    package_vars[pkg] = var

# Create radio buttons for pip version selection
pip_var = tk.StringVar(value='pip')
pip_frame = tk.Frame(root)
pip_frame.pack(anchor='w', pady=10)

tk.Label(pip_frame, text="Choose pip version:").pack(anchor='w')

pip_rb1 = tk.Radiobutton(pip_frame, text='pip', variable=pip_var, value='pip')
pip_rb1.pack(anchor='w')

pip_rb2 = tk.Radiobutton(pip_frame, text='pip3', variable=pip_var, value='pip3')
pip_rb2.pack(anchor='w')

# Create buttons for install, uninstall, and stop actions
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

install_btn = tk.Button(btn_frame, text='Install', command=install_packages)
install_btn.pack(side='left', padx=5)

uninstall_btn = tk.Button(btn_frame, text='Uninstall', command=uninstall_packages)
uninstall_btn.pack(side='left', padx=5)

stop_btn = tk.Button(btn_frame, text='Stop', command=stop_process, state='disabled')
stop_btn.pack(side='left', padx=5)

# Status label to display ongoing actions
status_label = tk.Label(root, text="")
status_label.pack()

# Text widget to display output
output_frame = tk.Frame(root)
output_frame.pack(fill='both', expand=True)

output_text = scrolledtext.ScrolledText(output_frame, wrap='word', height=15)
output_text.pack(fill='both', expand=True)

# Start updating the output_text widget
update_output()

# Start the Tkinter event loop
root.mainloop()
