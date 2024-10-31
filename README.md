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

TBD

### FINGERS

TBD

