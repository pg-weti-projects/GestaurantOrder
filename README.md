# GestaurantOrder

**This application implements a gesture-based system for ordering food in a restaurant environment. 
It allows users to navigate through the menu, select items, and place an order using hand gestures, 
eliminating the need for traditional input devices such as keyboards or touchscreens.**


## RUN
1. Create venv in repository root directory, activate it and install requirements from **requirements.txt** file.
2. Copy .env.example to repository root directory, fill it with proper values and change file name to **'.env'**.
3. From root repository directory run:
```shell
python app/app.py
```

## AVAILABLE OPTIONS
    F1 - Toggle main app preview

    F2 - Toggle Admin Panel preview

    F3 - Toggle camera preview

    F4 - Toggle help window


## GESTURE APP CONTROL

The application includes several gestures detected by the camera with which you cna control the application. These are:

- Thumb_Up
- Thumb_Down
- Open_Palm
- Closed_Fist
- Fingers number 0 - 10

When the app starts, the live camera reads the gestures that user shows in front of the camera. Then, the gestures are
interpreted by the application and a specific action assigned to a given gesture is performed in a given application window.

### MEDIAPIPE

The MediaPipe library is used for advanced gesture recognition. It leverages a pre-trained gesture recognition 
model, which is loaded when the application initializes. The **GestureDetector** class manages gesture detection through 
the MediaPipe’s GestureRecognizer, which processes each frame captured from the camera. This allows the application 
to identify various gestures with high accuracy and confidence levels, using data like hand landmarks, handedness
to recognize specific user inputs.

### FINGERS

The **FingersDetector** class is responsible for detecting the number of fingers shown by the user and interpreting 
the state of the hands (open or closed). It supports both single and dual-hand detection, calculating the number of 
extended fingers on each hand. This data can be used to trigger specific actions within the app:

_Finger count (0–10)_   – Indicates the selection number for menu items within the app.

_Closed hand (0)_   – Used to cancel the order.

