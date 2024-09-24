import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import csv
from release_widget import ReleaseCard

class ReleaseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Release Tracker")
        self.geometry("700x700")
        self.configure(bg="#f0f0f0")  # Set a background color

        # Main frame with padding and title
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add a title label
        title_label = ttk.Label(main_frame, text="Release Tracker", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Store release cards
        self.releases = []

        # Add buttons
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(fill=tk.X)

        add_button = ttk.Button(button_frame, text="Add New Release", command=self.add_release, width=20)
        add_button.pack(side=tk.LEFT, padx=5)

        save_button = ttk.Button(button_frame, text="Save to CSV", command=self.save_to_csv, width=20)
        save_button.pack(side=tk.LEFT, padx=5)

        load_button = ttk.Button(button_frame, text="Load from CSV", command=self.load_from_csv, width=20)
        load_button.pack(side=tk.LEFT, padx=5)

        # Frame to contain the release cards
        self.releases_frame = ttk.Frame(main_frame)
        self.releases_frame.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar to the releases frame
        self.canvas = tk.Canvas(self.releases_frame)
        scrollbar = ttk.Scrollbar(self.releases_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel scrolling
        self.bind_mouse_scroll()

    def bind_mouse_scroll(self):
        """Binds mouse wheel scrolling to the canvas."""
        if self.tk.call('tk', 'windowingsystem') == 'win32':
            self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(-int(event.delta / 120), "units"))
        else:
            self.canvas.bind_all("<Button-4>", lambda event: self.canvas.yview_scroll(-1, "units"))
            self.canvas.bind_all("<Button-5>", lambda event: self.canvas.yview_scroll(1, "units"))

    def add_release(self, release_number="", date="", joints=0, footage=0.0):
        release_card = ReleaseCard(self.scrollable_frame, release_number, date, joints, footage, on_remove=self.remove_release)
        release_card.pack(fill=tk.X, pady=5)
        self.releases.append(release_card)
        return release_card

    def remove_release(self, release_card):
        release_card.pack_forget()
        self.releases.remove(release_card)

    def save_to_csv(self):
        csv_data = [['Release Number', 'Date', 'Total Joints', 'Total Footage', 'Loadout Date', 'Loadout Joints', 'Loadout Footage']]
        for release_card in self.releases:
            loadouts = release_card.get_loadouts()
            if not loadouts:
                csv_data.append([release_card.release_number.get(), release_card.date.get(), release_card.joints.get(), release_card.footage.get(), "", "", ""])
            else:
                for loadout in loadouts:
                    csv_data.append([release_card.release_number.get(), release_card.date.get(), release_card.joints.get(), release_card.footage.get(), loadout['date'], loadout['joints'], loadout['footage']])

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(csv_data)
                messagebox.showinfo("Success", f"Data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def load_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='r') as file:
                    reader = csv.reader(file)
                    next(reader)
                    current_release = None

                    for release_card in self.releases:
                        release_card.pack_forget()
                    self.releases.clear()

                    for row in reader:
                        release_number, date, joints, footage, loadout_date, loadout_joints, loadout_footage = row

                        if current_release is None or release_number != current_release.release_number.get():
                            current_release = self.add_release(release_number, date, int(joints), float(footage))
                        
                        if loadout_date:
                            current_release.add_loadout(loadout_date, int(loadout_joints), float(loadout_footage))

                messagebox.showinfo("Success", "Releases loaded from CSV!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

if __name__ == "__main__":
    app = ReleaseTrackerApp()
    app.mainloop()
