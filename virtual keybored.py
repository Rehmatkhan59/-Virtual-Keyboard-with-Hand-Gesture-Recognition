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

# Keyboard layout (rows of keys)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M", " ", "<"]]  

# Variables for text display and typing effect
typed_text = ""
display_text = ""
last_click_time = 0
click_delay = 0.5  # Delay between clicks to avoid multiple registrations
typing_speed = 0.05  # Speed for typing effect
last_type_time = 0


# Draw keyboard
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + w, y + h), (175, 0, 175), cv2.FILLED)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # Special handling for space and backspace
        if button.text == " ":
            cv2.putText(img, "SPACE", (x + 10, y + 45),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        elif button.text == "<":
            cv2.putText(img, "BACK", (x + 15, y + 45),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        else:
            cv2.putText(img, button.text, (x + 25, y + 55),
                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


# Draw text display area
def drawTextArea(img, text):
    # Create text display area
    cv2.rectangle(img, (50, 450), (1230, 550), (50, 50, 50), cv2.FILLED)
    cv2.rectangle(img, (50, 450), (1230, 550), (255, 255, 255), 3)

    # Add title
    cv2.putText(img, "Typed Text:", (60, 440), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # Display text with word wrapping
    words = text.split(' ')
    lines = []
    current_line = ""
    max_chars_per_line = 30 

    for word in words:
        if len(current_line + word) < max_chars_per_line:
            current_line += word + " "
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    # Display lines (show only last 3 lines to fit in the area)
    display_lines = lines[-3:] if len(lines) > 3 else lines

    for i, line in enumerate(display_lines):
        y_pos = 480 + (i * 25)
        cv2.putText(img, line, (60, y_pos), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # Add cursor effect
    if len(display_lines) > 0:
        last_line = display_lines[-1]
        cursor_x = 60 + len(last_line) * 12
        cursor_y = 480 + (len(display_lines) - 1) * 25
        if int(time.time() * 2) % 2:  # Blinking cursor
            cv2.putText(img, "|", (cursor_x, cursor_y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    return img


# Button class
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


# Create buttons
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == " ":  # Space bar 
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key, [170, 85]))
        else:
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


# Typing effect function
def update_display_text():
    global display_text, typed_text, last_type_time
    current_time = time.time()

    if len(display_text) < len(typed_text) and current_time - last_type_time > typing_speed:
        display_text += typed_text[len(display_text)]
        last_type_time = current_time


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror image
    hands, img = detector.findHands(img)

    # Update typing effect
    update_display_text()

    img = drawAll(img, buttonList)
    img = drawTextArea(img, display_text)

    if hands:
        lmList = hands[0]['lmList']  # List of landmarks
        indexFinger = lmList[8]  # Index finger tip
        x, y = indexFinger[0], indexFinger[1]

        # Draw finger position
        cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)

        for button in buttonList:
            bx, by = button.pos
            bw, bh = button.size

            if bx < x < bx + bw and by < y < by + bh:
                # Highlight hovered button
                cv2.rectangle(img, (bx, by), (bx + bw, by + bh), (0, 255, 0), cv2.FILLED)

                # Special handling for space and backspace display
                if button.text == " ":
                    cv2.putText(img, "SPACE", (bx + 10, by + 45),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                elif button.text == "<":
                    cv2.putText(img, "BACK", (bx + 15, by + 45),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                else:
                    cv2.putText(img, button.text, (bx + 25, by + 55),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                # Detect "click" (distance between index tip and middle tip)
                # Extract only x, y coordinates (ignore z coordinate)
                indexTip = [lmList[8][0], lmList[8][1]]
                middleTip = [lmList[12][0], lmList[12][1]]
                l, _, _ = detector.findDistance(indexTip, middleTip, img)

                current_time = time.time()
                if l < 30 and current_time - last_click_time > click_delay:  # Made distance smaller for easier clicking
                    # Visual feedback for click
                    cv2.rectangle(img, (bx, by), (bx + bw, by + bh), (0, 0, 255), cv2.FILLED)

                    if button.text == " ":
                        cv2.putText(img, "SPACE", (bx + 10, by + 45),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                        typed_text += " "
                        pyautogui.press('space')
                    elif button.text == "<":
                        cv2.putText(img, "BACK", (bx + 15, by + 45),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                        if typed_text:
                            typed_text = typed_text[:-1]
                        pyautogui.press('backspace')
                    else:
                        cv2.putText(img, button.text, (bx + 25, by + 55),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        typed_text += button.text.lower()
                        pyautogui.write(button.text.lower())

                    last_click_time = current_time
                    print(f"Clicked: {button.text}, Text now: '{typed_text}'")  # Debug print

    # Instructions for user
    cv2.putText(img, "Virtual Keyboard - Point and pinch to type", (50, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(img, "Bring index and middle finger close together to click", (50, 630),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (200, 200, 200), 2)
    cv2.putText(img, "Press 'q' to quit", (50, 600),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
