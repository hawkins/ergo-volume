from pynput import keyboard
from pycaw.pycaw import AudioUtilities


class AudioController(object):
    def __init__(self):
        self.VOLUME_DELTA = 0.1
        self.super_held = False
        self.page_down_held = False
        self.page_up_held = False

    def on_press(self, key):
        if key is keyboard.Key.cmd:
            self.super_held = True
        elif key is keyboard.Key.page_up:
            self.page_up_held = True
        elif key is keyboard.Key.page_down:
            self.page_down_held = True

        if self.super_held:
            self.handle_volume_adjustment()

    def on_release(self, key):
        if key is keyboard.Key.cmd:
            self.super_held = False
        elif key is keyboard.Key.page_up:
            self.page_up_held = False
        elif key is keyboard.Key.page_down:
            self.page_down_held = False

        # # DEBUG
        # if key == keyboard.Key.esc:
        #     # Stop listener
        #     return False

    def handle_volume_adjustment(self):
        """Change volume as needed using pycaw."""

        if self.page_up_held:
            self.increase_volume()
        if self.page_down_held:
            self.decrease_volume()

    def decrease_volume(self):
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                interface = session.SimpleAudioVolume

                # 0.0 is the min value, reduce by decibels
                volume = max(0.0, interface.GetMasterVolume() -
                             self.VOLUME_DELTA)
                interface.SetMasterVolume(volume, None)
        except OSError as e:
            print(e)

    def increase_volume(self):
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                interface = session.SimpleAudioVolume

                # 1.0 is the max value, raise by decibels
                volume = min(1.0, interface.GetMasterVolume() +
                             self.VOLUME_DELTA)
                interface.SetMasterVolume(volume, None)
        except OSError as e:
            print(e)



# For some unknown reason, this must be called once before enterring
# listener.join() to prevent a CoInitialize related OSError
sessions = AudioUtilities.GetAllSessions()

# The audio controller will manage program volume levels
audio_controller = AudioController()

# Collect events until released
with keyboard.Listener(
        on_press=audio_controller.on_press,
        on_release=audio_controller.on_release) as listener:
    listener.join()
