import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import schedule
import time
import threading

# Initialize or load events DataFrame
try:
    events_df = pd.read_csv('events.csv')
except FileNotFoundError:
    events_df = pd.DataFrame(columns=["Title", "Date", "Time", "Reminder"])

# Save events to CSV
def save_events():
    events_df.to_csv('events.csv', index=False)

# Add new event to DataFrame and display
# Function to add a new event
def add_event():
    title = title_entry.get()
    date = date_entry.get()
    time = time_entry.get()
    reminder = reminder_var.get()

    if not title or not date or not time:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        # Check if date and time are in correct format
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(time, "%H:%M")

        # Create new event as a DataFrame and append using pd.concat
        new_event = pd.DataFrame({"Title": [title], "Date": [date], "Time": [time], "Reminder": [reminder]})
        global events_df
        events_df = pd.concat([events_df, new_event], ignore_index=True)
        save_events()

        # Clear input fields
        title_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        reminder_var.set(0)

        # Update the event list display
        update_event_list()
        messagebox.showinfo("Success", "Event added successfully!")
    except ValueError:
        messagebox.showerror("Date/Time Error", "Date must be YYYY-MM-DD and time HH:MM.")

# Update event list display
def update_event_list():
    event_listbox.delete(0, tk.END)
    sorted_events = events_df.sort_values(by=["Date", "Time"])
    for _, event in sorted_events.iterrows():
        event_listbox.insert(tk.END, f"{event['Date']} {event['Time']} - {event['Title']}")

# Set up scheduled reminders
def run_reminders():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for _, event in events_df.iterrows():
        event_time = f"{event['Date']} {event['Time']}"
        if event['Reminder'] == 1 and event_time == now:
            messagebox.showinfo("Reminder", f"Event Reminder: {event['Title']}")

# Background reminder checker using threading
def start_reminder_checker():
    def check_reminders():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    thread = threading.Thread(target=check_reminders, daemon=True)
    thread.start()

# Initialize the GUI
root = tk.Tk()
root.title("Event Scheduler and Reminder App")
root.geometry("500x600")
root.configure(bg="#2c2f33")

# Title input
tk.Label(root, text="Event Title:", font=("Arial", 12), fg="white", bg="#2c2f33").pack(pady=(20, 5))
title_entry = tk.Entry(root, font=("Arial", 12), bg="#23272a", fg="white", insertbackground="white")
title_entry.pack(pady=(0, 10))

# Date input
tk.Label(root, text="Event Date (YYYY-MM-DD):", font=("Arial", 12), fg="white", bg="#2c2f33").pack(pady=5)
date_entry = tk.Entry(root, font=("Arial", 12), bg="#23272a", fg="white", insertbackground="white")
date_entry.pack(pady=(0, 10))

# Time input
tk.Label(root, text="Event Time (HH:MM):", font=("Arial", 12), fg="white", bg="#2c2f33").pack(pady=5)
time_entry = tk.Entry(root, font=("Arial", 12), bg="#23272a", fg="white", insertbackground="white")
time_entry.pack(pady=(0, 10))

# Reminder checkbox
reminder_var = tk.IntVar()
reminder_checkbox = tk.Checkbutton(root, text="Set Reminder", variable=reminder_var, font=("Arial", 12), fg="white", bg="#2c2f33", selectcolor="#2c2f33")
reminder_checkbox.pack(pady=5)

# Add Event Button
add_event_button = tk.Button(root, text="Add Event", font=("Arial", 12), bg="#7289da", fg="white", command=add_event)
add_event_button.pack(pady=(20, 10))

# Event list display
tk.Label(root, text="Scheduled Events:", font=("Arial", 12), fg="white", bg="#2c2f33").pack(pady=10)
event_listbox = tk.Listbox(root, font=("Arial", 12), bg="#23272a", fg="white", selectbackground="#7289da", highlightthickness=0)
event_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

# Load existing events on startup
update_event_list()

# Start background reminder checker
start_reminder_checker()

root.mainloop()
