import cv2
import numpy as np

def detect_boxes_and_lines(image_path, display):
    # 1. Load the image

    ima1 = cv2.imread(image_path)
    dis1 = cv2.imread(display)




    image = cv2.resize(ima1, (1709, 1106))
    display = cv2.resize(dis1, (1709, 1106))
    if image is None:
        print("Error: Image not found!")
        return
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gamma = 0.2  # >1 makes image darker
    darker = np.uint8(255 * (gray/255) ** (1/gamma))

    cv2.imshow("grayed", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow("darker", darker)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 2. Preprocess (blur + edge detection)
    blur = cv2.GaussianBlur(darker, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    cv2.imshow("blur and edged", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]  # Simplify hierarchy array

    # Group contours based on hierarchy
    x_coords = []
    y_coords = []
    widths = []
    heights = []

    # Define minimum size thresholds (adjust as needed)
    MIN_WIDTH = 50  # Minimum width to keep
    MIN_HEIGHT = 50  # Minimum height to keep

    for i, contour in enumerate(contours):
        if hierarchy[i][3] == -1:  # Top-level parent contour
            x, y, w, h = cv2.boundingRect(contour)
        
        # Only store if both width and height meet minimum requirements
            if w*h >= 7500:
                x_coords.append(x)
                y_coords.append(y)
                widths.append(w)
                heights.append(h)
                cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw parent box



    cv2.imshow("lines", display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return x_coords, y_coords, widths, heights

    



# Run the detector
"""
detect_boxes_and_lines("yt.png", "white.png")
detect_boxes_and_lines("wb.png", "white.png")
detect_boxes_and_lines("ok.png", "white.png")
"""