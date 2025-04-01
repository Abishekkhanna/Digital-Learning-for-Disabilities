import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
import textwrap

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

# Define MCQ class
class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

# Load MCQs from CSV
pathCSV = "Mcqs.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

mcqList = [MCQ(q) for q in dataAll]
qNo = 0
qTotal = len(dataAll)
showScore = False

# Button Animation State
buttonClicked = False
clickedTime = 0
clickedButton = None

cv2.namedWindow("Quiz", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Quiz", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if qNo < qTotal:
        mcq = mcqList[qNo]

        # Wrap text for long questions
        wrapped_text = textwrap.wrap(mcq.question, width=40)
        y_offset = 100
        for line in wrapped_text:
            img, _ = cvzone.putTextRect(img, line, [100, y_offset], 2, 2, offset=30, colorR=(0, 0, 0))
            y_offset += 50

        # Answer choices
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=40, border=4, colorR=(0, 255, 0))
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=40, border=4, colorR=(0, 255, 0))
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=40, border=4, colorR=(0, 255, 0))
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=40, border=4, colorR=(0, 255, 0))

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, _, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)

            if length < 35:
                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                if mcq.userAns is not None:
                    time.sleep(0.3)
                    qNo += 1
    else:
        if not showScore:
            correct = sum(1 for mcq in mcqList if mcq.answer == mcq.userAns)
            incorrect = qTotal - correct
            score = round((correct / qTotal) * 100, 2)
            showScore = True

        img, _ = cvzone.putTextRect(img, f"QUIZ COMPLETED!  Your Score: {score}%", [400, 200], 2.5, 2, offset=50, border=5, colorR=(255, 50, 50))

        # Buttons
        img, bboxScore = cvzone.putTextRect(img, "View Score", [400, 350], 2, 2, offset=50, border=5, colorR=(50, 255, 50))
        img, bboxExit = cvzone.putTextRect(img, "Exit", [750, 350], 2, 2, offset=50, border=5, colorR=(255, 0, 0))

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, _, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)

            # Score Button
            x1, y1, x2, y2 = bboxScore
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2 and length < 35:
                img, _ = cvzone.putTextRect(img, f'Correct: {correct}', [400, 450], 2, 2, offset=50, border=5, colorR=(255, 255, 0))
                img, _ = cvzone.putTextRect(img, f'Incorrect: {incorrect}', [750, 450], 2, 2, offset=50, border=5, colorR=(255, 255, 0))
                time.sleep(1)

            # Exit Button
            x1, y1, x2, y2 = bboxExit
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2 and length < 35:
                break

    # Progress Bar
    barValue = 150 + (950 // qTotal) * qNo
    cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
    img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16, colorR=(0, 255, 255))

    cv2.imshow("Quiz", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
