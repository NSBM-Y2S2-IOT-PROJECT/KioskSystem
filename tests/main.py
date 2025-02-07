# Confirmation Needed
import cv2
import numpy as np
import libfreenect.wrappers.python.freenect as freenect

def get_video():
    """Get a frame from the Kinect's RGB camera."""
    frame, _ = freenect.sync_get_video()
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

def get_depth():
    """Get a depth frame from the Kinect's depth camera."""
    depth, _ = freenect.sync_get_depth()
    return depth

def detect_skin(frame):
    """Detect skin tone using a predefined HSV range."""
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([50, 255, 255], dtype=np.uint8)

    # Create a mask to detect skin region
    skin_mask = cv2.inRange(hsv_frame, lower_skin, upper_skin)
    skin_result = cv2.bitwise_and(frame, frame, mask=skin_mask)

    # Calculate the average skin tone
    skin_pixels = frame[skin_mask == 255]
    average_skin_tone = np.mean(skin_pixels, axis=0) if len(skin_pixels) > 0 else None

    return skin_result, skin_mask, average_skin_tone

def analyze_texture(skin_mask):
    """Analyze texture using Laplacian variance (sharpness measurement)."""
    texture_analysis = cv2.Laplacian(skin_mask, cv2.CV_64F).var()
    return texture_analysis

def apply_ir_mask(depth_frame, skin_mask):
    """Apply an IR mask based on depth data to refine skin detection."""
    # Define a threshold for depth (in mm)
    depth_threshold_min = 500  # Minimum depth (closer objects)
    depth_threshold_max = 2000  # Maximum depth (far objects)

    # Create an IR mask where depth is within the desired range
    ir_mask = np.logical_and(depth_frame > depth_threshold_min, depth_frame < depth_threshold_max)

    # Convert the IR mask to uint8 (0 or 255)
    ir_mask = (ir_mask.astype(np.uint8)) * 255

    # Apply the IR mask to the skin mask to refine the detected skin region
    combined_mask = cv2.bitwise_and(skin_mask, ir_mask)
    return combined_mask

def main():
    while True:
        frame = get_video()
        depth_frame = get_depth()  # Get depth frame

        # Detect skin
        skin_result, skin_mask, average_skin_tone = detect_skin(frame)

        # Apply IR mask to refine skin detection using depth frame
        ir_mask = apply_ir_mask(depth_frame, skin_mask)
        skin_result = cv2.bitwise_and(frame, frame, mask=ir_mask)

        # Analyze texture of the skin region
        texture_score = analyze_texture(ir_mask)

        # Display texture score
        cv2.putText(frame, f'Texture Score: {texture_score:.2f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if average_skin_tone is not None:
            average_skin_tone = average_skin_tone.astype(int)
            cv2.putText(frame, f'Skin Tone: {average_skin_tone}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Display a color swatch for the average skin tone
            swatch = np.zeros((50, 50, 3), dtype=np.uint8)
            swatch[:, :] = average_skin_tone
            frame[10:60, 10:60] = swatch

        # Show frames
        cv2.imshow('Original Frame', frame)
        cv2.imshow('Skin Detection with IR Mask', skin_result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
