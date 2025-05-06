import fetch
import image_processor
import numpy as np  
import cv2
import pyautogui
import time 
import keyboard
from pynput.keyboard import Key, Listener

time.sleep(5)
image = fetch.get_current_status()
x_coords, y_coords, widths, heights= image_processor.detect_boxes_and_lines("image1.png", "white.png")



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
        return (smaller_x + smaller_w / 2, smaller_y + smaller_h / 2)

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
            if midpoint is not None:  # Only append valid midpoints
                final.append((i, j, midpoint))

    return final


results = compare_all_rectangles(x_coords, y_coords, widths, heights)

# Print the results
continue_execution = True
pause_loop = False

def on_press(key):
    global continue_execution, pause_loop
    
    if key == Key.enter:
        print("Continuing to next rectangle...")
        pause_loop = False  # Resume the loop
    elif key == Key.esc:
        print("Exiting program...")
        continue_execution = False  # Stop everything
        return False  # This stops the listener

# Start the keyboard listener in non-blocking mode
listener = Listener(on_press=on_press)
listener.start()

for i, j, (mid_x, mid_y) in results:
    if not continue_execution:
        break
        
    # Move to adjusted position
    pyautogui.moveTo(mid_x - 2, mid_y - 6, duration=0.1)
    print(f"Moved to Rectangles {i} & {j} at ({mid_x-2:.1f}, {mid_y-6:.1f})")
    print("Press ENTER to continue or ESC to quit")
    
    # Pause until Enter is pressed
    pause_loop = True
    while pause_loop and continue_execution:
        pass  # Busy wait (minimal CPU usage)

# Clean up
listener.stop()

    

print(x_coords)
print(y_coords)









print("done")

"""
need to customize framsize, 
and exit key and aauto close window
turning off?



"""