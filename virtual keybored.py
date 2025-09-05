import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Keyboard layout
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", " ", "<"]]  

# Variables for text and click handling
typed_text = ""
last_click_time = 0
click_delay = 0.3  # Delay between clicks
button_clicked = False  # Track if button was clicked
clicked_button = None  # Store which button was clicked
green_button = None  # Store button to be drawn green
green_button_time = 0  # Time when button turned green
green_duration = 0.2  # Duration to keep button green


# Button class
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == " ":  
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key, [170, 85]))
        elif key == "<":  
            buttonList.append(Button([100 * j + 50 + 170, 100 * i + 50], key, [85, 85]))
        else:
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        # by clicking button should be green
        if button == green_button and time.time() - green_button_time < green_duration:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
        else:
            # purple color for buttons
            cv2.rectangle(img, (x, y), (x + w, y + h), (175, 0, 175), cv2.FILLED)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            
        if button.text == " ":
            cv2.putText(img, "SPACE", (x + 30, y + 45),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        elif button.text == "<":
            cv2.putText(img, "BACK", (x + 15, y + 45),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        else:
            cv2.putText(img, button.text, (x + 25, y + 55),
                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


def drawTextArea(img, text):
    cv2.rectangle(img, (50, 400), (1230, 470), (175, 0, 175), cv2.FILLED)
    cv2.rectangle(img, (50, 400), (1230, 470), (255, 255, 255), 3)
    cv2.putText(img, "Typed Text:", (60, 390), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # Display text 
    display_text = text
    if len(display_text) > 60: 
        display_text = "..." + display_text[-57:]

    cv2.putText(img, display_text, (60, 440), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    # Blinking cursor
    if int(time.time() * 2) % 2:
        cursor_x = 60 + len(display_text) * 18
        cv2.putText(img, "|", (cursor_x, 440), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    return img


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror the image
    hands, img = detector.findHands(img)
    img = drawAll(img, buttonList)
    img = drawTextArea(img, typed_text)

    if hands:
        # Get hand landmarks
        hand = hands[0]
        lmList = hand['lmList']

        # Get index finger tip position
        indexFinger = lmList[8]
        x, y = indexFinger[0], indexFinger[1]

        # Draw finger position
        cv2.circle(img, (x, y), 12, (255, 0, 255), cv2.FILLED)

        # Check which button is being hovered
        hovered_button = None
        for button in buttonList:
            bx, by = button.pos
            bw, bh = button.size

            if bx < x < bx + bw and by < y < by + bh:
                hovered_button = button

                # Darker purple when hovering (pointing at key)
                cv2.rectangle(img, (bx, by), (bx + bw, by + bh), (120, 0, 120), cv2.FILLED)

                # Display button text
                if button.text == " ":
                    cv2.putText(img, "SPACE", (bx + 30, by + 45),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                elif button.text == "<":
                    cv2.putText(img, "BACK", (bx + 15, by + 45),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                else:
                    cv2.putText(img, button.text, (bx + 25, by + 55),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                break

        # Check for pinch gesture (click detection)
        if hovered_button:
            # Calculate distance between index finger and thumb
            indexTip = lmList[8][:2]
            thumbTip = lmList[4][:2]

            # Use the correct findDistance method without draw parameter
            distance, _, img = detector.findDistance(indexTip, thumbTip, img)

            current_time = time.time()

            # Detect click (pinch gesture)
            if distance < 50:  # Fingers close together
                if not button_clicked and current_time - last_click_time > click_delay:
                    # Register the click
                    button_clicked = True
                    clicked_button = hovered_button
                    last_click_time = current_time

                    # Set button to turn green for visual feedback
                    green_button = hovered_button
                    green_button_time = current_time

                    # Process the button press
                    if hovered_button.text == " ":
                        typed_text += " "
                        pyautogui.press('space')
                    elif hovered_button.text == "<":
                        if typed_text:
                            typed_text = typed_text[:-1]
                            pyautogui.press('backspace')
                    else:
                        typed_text += hovered_button.text.lower()
                        pyautogui.write(hovered_button.text.lower())

                    print(f"Clicked: {hovered_button.text}")
            else:
                # Fingers are apart, reset click state
                button_clicked = False

    # Instructions
    cv2.putText(img, "Virtual Keyboard - Pinch (thumb + index) to click", (50, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(img, "Press 'q' to quit", (50, 680),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
