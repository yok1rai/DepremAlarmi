from pathlib import Path

from fetcher import fetch_earthquakes
from processor import parse_latest_quake
from alarm.alarm import handle
from alarm.sound import load, stop
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

        # --- Değişkenler ---

        self.ALARM_THRESHOLD = 4.0
        self.alarm_active = False
        self.last_quake_id = None
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

        val = self.ControlPanel.mag_var.get()
        if val:
            self.ALARM_THRESHOLD = float(val)
        else:
            self.ALARM_THRESHOLD = 4

        self.running = True
        self.ControlPanel.startBtn.config(state="disabled")
        self.ControlPanel.stopBtn.config(state="normal")
        self.ControlPanel.statusLabel.config(text="Aktif")

        self._loop()


    def stop_monitoring(self):
        if not self.running:
            return

        self.alarm_active = False
        self.running = False
        self.last_quake_id = None

        stop("alarm")

        self.ControlPanel.startBtn.config(state="normal")
        self.ControlPanel.stopBtn.config(state="disabled")
        self.ControlPanel.statusLabel.config(text="Beklemede")

    def _loop(self):
        if not self.running:
            return

        raw = fetch_earthquakes()
        quake = parse_latest_quake(raw)

        if quake:
            print(quake["place"], quake["magnitude"])

            place = quake["place"]
            quake_id = quake["id"]
            mag = quake["magnitude"]

            self.Location_Frame.add(place)
            self.Magnitude_Frame.add(mag)

            if not quake_exists(quake["id"]):
                self.Status_Frame.add("Yeni deprem")
                save_quake(quake)
                if mag >= self.ALARM_THRESHOLD and not self.alarm_active:
                    self.Alarm_Frame.add("Alarm çalıyor")
                    self.alarm_active = True

                    handle(quake)
                else:
                    self.alarm_active = False
                    self.Alarm_Frame.add("Alarm pasif")

                self.last_quake_id = quake_id
            else:
                self.Status_Frame.add("Aynı deprem")
                self.Alarm_Frame.add("Alarm pasif")

        self.after(5000, self._loop)

class ControlPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.mag_var = tk.StringVar()

        self._configure_grid()
        self._create_widgets()

    def _configure_grid(self):
        for col in range(4):
            self.columnconfigure(col, weight=1)

    def _on_keypress_mag(self, event):
        if event.keysym == "BackSpace":
            return

        if (event.state & 0x4) and event.keysym.lower() == "v":
            return "break"

        current = self.mag_var.get()
        ch = event.char

        if ch.isdigit():
            return

        if ch == ".":
            if current == "":
                return "break"
            if "." in current:
                return "break"
            return

        return "break"

    def _add_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.config(fg="grey")

        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg="black")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, text)
                entry.config(fg="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)


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

        self.enterMag = tk.Entry(self, justify="center", width=20, font=("Arial", 14),textvariable=self.mag_var)
        self.enterMag.bind("<KeyPress>", self._on_keypress_mag)
        self.enterMag.grid(
                        row=1,
                        column=2,
                        sticky="ew",
                        padx=5
        )
        self._add_placeholder(self.enterMag, "Büyüklüğü gir")

        self.statusLabel = tk.Label(self, text="Beklemede", font=("Arial", 14), bd=2, relief="raised", padx=12, pady=6, bg="#F0F0F0")
        self.statusLabel.grid(
            row=1,
            column=3,
            sticky="ew",
            padx=5
        )

class LocationFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        title = tk.Label(self, text="Konum", font=("Arial", 11, "bold"))
        title.grid(row=0, column=0, padx=5, pady=(4,0))

        self.listbox = tk.Listbox(self, height=10)
        self.listbox.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
        )

    def add(self, value):
        if self.listbox.size() >= 10:
            self.listbox.delete(0, tk.END)

        self.listbox.insert(tk.END, value)
        self.listbox.yview_moveto(1)



class MagnitudeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        title = tk.Label(self, text="Büyüklük", font=("Arial", 11, "bold"))
        title.grid(row=0, column=0, padx=5, pady=(4,0))

        self.listbox = tk.Listbox(self, height=10)
        self.listbox.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
        )

    def add(self, value):
        if self.listbox.size() >= 10:
            self.listbox.delete(0, tk.END)

        self.listbox.insert(tk.END, value)
        self.listbox.yview_moveto(1)


class StatusFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        title = tk.Label(self, text="Durum", font=("Arial", 11, "bold"))
        title.grid(row=0, column=0, padx=5, pady=(4,0))

        self.listbox = tk.Listbox(self, height=10)
        self.listbox.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
        )

    def add(self, value):
        if self.listbox.size() >= 10:
            self.listbox.delete(0, tk.END)

        self.listbox.insert(tk.END, value)
        self.listbox.yview_moveto(1)


class AlarmFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        title = tk.Label(self, text="Alarm Durumu", font=("Arial", 11, "bold"))
        title.grid(row=0, column=0, padx=5, pady=(4,0))

        self.listbox = tk.Listbox(self, height=10)
        self.listbox.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
        )

    def add(self, value):
        if self.listbox.size() >= 10:
            self.listbox.delete(0, tk.END)

        self.listbox.insert(tk.END, value)
        self.listbox.yview_moveto(1)




if __name__ == "__main__":
    main()
