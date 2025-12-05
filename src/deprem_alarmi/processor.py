def parse_latest_quake(raw):
    features = raw.get("features", [])
    if not features:
        return None

    quake = features[0]


    props = quake["properties"]
    coords = quake["geometry"]["coordinates"]

    return {
        "id"       : quake["id"],
        "magnitude": props["mag"],
        "place"    : props["place"],
        "time"     : props["time"],
        "lat"      : coords[1],
        "lon"      : coords[0],
        "depth"    : coords[2]
    }
