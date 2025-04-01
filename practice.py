import cv2
import numpy as np
import math
import os
from tkinter import Tk, Label, Button, Frame, Canvas
from PIL import Image, ImageTk
import time
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

# Set root directory
ROOT_DIR = os.getcwd()

# Initialize Tkinter window
root = Tk()
root.title("Hand Gesture Recognition")
root.attributes('-fullscreen', True)  # Open in fullscreen
root.configure(bg="white")

# OpenCV setup
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

# Load classifier
classifier = Classifier(r"E:\MRCE hack\Django Project\learning_platform\Model\keras_model.h5", 
                        r"E:\MRCE hack\Django Project\learning_platform\Model\labels.txt")

# Constants
offset = 20
imgSize = 300
labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Folder containing alphabet images
image_dir = os.path.join(ROOT_DIR, "Images")
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(".jpg")])
total_chars = len(image_files)
current_index = 0

# UI Layout - Moved lower to center vertically
frame1 = Frame(root, width=400, height=500, bg="white", relief="solid", bd=5, highlightbackground="#FFCC00", highlightthickness=8)
frame1.place(relx=0.3, rely=0.4, anchor="center")  # Lowered from 0.3 to 0.4

frame2 = Frame(root, width=400, height=500, bg="white", relief="solid", bd=5, highlightbackground="#FFCC00", highlightthickness=8)
frame2.place(relx=0.7, rely=0.4, anchor="center")  # Lowered from 0.3 to 0.4

label1 = Label(frame1, bg="white")
label1.pack(expand=True, fill="both")

label2 = Label(frame2, bg="white", relief="solid", bd=5)
label2.pack(expand=True, fill="both")

# Labels for detected text & static image info
detected_label = Label(root, text="Detected: ---", font=("Arial", 18, "bold"), fg="black", bg="white")
detected_label.place(relx=0.3, rely=0.6, anchor="center")  # Adjusted down

gesture_label = Label(root, text="Gesture Image: ---", font=("Arial", 18, "bold"), fg="black", bg="white")
gesture_label.place(relx=0.7, rely=0.6, anchor="center")  # Adjusted down

# Progress Bar - Lowered for better centering
canvas = Canvas(root, width=600, height=40, bg="#DDDDDD", highlightthickness=0)
canvas.place(relx=0.5, rely=0.75, anchor="center")  # Lowered from 0.65 to 0.7

progress_text = Label(root, text=f"0/{total_chars} (0%)", font=("Arial", 18, "bold"), fg="black", bg="white")
progress_text.place(relx=0.5, rely=0.82, anchor="center")  # Lowered from 0.7 to 0.75

# Exit Button - Moved slightly lower
exit_button = Button(root, text="Exit", font=("Arial", 14, "bold"), command=root.quit, bg="red", fg="white", width=15)
exit_button.place(relx=0.5, rely=0.90, anchor="center")  # Lowered from 0.8 to 0.85

# Function to update static image
def update_static_image():
    if current_index < total_chars:
        image_path = os.path.join(image_dir, image_files[current_index])
        right_img = Image.open(image_path).resize((350, 500))
        right_img = ImageTk.PhotoImage(right_img)
        label2.config(image=right_img)
        label2.image = right_img

        gesture_character = os.path.splitext(image_files[current_index])[0]
        gesture_label.config(text=f"Gesture Image: {gesture_character}")

# Function to update progress
def update_progress():
    canvas.delete("all")
    progress = (current_index / total_chars) * 600
    canvas.create_rectangle(0, 0, progress, 40, fill="#4CAF50", outline="")

    percentage = (current_index / total_chars) * 100
    progress_text.config(text=f"{current_index}/{total_chars} ({int(percentage)}%)")

# Function to close application when done
def check_completion():
    if current_index >= total_chars:
        time.sleep(1)
        root.quit()

# Function to process hand gestures
def update_frame():
    global current_index

    success, img = cap.read()
    if not success:
        root.after(10, update_frame)
        return

    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    label_text = "No Hand Detected"
    highlight_color = "#FF5733"

    if hands and current_index < total_chars:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        y1, y2 = max(0, y - offset), min(img.shape[0], y + h + offset)
        x1, x2 = max(0, x - offset), min(img.shape[1], x + w + offset)

        imgCrop = img[y1:y2, x1:x2]
        if imgCrop.size != 0:
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            aspectRatio = h / w

            try:
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                detected_letter = labels[index]
                label_text = f"Detected: {detected_letter}"

                detected_label.config(text=f"Detected: {detected_letter}")

                if detected_letter == labels[current_index]:
                    highlight_color = "#4CAF50"
                    label2.config(bg="#4CAF50")
                    root.after(500, lambda: label2.config(bg="white"))

                    current_index += 1
                    if current_index < total_chars:
                        update_static_image()
                        update_progress()
                    check_completion()

            except:
                label_text = "Error in Processing"

    img = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (400, 500))
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    label1.config(image=img)
    label1.image = img

    root.after(10, update_frame)

# Start with first static image and progress bar
update_static_image()
update_progress()

# Start updating frames
update_frame()

# Run the Tkinter main loop
root.mainloop()

cap.release()
cv2.destroyAllWindows()





