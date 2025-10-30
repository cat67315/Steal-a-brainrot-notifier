import time
import mss
from PIL import Image
import pytesseract
import tempfile
import os
import pyttsx3

screen = 1  # Change this to the screen where roblox is (1, 2, etc.) If you only have one screen, leave it as 1. If unsure open the "Display Settings" in Windows then click Identify wich will show what monitor is what number.

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"


def speak(text: str) -> None:
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    try:
        engine.stop()
    except Exception:
        pass

interval = 3  # seconds

# Load keywords
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f if line.strip()]


with mss.mss() as sct:
    monitor = sct.monitors[screen]  # What screen to capture
    while True:
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

        # Save screenshot as a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img.save(tmp.name)
            # Pass the file path to pytesseract
            text = pytesseract.image_to_string(tmp.name)
        os.remove(tmp.name)  # Delete the temporary file

        # Look for keywords
        found = [word for word in keywords if word.lower() in text.lower()]
        if found:
            message = ", ".join(found)
            print("Found:", message)
            speak("Found " + message) # Speak the brainrots found


        time.sleep(interval)