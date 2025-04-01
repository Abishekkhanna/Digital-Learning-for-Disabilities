import cv2
import numpy as np
import math
import os
from tkinter import Tk, Label, Button, Frame, Canvas
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

# Initialize Tkinter window
root = Tk()
root.title("Hand Gesture Recognition")
root.attributes('-fullscreen', True)  # Fullscreen mode
root.configure(bg="white")

# OpenCV setup
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

# Constants
offset = 20
imgSize = 300
labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
current_index = 0

# UI Layout
frame1 = Frame(root, width=500, height=600, bg="white", relief="solid", bd=5, highlightbackground="#FFCC00", highlightthickness=8)
frame1.place(relx=0.3, rely=0.4, anchor="center")

frame2 = Frame(root, width=500, height=600, bg="white", relief="solid", bd=5, highlightbackground="#FFCC00", highlightthickness=8)
frame2.place(relx=0.7, rely=0.4, anchor="center")

label1 = Label(frame1, bg="white")
label1.pack(fill="both", expand=True)

label2 = Label(frame2, bg="white")
label2.pack(fill="both", expand=True)

# Labels for detected text & static image info
detected_label = Label(root, text="Detected: ---", font=("Arial", 20, "bold"), fg="black", bg="white")
detected_label.place(relx=0.3, rely=0.65, anchor="center")

gesture_label = Label(root, text="Expected Letter: ---", font=("Arial", 20, "bold"), fg="black", bg="white")
gesture_label.place(relx=0.7, rely=0.65, anchor="center")

# Progress Bar
canvas = Canvas(root, width=800, height=50, bg="black", highlightthickness=2, highlightbackground="#FFCC00")
canvas.place(relx=0.5, rely=0.83, anchor="center")

progress_text = Label(root, text=f"0/{len(labels)} (0%)", font=("Arial", 20, "bold"), fg="black", bg="white")
progress_text.place(relx=0.5, rely=0.89, anchor="center")

# Exit Button
exit_button = Button(root, text="Exit", font=("Arial", 16, "bold"), command=root.quit, bg="red", fg="white", width=20, height=1)
exit_button.place(relx=0.5, rely=0.96, anchor="center")

# Function to generate large character image dynamically
def generate_character_image(character):
    img = Image.new("RGB", (400, 600), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 300)  # Adjust size if needed
    except:
        font = ImageFont.load_default()

    text_size = draw.textbbox((0, 0), character, font=font)
    text_width = text_size[2] - text_size[0]
    text_height = text_size[3] - text_size[1]

    x = (400 - text_width) // 2
    y = (600 - text_height) // 2
    draw.text((x, y), character, font=font, fill="black")

    return ImageTk.PhotoImage(img)

# Function to update the displayed letter
def update_letter_display():
    if current_index < len(labels):
        letter_img = generate_character_image(labels[current_index])
        label2.config(image=letter_img)
        label2.image = letter_img
        gesture_label.config(text=f"Expected Letter: {labels[current_index]}")

# Function to animate progress
def update_progress():
    canvas.delete("all")
    progress = (current_index / len(labels)) * 800
    canvas.create_rectangle(0, 0, progress, 50, fill="#4CAF50", outline="")

    percentage = (current_index / len(labels)) * 100
    progress_text.config(text=f"{current_index}/{len(labels)} ({int(percentage)}%)")

# Function to check completion
def check_completion():
    if current_index >= len(labels):
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

    if hands and current_index < len(labels):
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
                    label2.config(bg="#4CAF50")
                    root.after(500, lambda: label2.config(bg="white"))

                    current_index += 1
                    if current_index < len(labels):
                        update_letter_display()
                        update_progress()
                    check_completion()

            except:
                label_text = "Error in Processing"

    img = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (500, 600))
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    label1.config(image=img)
    label1.image = img

    root.after(10, update_frame)

# Start with first letter and progress bar
update_letter_display()
update_progress()

# Start updating frames
update_frame()

# Run the Tkinter main loop
root.mainloop()

cap.release()
cv2.destroyAllWindows()
