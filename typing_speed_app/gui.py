import tkinter as tk
from tkinter import ttk


class AppWindow(tk.Tk):
    def __init__(self, container):
        super().__init__()

        self.title("Typing Speed Test")
        self.size = "800x400"
        self.resizable = (False, False)

    def __repr__(self) -> str:
        return f"Subclass {AppWindow} of {super().__repr__()}"
