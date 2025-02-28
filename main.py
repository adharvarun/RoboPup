# Importing libraries
import requests
import tensorflow as tf
import cv2
import http.client
import numpy as np
import time
import mediapipe as mp

# Robot's Host Configuration
host = '192.168.91.20'
port = 80

# Set motor speeds
requests.get(f'http://{host}/?cmd=lb_speed=220')
requests.get(f'http://{host}/?cmd=rb_speed=220')
requests.get(f'http://{host}/?cmd=lf_speed=220')
requests.get(f'http://{host}/?cmd=rf_speed=220')

def send_re_httpquest(host, port, path):
    """ Sends an HTTP GET request with retries. """
    retries = 10
    for _ in range(retries):
        conn = None
        try:
            conn = http.client.HTTPConnection(host, port)
            conn.request("GET", path)
            response = conn.getresponse()
            return response.read().decode("utf-8")
        except Exception as e:
            print(f"Error: {e}, retrying... ({_+1}/{retries})")
            time.sleep(1)
        finally:
            if conn:
                conn.close()
    return None  # If all retries fail

def custom_hand_detection():
    """ Detects hand gestures and controls the robot. """
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    # Define robot movements
    def excited_hop():
        commands = ["/?cmd=f(500)", "/?cmd=b(500)", "/?cmd=f(500)", "/?cmd=b(500)"]
        for cmd in commands:
            send_re_httpquest(host, port, cmd)

    def twister():
        commands = ["/?cmd=l(1000)", "/?cmd=f(1000)", "/?cmd=r(1000)"]
        for cmd in commands:
            send_re_httpquest(host, port, cmd)

    # Start video stream
    cap = cv2.VideoCapture(0)  # Adjust IP if needed

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: No frame received.")
            break

        # Convert the frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for hand detection
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Thumb gesture detection
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
                # Index finger gesture detection
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]

                if index_tip.y < index_dip.y:  # Index finger up gesture
                    print("Index Finger Up - Move Forward!")
                    send_re_httpquest(host, port, "/?cmd=f(1000)")
                else:  # Index finger down gesture
                    print("Index Finger Down - Move Backward!")
                    send_re_httpquest(host, port, "/?cmd=b(1000)")

                # Hand pointing left or right detection
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

                if pinky_tip.x < wrist.x:  # Hand pointing left
                    print("Hand Pointing Left - Move Left!")
                    send_re_httpquest(host, port, "/?cmd=l(1000)")
                elif pinky_tip.x > wrist.x:  # Hand pointing right
                    print("Hand Pointing Right - Move Right!")
                    send_re_httpquest(host, port, "/?cmd=r(1000)")

                if thumb_tip.y < thumb_ip.y:  # Thumb-up gesture
                    print("Thumbs Up - Excited Hop!")
                    excited_hop()
                else:
                    print("Thumbs Down - Twister!")
                    twister()

        # Display the frame
        cv2.imshow("Robotic Dog by Team 17/57", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

# Run the script
if __name__ == "__main__":
    custom_hand_detection()