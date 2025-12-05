from fetcher import fetch_earthquakes
from processor import parse_latest_quake
from alarm.alarm import handle
from alarm.sound import load
from time import sleep as sl

load("alarm", r"assets\sounds\anons.wav", channel_id=0)

last_quake_id = None

print("Deprem alarmı başlatıldı..\n")

while True:
    raw = fetch_earthquakes()
    quake = parse_latest_quake(raw)

    if not quake:
        print("Deprem verisi alınamadı")
        handle(None)
        sl(5)
        continue

    if quake["id"] != last_quake_id:
        print(
            "Yeni deprem",
            quake["place"],
            quake["magnitude"]
        )

        handle(quake)
        last_quake_id = quake["id"]

    else:
        print(
            "Hala aynı deprem",
            quake["place"],
            quake["magnitude"]
        )

    sl(5)

