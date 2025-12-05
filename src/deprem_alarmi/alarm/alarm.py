from alarm.sound import play, stop
from alarm.rules import should_alarm

_alarm_active = False

def handle(quake):
    global _alarm_active

    if not quake:
        if _alarm_active:
            stop("alarm")
            _alarm_active = False
        return

    if should_alarm(quake):
        if not _alarm_active:
            play("alarm", loop=True)
            _alarm_active = True

    else:
        if _alarm_active:
            stop("alarm")
            _alarm_active = False
