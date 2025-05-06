import numpy as np
import cv2
import pyautogui


def get_current_status():
    image1 = pyautogui.screenshot()
    image1.save("image1.png")
    imagebruh = cv2.imread("image1.png")
    return imagebruh


