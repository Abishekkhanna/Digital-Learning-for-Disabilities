import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time  # Added for delay control

# Initialize Mediapipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Get screen size
screen_width, screen_height = pyautogui.size()

# Webcam Capture
cap = cv2.VideoCapture(0)

# Define threshold and delay for zoom
zoom_reference = None
last_zoom_time = time.time()

# Define threshold and delay for rotation
rotation_reference = None
last_rotation_time = time.time()

# Find Euclidean Distance
def find_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)  # Flip for natural interaction
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get landmark positions
            landmarks = hand_landmarks.landmark
            index_tip = (landmarks[8].x, landmarks[8].y)  # Index Finger Tip
            thumb_tip = (landmarks[4].x, landmarks[4].y)  # Thumb Tip
            pinky_tip = (landmarks[20].x, landmarks[20].y)  # Pinky Tip

            # Convert to screen coordinates
            index_x, index_y = int(index_tip[0] * screen_width), int(index_tip[1] * screen_height)

            # Calculate distances
            zoom_distance = find_distance(thumb_tip, index_tip)
            hand_spread = find_distance(index_tip, pinky_tip)

            # Move Cursor (if needed for future)
            if hand_spread > 0.15:  
                pyautogui.moveTo(index_x, index_y, duration=0.1)

            # Zoom In/Out - Adjusted Sensitivity
            if zoom_reference is None:
                zoom_reference = zoom_distance  # Set initial reference

            zoom_change = zoom_distance - zoom_reference
            current_time = time.time()

            if current_time - last_zoom_time > 0.5:  # Add delay to slow down zooming
                if zoom_change > 0.07:  # Increased threshold for smoother zoom
                    pyautogui.hotkey('ctrl', '+')  # Zoom In
                    zoom_reference = zoom_distance
                    last_zoom_time = current_time
                    cv2.putText(img, "Zoom In", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                elif zoom_change < -0.07:  
                    pyautogui.hotkey('ctrl', '-')  # Zoom Out
                    zoom_reference = zoom_distance
                    last_zoom_time = current_time
                    cv2.putText(img, "Zoom Out", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # **Map Rotation Control** (New Feature)
            if rotation_reference is None:
                rotation_reference = index_x  # Set initial hand X position

            rotation_change = index_x - rotation_reference

            if current_time - last_rotation_time > 0.5:  # Slow down rotation response
                if rotation_change > 50:  # Move right
                    pyautogui.hotkey('right')  # Simulate right arrow key
                    rotation_reference = index_x
                    last_rotation_time = current_time
                    cv2.putText(img, "Rotate Right", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                elif rotation_change < -50:  # Move left
                    pyautogui.hotkey('left')  # Simulate left arrow key
                    rotation_reference = index_x
                    last_rotation_time = current_time
                    cv2.putText(img, "Rotate Left", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Draw Landmarks
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display Camera Feed
    cv2.imshow("Gesture Mouse Control", img)

    # Exit on 'Esc' Key Press
    if cv2.waitKey(1) & 0xFF == 27:  
        break

# Release Resources
cap.release()
cv2.destroyAllWindows()
