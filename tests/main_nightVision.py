# Working
import libfreenect.wrappers.python.freenect as freenect
import cv2
import numpy as np

def get_ir_frame():
    """Fetch an infrared frame from the Kinect."""
    frame, _ = freenect.sync_get_video(format=freenect.VIDEO_IR_8BIT)
    return frame

def main():
    """Main loop to display the Kinect's infrared feed."""
    cv2.namedWindow('Kinect v1 Night Vision Test', cv2.WINDOW_AUTOSIZE)

    while True:
        # Get the IR frame
        ir_frame = get_ir_frame()

        # Convert frame to grayscale (optional: apply colormap for better visualization)
        ir_colored = cv2.applyColorMap(ir_frame, cv2.COLORMAP_JET)

        # Show the IR frame
        cv2.imshow('Kinect v1 Night Vision Test', ir_colored)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cv2.destroyAllWindows()
    freenect.sync_stop()

if __name__ == "__main__":
    main()
