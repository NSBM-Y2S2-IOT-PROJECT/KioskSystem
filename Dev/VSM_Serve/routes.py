from flask import Blueprint, request, jsonify
from infoWrap import Info
from analysis import analyze_skin
from PIL import Image
import io

# Initialize logger
logger = Info()

# Create a Blueprint for the routes
routes = Blueprint('routes', __name__)

@routes.route('/data/image_check', methods=['POST'])
def image_check():
    try:
        # Check if an image file is included in the request
        if 'image' not in request.files:
            logger.error("No image file found in the request.")
            return jsonify({"error": "No image file provided"}), 400

        # Read the image file
        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read()))

        # Log the received image
        logger.info("Image received for analysis.")

        # Analyze the image
        skin_color, texture = analyze_skin(image)

        # Log the analysis results
        logger.info(f"Skin Color: {skin_color}, Texture: {texture}")

        # Return the results as JSON
        return jsonify({
            "skin_color": skin_color,
            "texture": texture
        })

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An error occurred during processing"}), 500

@routes.route('/data/sys_check/<module>', methods=['GET'])
def sys_check(module):
    try:
        import os
        file_path = os.path.expanduser(f'~/.sysCheck{module}.log')
        with open(file_path, 'r') as data:
            data = data.read()
        logger.info(f"{module} data read successfully.")
        return jsonify({"info": data}), 200

    except Exception as e:
        logger.error(f"Unable to read {module} data: {str(e)}")
        return jsonify({"error": "False"}), 500
