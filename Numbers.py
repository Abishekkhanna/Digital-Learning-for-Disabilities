import cv2
import numpy as np
import math
import tkinter as tk
from tkinter import Label, ttk
from PIL import Image, ImageTk
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

# Load the gesture recognition model
classifier = Classifier(r"D:\computer vision\numbers\Model\keras_model.h5", 
                        r"D:\computer vision\numbers\Model\labels.txt")

# Constants
offset = 20
imgSize = 300
labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
current_index = 0  # Track the current number (0 to 9)

# Initialize Camera
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

# Tkinter GUI
root = tk.Tk()
root.title("Gesture Recognition")
root.attributes('-fullscreen', True)  # Make it full screen

# Border Frame
border_frame = tk.Frame(root, bg="#303030", bd=15, relief="ridge")
border_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Content Frame (Inside Border)
content_frame = tk.Frame(border_frame, bg="white")
content_frame.pack(expand=True, fill="both")

# Camera Label (Left Side)
camera_label = Label(content_frame, bg="black")
camera_label.grid(row=0, column=0, padx=120, pady=40)

# Static Image Label (Right Side)
static_image_label = Label(content_frame, bg="black")
static_image_label.grid(row=0, column=1, padx=120, pady=40)

# Progress Bar
progress = ttk.Progressbar(content_frame, length=500, mode='determinate', maximum=100)
progress.grid(row=1, column=0, columnspan=2, pady=10)

# Status Label
status_label = Label(content_frame, text="Progress: 0%", font=("Arial", 16), fg="white", bg="black")
status_label.grid(row=2, column=0, columnspan=2, pady=10)

# Exit Function
def exit_app():
    """Closes the camera and exits the program safely."""
    global cap
    print("Exiting application...")
    cap.release()
    root.destroy()

# Button Frame
button_frame = tk.Frame(content_frame, bg="black")
button_frame.grid(row=3, column=0, columnspan=2, pady=20)

# Exit Button (Styled)
exit_button = tk.Button(button_frame, text="Exit", command=exit_app, bg="red", fg="white",
                        font=("Arial", 14, "bold"), width=15, height=2)
exit_button.pack()

# Function to update the UI
def update_ui():
    global current_index

    success, img = cap.read()
    if not success:
        print("Error: Camera feed not detected!")
        return

    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        if imgCrop.shape[0] > 0 and imgCrop.shape[1] > 0:
            aspectRatio = h / w
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

            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                          (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y - 26), 
                        cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (255, 0, 255), 4)

            # Check if the detected number matches the current reference image
            if labels[index] == str(current_index + 1):
                print(f"Matched: {labels[index]} (Current: {current_index+1})")
                current_index += 1
                progress["value"] = (current_index / 10) * 100
                status_label.config(text=f"Progress: {current_index * 10}%")

                # Exit only when we reach 10
                if current_index == 10:
                    print("🎉 All gestures matched! Exiting...")
                    root.after(1000, exit_app)  # Wait 1 second before exiting

    # Convert OpenCV image to Tkinter format
    imgRGB = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
    imgRGB = cv2.resize(imgRGB, (450, 450))
    imgTk = ImageTk.PhotoImage(Image.fromarray(imgRGB))
    camera_label.imgTk = imgTk
    camera_label.config(image=imgTk)

    # Load and display the static image
    static_img_path = f"D:/computer vision/numbers/num_img/{current_index+1}.jpg"
    try:
        static_img = Image.open(static_img_path).resize((450, 450))
        static_imgTk = ImageTk.PhotoImage(static_img)
        static_image_label.imgTk = static_imgTk
        static_image_label.config(image=static_imgTk)
    except Exception as e:
        print(f"Error loading static image: {e}")

    root.after(50, update_ui)

# Start UI Update
update_ui()

# Run Tkinter Main Loop
root.mainloop()
