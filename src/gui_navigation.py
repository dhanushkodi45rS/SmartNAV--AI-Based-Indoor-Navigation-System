# gui_navigation.py

import tkinter as tk
from tkinter import ttk, messagebox
from sample_map import MARKER_LOCATIONS

class NavigationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MGRNav - Indoor Navigation System")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c3e50")
        
        self.selected_destination = None
        self.navigation_started = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text=" MGRNav Indoor Navigation",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Destination Selection Frame
        selection_frame = tk.Frame(self.root, bg="#34495e", padx=20, pady=20)
        selection_frame.pack(pady=20, padx=40, fill="x")
        
        tk.Label(
            selection_frame,
            text="Select Your Destination:",
            font=("Arial", 14),
            bg="#34495e",
            fg="white"
        ).pack(pady=10)
        
        # Dropdown
        self.destination_var = tk.StringVar()
        destination_options = [f"{id} - {name}" for id, name in MARKER_LOCATIONS.items()]
        
        self.destination_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.destination_var,
            values=destination_options,
            state="readonly",
            font=("Arial", 12),
            width=30
        )
        self.destination_dropdown.pack(pady=10)
        self.destination_dropdown.set("Select destination...")
        
        # Start Button
        self.start_button = tk.Button(
            selection_frame,
            text=" Start Navigation",
            command=self.start_navigation,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.start_button.pack(pady=10)
        
        # Status Frame
        status_frame = tk.Frame(self.root, bg="#34495e", padx=20, pady=20)
        status_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        tk.Label(
            status_frame,
            text="Navigation Status:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        ).pack(anchor="w")
        
        self.status_label = tk.Label(
            status_frame,
            text="Please select a destination and click Start",
            font=("Arial", 11),
            bg="#34495e",
            fg="#ecf0f1",
            wraplength=500,
            justify="left"
        )
        self.status_label.pack(pady=10, anchor="w")
        
        # Instruction Label
        tk.Label(
            status_frame,
            text="Current Instruction:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="white"
        ).pack(anchor="w", pady=(20, 0))
        
        self.instruction_label = tk.Label(
            status_frame,
            text="Waiting to start...",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#3498db",
            wraplength=500,
            justify="left"
        )
        self.instruction_label.pack(pady=10, anchor="w")
        
        # Distance Label
        self.distance_label = tk.Label(
            status_frame,
            text="",
            font=("Arial", 11),
            bg="#34495e",
            fg="#e74c3c"
        )
        self.distance_label.pack(pady=5, anchor="w")
        
        # Reset Button
        self.reset_button = tk.Button(
            self.root,
            text=" Reset Navigation",
            command=self.reset_navigation,
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5,
            cursor="hand2",
            state="disabled"
        )
        self.reset_button.pack(pady=10)
    
    def start_navigation(self):
        selected = self.destination_var.get()
        
        if selected == "Select destination...":
            messagebox.showwarning("No Destination", "Please select a destination first!")
            return
        
        # Extract marker ID from selection
        dest_id = int(selected.split(" - ")[0])
        self.selected_destination = dest_id
        self.navigation_started = True
        
        # Update UI
        self.start_button.config(state="disabled")
        self.destination_dropdown.config(state="disabled")
        self.reset_button.config(state="normal")
        
        self.status_label.config(
            text=f" Destination set to: {MARKER_LOCATIONS[dest_id]}\n📷 Please scan any marker to start navigation...",
            fg="#2ecc71"
        )
        self.instruction_label.config(text="Waiting for first marker scan...")
    
    def update_status(self, message, color="#ecf0f1"):
        """Update the status label"""
        self.status_label.config(text=message, fg=color)
    
    def update_instruction(self, instruction, distance=None):
        """Update navigation instruction"""
        self.instruction_label.config(text=instruction)
        if distance:
            self.distance_label.config(text=f"📏 Distance: {distance}m")
        else:
            self.distance_label.config(text="")
    
    def show_completion(self):
        """Show destination reached"""
        self.instruction_label.config(text=" DESTINATION REACHED!", fg="#2ecc71")
        self.status_label.config(text=" Navigation completed successfully!", fg="#2ecc71")
        self.distance_label.config(text="")
    
    def show_rerouting(self):
        """Show re-routing message"""
        self.status_label.config(text=" Wrong turn detected! Recalculating route...", fg="#f39c12")
    
    def reset_navigation(self):
        """Reset the navigation"""
        self.selected_destination = None
        self.navigation_started = False
        
        self.destination_var.set("Select destination...")
        self.destination_dropdown.config(state="readonly")
        self.start_button.config(state="normal")
        self.reset_button.config(state="disabled")
        
        self.status_label.config(
            text="Please select a destination and click Start",
            fg="#ecf0f1"
        )
        self.instruction_label.config(text="Waiting to start...", fg="#3498db")
        self.distance_label.config(text="")
    
    def get_destination(self):
        """Get selected destination"""
        return self.selected_destination
    
    def is_started(self):
        """Check if navigation has started"""
        return self.navigation_started