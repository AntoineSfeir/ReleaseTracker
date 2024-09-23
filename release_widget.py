import tkinter as tk
from tkinter import ttk  # Themed widgets

class ReleaseCard(tk.Frame):
    def __init__(self, parent, release_number, date, joints, footage, on_remove):
        super().__init__(parent, padx=10, pady=10, bd=2, relief="groove")  # Add border for better visibility
        self.release_number = tk.StringVar(value=release_number)
        self.date = tk.StringVar(value=date)
        self.joints = tk.IntVar(value=joints)
        self.footage = tk.DoubleVar(value=footage)
        self.loadouts = []

        # Create release card layout with grid
        tk.Label(self, text="Release Number:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.release_number, font=("Arial", 12), width=20).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Date:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.date, font=("Arial", 12), width=20).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Total Joints:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.joints, font=("Arial", 12), width=20).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Total Footage:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.footage, font=("Arial", 12), width=20).grid(row=3, column=1, padx=5, pady=5)

        # Remaining joints and footage
        self.remaining_joints_label = tk.Label(self, text="Remaining Joints: ", font=("Arial", 12, "bold"))
        self.remaining_joints_label.grid(row=4, column=0, padx=5, pady=5, sticky="w", columnspan=2)

        self.remaining_footage_label = tk.Label(self, text="Remaining Footage: ", font=("Arial", 12, "bold"))
        self.remaining_footage_label.grid(row=5, column=0, padx=5, pady=5, sticky="w", columnspan=2)

        # Buttons
        tk.Button(self, text="Add Loadout", command=self.add_loadout, font=("Arial", 12), width=15).grid(row=6, column=0, padx=5, pady=5)
        tk.Button(self, text="Remove Release", command=lambda: on_remove(self), font=("Arial", 12), width=15, bg="red", fg="white").grid(row=6, column=1, padx=5, pady=5)

        # Loadouts area
        self.loadouts_frame = tk.Frame(self)
        self.loadouts_frame.grid(row=7, column=0, columnspan=2, pady=10)

        self.update_remaining_values()

    def add_loadout(self, date="", joints=0, footage=0.0):
        loadout = {
            "date": tk.StringVar(value=date),
            "joints": tk.IntVar(value=joints),
            "footage": tk.DoubleVar(value=footage)
        }
        row = len(self.loadouts)

        # Create loadout input fields with labels
        tk.Label(self.loadouts_frame, text="Loadout Date:", font=("Arial", 10)).grid(row=row, column=0, padx=5, pady=2, sticky="w")
        tk.Entry(self.loadouts_frame, textvariable=loadout["date"], font=("Arial", 10), width=15).grid(row=row, column=1, padx=5, pady=2)

        tk.Label(self.loadouts_frame, text="Joints:", font=("Arial", 10)).grid(row=row, column=2, padx=5, pady=2, sticky="w")
        
        # Split declaration and layout of joints_entry
        joints_entry = tk.Entry(self.loadouts_frame, textvariable=loadout["joints"], font=("Arial", 10), width=10)
        joints_entry.grid(row=row, column=3, padx=5, pady=2)

        tk.Label(self.loadouts_frame, text="Footage:", font=("Arial", 10)).grid(row=row, column=4, padx=5, pady=2, sticky="w")
        
        # Split declaration and layout of footage_entry
        footage_entry = tk.Entry(self.loadouts_frame, textvariable=loadout["footage"], font=("Arial", 10), width=10)
        footage_entry.grid(row=row, column=5, padx=5, pady=2)

        # Bind the <KeyRelease> event to both Entry widgets to update the remaining values when modified
        joints_entry.bind("<KeyRelease>", lambda event: self.update_remaining_values())
        footage_entry.bind("<KeyRelease>", lambda event: self.update_remaining_values())

        self.loadouts.append(loadout)

        # Update the remaining values when a new loadout is added
        self.update_remaining_values()

    def get_loadouts(self):
        return [{"date": loadout["date"].get(), "joints": loadout["joints"].get(), "footage": loadout["footage"].get()} for loadout in self.loadouts]

    def update_remaining_values(self):
        # Calculate total loadout joints and footage
        total_loadout_joints = sum(loadout["joints"].get() for loadout in self.loadouts)
        total_loadout_footage = sum(loadout["footage"].get() for loadout in self.loadouts)

        # Calculate remaining joints and footage
        remaining_joints = self.joints.get() - total_loadout_joints
        remaining_footage = self.footage.get() - total_loadout_footage

        # Update labels with the remaining values
        self.remaining_joints_label.config(text=f"Remaining Joints: {remaining_joints}")
        self.remaining_footage_label.config(text=f"Remaining Footage: {remaining_footage:.2f}")
