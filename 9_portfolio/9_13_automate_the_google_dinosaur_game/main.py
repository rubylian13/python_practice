import pyautogui
import time
from PIL import ImageGrab
import webbrowser

class DinoGameBot:
    """
    Write Python code to play the Google Dinosaur Game.
    """
    def __init__(self):
        webbrowser.open("https://elgoog.im/t-rex/")
        time.sleep(5)
        pyautogui.press("space")
        time.sleep(0.5)
        # box = (left, top, right, bottom)
        self.box = (400, 360, 500, 450)

    def dino_bot(self):
        print("開始自動玩！")
        while True:
            screen = ImageGrab.grab(bbox=self.box)
            gray = screen.convert("L")
            pixels = gray.getdata()

            if min(pixels) < 100:  # 前方出現黑色障礙物
                pyautogui.press("space")

            time.sleep(0.01)

if __name__ == "__main__":
    game = DinoGameBot()
    game.dino_bot()
