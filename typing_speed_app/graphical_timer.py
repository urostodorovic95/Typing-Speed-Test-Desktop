"""
Module: countdown_timer

This module defines a simple CountdownTimer class for creating
 a countdown timer with GUI components.

Classes:
- CountdownTimer: A class representing a countdown timer.

Usage Example:
--------------
from tkinter import Tk, Label, Progressbar
from countdown_timer import CountdownTimer

root = Tk()

# Create label and progress bar widgets
label = Label(root, text="Time left: 0 seconds")
label.pack()

progressbar = Progressbar(root, length=200, mode='determinate')
progressbar.pack()

# Create CountdownTimer instance
timer = CountdownTimer(time_ms=5000, parent=root, label=label, progressbar=progressbar)

# Initialize and start the timer
timer.init_timer()

# Run the Tkinter main loop
root.mainloop()
"""


class CountdownTimer:
    """
    A simple countdown timer class with GUI components.

    Attributes:
    - time_ms (int): Total time in milliseconds.
    - parent: The parent widget for the timer.
    - label: The label widget to display time information.
    - progressbar: The progress bar widget to show the timer progress.

    Methods:
    - __init__(self, time_ms, parent, label, progressbar): Constructor to initialize the timer.
    - init_timer(self): Initialize and start the timer.
    - update_time_left(self): Update the time left, label, and progress bar.
    """

    def __init__(self, time_ms, parent, label, progressbar):
        """
        Initialize the CountdownTimer.

        Parameters:
        - time_ms (int): Total time in milliseconds.
        - parent: The parent widget for the timer.
        - label: The label widget to display time information.
        - progressbar: The progress bar widget to show the timer progress.
        """
        self.parent = parent
        self.total_time = time_ms / 1000  # Total time in seconds
        self.time_left = self.total_time  # Initial time

        self.label = label
        self.progress = progressbar

    def init_timer(self):
        """
        Initialize and start the countdown timer.

        This method calls the update_time_left function every second.
        """
        # Call the update_time_left function every second
        self.parent.after(1000, self.update_time_left)

    def update_time_left(self):
        """
        Update the time left, label, and progress bar.

        This method decrements the time_left attribute, updates the label
        with the remaining time, and adjusts the progress bar accordingly.
        If time has run out, it displays "Time's up!" on the label.
        """
        self.time_left -= 1
        self.label.config(text=f"Time left: {self.time_left} seconds")

        # update the progress bar from full to 0
        progress_value = (self.time_left / self.total_time) * 100
        self.progress["value"] = progress_value

        # Check if time has run out
        if self.time_left <= 0:
            self.label.config(text="Time's up!")
            self.progress["value"] = 0
        else:
            # Call the update_time_left function again after 1000 milliseconds
            self.parent.after(1000, self.update_time_left)
