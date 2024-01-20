class CountdownTimer:
    def __init__(self, time_ms, parent, label, progressbar):
        self.parent = parent
        self.total_time = time_ms / 1000  # Total time in seconds
        self.time_left = self.total_time  # Initial time

        self.label = label
        self.progress = progressbar

    def init_timer(self):
        # Call the update_time_left function every second
        self.parent.after(1000, self.update_time_left)

    def update_time_left(self):
        self.time_left -= 1
        self.label.config(text=f"Time left: {self.time_left} seconds")

        # Update the progress bar
        progress_value = ((self.total_time - self.time_left) / self.total_time) * 100
        self.progress["value"] = progress_value

        # Check if time has run out
        if self.time_left <= 0:
            self.label.config(text="Time's up!")
            self.progress["value"] = 100
        else:
            # Call the update_time_left function again after 1000 milliseconds
            self.parent.after(1000, self.update_time_left)
