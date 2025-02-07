# Confirmation Required
import libfreenect.wrappers.python.freenect as freenect
import cv2
import numpy as np

# Function to detect skin color and calculate the average skin tone in an image
def detect_skin_color_in_video():
    # Start Kinect video stream
    while True:
        # Capture color frame from Kinect
        color_frame, _ = freenect.sync_get_video()

        # Convert the frame to BGR format
        frame = cv2.cvtColor(color_frame, cv2.COLOR_RGB2BGR)

        # Convert the frame from BGR to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define lower and upper bounds for skin color in HSV space
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        # Create a binary mask where skin color is detected
        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # Apply the mask to the original frame
        skin_detected = cv2.bitwise_and(frame, frame, mask=skin_mask)

        # Calculate the average color of the detected skin region
        skin_pixels = cv2.bitwise_and(frame, frame, mask=skin_mask)
        average_skin_tone = cv2.mean(skin_pixels, mask=skin_mask)

        # Display the average skin tone on the frame
        average_color_text = f"Avg Skin Tone (BGR): {int(average_skin_tone[0])}, {int(average_skin_tone[1])}, {int(average_skin_tone[2])}"
        cv2.putText(frame, average_color_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the results
        cv2.imshow('Original Frame', frame)
        cv2.imshow('Skin Detected', skin_detected)

        # Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the OpenCV windows
    cv2.destroyAllWindows()

# Run the live skin detection
detect_skin_color_in_video()
