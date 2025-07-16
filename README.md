README FILE

--------------------------------

Real-Time Mood Detector App

Description:
This Streamlit app uses a webcam and DeepFace to detect the user's real-time emotion and plays music based on the detected mood. It supports basic emotions like happy, sad, angry, and neutral, and responds accordingly with music and visual feedback.

--------------------------------
--------------------------------

Features:
- Detects real-time facial emotion using webcam.
- Maps emotion to a suitable music track.
- Draws a bounding box around the detected face.
- Shows live video feed and detected emotion with confidence.
- Includes a thank-you screen upon stopping.
- Handles no-face and low-confidence scenarios.
- Groups similar emotions (e.g., "disgust", "fear" → "sad").

----------------------------
----------------------------

Requirements:
- Python 3.7+
- Libraries:
  - streamlit
  - opencv-python
  - deepface
  - pygame

--------------------------------
--------------------------------

Install required packages:
   pip install streamlit opencv-python deepface pygame

--------------------------------
--------------------------------
How to Run:
streamlit run mood_app.py

--------------------------------
--------------------------------

Usage Instructions:
1. Click on “▶️ Start Detection”.
2. Allow webcam access.
3. The app will analyze your facial expression and play matching music.
4. To stop detection, type `q` in the text input and press Enter.
5. A thank-you message will be displayed.

--------------------------------
--------------------------------
Notes:
- If no face is detected, the music stops.
- If detected emotion changes and is stable for a short duration, music updates accordingly.
- The app avoids switching tracks frequently using emotion stability logic.

------------------------------
------------------------------
Made By: Muhammad Shameer Asim
