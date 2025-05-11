import numpy as np
from sklearn.cluster import KMeans
import cv2


def analyze_skin(image_pil):
    image_np = np.array(image_pil)
    if len(image_np.shape) == 2:
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
    elif image_np.shape[2] == 4:
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
    else:
        image_rgb = image_np

    height, width = image_rgb.shape[:2]
    max_dim = 600
    scale = max_dim / max(height, width)
    resized = cv2.resize(image_rgb, (int(width * scale), int(height * scale)))
    opencv_image = cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    boxes, weights = hog.detectMultiScale(opencv_image, winStride=(8, 8), padding=(16, 16), scale=1.05)

    if len(boxes) == 0:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            largest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_face
            x = max(0, x - int(w * 0.2))
            y = max(0, y - int(h * 0.2))
            w = min(resized.shape[1] - x, int(w * 1.4))
            h = min(resized.shape[0] - y, int(h * 1.4))
            cropped = resized[y:y+h, x:x+w]
        else:
            h, w = resized.shape[:2]
            center_x, center_y = w // 2, h // 2
            crop_size = min(w, h) // 2
            x1, y1 = center_x - crop_size, center_y - crop_size
            x2, y2 = center_x + crop_size, center_y + crop_size
            cropped = resized[y1:y2, x1:x2]
    else:
        x, y, w, h = boxes[0]
        x, y, w, h = max(0, x), max(0, y), min(w, resized.shape[1] - x), min(h, resized.shape[0] - y)
        cropped = resized[y:y+h, x:x+w]

    cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB) if len(boxes) > 0 else cropped
    pixels = cropped_rgb.reshape(-1, 3)
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    color_counts = np.bincount(kmeans.labels_)
    dominant_color_idx = np.argsort(color_counts)[-3:]
    skin_colors = []
    for idx in dominant_color_idx:
        r, g, b = dominant_colors[idx]
        if r > g and r > b and r > 60 and g > 40 and b > 20:
            skin_colors.append((r, g, b))

    if not skin_colors:
        dominant_color = dominant_colors[dominant_color_idx[-1]]
    else:
        dominant_color = max(skin_colors, key=lambda x: x[0] * 0.5 + x[1] * 0.3 + x[2] * 0.2)

    r, g, b = dominant_color
    import colorsys
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

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
    
    gray = cv2.cvtColor(cropped_rgb, cv2.COLOR_RGB2GRAY)
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    laplacian = cv2.Laplacian(filtered, cv2.CV_64F)
    texture_variance = np.var(laplacian)

    if texture_variance < 20:
        texture_label = "Smooth"
    elif texture_variance < 50:
        texture_label = "Oily"
    else:
        texture_label = "Rough"

    return skin_tone, texture_label

def validate_landmarks(landmarks):

    if not isinstance(landmarks, list) or len(landmarks) < 5:
        return False, "Landmarks should be a list of at least 5 points."
    
    for point in landmarks:
        if not isinstance(point, list) or len(point) != 2:
            return False, "Each landmark should be a list of two numerical values [x, y]."
        if not all(isinstance(coord, (int, float)) for coord in point):
            return False, "Each coordinate [x, y] should be a number."
    
    return True, None

def analyze_image_for_beauty(landmarks: list) -> float:
    try:
        left_eye = landmarks[0]
        right_eye = landmarks[1]
        nose = landmarks[2]
        mouth_left = landmarks[3]
        mouth_right = landmarks[4]

        # Calculate distances
        eye_distance = np.linalg.norm(np.array(left_eye) - np.array(right_eye))
        nose_to_eye_distance = np.linalg.norm(np.array(nose) - np.array(left_eye))
        mouth_to_nose_distance = np.linalg.norm(np.array(mouth_left) - np.array(nose))

        # Calculate Golden Ratio-based score
        ratio_1 = eye_distance / nose_to_eye_distance
        ratio_2 = mouth_to_nose_distance / nose_to_eye_distance

        # Beauty score
        beauty_score = (abs(ratio_1 - GOLDEN_RATIO) + abs(ratio_2 - GOLDEN_RATIO)) * 50
        beauty_score = max(min(beauty_score, 100), 0)  # Ensure score is between 0 and 100
        return round(beauty_score, 2)

    except Exception as e:
        print(f"Error in analyzing image: {e}")
        return 0