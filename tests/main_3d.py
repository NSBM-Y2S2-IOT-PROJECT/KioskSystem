# Problematic
import libfreenect.wrappers.python.freenect as freenect
import numpy as np
import open3d as o3d
import cv2

def get_depth_frame():
    """Fetch a depth frame from the Kinect sensor."""
    depth, _ = freenect.sync_get_depth()
    depth = depth.astype(np.float32)
    depth[depth == 2047] = 0  # Remove invalid depth data
    return depth

def create_point_cloud(depth_frame):
    """Convert a depth frame into a 3D point cloud."""
    h, w = depth_frame.shape
    fx = fy = 580.0  # Approximate focal length of Kinect v1
    cx, cy = w / 2, h / 2

    points = []
    for y in range(h):
        for x in range(w):
            z = depth_frame[y, x]
            if z > 0:  # Ignore zero depth points
                X = (x - cx) * z / fx
                Y = (y - cy) * z / fy
                Z = z
                points.append([X, Y, Z])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(np.array(points))
    return point_cloud

def main():
    print("Capturing depth frame...")
    depth_frame = get_depth_frame()
    
    # Display the depth frame for reference
    cv2.imshow("Depth Frame", depth_frame / np.max(depth_frame))
    cv2.waitKey(500)

    print("Creating 3D point cloud...")
    point_cloud = create_point_cloud(depth_frame)

    print("Generating 3D mesh from the point cloud...")
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(point_cloud, alpha=0.03)
    mesh.compute_vertex_normals()

    print("Displaying 3D mesh with black background...")
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(mesh)
    opt = vis.get_render_option()
    opt.background_color = np.array([0, 0, 0])  # Set background to black
    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    main()
