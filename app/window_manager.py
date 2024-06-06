import tkinter as tk
from tkinter import ttk
from util import logger
from app import PriceManager


class WindowManager:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WindowManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self.__class__._is_initialized:
            logger.debug("Initializing Window Manager")
            self.root = tk.Tk()
            self.root.title("Crypto Prices")
            self.labels = {}

            self.__class__._is_initialized = True  

    # Function to refresh the displayed data
    def refresh_data(self):
        data = PriceManager().rolling_sums
        sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
        
        for widget in self.frame.winfo_children():
            widget.destroy()
        # Update data
        for row, (key, value) in enumerate(sorted_data):
            text = f"{key}: {value:.8f}"
            label = ttk.Label(self.frame, text=text)
            label.grid(row=row, column=0, sticky=tk.W)
    
        self.root.after(5000, self.refresh_data)  # Schedule the next refresh


    # Create labels for each item in the data dictionary
    def start_window(self):
        
        # Create a frame to hold the labels
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Start the refresh loop
        self.root.after(5000, self.refresh_data)

        # Run the application
        self.root.mainloop()