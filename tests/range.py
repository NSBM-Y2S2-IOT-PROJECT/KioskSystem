import libfreenect.wrappers.python.freenect as freenect
import cv2
import numpy as np

# Function to get depth data from the Kinect
def get_depth():
    return freenect.sync_get_depth()[0]

# Function to process the depth data and filter pixels within the range [100mm, 300mm]
def process_depth(depth_data):
    # Convert depth data to millimeters
    depth_mm = depth_data * 0.124987  # Convert from raw depth to millimeters

    # Create a mask for pixels within the range [50mm, 100mm]
    mask = np.logical_and(depth_mm >= 50, depth_mm <= 100)

    # Create an output image where only the pixels within the range are shown
    output = np.zeros_like(depth_mm)
    output[mask] = 255  # Set pixels within the range to white (255)

    return output, mask, depth_mm

# Function to calculate the centroid and average depth of the masked region
def calculate_centroid_and_depth(mask, depth_mm):
    # Find the coordinates of the non-zero pixels in the mask
    y_coords, x_coords = np.nonzero(mask)

    if len(x_coords) == 0 or len(y_coords) == 0:
        return None, None  # No pixels in the range

    # Calculate the centroid (average of x and y coordinates)
    centroid_x = int(np.mean(x_coords))
    centroid_y = int(np.mean(y_coords))

    # Calculate the average depth of the masked region
    average_depth = np.mean(depth_mm[mask])

    return (centroid_x, centroid_y), average_depth

# Main loop
def main():
    while True:
        # Get depth data
        depth_data = get_depth()

        # Process depth data to show only pixels within the range [50mm, 100mm]
        filtered_depth, mask, depth_mm = process_depth(depth_data)

        # Calculate the centroid and average depth of the masked region
        centroid, average_depth = calculate_centroid_and_depth(mask, depth_mm)

        # Convert the filtered depth image to a 3-channel image for drawing
        output_image = cv2.cvtColor(filtered_depth.astype(np.uint8), cv2.COLOR_GRAY2BGR)

        if centroid is not None and average_depth is not None:
            # Map the average depth to a circle radius
            # You can adjust the scaling factor to control the size of the circle
            min_depth = 50
            max_depth = 100
            min_radius = 5
            max_radius = 50
            radius = int(np.interp(average_depth, [min_depth, max_depth], [max_radius, min_radius]))

            # Draw a circle at the centroid with the dynamically calculated radius
            cv2.circle(output_image, centroid, radius, (0, 0, 255), -1)  # Red circle

        # Display the output image
        cv2.imshow('Inverted Filtered Depth with Centroid', output_image)
        print(centroid, average_depth)
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()