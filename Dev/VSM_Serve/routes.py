from flask import Blueprint, request, jsonify
from infoWrap import Info
from face_analysis.analysis import analyze_skin
from llm_service import llmBridge, initializeChroma
from PIL import Image
from BLE_Service import BluetoothMonitor
import io
import asyncio
from sysCheck import System, BtLowEnergy, Gpio, VisumServer, Kinect

logger = Info()
initializeChroma()

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "bluetooth_monitoring"
COLLECTION_NAME = "kiosk_bt_user_sessions"

routes = Blueprint('routes', __name__)

@routes.route('/data/image_check', methods=['POST'])
def image_check():
    try:
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

@routes.route('/data/get_recommendations/<skin_color>/<skin_texture>', methods=['GET'])
def get_recommendations(skin_color, skin_texture):
    try:
        logger.info(f"Received Recommendation Request for Skin Color{skin_color} and Texture {skin_texture}")
        output = llmBridge(f"Recommendations for {skin_color, skin_texture}", rag=True)
        logger.debug(output)
        return llmBridge(f"Recommendations for {skin_color, skin_texture}", rag=True)
        # return jsonify({"recommendations": "Use these stuff, <Links> Stuff names etc."}), 200
    except Exception as e:
        logger.error(f"Error in Recommendation Request, {str(e)}")
        return jsonify({"error": "False"}), 500

@routes.route('/data/scan_bluetooth', methods=['GET'])
def scan_bluetooth():
    sysCheck = BtLowEnergy()
    sysCheck.setModal("True")
    try:
        scan_duration = float(request.args.get('duration', 10.0))
        
        logger.info(f"Starting Bluetooth scan with duration {scan_duration}s")
        
        # Initialize the Bluetooth monitor
        monitor = BluetoothMonitor(
            mongo_uri=MONGO_URI,
            db_name=DB_NAME,
            collection_name=COLLECTION_NAME
        )
        
        # Run the scan in an async context
        async def find_closest_device():
            # Perform a single scan
            devices = await monitor.scan_devices(scan_duration=scan_duration)
            
            if not devices:
                return None, None
            
            # Find the device with strongest signal (closest proximity)
            closest_device = max(devices, key=lambda device: device.rssi)
            
            # Get the name of the device
            device_name = await monitor.get_device_name(closest_device)
            
            return closest_device, device_name
        
        # Execute the async function
        closest_device, device_name = asyncio.run(find_closest_device())
        
        if closest_device:
            logger.info(f"Found closest Bluetooth device: {closest_device.address} ({device_name})")
            
            # Save the device information to MongoDB
            async def save_device():
                await monitor.save_device_info({closest_device.address: closest_device})
            
            asyncio.run(save_device())
            
            # Return device information
            sysCheck.setModal("False")
            return jsonify({
                "found": True,
                "device": {
                    "address": closest_device.address,
                    "name": device_name,
                    "rssi": closest_device.rssi
                }
            }), 200
        else:
            logger.info("No Bluetooth devices found")
            sysCheck.setModal("False")
            return jsonify({
                "found": False,
                "message": "No Bluetooth devices found in range"
            }), 200
            
    except Exception as e:
        logger.error(f"Error during Bluetooth scan: {str(e)}")
        sysCheck.setModal("False")
        return jsonify({
            "error": f"An error occurred during Bluetooth scanning: {str(e)}"
        }), 500