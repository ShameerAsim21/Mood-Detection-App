import streamlit as st
import cv2
from deepface import DeepFace
import pygame
import os
import time

# Initialize session state
if "run_on_save" not in st.session_state:
    st.session_state.run_on_save = False
if "show_thank_you" not in st.session_state:
    st.session_state.show_thank_you = False

# Initialize Pygame mixer
pygame.mixer.init()

# Map moods to music
music_dict = {
    'happy': 'music/happy.mp3',
    'sad': 'music/sad.mp3',
    'angry': 'music/angry.mp3',
    'neutral': 'music/neutral.mp3'
}

# Emotion grouping
emotion_map = {
    'happy': 'happy',
    'sad': 'sad',
    'disgust': 'sad',
    'fear': 'sad',
    'angry': 'angry',
    'neutral': 'neutral',
    'surprise': 'neutral'
}

# Emotion stability tracking
last_emotion = None
current_emotion = None
stable_count = 0
stable_threshold = 2
confidence_threshold = 15  # %age of confidence

def play_music(emotion):
    music_file = music_dict.get(emotion)
    if music_file and os.path.exists(music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        st.toast(f"🎵 Playing: {emotion.capitalize()} music")

# Setup
st.set_page_config("Real-Time Mood Detector", layout="centered")
st.title("Real-Time Mood Detector")

frame_placeholder = st.empty()
emotion_placeholder = st.empty()
instruction_placeholder = st.empty()

if st.button("▶️ Start Detection"):
    st.session_state.run_on_save = True
    st.session_state.show_thank_you = False

# Stop detection by pressing "q"
stop_input = st.text_input("Type 'q' and press Enter to stop detection")

if stop_input.strip().lower() == 'q':
    st.session_state.run_on_save = False
    pygame.mixer.music.stop()
    st.session_state.show_thank_you = True

# Loop
if st.session_state.run_on_save:
    cap = cv2.VideoCapture(0)
    
    while st.session_state.run_on_save:
        ret, frame = cap.read()
        if not ret:
            st.error("Webcam not accessible.")
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

            if not result or 'region' not in result[0]:
                emotion_placeholder.warning("No face detected.")
                pygame.mixer.music.stop()  
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, channels="RGB")
                continue

            region = result[0]['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']

            # Rectangle on face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            detected = result[0]['dominant_emotion'].lower()
            confidence = result[0]['emotion'][detected]

            if confidence < confidence_threshold:
                continue

            mapped_emotion = emotion_map.get(detected, 'neutral')

            if mapped_emotion == current_emotion:
                stable_count += 1
            else:
                current_emotion = mapped_emotion
                stable_count = 1

            if stable_count >= stable_threshold and current_emotion != last_emotion:
                last_emotion = current_emotion
                pygame.mixer.music.stop()
                play_music(current_emotion)

            emotion_placeholder.markdown(
                f"### 🔁 Detected Emotion: **{current_emotion.capitalize()}** (Confidence: {confidence:.1f}%)"
            )

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB")

        except Exception as e:
            emotion_placeholder.warning(f"Detection error: {e}")
            pygame.mixer.music.stop()  
        time.sleep(0.5)

    cap.release()
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    frame_placeholder.empty()
    emotion_placeholder.empty()
    instruction_placeholder.empty()

# Thank-you screen
if st.session_state.show_thank_you:
    st.markdown(
        """
        <div style='text-align: center; padding: 100px 0; font-size: 50px; color: red;'>
            😊 Thank You for Using the Real-Time Mood Detector App!
        </div>
        """,
        unsafe_allow_html=True
    )

# run using: streamlit run mood_app.py

