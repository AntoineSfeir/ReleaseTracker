# Release Tracker Application

## Overview

The **Release Tracker Application** is a desktop application built using Python's `tkinter` library. It is designed for tracking pipe shipping and receiving activities at an oilfield pipe yard. The application allows users to manage releases of pipes by tracking the total number of joints and footage for each release. Additionally, users can log and track loadouts for each release, which are subtracted from the total release values. The program also supports saving and loading release data using CSV files.

## Features

- **Add and Manage Releases**: Users can add new releases, providing details like release number, date, total joints, and footage.
- **Track Loadouts**: Each release can have multiple loadouts, where users specify loadout date, joints, and footage.
- **Visual Charts**: For each release, the application generates pie charts to visually display the remaining and used joints/footage.
- **Save and Load from CSV**: Users can save the release and loadout data to a CSV file and later load it back into the application.
- **Scrollable Interface**: The application supports vertical scrolling for managing multiple releases with an intuitive scrollable interface.

## Installation

1. **Clone the repository or download the files**:
   ```bash
   git clone https://github.com/AntoineSfeir/ReleaseTracker
   ```
   
2. **Install the required dependencies**:
   The application requires the following Python libraries:
   - `tkinter`: Comes pre-installed with most Python installations. If not, install it via your system's package manager.
   - `tkcalendar`: Used for selecting dates.
   - `matplotlib`: Used for generating charts.

   You can install the required libraries using `pip`:
   ```bash
   pip install tkcalendar matplotlib
   ```

3. **Run the application**:
   To start the application, navigate to the project directory and run the following command:
   ```bash
   python main.py
   ```

## Usage

1. **Main Interface**: Once the program starts, you will see the main interface of the Release Tracker.
   - **Add New Release**: Click on the "Add New Release" button to add a new release. You will be prompted to enter the release number, date, total joints, and total footage.
   - **Add Loadout**: For each release, click on the "Add Loadout" button to track a specific loadout (including loadout date, joints, and footage).
   - **Remove Release**: You can remove a release by clicking the "Remove Release" button on the respective release card.
   - **Save to CSV**: Click the "Save to CSV" button to export your release data (including loadouts) to a CSV file.
   - **Load from CSV**: Click the "Load from CSV" button to import release data from a previously saved CSV file.

2. **Managing Loadouts**:
   - Add multiple loadouts to each release.
   - View the remaining joints and footage after subtracting loadouts from the total release.
   - Remove loadouts if needed.

3. **Charts**: Each release card shows two pie charts: one for the total and remaining joints and another for the total and remaining footage.

## CSV File Format

The program saves and loads release and loadout data in a CSV format with the following structure:

| Release Number | Date | Total Joints | Total Footage | Loadout Date | Loadout Joints | Loadout Footage |
| -------------- | ---- | ------------ | ------------- | ------------ | -------------- | --------------- |
| R001           | 2023-09-01 | 100 | 1000.0 | 2023-09-02 | 20 | 200.0 |
| R001           | 2023-09-01 | 100 | 1000.0 | 2023-09-05 | 30 | 300.0 |
| R002           | 2023-09-03 | 150 | 1500.0 |  |  |  |

- The first four columns (Release Number, Date, Total Joints, Total Footage) correspond to the release information.
- The next three columns (Loadout Date, Loadout Joints, Loadout Footage) correspond to individual loadouts associated with that release.

## Future Improvements

- **Undo/Redo Support**: Allow users to undo and redo actions, such as adding or removing loadouts and releases.
- **Autosave**: Implement autosave functionality to periodically save data to prevent data loss.
- **Export to Excel**: Add the ability to export release data to an Excel file (.xlsx) for more flexibility.
- **Search Functionality**: Implement a search bar to quickly find releases by release number.

## Troubleshooting

1. **Matplotlib not displaying charts**:
   - Ensure you have `matplotlib` installed properly using `pip install matplotlib`.
   - If the issue persists, try upgrading `matplotlib` or reinstalling it.

2. **CSV not loading correctly**:
   - Ensure that the CSV file follows the correct format. If your CSV file was edited manually, make sure that all required fields are present and correctly ordered.
