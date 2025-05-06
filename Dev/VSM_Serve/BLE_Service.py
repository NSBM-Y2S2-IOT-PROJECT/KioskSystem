import asyncio
import datetime
from typing import List, Dict, Any
from pymongo import MongoClient
from bleak import BleakScanner, BleakClient, BLEDevice

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "bluetooth_monitoring"
COLLECTION_NAME = "kiosk_bt_user_sessions"

class BluetoothMonitor:
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        """
        Initialize the Bluetooth monitor with MongoDB connection parameters.
        """
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        print(f"Connected to MongoDB: {db_name}.{collection_name}")

    async def scan_devices(self, scan_duration: float = 10.0) -> List[BLEDevice]:
        """
        Scan for nearby Bluetooth devices.

        Args:
            scan_duration: Duration of the scan in seconds

        Returns:
            List of discovered BLE devices
        """
        print(f"Scanning for Bluetooth devices for {scan_duration} seconds...")
        devices = await BleakScanner.discover(timeout=scan_duration)
        return devices

    async def get_device_name(self, device: BLEDevice) -> str:
        """
        Try to get the device name by connecting to it if the name is not available.

        Args:
            device: BLE device to connect to

        Returns:
            Device name or "Unknown" if it cannot be retrieved
        """
        if device.name:
            return device.name

        try:
            client = BleakClient(device)
            await client.connect(timeout=5.0)
            # Try to get device information if possible
            services = await client.get_services()
            for service in services:
                if "1800" in service.uuid:  # Generic Access service
                    for char in service.characteristics:
                        if "2a00" in char.uuid:  # Device Name characteristic
                            name_bytes = await client.read_gatt_char(char.uuid)
                            await client.disconnect()
                            return name_bytes.decode('utf-8')
            await client.disconnect()
        except Exception as e:
            print(f"Could not connect to {device.address} to get name: {str(e)}")

        return "Unknown"

    async def save_device_info(self, device_map: Dict[str, BLEDevice]) -> None:
        timestamp = datetime.datetime.now()

        for address, device in device_map.items():
            device_name = await self.get_device_name(device)
            device_info = {
                "mac_address": device.address,
                "name": device_name,
                "rssi": device.rssi,
                "detection_time": timestamp,
            }

            # Insert or update device information
            self.collection.update_one(
                {"mac_address": device.address},
                {"$set": device_info,
                 "$addToSet": {"sessions": timestamp}},
                upsert=True
            )

        print(f"Saved information for {len(device_map)} devices to MongoDB")

    async def run_detection_cycle(self, num_scans: int = 4, scan_interval: float = 5.0, scan_duration: float = 10.0):
        try:
            strongest_devices = {}

            for scan_num in range(1, num_scans + 1):
                print(f"Starting scan {scan_num} of {num_scans}")
                devices = await self.scan_devices(scan_duration)

                if devices:
                    print(f"Found {len(devices)} Bluetooth devices on scan {scan_num}:")
                    for device in devices:
                        device_name = await self.get_device_name(device)
                        print(f"  - {device.address} ({device_name}): RSSI {device.rssi}")

                        # Update if this is a new device or has a stronger signal than previously recorded
                        if (device.address not in strongest_devices or
                            device.rssi > strongest_devices[device.address].rssi):
                            strongest_devices[device.address] = device
                            print(f"    (Updated as strongest signal for this device)")
                else:
                    print(f"No Bluetooth devices found on scan {scan_num}")

                if scan_num < num_scans:
                    print(f"Waiting {scan_interval} seconds until next scan...")
                    await asyncio.sleep(scan_interval)

            # Save only the devices with strongest signals
            print(f"\nFinished all {num_scans} scans. Recording devices with strongest signals:")
            for address, device in strongest_devices.items():
                device_name = await self.get_device_name(device)
                print(f"  - {address} ({device_name}): RSSI {device.rssi}")

            await self.save_device_info(strongest_devices)

        except KeyboardInterrupt:
            print("Monitoring stopped by user")
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.client.close()
            print("MongoDB connection closed")


async def main():
    monitor = BluetoothMonitor(
        mongo_uri=MONGO_URI,
        db_name=DB_NAME,
        collection_name=COLLECTION_NAME
    )

    await monitor.run_detection_cycle(num_scans=4, scan_interval=5, scan_duration=10)


if __name__ == "__main__":
    print("Starting Bluetooth device monitoring...")
    asyncio.run(main())
