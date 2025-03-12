import cv2
import pytesseract


def analyze_videos():
    video_path = "nhl_game.mp4"
    cap = cv2.VideoCapture(video_path)
    scores = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Extract text using Tesseract OCR
        text = pytesseract.image_to_string(gray)
        if "Goal" in text or "Score" in text:
            scores.append(text)

    cap.release()
    return {"video_analysis": scores}
