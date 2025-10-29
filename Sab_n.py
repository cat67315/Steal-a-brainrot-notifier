import time
import mss
from PIL import Image
import pytesseract
import tempfile
import os
import pyttsx3

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"


def speak(text: str) -> None:
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    try:
        engine.stop()
    except Exception:
        # best-effort cleanup; ignore if driver already closed
        pass

interval = 3  # seconds

# Load keywords from file
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f if line.strip()]


with mss.mss() as sct:
    monitor = sct.monitors[1]  # full screen
    while True:
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

        # Save screenshot to a temporary PNG file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img.save(tmp.name)
            # Pass the file path to pytesseract
            text = pytesseract.image_to_string(tmp.name)
        os.remove(tmp.name)  # cleanup

        # Filter for keywords
        found = [word for word in keywords if word.lower() in text.lower()]
        if found:
            message = ", ".join(found)
            print("Found:", message)
            # speak using a short-lived engine to avoid driver/state issues
            speak("Found " + message)


        time.sleep(interval)
