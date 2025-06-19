This repository provides a real-time system for counting people using YOLOv8 and OpenCV. The solution leverages YOLOv8 — a cutting-edge object detection model — to identify people in both images and videos. Additionally, a custom class is included for people detection without depending on YOLOv8. You can use other yolo versions according to ultralytics documentations. If you are using a web camara, please set cap=cv2.VideoCapture(0).

Overview
This project aims to detect and count people in real-time from images or video streams. YOLOv8 (short for "You Only Look Once, version 8") is an advanced object detection model capable of recognizing multiple objects within an image simultaneously. The system integrates YOLOv8 with OpenCV for live, real-time detection.

Installation
To get started with the system:

1. Clone the repository using git clone

2. Set up your environment and install the dependencies (a virtual environment is recommended):
-python -m venv venv
-source venv/bin/activate # On Windows: venv\Scripts\activate

3.Then install the necessary packages:
-ultralytics
-opencv
-cvzone

Running the Application
Start the people counting system with this command:

python counting.py

By default, this will activate your webcam, process the live feed, and display the results in real-time — including bounding boxes around detected individuals and an on-screen count.

Controls
Press 'Esc' to exit the application.
