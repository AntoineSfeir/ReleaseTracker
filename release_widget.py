import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReleaseCard(tk.Frame):
    def __init__(self, parent, release_number, date, joints, footage, on_remove):
        super().__init__(parent, padx=10, pady=10, bd=2, relief="groove", bg="#ffffff")
        self.release_number = tk.StringVar(value=release_number)
        self.date = tk.StringVar(value=date)
        self.joints = tk.IntVar(value=joints)
        self.footage = tk.DoubleVar(value=footage)
        self.loadouts = []

        # Create release card layout with grid
        tk.Label(self, text="Release Number:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.release_number, font=("Arial", 12), width=25).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Date:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = DateEntry(self, textvariable=self.date, font=("Arial", 12), width=25, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Total Joints:", font=("Arial", 12), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.joints, font=("Arial", 12), width=25).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Total Footage:", font=("Arial", 12), bg="#ffffff").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.footage, font=("Arial", 12), width=25).grid(row=3, column=1, padx=5, pady=5)

        # Remaining joints and footage
        self.remaining_joints_label = tk.Label(self, text="Remaining Joints: ", font=("Arial", 12, "bold"), bg="#ffffff")
        self.remaining_joints_label.grid(row=4, column=0, padx=5, pady=5, sticky="w", columnspan=2)

        self.remaining_footage_label = tk.Label(self, text="Remaining Footage: ", font=("Arial", 12, "bold"), bg="#ffffff")
        self.remaining_footage_label.grid(row=5, column=0, padx=5, pady=5, sticky="w", columnspan=2)

        # Add buttons
        tk.Button(self, text="Add Loadout", command=self.add_loadout, font=("Arial", 12), width=15, bg="#4CAF50", fg="white").grid(row=6, column=0, padx=5, pady=5)
        tk.Button(self, text="Remove Release", command=lambda: on_remove(self), font=("Arial", 12), width=15, bg="red", fg="white").grid(row=6, column=1, padx=5, pady=5)

        # Loadouts area
        self.loadouts_frame = tk.Frame(self, bg="#ffffff")
        self.loadouts_frame.grid(row=7, column=0, columnspan=2, pady=10)

        # Chart area
        self.chart_frame = tk.Frame(self, bg="#ffffff")
        self.chart_frame.grid(row=8, column=0, columnspan=2)

        # Initialize remaining values and chart
        self.update_remaining_values()
        self.draw_chart()

    def add_loadout(self, date="", joints=0, footage=0.0):
        loadout = {
            "date": tk.StringVar(value=date),
            "joints": tk.IntVar(value=joints),
            "footage": tk.DoubleVar(value=footage)
        }
        row = len(self.loadouts)

        # Create loadout input fields with labels
        tk.Label(self.loadouts_frame, text="Loadout Date:", font=("Arial", 10), bg="#ffffff").grid(row=row, column=0, padx=5, pady=2, sticky="w")
        loadout_date_entry = DateEntry(self.loadouts_frame, textvariable=loadout["date"], font=("Arial", 10), width=15, date_pattern='yyyy-mm-dd')
        loadout_date_entry.grid(row=row, column=1, padx=5, pady=2)

        tk.Label(self.loadouts_frame, text="Joints:", font=("Arial", 10), bg="#ffffff").grid(row=row, column=2, padx=5, pady=2, sticky="w")
        joints_entry = tk.Entry(self.loadouts_frame, textvariable=loadout["joints"], font=("Arial", 10), width=10)
        joints_entry.grid(row=row, column=3, padx=5, pady=2)

        tk.Label(self.loadouts_frame, text="Footage:", font=("Arial", 10), bg="#ffffff").grid(row=row, column=4, padx=5, pady=2, sticky="w")
        footage_entry = tk.Entry(self.loadouts_frame, textvariable=loadout["footage"], font=("Arial", 10), width=10)
        footage_entry.grid(row=row, column=5, padx=5, pady=2)

        # Bind events to update remaining values
        joints_entry.bind("<KeyRelease>", lambda event: self.update_remaining_values())
        footage_entry.bind("<KeyRelease>", lambda event: self.update_remaining_values())
        loadout_date_entry.bind("<FocusOut>", lambda event: self.update_remaining_values())

        # Add a Remove Loadout button
        remove_button = tk.Button(
            self.loadouts_frame,
            text="Remove",
            command=lambda: self.remove_loadout(loadout, row),
            font=("Arial", 10),
            bg="red",
            fg="white"
        )
        remove_button.grid(row=row, column=6, padx=5, pady=2)

        self.loadouts.append(loadout)

        # Update the remaining values when a new loadout is added
        self.update_remaining_values()
        self.draw_chart()

    def remove_loadout(self, loadout, row):
        if loadout in self.loadouts:
            self.loadouts.remove(loadout)
            for widget in self.loadouts_frame.grid_slaves(row=row):
                widget.destroy()
            self.update_remaining_values()
            self.draw_chart()

    def get_loadouts(self):
        return [
            {
                "date": loadout["date"].get(),
                "joints": loadout["joints"].get(),
                "footage": loadout["footage"].get()
            }
            for loadout in self.loadouts
        ]

    def update_remaining_values(self):
        total_loadout_joints = sum(loadout["joints"].get() for loadout in self.loadouts)
        total_loadout_footage = sum(loadout["footage"].get() for loadout in self.loadouts)

        remaining_joints = self.joints.get() - total_loadout_joints
        remaining_footage = self.footage.get() - total_loadout_footage

        remaining_joints = max(remaining_joints, 0)
        remaining_footage = max(remaining_footage, 0.0)

        self.remaining_joints_label.config(text=f"Remaining Joints: {remaining_joints}")
        self.remaining_footage_label.config(text=f"Remaining Footage: {remaining_footage:.2f}")

    def draw_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()  # Clear previous chart
        
        fig, axs = plt.subplots(1, 2, figsize=(6, 3))

        # Data for joints pie chart
        total_joints = self.joints.get()
        remaining_joints = max(self.joints.get() - sum(loadout["joints"].get() for loadout in self.loadouts), 0)
        used_joints = total_joints - remaining_joints

        # Data for footage pie chart
        total_footage = self.footage.get()
        remaining_footage = max(self.footage.get() - sum(loadout["footage"].get() for loadout in self.loadouts), 0)
        used_footage = total_footage - remaining_footage

        # Pie chart for joints
        axs[0].pie([remaining_joints, used_joints], labels=['Remaining', 'Used'], autopct='%1.1f%%', colors=['#4CAF50', '#FF5722'], startangle=90)
        axs[0].set_title('Joints')

        # Pie chart for footage
        axs[1].pie([remaining_footage, used_footage], labels=['Remaining', 'Used'], autopct='%1.1f%%', colors=['#2196F3', '#FFC107'], startangle=90)
        axs[1].set_title('Footage')

        for ax in axs:
            ax.axis('equal')  # Equal aspect ratio ensures the pie chart is a circle

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
