import customtkinter as ctk
import threading
import time
import tkinter.messagebox as msgbox
from tkinter import PhotoImage
import math

class PomodoroTimer:
    def __init__(self):
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("420x550")   
        self.root.minsize(400, 550)     # Ensure minimum size fits everything
        
        # Rich color palette
        self.colors = {
            "bg_primary": "#0a0a0a",
            "bg_secondary": "#1a1a1a",
            "accent_gold": "#FFD700",
            "accent_crimson": "#DC143C",
            "accent_emerald": "#50C878",
            "accent_purple": "#8A2BE2",
            "text_primary": "#FFFFFF",
            "text_secondary": "#CCCCCC",
            "gradient_start": "#FF6B6B",
            "gradient_end": "#4ECDC4"
        }
        
        # Configure root background
        self.root.configure(fg_color=self.colors["bg_primary"])
        
        # Timer states
        self.is_running = False
        self.is_paused = False
        self.current_session = "work"  # work, short_break, long_break
        self.session_count = 0
        
        # Time settings (in seconds)
        self.work_time = 25 * 60
        self.short_break_time = 5 * 60
        self.long_break_time = 15 * 60
        
        # Current time remaining
        self.time_remaining = self.work_time
        
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        # Create main container with accent streaks
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.colors["bg_secondary"],
            corner_radius=20,
            border_width=2,
            border_color=self.colors["accent_gold"]
        )
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Title with accent streaks
        self.create_title_section()
        
        # Circular progress indicator
        self.create_progress_section()
        
        # Time display
        self.create_time_display()
        
        # Session indicator
        self.create_session_indicator()
        
        # Control buttons
        self.create_control_buttons()
        
    def create_title_section(self):
        # Title frame with accent streaks
        title_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            height=60
        )
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        title_frame.pack_propagate(False)
        
        # Left accent streak
        left_streak = ctk.CTkFrame(
            title_frame,
            fg_color=self.colors["accent_crimson"],
            width=3,
            height=40,
            corner_radius=2
        )
        left_streak.pack(side="left", padx=(0, 15))
        
        # Title text
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="POMODORO TIMER",
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color=self.colors["accent_gold"]
        )
        self.title_label.pack(side="left", expand=True, fill="x")
        
        # Right accent streak
        right_streak = ctk.CTkFrame(
            title_frame,
            fg_color=self.colors["accent_emerald"],
            width=3,
            height=40,
            corner_radius=2
        )
        right_streak.pack(side="right", padx=(15, 0))
        
    def create_progress_section(self):
        # Progress container
        self.progress_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            height=180
        )
        self.progress_frame.pack(fill="x", padx=20, pady=10)
        self.progress_frame.pack_propagate(False)
        
        # Create canvas for circular progress
        self.canvas = ctk.CTkCanvas(
            self.progress_frame,
            width=160,
            height=160,
            bg=self.colors["bg_secondary"],
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        
    def create_time_display(self):
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="25:00",
            font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.time_label.pack(pady=(0, 20))
        
    def create_session_indicator(self):
        indicator_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        indicator_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        self.session_label = ctk.CTkLabel(
            indicator_frame,
            text="WORK SESSION",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color=self.colors["accent_crimson"]
        )
        self.session_label.pack()
        
        # Session counter
        self.counter_label = ctk.CTkLabel(
            indicator_frame,
            text="Session 1 of 4",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text_secondary"]
        )
        self.counter_label.pack()
        
    def create_control_buttons(self):
        button_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        # Start/Pause button
        self.start_button = ctk.CTkButton(
            button_frame,
            text="START",
            command=self.toggle_timer,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            fg_color=self.colors["accent_emerald"],
            hover_color=self.colors["accent_gold"],
            width=120,
            height=40,
            corner_radius=20
        )
        self.start_button.pack(side="left", expand=True, padx=(0, 10))
        
        # Reset button
        self.reset_button = ctk.CTkButton(
            button_frame,
            text="RESET",
            command=self.reset_timer,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            fg_color=self.colors["accent_purple"],
            hover_color=self.colors["accent_crimson"],
            width=120,
            height=40,
            corner_radius=20
        )
        self.reset_button.pack(side="right", expand=True, padx=(10, 0))
        
    def draw_progress_circle(self, progress):
        self.canvas.delete("all")
        
        # Circle dimensions
        x, y = 80, 80
        radius = 70
        
        # Background circle
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            outline=self.colors["bg_primary"], width=8
        )
        
        # Progress arc
        if progress > 0:
            angle = 360 * progress
            self.canvas.create_arc(
                x - radius, y - radius, x + radius, y + radius,
                start=90, extent=-angle,
                outline=self.get_session_color(), width=8,
                style="arc"
            )
        
        # Inner decorative circle
        inner_radius = radius - 20
        self.canvas.create_oval(
            x - inner_radius, y - inner_radius, x + inner_radius, y + inner_radius,
            outline=self.colors["accent_gold"], width=2
        )
        
    def get_session_color(self):
        colors = {
            "work": self.colors["accent_crimson"],
            "short_break": self.colors["accent_emerald"],
            "long_break": self.colors["accent_purple"]
        }
        return colors.get(self.current_session, self.colors["accent_gold"])
        
    def toggle_timer(self):
        if not self.is_running:
            self.start_timer()
        else:
            self.pause_timer()
            
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.start_button.configure(text="PAUSE")
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()
            
    def pause_timer(self):
        self.is_running = False
        self.is_paused = True
        self.start_button.configure(text="RESUME")
        
    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.start_button.configure(text="START")
        
        # Reset to work session
        self.current_session = "work"
        self.time_remaining = self.work_time
        self.session_count = 0
        
        self.update_display()
        
    def run_timer(self):
        while self.is_running and self.time_remaining > 0:
            time.sleep(1)
            if self.is_running:
                self.time_remaining -= 1
                self.root.after(0, self.update_display)
                
        if self.is_running:  # Timer completed
            self.root.after(0, self.session_complete)
            
    def session_complete(self):
        self.is_running = False
        self.start_button.configure(text="START")
        
        # Show completion message
        session_name = self.current_session.replace("_", " ").title()
        msgbox.showinfo("Session Complete", f"{session_name} completed!")
        
        # Move to next session
        self.next_session()
        
    def next_session(self):
        if self.current_session == "work":
            self.session_count += 1
            if self.session_count % 4 == 0:
                self.current_session = "long_break"
                self.time_remaining = self.long_break_time
            else:
                self.current_session = "short_break"
                self.time_remaining = self.short_break_time
        else:
            self.current_session = "work"
            self.time_remaining = self.work_time
            
        self.update_display()
        
    def update_display(self):
        # Update time display
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_text = f"{minutes:02d}:{seconds:02d}"
        self.time_label.configure(text=time_text)
        
        # Update session indicator
        session_names = {
            "work": "WORK SESSION",
            "short_break": "SHORT BREAK",
            "long_break": "LONG BREAK"
        }
        self.session_label.configure(
            text=session_names[self.current_session],
            text_color=self.get_session_color()
        )
        
        # Update session counter
        if self.current_session == "work":
            self.counter_label.configure(text=f"Session {self.session_count + 1} of 4")
        else:
            self.counter_label.configure(text=f"Break Time")
        
        # Update progress circle
        total_time = {
            "work": self.work_time,
            "short_break": self.short_break_time,
            "long_break": self.long_break_time
        }[self.current_session]
        
        progress = 1 - (self.time_remaining / total_time)
        self.draw_progress_circle(progress)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()