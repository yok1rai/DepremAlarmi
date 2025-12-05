def should_alarm(quake, threshold=4.5):
    if quake is None:
        return False
    return quake["magnitude"] >= threshold
