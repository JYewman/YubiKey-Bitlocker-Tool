import os
import sys
import ctypes
import subprocess
import logging
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

# Set up logging to output to a file
log_file_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "elevation_log.txt")
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to check if the script is running with admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to elevate privileges using ShellExecuteW without a new terminal
def elevate_privileges():
    """ Relaunch the script with elevated privileges using pythonw.exe and log output to a file. """
    logging.info("Attempting to elevate privileges.")
    if not is_admin():
        try:
            # Use pythonw.exe for GUI applications to avoid opening a terminal window
            executable = sys.executable.replace("python.exe", "pythonw.exe")
            script_path = os.path.abspath(sys.argv[0])
            params = f'"{script_path}"'
            
            logging.info(f"Relaunching with elevated privileges: {executable} {params}")
            with open(log_file_path, 'a') as log:
                log.write("Elevating process...\n")
                log.write(f"Executable: {executable}\n")
                log.write(f"Script Path: {script_path}\n")
            
            ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
            sys.exit()  # Exit the original process after launching elevated instance
        except Exception as e:
            logging.error(f"Failed to elevate privileges: {e}")
            with open(log_file_path, 'a') as log:
                log.write(f"Failed to elevate privileges: {e}\n")
            messagebox.showerror("Error", f"Failed to elevate privileges: {e}")
            sys.exit()

# Custom Tooltip Class for Tkinter
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

    def show(self):
        "Display the tooltip"
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="lightyellow", relief="solid", borderwidth=1, padx=5, pady=2)
        label.pack()

    def hide(self):
        "Hide the tooltip"
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

# Tooltip function to provide contextual help
def set_tooltip(widget, text):
    """Sets a tooltip for a widget."""
    tooltip = ToolTip(widget, text)
    widget.bind("<Enter>", lambda e: tooltip.show())
    widget.bind("<Leave>", lambda e: tooltip.hide())

# Help dialog to explain how the tool works
def show_help():
    """Displays a help dialog with information on how to use the tool."""
    help_text = (
        "This tool allows you to manage TPM & BitLocker PINs using a YubiKey.\n\n"
        "Steps:\n"
        "1. Enter a valid 8-character alphanumeric PIN (at least 1 uppercase letter and 1 number).\n"
        "2. Press your YubiKey to generate a unique string.\n"
        "3. The PIN will be combined with the YubiKey string and set as the new BitLocker PIN."
    )
    messagebox.showinfo("Help", help_text)

# Function to confirm the user-entered PIN and ensure it meets the security requirements
def confirm_pin():
    """Confirms the pin, validates it, and enables the YubiKey input."""
    pin = pin_entry.get()
    confirm_pin = confirm_pin_entry.get()

    if len(pin) == 8 and pin == confirm_pin:
        logging.info("Pin confirmed successfully.")
        messagebox.showinfo("Success", "PIN confirmed successfully.")
        yubikey_entry.config(state=tk.NORMAL)  # Enable YubiKey input
        yubikey_entry.focus_set()  # Automatically focus on the YubiKey input field
    else:
        logging.error("Pins do not match or are not 8 characters.")
        messagebox.showerror("Error", "Pins don't match or are not 8 characters long.")

# Function to set TPM and PIN by combining user PIN and YubiKey-generated code
def set_tpm_pin():
    """Sets the TPM & PIN by concatenating the user PIN and YubiKey-generated string."""
    pin = pin_entry.get()
    yubikey_string = yubikey_entry.get()

    if len(pin) == 8 and yubikey_string:
        combined_pin = pin + yubikey_string
        logging.info(f"Combined pin: {combined_pin}")
        set_bitlocker_tpm(combined_pin)
    else:
        logging.error("PIN or YubiKey string is missing.")
        messagebox.showerror("Error", "Both PIN and YubiKey string are required.")

# Function to set or change the TPM & Pin using PowerShell
def set_bitlocker_tpm(pin):
    """Runs PowerShell to set the TPM & Pin."""
    logging.info("Setting BitLocker TPM & Pin.")
    try:
        set_command = f"powershell.exe manage-bde -protectors -add C: -TPMandPIN -pin {pin}"
        set_process = subprocess.run(set_command, shell=True, capture_output=True, text=True)

        if set_process.returncode == 0:
            logging.info("TPM & Pin set successfully.")
            messagebox.showinfo("Success", "TPM & Pin set successfully.")
            update_bitlocker_status()
        else:
            logging.error(f"Failed to set TPM & Pin: {set_process.stderr}")
            messagebox.showerror("Error", f"Failed to set TPM & Pin: {set_process.stderr}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Fluent UI-inspired GUI initialization with ttkbootstrap
def setup_gui():
    logging.info("Initializing GUI with ttkbootstrap.")
    try:
        app = ttkb.Window(themename="superhero")
        app.title("BitLocker TPM & Pin Setup")
        app.geometry("600x600")

        # Header Section
        header_frame = ttkb.Frame(app)
        header_frame.pack(fill="x", pady=10)

        header_label = ttkb.Label(header_frame, text="BitLocker TPM & Pin Management", font=("Segoe UI", 16, "bold"))
        header_label.pack(pady=10)

        # Detailed BitLocker Status
        status_frame = ttkb.Frame(app, padding=20)
        status_frame.pack(fill="x", pady=20)

        ttkb.Label(status_frame, text="BitLocker Status:", font=("Segoe UI", 14)).pack(side="left", padx=10)
        global bitlocker_status_label
        bitlocker_status_label = ttkb.Label(status_frame, text="Checking...", font=("Segoe UI", 14, "bold"), bootstyle="info")
        bitlocker_status_label.pack(side="left", padx=10)

        refresh_button = ttkb.Button(status_frame, text="Refresh Status", command=update_bitlocker_status, bootstyle="primary-outline")
        refresh_button.pack(side="right", padx=10)
        set_tooltip(refresh_button, "Click to refresh BitLocker status")

        # Form fields for PIN and YubiKey input
        form_frame = ttkb.Frame(app, padding=20)
        form_frame.pack(fill="both", expand=True)

        ttkb.Label(form_frame, text="Enter 8-character PIN:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        global pin_entry
        pin_entry = ttkb.Entry(form_frame, bootstyle="light", show="•")
        pin_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        set_tooltip(pin_entry, "Enter a PIN with at least 1 uppercase letter and 1 number")

        ttkb.Label(form_frame, text="Confirm PIN:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        global confirm_pin_entry
        confirm_pin_entry = ttkb.Entry(form_frame, bootstyle="light", show="•")
        confirm_pin_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        set_tooltip(confirm_pin_entry, "Re-enter the PIN to confirm")

        ttkb.Label(form_frame, text="Press YubiKey:", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        global yubikey_entry
        yubikey_entry = ttkb.Entry(form_frame, state=tk.DISABLED, bootstyle="light")
        yubikey_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        set_tooltip(yubikey_entry, "Press your YubiKey to generate a unique string")

        # Buttons for confirming the PIN and setting the TPM & PIN
        button_frame = ttkb.Frame(app, padding=20)
        button_frame.pack(fill="x", expand=True)

        confirm_button = ttkb.Button(button_frame, text="Confirm PIN", command=confirm_pin, bootstyle="success")
        confirm_button.pack(side="left", padx=10, pady=10)
        set_tooltip(confirm_button, "Click to confirm your PIN")

        set_tpm_button = ttkb.Button(button_frame, text="Set TPM & PIN", command=set_tpm_pin, bootstyle="info")
        set_tpm_button.pack(side="right", padx=10, pady=10)
        set_tooltip(set_tpm_button, "Click to set the BitLocker TPM & PIN using your PIN and YubiKey")

        # Help button for instructions
        help_button = ttkb.Button(app, text="Help", command=show_help, bootstyle="secondary")
        help_button.pack(pady=10)
        set_tooltip(help_button, "Click for more information on how to use this tool")

        update_bitlocker_status()
        app.mainloop()

    except Exception as e:
        logging.error(f"Error initializing GUI: {e}")
        messagebox.showerror("Error", f"Error initializing GUI: {e}")

def update_bitlocker_status():
    """Updates the BitLocker status label."""
    try:
        status_command = "powershell.exe -command \"(Get-BitLockerVolume).VolumeStatus\""
        status_process = subprocess.run(status_command, shell=True, capture_output=True, text=True)
        output = status_process.stdout.strip()

        if "FullyEncrypted" in output:
            bitlocker_status_label.config(text="BitLocker is Enabled", bootstyle="success")
        else:
            bitlocker_status_label.config(text="BitLocker is Disabled", bootstyle="danger")
        logging.info(f"BitLocker status updated: {output}")
    except Exception as e:
        logging.error(f"Error updating BitLocker status: {e}")
        messagebox.showerror("Error", f"Error updating BitLocker status: {e}")

def main():
    logging.info("Starting main program.")
    with open(log_file_path, 'a') as log:
        log.write("Main script started.\n")

    if is_admin():
        logging.info("Running with elevated privileges.")
        with open(log_file_path, 'a') as log:
            log.write("Running with elevated privileges.\n")
        setup_gui()  # Launch the GUI
    else:
        logging.warning("This program requires elevated privileges. Attempting to elevate.")
        with open(log_file_path, 'a') as log:
            log.write("Attempting to elevate privileges...\n")
        elevate_privileges()

if __name__ == "__main__":
    main()
