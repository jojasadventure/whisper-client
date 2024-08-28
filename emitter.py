import pyperclip # type: ignore
import pyautogui # type: ignore

class Emitter:
    def __init__(self):
        self.output_method = self.clipboard_output
        self.should_paste = True

    def emit(self, text):
        self.output_method(text)

    def set_output_method(self, method):
        self.output_method = method

    def set_should_paste(self, should_paste):
        self.should_paste = should_paste

    def clipboard_output(self, text):
        pyperclip.copy(text)
        print(f"Debug: Copied to clipboard: {text}")
        if self.should_paste:
            pyautogui.hotkey('command', 'v')
            print("Debug: Pasted from clipboard")
        else:
            print("Debug: Text copied to clipboard but not pasted (paste disabled)")

    # Example of how to add a new output method
    def console_output(self, text):
        print(f"Console Output: {text}")

    # You can add more output methods here in the future
    # def file_output(self, text):
    #     with open('output.txt', 'a') as f:
    #         f.write(text + '\n')
    #     print(f"Debug: Written to file: {text}")

    # def network_output(self, text):
    #     # Send text to a network destination
    #     pass