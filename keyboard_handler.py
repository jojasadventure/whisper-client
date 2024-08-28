from pynput import keyboard

class KeyboardHandler:
    def __init__(self, app):
        self.app = app
        self.current = set()
        self.listener = None

    def setup_listener(self):
        self.RECORD_COMBINATION = self.parse_hotkey(self.app.ui.record_hotkey_var.get())
        self.LANGUAGE_COMBINATION = self.parse_hotkey(self.app.ui.language_hotkey_var.get())
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        print("Debug: Keyboard listener setup complete")

    def parse_hotkey(self, hotkey_str):
        keys = hotkey_str.split('+')
        parsed_keys = set()
        for key in keys:
            key = key.strip().lower()
            if key == 'cmd':
                parsed_keys.add(keyboard.Key.cmd)
            elif key == 'ctrl':
                parsed_keys.add(keyboard.Key.ctrl)
            elif len(key) == 1:
                parsed_keys.add(keyboard.KeyCode.from_char(key))
        return parsed_keys

    def on_press(self, key):
        self.current.add(key)
        if all(k in self.current for k in self.RECORD_COMBINATION):
            print("Debug: Record hotkey combination pressed")
            self.app.master.after(0, self.app.toggle_recording)
        elif all(k in self.current for k in self.LANGUAGE_COMBINATION):
            print("Debug: Language toggle hotkey combination pressed")
            self.app.master.after(0, self.app.toggle_language)

    def on_release(self, key):
        try:
            self.current.remove(key)
        except KeyError:
            pass

    def update_hotkeys(self):
        self.RECORD_COMBINATION = self.parse_hotkey(self.app.ui.record_hotkey_var.get())
        self.LANGUAGE_COMBINATION = self.parse_hotkey(self.app.ui.language_hotkey_var.get())
        print("Debug: Hotkeys updated")