def analyze_skin(image_pil):
    import numpy as np
    from sklearn.cluster import KMeans
    import cv2

    image_np = np.array(image_pil)

    # Convert to RGB if image is in a different format
    if len(image_np.shape) == 2:  # Grayscale
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
    elif image_np.shape[2] == 4:  # RGBA
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
    else:
        image_rgb = image_np

    # Resize image for faster processing while maintaining aspect ratio
    height, width = image_rgb.shape[:2]
    max_dim = 600
    scale = max_dim / max(height, width)
    resized = cv2.resize(image_rgb, (int(width * scale), int(height * scale)))

    # Convert to OpenCV format for human detection
    opencv_image = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)

    # Initialize human detector (HOG + Linear SVM)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Detect humans in the image
    boxes, weights = hog.detectMultiScale(opencv_image, winStride=(8, 8), padding=(16, 16), scale=1.05)

    # If no human detected, use face detection as fallback
    if len(boxes) == 0:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            # Use the largest face detected
            largest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_face
            # Expand the region a bit to include more of the face
            x = max(0, x - int(w * 0.2))
            y = max(0, y - int(h * 0.2))
            w = min(resized.shape[1] - x, int(w * 1.4))
            h = min(resized.shape[0] - y, int(h * 1.4))
            cropped = resized[y:y+h, x:x+w]
        else:
            # If no face detected either, use the center portion of the image
            h, w = resized.shape[:2]
            center_x, center_y = w // 2, h // 2
            crop_size = min(w, h) // 2
            x1, y1 = center_x - crop_size, center_y - crop_size
            x2, y2 = center_x + crop_size, center_y + crop_size
            cropped = resized[y1:y2, x1:x2]
    else:
        # Use the human with highest confidence (first in the list)
        x, y, w, h = boxes[0]
        # Ensure coordinates are within image bounds
        x, y, w, h = max(0, x), max(0, y), min(w, resized.shape[1] - x), min(h, resized.shape[0] - y)
        cropped = resized[y:y+h, x:x+w]

    # Convert cropped image to RGB for further processing
    cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB) if len(boxes) > 0 else cropped

    # Reshape the image to be a list of pixels
    pixels = cropped_rgb.reshape(-1, 3)

    # Apply K-means clustering to find dominant colors
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(pixels)

    # Get dominant color (typically skin color in a human subject image)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    color_counts = np.bincount(kmeans.labels_)
    dominant_color_idx = np.argsort(color_counts)[-3:]  # Get top 3 most common colors

    # Filter to find skin tones (within certain RGB ranges typical for skin)
    skin_colors = []
    for idx in dominant_color_idx:
        r, g, b = dominant_colors[idx]
        # Simple heuristic for skin detection:
        # R > G and R > B for most skin tones, and certain ratios between channels
        if r > g and r > b and r > 60 and g > 40 and b > 20:
            skin_colors.append((r, g, b))

    # If no skin color found, use the most dominant color
    if not skin_colors:
        dominant_color = dominant_colors[dominant_color_idx[-1]]
    else:
        # Use the most dominant skin color
        dominant_color = max(skin_colors, key=lambda x: x[0] * 0.5 + x[1] * 0.3 + x[2] * 0.2)

    r, g, b = dominant_color

    # Analyze skin tone based on dominant color
    # Convert to HSV for better skin tone classification
    import colorsys
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

    # Classify based on value (brightness)
    if v < 0.4:
        skin_tone = "Dark"
    elif v < 0.55:
        skin_tone = "Medium Dark"
    elif v < 0.7:
        skin_tone = "Medium"
    elif v < 0.85:
        skin_tone = "Medium Light"
    else:
        skin_tone = "Pale"

    # Analyze texture using edge detection
    gray = cv2.cvtColor(cropped_rgb, cv2.COLOR_RGB2GRAY)

    # Apply bilateral filter to reduce noise while preserving edges
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)

    # Use Laplacian for texture analysis (detects edges in all directions)
    laplacian = cv2.Laplacian(filtered, cv2.CV_64F)

    # Get texture metrics
    texture_variance = np.var(laplacian)
    texture_std = np.std(laplacian)

    # Classify texture
    if texture_variance < 20:
        texture_label = "Smooth"
    elif texture_variance < 50:
        texture_label = "Oily"
    else:
        texture_label = "Rough"

    return skin_tone, texture_label
