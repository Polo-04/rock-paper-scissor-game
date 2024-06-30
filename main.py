import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random  # Import the random module

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set the width of the webcam feed
cap.set(4, 480)  # Set the height of the webcam feed

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]
initialTime = None  # Initialize the initialTime variable

while True:
    imgBG = cv2.imread("Resources/BG.png")  # Read the background image
    success, img = cap.read()  # Capture a frame from the webcam

    if not success:
        break  # If the frame was not successfully captured, exit the loop

    # Resize the captured frame
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)

    # Crop the resized image to the correct dimensions
    imgScaled = imgScaled[0:420, 0:400]  # This ensures imgScaled has shape (420, 400, 3)

    # Find Hands
    hands, imgScaled = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Scissors

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI Wins
                    elif (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

                    print(playerMove)

    # Insert the scaled image into the background image
    imgBG[233:653, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Display the scores
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # Display the images
    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    # Break the loop when 'q' key is pressed
    if key == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
