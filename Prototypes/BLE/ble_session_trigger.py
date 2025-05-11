import asyncio
from BLE.ble_handler import scan_devices
from BLE.ble_constants import DEVICE_WHITELIST, DEFAULT_SCAN_TIMEOUT

#triggers a session if known devices are found

async def trigger_session_on_detect() -> bool:
    nearby_devices = await scan_devices(timeout=DEFAULT_SCAN_TIMEOUT)

    for name, address in nearby_devices:
        # Direct MAC match
        if address in DEVICE_WHITELIST.values():
            print(f"[BLE Trigger] Recognised device: {name} ({address})")
         #New Sesh, If Needed
            return True

    return False
if __name__ == "__main__":
    print("[BLE Trigger] Scanning for known users...")
    match = asyncio.run(trigger_session_on_detect())

    if match:
        print("[BLE Trigger] Session triggered.")
    else:
        print("[BLE Trigger] No known devices nearby.")
