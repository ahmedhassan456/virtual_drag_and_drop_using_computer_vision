import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np
import math

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.3, maxHands=1)
colorR = (255, 0, 255)

cx, cy, w, h = 100, 100, 200, 200


class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter[0], self.posCenter[1]
        w, h = self.size

        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and \
                cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor


rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    lmList, img = detector.findHands(img)

    if lmList:
        cursor = lmList[0]['lmList'][4]
        cursor2 = lmList[0]['lmList'][8]
        l = math.hypot(cursor2[0]-cursor[0], cursor2[1]-cursor[1])

        cv2.circle(img, (cursor[0], cursor[1]), 15, (0,255,0), cv2.FILLED)
        cv2.circle(img, (cursor2[0], cursor2[1]), 15, (0,255,0), cv2.FILLED)

        print(l)
        if l < 40:
            for rect in rectList:
                rect.update(cursor)


    ## Draw Transperency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter[0], rect.posCenter[1]
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 30, rt=3)

    out = img.copy()
    alpha = 0.5
    out = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)

    cv2.imshow("Image", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()