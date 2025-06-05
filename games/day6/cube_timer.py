import tkinter as tk
from tkinter import messagebox
import time
import json
import os

DATA_FILE = "cube_times.json"


class CubeTimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cube Timer & Analysis")
        # Increase window size
        self.geometry("600x500")
        # Light background
        self.configure(bg="#f0f0f0")

        self.cube_size = None
        self.start_time = None
        self.elapsed_time = 0.0
        self.running = False
        self.timer_job = None

        # Data structure for recorded times
        self.data = {"3x3": [], "6x6": []}
        self._load_data()
        self._build_main_page()

    def _load_data(self):
        """Load recorded times from JSON file, or initialize if not present."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    loaded = json.load(f)
                    self.data["3x3"] = loaded.get("3x3", [])
                    self.data["6x6"] = loaded.get("6x6", [])
            except Exception:
                # If file is corrupted, reset
                self.data = {"3x3": [], "6x6": []}
        else:
            self._save_data()

    def _save_data(self):
        """Write current data (times) to JSON file."""
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save data:\n{e}")

    def _build_main_page(self):
        """First page: choose 3×3, 6×6, or go to Analysis."""
        self._clear_widgets()
        self.configure(bg="#f0f0f0")

        lbl = tk.Label(
            self,
            text="Select an Option",
            font=("Arial", 28, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        )
        lbl.pack(pady=(50, 30))

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        btn_3x3 = tk.Button(
            btn_frame,
            text="3×3 Timer",
            width=20,
            height=2,
            font=("Arial", 16, "bold"),
            bg="#0066cc",
            fg="white",
            activebackground="#005bb5",
            activeforeground="white",
            relief="raised",
            bd=3,
            command=lambda: self._build_timer_page("3x3"),
        )
        btn_3x3.grid(row=0, column=0, padx=20, pady=10)

        btn_6x6 = tk.Button(
            btn_frame,
            text="6×6 Timer",
            width=20,
            height=2,
            font=("Arial", 16, "bold"),
            bg="#0066cc",
            fg="white",
            activebackground="#005bb5",
            activeforeground="white",
            relief="raised",
            bd=3,
            command=lambda: self._build_timer_page("6x6"),
        )
        btn_6x6.grid(row=0, column=1, padx=20, pady=10)

        btn_analysis = tk.Button(
            self,
            text="Analysis",
            width=20,
            height=2,
            font=("Arial", 16, "bold"),
            bg="#009933",
            fg="white",
            activebackground="#00802b",
            activeforeground="white",
            relief="raised",
            bd=3,
            command=self._build_analysis_selection_page,
        )
        btn_analysis.pack(pady=(40, 10))

    def _build_timer_page(self, size):
        """Timer page for chosen cube size. Clicking on the time display toggles timer."""
        self.cube_size = size
        self.start_time = None
        self.elapsed_time = 0.0
        self.running = False
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        self._clear_widgets()
        self.configure(bg="#ffffff")

        lbl_title = tk.Label(
            self,
            text=f"{size} Timer",
            font=("Arial", 22, "bold"),
            bg="#ffffff",
            fg="#222222",
        )
        lbl_title.pack(pady=(40, 15))

        # Time display label: extra large font
        self.time_label = tk.Label(
            self,
            text="00.00",
            font=("Arial", 72, "bold"),
            fg="#cc0000",
            bg="#ffffff",
        )
        self.time_label.pack(pady=30)

        lbl_instr = tk.Label(
            self,
            text="Tap the time above to Start/Stop\n(Records to two decimals)",
            font=("Arial", 12),
            bg="#ffffff",
            fg="#555555",
            justify="center",
        )
        lbl_instr.pack(pady=(0, 20))

        # Bind click on time_label to toggle timer
        self.time_label.bind("<Button-1>", self._toggle_timer_event)

        btn_back = tk.Button(
            self,
            text="Back",
            width=15,
            height=1,
            font=("Arial", 14),
            bg="#cccccc",
            fg="#000000",
            activebackground="#aaaaaa",
            activeforeground="#000000",
            relief="raised",
            bd=2,
            command=self._build_main_page,
        )
        btn_back.pack(side="bottom", pady=30)

    def _toggle_timer_event(self, event):
        """Event handler: toggle timer on click."""
        if not self.running:
            self._start_timer()
        else:
            self._stop_timer()

    def _start_timer(self):
        """Start or resume the timer."""
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self._update_timer_display()

    def _stop_timer(self):
        """Stop/pause the timer, then prompt to save or discard."""
        if self.running:
            if self.timer_job:
                self.after_cancel(self.timer_job)
                self.timer_job = None
            self.elapsed_time = time.time() - self.start_time
            self.running = False

            elapsed_formatted = round(self.elapsed_time, 2)

            confirm = messagebox.askyesno(
                title="Register Attempt?",
                message=f"Time recorded: {elapsed_formatted:.2f} seconds\n\nRegister this attempt?",
                icon=messagebox.QUESTION,
            )
            if confirm:
                self.data[self.cube_size].append(elapsed_formatted)
                self._save_data()
                messagebox.showinfo(
                    "Saved", f"{elapsed_formatted:.2f} s saved for {self.cube_size}."
                )
            else:
                messagebox.showinfo("Discarded", "Attempt discarded.")

            self.start_time = None
            self.elapsed_time = 0.0
            self.time_label.config(text="00.00")

    def _update_timer_display(self):
        """Update the timer label every 100 ms while running."""
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            seconds_str = f"{self.elapsed_time:.2f}"
            self.time_label.config(text=seconds_str)
            self.timer_job = self.after(100, self._update_timer_display)

    def _build_analysis_selection_page(self):
        """Page to choose cube size for analysis."""
        self._clear_widgets()
        self.configure(bg="#f0f0f0")

        lbl = tk.Label(
            self,
            text="Select Cube Size for Analysis",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        )
        lbl.pack(pady=(50, 30))

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        btn_3x3 = tk.Button(
            btn_frame,
            text="3×3 Analysis",
            width=20,
            height=2,
            font=("Arial", 16, "bold"),
            bg="#009933",
            fg="white",
            activebackground="#00802b",
            activeforeground="white",
            relief="raised",
            bd=3,
            command=lambda: self._build_analysis_page("3x3"),
        )
        btn_3x3.grid(row=0, column=0, padx=20, pady=10)

        btn_6x6 = tk.Button(
            btn_frame,
            text="6×6 Analysis",
            width=20,
            height=2,
            font=("Arial", 16, "bold"),
            bg="#009933",
            fg="white",
            activebackground="#00802b",
            activeforeground="white",
            relief="raised",
            bd=3,
            command=lambda: self._build_analysis_page("6x6"),
        )
        btn_6x6.grid(row=0, column=1, padx=20, pady=10)

        btn_back = tk.Button(
            self,
            text="Back",
            width=15,
            height=1,
            font=("Arial", 14),
            bg="#cccccc",
            fg="#000000",
            activebackground="#aaaaaa",
            activeforeground="#000000",
            relief="raised",
            bd=2,
            command=self._build_main_page,
        )
        btn_back.pack(side="bottom", pady=30)

    def _build_analysis_page(self, size):
        """Display statistics for the selected cube size."""
        self._clear_widgets()
        self.configure(bg="#ffffff")

        lbl_title = tk.Label(
            self,
            text=f"{size} Analysis",
            font=("Arial", 24, "bold"),
            bg="#ffffff",
            fg="#222222",
        )
        lbl_title.pack(pady=(40, 20))

        times = self.data.get(size, [])
        if not times:
            lbl_no_data = tk.Label(
                self,
                text="No recorded attempts yet.",
                font=("Arial", 16),
                bg="#ffffff",
                fg="#555555",
            )
            lbl_no_data.pack(pady=20)
        else:
            total_attempts = len(times)
            lifetime_avg = sum(times) / total_attempts

            last_15 = times[-15:] if total_attempts >= 15 else times[:]
            ma_15 = sum(last_15) / len(last_15)

            last_5 = times[-5:] if total_attempts >= 5 else times[:]
            ma_5 = sum(last_5) / len(last_5)

            least_time = min(times)
            max_time = max(times)

            # Determine threshold for sub solves
            if size == "3x3":
                threshold = 55.0
                sub_label = "Solves under 55 seconds"
            else:
                threshold = 300.0  # 5 minutes in seconds
                sub_label = "Solves under 5 minutes"

            sub_solves = sum(1 for t in times if t < threshold)

            stats = [
                ("Lifetime Average", lifetime_avg),
                ("Moving Avg (last 15)", ma_15),
                ("Moving Avg (last 5)", ma_5),
                ("Fastest Solve", least_time),
                ("Slowest Solve", max_time),
                ("Total Solves (lifetime)", total_attempts),
                (sub_label, sub_solves),
            ]

            stat_frame = tk.Frame(self, bg="#ffffff")
            stat_frame.pack(pady=(10, 20), fill="x", padx=50)

            for label_text, value in stats:
                if isinstance(value, float):
                    display = f"{value:.2f} seconds"
                else:
                    display = str(value)
                lbl_stat = tk.Label(
                    stat_frame,
                    text=f"{label_text}: {display}",
                    font=("Arial", 16),
                    bg="#ffffff",
                    fg="#333333",
                    anchor="w",
                )
                lbl_stat.pack(fill="x", pady=6)

        btn_back = tk.Button(
            self,
            text="Back",
            width=15,
            height=1,
            font=("Arial", 14),
            bg="#cccccc",
            fg="#000000",
            activebackground="#aaaaaa",
            activeforeground="#000000",
            relief="raised",
            bd=2,
            command=self._build_analysis_selection_page,
        )
        btn_back.pack(side="bottom", pady=30)

    def _clear_widgets(self):
        """Remove all existing widgets from the window."""
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = CubeTimerApp()
    app.mainloop()
