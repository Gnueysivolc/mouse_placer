import fetch
import image_processor
import numpy as np  
import cv2
import pyautogui
import time 
import sys
import tty
import termios
import os
import sys



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Load your image like this:
image_path = resource_path("white.png")
dis1 = cv2.imread(image_path)



time.sleep(5)
image = fetch.get_current_status()
x_coords, y_coords, widths, heights= image_processor.detect_boxes_and_lines("image1.png", dis1)



def compare_rectangles(x1, y1, w1, h1, x2, y2, w2, h2):
    x1_end, y1_end = x1 + w1, y1 + h1
    x2_end, y2_end = x2 + w2, y2 + h2

    if x1_end < x2:
        x_pos = "left"
    elif x1 > x2_end:
        x_pos = "right"
    else:
        x_pos = "overlap_x"

    if y1_end < y2:
        y_pos = "above"
    elif y1 > y2_end:
        y_pos = "below"
    else:
        y_pos = "overlap_y"

    if x_pos == "overlap_x" and y_pos == "overlap_y":
        return "overlap"
    else:
        return f"{y_pos} and {x_pos}" if y_pos != x_pos else y_pos
    


def calculate_midpoint(x1, y1, w1, h1, x2, y2, w2, h2, relationship):
    """Calculate midpoint only if the closest distance between rects >= 50."""
    # Calculate closest distance
    x_dist = max(x1, x2) - min(x1 + w1, x2 + w2) if x1 + w1 < x2 or x2 + w2 < x1 else 0
    y_dist = max(y1, y2) - min(y1 + h1, y2 + h2) if y1 + h1 < y2 or y2 + h2 < y1 else 0
    closest_distance = max(x_dist, y_dist)  # Minimum separation

    if closest_distance < 20:
        return None  # Skip if too close

    area1 = w1 * h1
    area2 = w2 * h2
    smaller_x, smaller_y, smaller_w, smaller_h = (x1, y1, w1, h1) if area1 < area2 else (x2, y2, w2, h2)

    if "above" in relationship or "below" in relationship:
        mid_x = smaller_x + smaller_w / 2
        y_top = max(y1, y2)
        y_bottom = min(y1 + h1, y2 + h2)
        mid_y = (y_top + y_bottom) / 2
        return (mid_x, mid_y)
    elif "left" in relationship or "right" in relationship:
        mid_y = smaller_y + smaller_h / 2
        x_left = max(x1, x2)
        x_right = min(x1 + w1, x2 + w2)
        mid_x = (x_left + x_right) / 2
        return (mid_x, mid_y)
    else:  # Overlapping
        return (0, 0)

def compare_all_rectangles(x_coords, y_coords, widths, heights):
    n = len(x_coords)
    final = []

    print("Starting comparison...")

    for i in range(n):

        print(f"Comparing rectangle {i} with others...")

        for j in range(i + 1, n):
            
            print(f"Comparing with rectangle {j}...")

            x1, y1, w1, h1 = x_coords[i], y_coords[i], widths[i], heights[i]
            x2, y2, w2, h2 = x_coords[j], y_coords[j], widths[j], heights[j]
            
            relationship = compare_rectangles(x1, y1, w1, h1, x2, y2, w2, h2)
            midpoint = calculate_midpoint(x1, y1, w1, h1, x2, y2, w2, h2, relationship)
            if midpoint == (0, 0):  # Skip this j if midpoint is (0,0)
                continue
            if midpoint is not None:  # Only append valid midpoints
                final.append((i, j, midpoint))

    return final


results = compare_all_rectangles(x_coords, y_coords, widths, heights)


# Control flags
def get_key():
    """Get single key press without Enter (Unix/Mac compatible)"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

print("Press ENTER to move to next coordinate, 'o' to exit")
for i, j, (mid_x, mid_y) in results:
    # Move to adjusted position
    pyautogui.moveTo(mid_x-2, mid_y-6, duration=0.1)
    print(f"Moved to rectangle pair {i}-{j} at ({mid_x-2:.1f}, {mid_y-6:.1f})")
    
    # Wait for key press
    print("Waiting for input (ENTER=continue, o=exit)...")
    while True:
        key = get_key()
        if key == '\r':  # ENTER pressed
            print("Continuing...")
            break
        elif key.lower() == 'o':
            print("Exiting program")
            sys.exit(0)
        # Add slight delay to prevent CPU overload
        time.sleep(0.1)






print(x_coords)
print(y_coords)









print("done")

"""
need to customize framsize, 
and exit key and aauto close window
turning off?



"""