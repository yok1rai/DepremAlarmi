# Hatalı olabilir artık çalışmıyor

from pathlib import Path
from time import sleep as sl

from deprem_alarmi.fetcher import fetch_earthquakes
from deprem_alarmi.processor import parse_latest_quake
from deprem_alarmi.alarm.alarm import handle
from deprem_alarmi.alarm.sound import load
from deprem_alarmi.storage.sqlite import init_db, save_quake, quake_exists


def main():
    # --- DB ---
    init_db()

    # --- ses ---

    BASE_DIR = Path(__file__).resolve().parents[2]
    sound_path = BASE_DIR / "assets" / "sounds" / "anons.wav"

    load("alarm", sound_path, channel_id=0)

    # --- olay ---

    print("Deprem alarmı başlatıldı..\n")

    while True:
        raw = fetch_earthquakes()
        quake = parse_latest_quake(raw)

        if not quake:
            print("Deprem verisi alınamadı")
            sl(5)
            continue

        if not quake_exists(quake["id"]):
            print(
                "Yeni deprem",
                quake["place"],
                quake["magnitude"]
            )

            save_quake(quake)
            handle(quake)

        else:
            print(
                "Aynı deprem",
                quake["place"],
                quake["magnitude"]
            )

        sl(5)

if __name__ == "__main__":
    main()
