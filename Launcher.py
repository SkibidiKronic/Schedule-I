import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import math
import random
import time
from datetime import datetime, timezone

class AnimatedBackground(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg='#000000', highlightthickness=0)
        self.pack(fill=tk.BOTH, expand=True)
        
        self.dots = []
        self.velocities = []
        
        # Create initial dots
        for _ in range(50):
            x, y = random.randint(0, 1000), random.randint(0, 700)
            dot = self.create_oval(
                x - 2, y - 2, x + 2, y + 2,
                fill='white',
                outline='white'
            )
            self.dots.append((x, y, dot))
            velocity_x = random.uniform(-0.5, 0.5)
            velocity_y = random.uniform(-0.5, 0.5)
            self.velocities.append((velocity_x, velocity_y))
        
        self.animate()
    
    def animate(self):
        self.delete('line')
        
        # Update dots
        for i, ((x, y, dot), (vx, vy)) in enumerate(zip(self.dots, self.velocities)):
            new_x = x + vx
            new_y = y + vy
            
            # Bounce off walls
            if new_x < 0 or new_x > self.winfo_width():
                vx = -vx
                new_x = x
            if new_y < 0 or new_y > self.winfo_height():
                vy = -vy
                new_y = y
            
            self.dots[i] = (new_x, new_y, dot)
            self.velocities[i] = (vx, vy)
            
            self.coords(
                dot,
                new_x - 2, new_y - 2,
                new_x + 2, new_y + 2
            )
        
        # Draw connecting lines
        for i, (x1, y1, dot1) in enumerate(self.dots):
            for j, (x2, y2, dot2) in enumerate(self.dots):
                if i != j:
                    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    if distance < 150:
                        opacity = int(40 * (1 - distance/150))
                        gray_value = hex(opacity)[2:].zfill(2)
                        color = f'#{gray_value}{gray_value}{gray_value}'
                        self.create_line(
                            x1, y1, x2, y2,
                            fill=color,
                            width=0.5,
                            tags='line'
                        )
        
        self.after(50, self.animate)

class GameLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Schedule I Launcher")
        self.geometry("1200x800")
        self.attributes('-topmost', True)
        
        # Set dark theme
        ctk.set_appearance_mode("dark")
        
        # Create animated background
        self.bg_canvas = AnimatedBackground(self)
        
        # User info frame (bottom left)
        self.user_frame = ctk.CTkFrame(self, fg_color="#101010", corner_radius=15)
        self.user_frame.place(relx=0.02, rely=0.92, anchor="sw")
        
        # Time display with exact format
        self.time_label = ctk.CTkLabel(
            self.user_frame,
            text="",
            font=("Consolas", 12),
            text_color="#ffffff",
            justify="left",
            anchor="w"
        )
        self.time_label.pack(pady=(10, 5), padx=15)
        
        # Username display with exact format
        self.user_label = ctk.CTkLabel(
            self.user_frame,
            text="Current User's Login: SkibidiKronic",
            font=("Consolas", 20, "bold"),
            text_color="#ffffff",
            justify="left",
            anchor="w"
        )
        self.user_label.pack(pady=(0, 10), padx=15)
        
        # Main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Side menu
        self.side_menu = ctk.CTkFrame(self.main_container, fg_color="#101010", corner_radius=15)
        self.side_menu.pack(side="left", fill="y", padx=20, pady=20)
        
        # Button styling
        button_color = "#1f1f1f"
        hover_color = "#2d2d2d"
        
        # Side buttons
        buttons = [
            ("Games", self.show_games),
            ("Settings", self.show_settings),
            ("Updates", self.show_updates),
            ("Creator", self.show_creator),
            ("Support", self.show_support),
            ("Source", self.show_source)
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(
                self.side_menu,
                text=text,
                fg_color=button_color,
                hover_color=hover_color,
                corner_radius=10,
                height=40,
                command=command
            )
            btn.pack(pady=10, padx=20)
        
        # Main content area
        self.main_frame = ctk.CTkFrame(self.main_container, fg_color="#101010", corner_radius=15)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Initialize current frame
        self.current_frame = None
        
        # Start time updates
        self.update_time()
        
        # Show games by default
        self.show_games()

    def update_time(self):
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        self.time_label.configure(text=f"Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {current_time}")
        self.after(1000, self.update_time)

    def clear_main_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None
            
    def show_games(self):
        self.clear_main_frame()
        self.current_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Game title
        game_label = ctk.CTkLabel(
            self.current_frame,
            text="Schedule I",
            font=("Helvetica", 42, "bold"),
            text_color="#ffffff"
        )
        game_label.pack(pady=(50,40))
        
        # Play button
        play_btn = ctk.CTkButton(
            self.current_frame,
            text="PLAY GAME",
            fg_color="#1f1f1f",
            hover_color="#2d2d2d",
            width=400,
            height=100,
            corner_radius=15,
            font=("Helvetica", 32, "bold"),
            command=self.play_game
        )
        play_btn.pack(pady=40)
        
        # Path selection frame with background
        path_frame = ctk.CTkFrame(self.current_frame, fg_color="#1a1a1a", corner_radius=10)
        path_frame.pack(pady=30, fill="x", padx=100)
        
        # Path label
        path_label = ctk.CTkLabel(
            path_frame,
            text="Game Path:",
            font=("Helvetica", 18),
            text_color="#ffffff"
        )
        path_label.pack(side="left", padx=(20,0), pady=20)
        
        # Path entry with increased size
        self.path_entry = ctk.CTkEntry(
            path_frame,
            fg_color="#101010",
            text_color="white",
            width=600,
            height=45,
            font=("Consolas", 16),
            placeholder_text="Select game path...",
            border_color="#2d2d2d",
            border_width=2
        )
        self.path_entry.pack(side="left", padx=20, pady=20)
        
        # Browse button with improved visibility
        browse_btn = ctk.CTkButton(
            path_frame,
            text="Browse",
            fg_color="#2d2d2d",
            hover_color="#3d3d3d",
            width=120,
            height=45,
            corner_radius=8,
            font=("Helvetica", 16, "bold"),
            command=self.browse_file
        )
        browse_btn.pack(side="left", padx=(0,20), pady=20)

    def show_settings(self):
        self.clear_main_frame()
        self.current_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        title = ctk.CTkLabel(
            self.current_frame,
            text="Settings",
            font=("Helvetica", 32, "bold"),
            text_color="#ffffff"
        )
        title.pack(pady=(20,40))
        
        settings = [
            ("Auto-Launch on Startup", False),
            ("Always on Top", True),
            ("Dark Mode", True)
        ]
        
        for setting, default_value in settings:
            setting_frame = ctk.CTkFrame(self.current_frame, fg_color="#1a1a1a", corner_radius=10)
            setting_frame.pack(fill="x", pady=10, padx=20)
            
            label = ctk.CTkLabel(
                setting_frame,
                text=setting,
                font=("Helvetica", 16),
                text_color="#ffffff"
            )
            label.pack(side="left", padx=20, pady=20)
            
            switch = ctk.CTkSwitch(
                setting_frame,
                text="",
                fg_color="#2d2d2d",
                progress_color="#00aa00",
                button_color="#ffffff"
            )
            switch.pack(side="right", padx=20, pady=20)
            if default_value:
                switch.select()

    def show_updates(self):
        self.clear_main_frame()
        self.current_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        title = ctk.CTkLabel(
            self.current_frame,
            text="Updates",
            font=("Helvetica", 32, "bold"),
            text_color="#ffffff"
        )
        title.pack(pady=(20,40))
        
        version_frame = ctk.CTkFrame(self.current_frame, fg_color="#1a1a1a", corner_radius=10)
        version_frame.pack(fill="x", pady=20, padx=20)
        
        version_label = ctk.CTkLabel(
            version_frame,
            text="Current Version: 1.0.0",
            font=("Helvetica", 16),
            text_color="#ffffff"
        )
        version_label.pack(pady=20, padx=20)
        
        status_label = ctk.CTkLabel(
            self.current_frame,
            text="Your software is up to date!",
            font=("Helvetica", 14),
            text_color="#00aa00"
        )
        status_label.pack(pady=20)
        
        update_btn = ctk.CTkButton(
            self.current_frame,
            text="Check for Updates",
            fg_color="#2d2d2d",
            hover_color="#3d3d3d",
            corner_radius=8,
            height=40,
            command=lambda: status_label.configure(text="Checking for updates...")
        )
        update_btn.pack(pady=20)

    def show_creator(self):
        self.clear_main_frame()
        self.current_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        label = ctk.CTkLabel(
            self.current_frame,
            text="Created by SkibidiKronic\nVersion 1.0.0",
            font=("Helvetica", 24)
        )
        label.pack(pady=20)

    def show_support(self):
        self.clear_main_frame()
        self.current_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        title = ctk.CTkLabel(
            self.current_frame,
            text="Support",
            font=("Helvetica", 32, "bold"),
            text_color="#ffffff"
        )
        title.pack(pady=(20,40))
        
        options = [
            ("Documentation", "View the documentation"),
            ("FAQ", "Frequently Asked Questions"),
            ("Report Bug", "Submit a bug report"),
            ("Contact Us", "Get in touch with our team")
        ]
        
        for option_title, description in options:
            option_frame = ctk.CTkFrame(self.current_frame, fg_color="#1a1a1a", corner_radius=10)
            option_frame.pack(fill="x", pady=10, padx=20)
            
            option_btn = ctk.CTkButton(
                option_frame,
                text=option_title,
                fg_color="transparent",
                hover_color="#2d2d2d",
                anchor="w",
                font=("Helvetica", 16, "bold")
            )
            option_btn.pack(side="left", pady=20, padx=20)
            
            desc_label = ctk.CTkLabel(
                option_frame,
                text=description,
                font=("Helvetica", 14),
                text_color="#888888"
            )
            desc_label.pack(side="left", pady=20)

    def show_source(self):
        self.clear_main_frame()
        self.current_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        label = ctk.CTkLabel(
            self.current_frame,
            text="Source Code\nhttps://github.com/SkibidiKronic/Schedule-I",
            font=("Helvetica", 24)
        )
        label.pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)

    def play_game(self):
        game_path = self.path_entry.get()
        if game_path.endswith('.exe'):
            try:
                import subprocess
                subprocess.Popen([game_path])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch game: {str(e)}")
        else:
            messagebox.showerror("Error", "Please select a valid game executable (.exe) file")

if __name__ == "__main__":
    app = GameLauncher()
    app.mainloop()
