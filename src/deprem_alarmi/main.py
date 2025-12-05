from pathlib import Path

from fetcher import fetch_earthquakes
from processor import parse_latest_quake
from alarm.alarm import handle
from alarm.sound import load
from storage.sqlite import init_db, save_quake, quake_exists
import tkinter as tk

def main():
    app = EarthqQuakeApp()
    app.mainloop()

class EarthqQuakeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Pencere ---
        self.title("Deprem uygulaması")
        self.geometry("1200x450")
        self.resizable(True, False)

        # --- DB ---
        init_db()

        # --- ses ---
        base_dir = Path(__file__).resolve().parents[2]
        sound_path = base_dir / "assets" / "sounds" / "anons.wav"
        load("alarm", sound_path, channel_id=0)

        # --- Değişken ---
        self.running = False

        # --- Frame'ler ---

        self._configure_grid()
        self._create_widgets()

    def _configure_grid(self):
        for col in range(4):
            self.columnconfigure(col, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def _create_widgets(self):
        self.ControlPanel = ControlPanel(self)
        self.ControlPanel.grid(
            row=0,
            column=0,
            columnspan=4,
            rowspan=1,
            sticky="ew",
            padx=5,
            pady=5)

        self.Location_Frame = LocationFrame(self)
        self.Location_Frame.grid(row=1, column=0, sticky="nsew", padx=5)

        self.Magnitude_Frame = MagnitudeFrame(self)
        self.Magnitude_Frame.grid(row=1, column=1, sticky="nsew", padx=5)

        self.Status_Frame = StatusFrame(self)
        self.Status_Frame.grid(row=1, column=2, sticky="nsew", padx=5)

        self.Alarm_Frame = AlarmFrame(self)
        self.Alarm_Frame.grid(row=1, column=3, sticky="nsew", padx=5)

    def start_monitoring(self):
        if self.running:
            return

        self.running = True
        self.ControlPanel.startBtn.config(state="disabled")
        self.ControlPanel.stopBtn.config(state="normal")
        self.ControlPanel.statusLabel.config(text="Aktif")


    def stop_monitoring(self):
        if not self.running:
            return

        self.running = False
        self.ControlPanel.startBtn.config(state="normal")
        self.ControlPanel.stopBtn.config(state="disabled")
        self.ControlPanel.statusLabel.config(text="Beklemede")

class ControlPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self._configure_grid()
        self._create_widgets()

    def _configure_grid(self):
        for col in range(4):
            self.columnconfigure(col, weight=1)

    def _create_widgets(self):
        self.welcome = tk.Label(self, text="Deprem Alarmı Uygulaması!", font=("Arial", 16))
        self.welcome.grid(
                        row=0,
                        column=0,
                        columnspan=4,
                        )

        self.startBtn = tk.Button(self, text="Başlat", font=("Arial", 14), command=self.parent.start_monitoring)
        self.startBtn.grid(
                        row=1,
                        column=0,
                        sticky="ew",
                        padx=5
        )

        self.stopBtn = tk.Button(self, text="Durdur", font=("Arial", 14), state="disabled", command=self.parent.stop_monitoring)
        self.stopBtn.grid(
                        row=1,
                        column=1,
                        sticky="ew",
                        padx=5
        )
        self.clearBtn = tk.Button(self, text="Temizle", font=("Arial", 14), state="disabled")
        self.clearBtn.grid(
                        row=1,
                        column=2,
                        sticky="ew",
                        padx=5
        )

        self.statusLabel = tk.Label(self, text="Beklemede", font=("Arial", 14), bd=2, relief="raised", padx=12, pady=6, bg="#F0F0F0")
        self.statusLabel.grid(
            row=1,
            column=3,
            sticky="ew",
            padx=5
        )

class LocationFrame(tk.Frame):
    pass

class MagnitudeFrame(tk.Frame):
    pass

class StatusFrame(tk.Frame):
    pass

class AlarmFrame(tk.Frame):
    pass



if __name__ == "__main__":
    main()
