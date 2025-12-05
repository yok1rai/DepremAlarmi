from fetcher import fetch_earthquakes
from processor import parse_latest_quake
from alarm.sound import should_alarm
from time import sleep as sl

last_quake_id = None

while True:
    raw = fetch_earthquakes()
    quake = parse_latest_quake(raw)

    if not quake:
        print("Deprem verisi alınamadı")
        sl(5)
        continue

    if quake and quake["id"] != last_quake_id:
        if should_alarm(quake):
            print("Alarm", quake["place"], quake["magnitude"])
            last_quake_id = quake["id"]
        else:
            print(
                "Yeni deprem ama alarm eşiği altında",
                quake["place"], quake["magnitude"])

        last_quake_id = quake["id"]

    else:
        print(
            "Hala aynı deprem",
            quake["place"],
            quake["magnitude"])


    sl(5)

