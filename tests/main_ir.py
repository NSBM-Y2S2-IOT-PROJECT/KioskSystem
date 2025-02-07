# Working
import cv2
import numpy as np
import libfreenect.wrappers.python.freenect as freenect

def get_ir():
    """Get a frame from the Kinect's IR camera."""
    ir_frame, _ = freenect.sync_get_depth()
    # Convert depth frame to an 8-bit grayscale image for easier processing
    ir_frame = np.uint8(ir_frame / np.max(ir_frame) * 255)
    return ir_frame

def detect_skin_ir(frame):
    """Detect regions in the IR frame based on intensity thresholds."""
    # Define intensity range for skin detection in the IR frame
    lower_intensity = 100
    upper_intensity = 200

    # Create a mask to detect skin-like regions
    skin_mask = cv2.inRange(frame, lower_intensity, upper_intensity)
    skin_result = cv2.bitwise_and(frame, frame, mask=skin_mask)

    return skin_result, skin_mask

def analyze_texture(skin_mask):
    """Analyze texture using Laplacian variance (sharpness measurement)."""
    texture_analysis = cv2.Laplacian(skin_mask, cv2.CV_64F).var()
    return texture_analysis

def main():
    while True:
        frame = get_ir()
        skin_result, skin_mask = detect_skin_ir(frame)
        texture_score = analyze_texture(skin_mask)

        cv2.putText(frame, f'Texture Score: {texture_score:.2f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('IR Frame', frame)
        cv2.imshow('Skin Detection (IR)', skin_result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
