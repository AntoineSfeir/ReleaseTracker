import tkinter as tk
from tkinter import ttk  # Themed widgets


class ReleaseCard(tk.Frame):
    def __init__(self, parent, release_number, date, joints, footage, on_remove):
        super().__init__(
            parent, padx=10, pady=10, bd=2, relief="groove", bg="#ffffff"
        )  # Add border and background color
        self.release_number = tk.StringVar(value=release_number)
        self.date = tk.StringVar(value=date)
        self.joints = tk.IntVar(value=joints)
        self.footage = tk.DoubleVar(value=footage)
        self.loadouts = []

        # Create release card layout with grid
        tk.Label(self, text="Release Number:", font=("Arial", 12), bg="#ffffff").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        tk.Entry(
            self, textvariable=self.release_number, font=("Arial", 12), width=25
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Date:", font=("Arial", 12), bg="#ffffff").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        tk.Entry(self, textvariable=self.date, font=("Arial", 12), width=25).grid(
            row=1, column=1, padx=5, pady=5
        )

        tk.Label(self, text="Total Joints:", font=("Arial", 12), bg="#ffffff").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        tk.Entry(self, textvariable=self.joints, font=("Arial", 12), width=25).grid(
            row=2, column=1, padx=5, pady=5
        )

        tk.Label(self, text="Total Footage:", font=("Arial", 12), bg="#ffffff").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        tk.Entry(self, textvariable=self.footage, font=("Arial", 12), width=25).grid(
            row=3, column=1, padx=5, pady=5
        )

        # Remaining joints and footage
        self.remaining_joints_label = tk.Label(
            self, text="Remaining Joints: ", font=("Arial", 12, "bold"), bg="#ffffff"
        )
        self.remaining_joints_label.grid(
            row=4, column=0, padx=5, pady=5, sticky="w", columnspan=2
        )

        self.remaining_footage_label = tk.Label(
            self, text="Remaining Footage: ", font=("Arial", 12, "bold"), bg="#ffffff"
        )
        self.remaining_footage_label.grid(
            row=5, column=0, padx=5, pady=5, sticky="w", columnspan=2
        )

        # Buttons
        tk.Button(
            self,
            text="Add Loadout",
            command=self.add_loadout,
            font=("Arial", 12),
            width=15,
            bg="#4CAF50",
            fg="white",
        ).grid(row=6, column=0, padx=5, pady=5)
        tk.Button(
            self,
            text="Remove Release",
            command=lambda: on_remove(self),
            font=("Arial", 12),
            width=15,
            bg="red",
            fg="white",
        ).grid(row=6, column=1, padx=5, pady=5)

        # Loadouts area
        self.loadouts_frame = tk.Frame(self, bg="#ffffff")
        self.loadouts_frame.grid(row=7, column=0, columnspan=2, pady=10)

        # Initialize remaining values
        self.update_remaining_values()

    def add_loadout(
        self, date="", joints=0, footage=0.0, remaining_joints=0, remaining_footage=0.0
    ):
        loadout = {
            "date": tk.StringVar(value=date),
            "joints": tk.IntVar(value=joints),
            "footage": tk.DoubleVar(value=footage),
            "remaining_joints": tk.IntVar(value=remaining_joints),
            "remaining_footage": tk.DoubleVar(value=remaining_footage),
        }
        row = len(self.loadouts)

        # Create loadout input fields with labels
        tk.Label(
            self.loadouts_frame, text="Loadout Date:", font=("Arial", 10), bg="#ffffff"
        ).grid(row=row, column=0, padx=5, pady=2, sticky="w")
        loadout_date_entry = tk.Entry(
            self.loadouts_frame,
            textvariable=loadout["date"],
            font=("Arial", 10),
            width=15,
        )
        loadout_date_entry.grid(row=row, column=1, padx=5, pady=2)

        tk.Label(
            self.loadouts_frame, text="Joints:", font=("Arial", 10), bg="#ffffff"
        ).grid(row=row, column=2, padx=5, pady=2, sticky="w")
        joints_entry = tk.Entry(
            self.loadouts_frame,
            textvariable=loadout["joints"],
            font=("Arial", 10),
            width=10,
        )
        joints_entry.grid(row=row, column=3, padx=5, pady=2)

        tk.Label(
            self.loadouts_frame, text="Footage:", font=("Arial", 10), bg="#ffffff"
        ).grid(row=row, column=4, padx=5, pady=2, sticky="w")
        footage_entry = tk.Entry(
            self.loadouts_frame,
            textvariable=loadout["footage"],
            font=("Arial", 10),
            width=10,
        )
        footage_entry.grid(row=row, column=5, padx=5, pady=2)

        # Bind the <KeyRelease> and <FocusOut> events to update remaining values dynamically
        joints_entry.bind("<KeyRelease>", lambda event: self.update_remaining_values())
        footage_entry.bind("<KeyRelease>", lambda event: self.update_remaining_values())
        loadout_date_entry.bind(
            "<FocusOut>", lambda event: self.update_remaining_values()
        )
        joints_entry.bind("<FocusOut>", lambda event: self.update_remaining_values())
        footage_entry.bind("<FocusOut>", lambda event: self.update_remaining_values())

        # Add a Remove Loadout button
        remove_button = tk.Button(
            self.loadouts_frame,
            text="Remove",
            command=lambda: self.remove_loadout(loadout, row),
            font=("Arial", 10),
            bg="red",
            fg="white",
        )
        remove_button.grid(row=row, column=6, padx=5, pady=2)

        # Update the remaining values when a new loadout is added
        self.update_remaining_values()

        self.loadouts.append(loadout)

    def remove_loadout(self, loadout, row):
        # Remove loadout from the list
        if loadout in self.loadouts:
            self.loadouts.remove(loadout)
            # Clear the entries in the grid
            for widget in self.loadouts_frame.grid_slaves(row=row):
                widget.destroy()
            # Re-add remaining loadouts to update the layout
            for i, loadout in enumerate(self.loadouts):
                for widget in self.loadouts_frame.grid_slaves(row=i):
                    widget.destroy()
                self.readd_loadout(i, loadout)
            # Update the remaining values
            self.update_remaining_values()

    def readd_loadout(self, row, loadout):
        # Recreate the loadout widgets after removal
        tk.Label(
            self.loadouts_frame, text="Loadout Date:", font=("Arial", 10), bg="#ffffff"
        ).grid(row=row, column=0, padx=5, pady=2, sticky="w")
        loadout_date_entry = tk.Entry(
            self.loadouts_frame,
            textvariable=loadout["date"],
            font=("Arial", 10),
            width=15,
        )
        loadout_date_entry.grid(row=row, column=1, padx=5, pady=2)

        tk.Label(
            self.loadouts_frame, text="Joints:", font=("Arial", 10), bg="#ffffff"
        ).grid(row=row, column=2, padx=5, pady=2, sticky="w")
        joints_entry = tk.Entry(
            self.loadouts_frame,
            textvariable=loadout["joints"],
            font=("Arial", 10),
            width=10,
        )
        joints_entry.grid(row=row, column=3, padx=5, pady=2)

        tk.Label(
            self.loadouts_frame, text="Footage:", font=("Arial", 10), bg="#ffffff"
        ).grid(row=row, column=4, padx=5, pady=2, sticky="w")
        footage_entry = tk.Entry(
            self.loadouts_frame,
            textvariable=loadout["footage"],
            font=("Arial", 10),
            width=10,
        )
        footage_entry.grid(row=row, column=5, padx=5, pady=2)

        # Bind the <KeyRelease> and <FocusOut> events to update remaining values dynamically
        joints_entry.bind("<KeyRelease>", lambda event: self.update_remaining_values())
        footage_entry.bind("<KeyRelease>", lambda event: self.update_remaining_values())
        loadout_date_entry.bind(
            "<FocusOut>", lambda event: self.update_remaining_values()
        )
        joints_entry.bind("<FocusOut>", lambda event: self.update_remaining_values())
        footage_entry.bind("<FocusOut>", lambda event: self.update_remaining_values())

        # Add a Remove Loadout button
        remove_button = tk.Button(
            self.loadouts_frame,
            text="Remove",
            command=lambda: self.remove_loadout(loadout, row),
            font=("Arial", 10),
            bg="red",
            fg="white",
        )
        remove_button.grid(row=row, column=6, padx=5, pady=2)

    def get_loadouts(self):
        self.update_remaining_values()
        return [
            {
                "date": loadout["date"].get(),
                "joints": loadout["joints"].get(),
                "footage": loadout["footage"].get(),
                "remaining_joints": loadout["remaining_joints"].get(),
                "remaining_footage": loadout["remaining_footage"].get(),
            }
            for loadout in self.loadouts
        ]

    def update_remaining_values(self):
        total_loadout_joints = 0
        total_loadout_footage = 0.0

        # Iterate through each loadout and update the remaining joints/footage progressively
        for loadout in self.loadouts:
            try:
                # Safely get the joints value, use 0 if it's empty or invalid
                joints_value = loadout["joints"].get()
                joints_value = int(joints_value) if joints_value else 0
                total_loadout_joints += joints_value

                # Safely get the footage value, use 0.0 if it's empty or invalid
                footage_value = loadout["footage"].get()
                footage_value = float(footage_value) if footage_value else 0.0
                total_loadout_footage += footage_value
            except (ValueError, TclError):
                # If there's an error in conversion (e.g., non-numeric values), use default
                total_loadout_joints += 0
                total_loadout_footage += 0.0

            # Calculate the remaining joints and footage for this specific loadout
            remaining_joints = self.joints.get() - total_loadout_joints
            remaining_footage = self.footage.get() - total_loadout_footage

            # Ensure that remaining values do not go below zero
            remaining_joints = max(remaining_joints, 0)
            remaining_footage = max(remaining_footage, 0.0)

            # Update remaining joints and footage for this loadout
            loadout["remaining_joints"].set(remaining_joints)
            loadout["remaining_footage"].set(remaining_footage)

        # Update the overall remaining values for the release card
        if self.loadouts:
            last_loadout = self.loadouts[-1]
            final_remaining_joints = last_loadout["remaining_joints"].get()
            final_remaining_footage = last_loadout["remaining_footage"].get()
        else:
            final_remaining_joints = self.joints.get()
            final_remaining_footage = self.footage.get()

        self.remaining_joints_label.config(text=f"Remaining Joints: {final_remaining_joints}")
        self.remaining_footage_label.config(text=f"Remaining Footage: {final_remaining_footage:.2f}")

