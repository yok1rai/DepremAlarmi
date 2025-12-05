from alarm.sound import play
from alarm.rules import should_alarm

_last_quake_id = None

def handle(quake):
    global _last_quake_id

    if not quake:
        return

    # Aynı deprem için tekrar alarm verme
    if quake["id"] == _last_quake_id:
        return

    if should_alarm(quake):
        # 3 kez çal -> loops=2
        play("alarm", volume=1.0, force=True, loops=2)
        _last_quake_id = quake["id"]
