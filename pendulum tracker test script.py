import cv2
import numpy as np

def track_pendulum():
    # Open a video capture object (0 represents the default camera)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the frame to HSV (Hue, Saturation, Value) color space
        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Define the range for the orange color
        lower_orange = np.array([200, 200, 200])
        upper_orange = np.array([255, 255, 255])

        # lower_orange = np.array([130, 160, 220])
        # upper_orange = np.array([140, 170, 230])

        # lower_orange = np.array([220, 160, 130])
        # upper_orange = np.array([230, 170, 140])


        # Create a mask using the specified color range
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If any contours are found
        if contours:
            # Find the contour with the maximum area
            max_contour = max(contours, key=cv2.contourArea)

            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(max_contour)

            # Draw a rectangle around the detected region
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Pendulum Tracking', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    cap.release()

    # Destroy all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_pendulum()
