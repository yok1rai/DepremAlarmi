import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

pygame.mixer.init()

_sounds = {}
_channels = {}

def load(name, path, channel_id=None):
    _sounds[name] = pygame.mixer.Sound(path)
    if channel_id is not None:
        _channels[name] = pygame.mixer.Channel(channel_id)

def play(name, loop=False, volume=1.0, force=False, loops=None):
    if name not in _sounds:
        raise ValueError(f"Ses '{name}' yüklenmemiş")

    sound = _sounds[name]
    sound.set_volume(volume)

    channel = _channels.get(name)

    # loops parametresi varsa onu kullan
    if loops is not None:
        play_loops = loops
    else:
        play_loops = -1 if loop else 0

    if channel:
        if force or not channel.get_busy():
            channel.play(sound, loops=play_loops)
    else:
        sound.play(loops=play_loops)


def stop(name):
    if name in _channels:
        _channels[name].stop()
    elif name in _sounds:
        _sounds[name].stop()

