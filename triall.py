import pyautogui

# Dictionary mapping keys to rectangle pairs and their midpoints
midpoints = {
    '1': (1366.5, 909.0),   # Rectangles 0 & 2
    '2': (1271.0, 1013.0),  # Rectangles 0 & 3
    '3': (1367.0, 857.5),   # Rectangles 0 & 4
    '4': (1367.0, 539.5),   # Rectangles 0 & 5
    '5': (1271.0, 907.0),   # Rectangles 1 & 3
    '6': (1367.0, 804.5),   # Rectangles 1 & 4
    '7': (1367.0, 486.5),   # Rectangles 1 & 5
    '8': (1271.0, 805.0),   # Rectangles 2 & 3
    '9': (1366.5, 435.5),   # Rectangles 2 & 5
    '0': (1271.0, 702.5),   # Rectangles 3 & 4
    'q': (780.5, 394.5),    # Rectangles 3 & 5
    'w': (1367.0, 384.5)    # Rectangles 4 & 5
}

print("Key Mapping:")
print("1: Rectangles 0 & 2 | 2: 0 & 3 | 3: 0 & 4 | 4: 0 & 5")
print("5: Rectangles 1 & 3 | 6: 1 & 4 | 7: 1 & 5 | 8: 2 & 3")
print("9: Rectangles 2 & 5 | 0: 3 & 4 | q: 3 & 5 | w: 4 & 5")
print("\nPress a key (0-9, q, w) to move, or 'c' to quit...")

while True:
    user_input = input("> ").lower()
    print("your mom")
    if user_input == 'c':
        print("Exiting...")
        break
    elif user_input in midpoints:
        x, y = midpoints[user_input]
        pyautogui.moveTo(x-2, y-6, duration=0.5)
    else:
        print("Invalid key. Press 0-9/q/w or 'c' to quit.")






