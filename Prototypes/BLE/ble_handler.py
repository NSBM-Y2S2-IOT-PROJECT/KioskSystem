from bleak import BleakScanner
from typing import List, Tuple

# Scans the airwaves for nearby BLE devices

async def scan_devices(timeout: int = 5) -> List[Tuple[str, str]]:
    devices_found: List[Tuple[str, str]] = []

    try:
        results = await BleakScanner.discover(timeout=timeout)

        for device in results:
            name = device.name
            address = device.address

            # Ignore unidentifiable broadcasts
            if name and address:
                devices_found.append((name, address))

    except Exception:
        # Fail silently – BLE can be unpredictable depending on hardware
        pass

    return devices_found
