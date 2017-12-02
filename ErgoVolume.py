from pynput import keyboard
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


class AudioController(object):
    def __init__(self):
        self.VOLUME_DELTA = 0.01

    def decrease_volume(self):
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                interface = session.SimpleAudioVolume

                # 0.0 is the min value, reduce by decibels
                volume = max(0.0, interface.GetMasterVolume() - self.VOLUME_DELTA)
                interface.SetMasterVolume(volume, None)
                print('Volume reduced to', volume)  # debug
        except OSError as e:
            print(e)

    def increase_volume(self):
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                interface = session.SimpleAudioVolume

                # 1.0 is the max value, raise by decibels
                volume = min(1.0, interface.GetMasterVolume() + self.VOLUME_DELTA)
                interface.SetMasterVolume(volume, None)
                print('Volume raised to', volume)  # debug
        except OSError as e:
            print(e)


# These variables describe the state of the application
super_held = False
page_up_held = False
page_down_held = False
audio_controller = AudioController()


def handle_volume_adjustment():
    """Change volume as needed using pycaw."""

    global page_down_held
    global page_up_held
    global audio_controller

    if page_up_held:
        audio_controller.increase_volume()
    if page_down_held:
        audio_controller.decrease_volume()


def on_press(key):
    global super_held
    global page_down_held
    global page_up_held

    if key is keyboard.Key.cmd:
        super_held = True
    elif key is keyboard.Key.page_up:
        page_up_held = True
    elif key is keyboard.Key.page_down:
        page_down_held = True

    if super_held:
        handle_volume_adjustment()

def on_release(key):
    global super_held
    global page_down_held
    global page_up_held

    if key is keyboard.Key.cmd:
        super_held = False
    elif key is keyboard.Key.page_up:
        page_up_held = False
    elif key is keyboard.Key.page_down:
        page_down_held = False

    # DEBUG
    if key == keyboard.Key.esc:
        # Stop listener
        return False


sessions = AudioUtilities.GetAllSessions()
# for session in sessions:
#     session._ctl.QueryInterface(ISimpleAudioVolume)


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
