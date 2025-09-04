# 🖐️ Virtual Keyboard with Hand Gesture Recognition
A real-time virtual keyboard that allows users to type using hand gestures captured through a webcam. Built with OpenCV, CVZone and MediaPipe for accurate hand tracking and gesture recognition.
# ✨ Features

Real-time Hand Tracking: Uses MediaPipe for accurate hand landmark detection
Gesture-based Typing: Pinch gesture (index finger + middle finger) to select keys

# Visual Feedback:
Green highlighting for key hover
Red flash and yellow border for successful clicks
Real-time distance display for gesture debugging

Click Prevention: Smart "click-and-release" mechanism prevents continuous typing
Live Text Display: See your typed text with typewriter effect
Dual Output: Text appears both on-screen and in external applications (Notepad, etc.)
Special Keys: Space bar and backspace functionality
Responsive Design: Optimized button layout for easy interaction

# 🎯 How It Works
Point: Hover your index finger over the desired key
Pinch: Bring your index finger and middle finger close together (distance < 40 pixels)
Release: Separate fingers to reset for next character
Repeat: Continue typing with pinch-and-release gestures

# 🛠️ Installation
Prerequisites
bashPython 3.7+
Webcam
Install Dependencies
bashpip install opencv-python
pip install cvzone
pip install pyautogui
pip install mediapipe

# Controls
Hover: Point index finger at keys
Click: Pinch index and middle finger together
Space: Use the wide space bar key
Backspace: Use the "<" key to delete characters
Quit: Press 'q' key to exit

# 📊 Technical Details
Key Components
Hand Detection: CVZone HandTrackingModule with MediaPipe backend
Gesture Recognition: Distance calculation between fingertips
Visual Interface: OpenCV for real-time video processing and UI
System Integration: PyAutoGUI for external application typing

# Performance Optimizations
Single hand detection for better performance
Optimized button layout and collision detection
Smart click debouncing to prevent double-clicks
Efficient real-time video processing

# 🎨 Customization
Keyboard Layout
Modify the keys array to customize the keyboard layout:
pythonkeys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M"," ","<"]]
Gesture Sensitivity
Adjust the distance threshold for click detection:
pythondistance < 40  # Decrease for more sensitive, increase for less sensitive
Visual Styling
Customize colors and button sizes in the Button class and drawAll() function.

# 🔧 Troubleshooting
Common Issues
Hand not detected:
Ensure good lighting
Keep hand within webcam frame
Check if webcam is working properly

Clicks not registering:
Watch the distance counter (should be < 40)
Make sure pinch gesture is clear
Check console output for click events

Multiple characters typed:
Ensure you're releasing the pinch gesture
Check the click state indicator on screen


# 📞 Contact
www.linkedin.com/in/rehmatkhan59
