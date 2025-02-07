import libfreenect.wrappers.python.freenect as freenect
import cv2
import numpy as np
import mediapipe as mp

# Initialize Mediapipe Hand Tracker
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize Kinect
def get_kinect_depth_and_rgb():
    depth, _ = freenect.sync_get_depth()  # Depth image
    rgb, _ = freenect.sync_get_video()  # RGB image
    return depth, rgb

# Process the RGB image for hand tracking
def track_hands_in_rgb(rgb_image):
    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    results = hands.process(rgb_image)
    hand_landmarks = []
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(rgb_image, landmarks, mp_hands.HAND_CONNECTIONS)
            # Extract hand landmarks
            hand_landmarks.append(landmarks)
    return rgb_image, hand_landmarks

# Convert 2D hand landmarks to 3D positions using depth information
def get_3d_hand_positions(hand_landmarks, depth_image):
    height, width = depth_image.shape
    hand_positions_3d = []
    for landmarks in hand_landmarks:
        for lm in landmarks.landmark:
            # Convert landmark position from normalized coordinates to pixel coordinates
            x, y = int(lm.x * width), int(lm.y * height)
            # Get depth value at (x, y) pixel position
            depth_value = depth_image[y, x]  # depth value is typically in millimeters
            hand_positions_3d.append((x, y, depth_value))
    return hand_positions_3d

# Visualize the hand positions on the depth image
def visualize_hand_positions_on_depth(depth_image, hand_positions_3d):
    for (x, y, depth_value) in hand_positions_3d:
        # Draw circles on the depth image where the hand landmarks are detected
        cv2.circle(depth_image, (x, y), 5, (0, 255, 0), -1)
        cv2.putText(depth_image, f'{depth_value}mm', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return depth_image

# Main loop
def main():
    while True:
        # Get the depth and RGB data from Kinect
        depth, rgb = get_kinect_depth_and_rgb()
        
        # Process RGB image for hand tracking
        tracked_rgb_image, hand_landmarks = track_hands_in_rgb(rgb)
        
        # Get the 3D hand positions based on the depth image
        hand_positions_3d = get_3d_hand_positions(hand_landmarks, depth)
        
        # Convert depth to a color map to visualize it
        depth_color_map = cv2.applyColorMap(depth.astype(np.uint8), cv2.COLORMAP_JET)
        
        # Visualize hand positions on the depth image
        depth_with_hand_positions = visualize_hand_positions_on_depth(depth_color_map, hand_positions_3d)
        
        # Show the images
        cv2.imshow('RGB Image with Hand Tracking', tracked_rgb_image)
        cv2.imshow('Kinect Depth Image with Hand Positions', depth_with_hand_positions)
        
        # Exit on 'ESC' key press
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
