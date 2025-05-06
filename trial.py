from pynput.keyboard import Key, Listener
import pyautogui

coordinates = {
    '1': (1366.5, 909.0),
    '2': (1271.0, 1013.0),
    'c': None  # Quit
}

def on_press(key):
    try:
        key_char = key.char
    except AttributeError:
        return  # Ignore non-character keys

    if key_char == 'c':
        print("Exiting...")
        return False  # Stop listener
    elif key_char in coordinates:
        x, y = coordinates[key_char]
        pyautogui.moveTo(x, y, duration=0.5)
        print(f"Moved to ({x}, {y})")

print("Press 1/2 or 'c' to quit...")
with Listener(on_press=on_press) as listener:
    listener.join()