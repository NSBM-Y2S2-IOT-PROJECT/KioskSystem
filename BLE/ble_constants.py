from typing import Dict

# Devices we care about, filtered by MAC address
DEVICE_WHITELIST: Dict[str, str] = {
    "Risura’s iPhone": "D4:36:39:AD:72:91",
    "Crown_iPad": "C0:12:34:56:78:90"
}
# Can be used to identify devices
TARGET_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb" 

# Scan timing config
DEFAULT_SCAN_TIMEOUT = 5 
