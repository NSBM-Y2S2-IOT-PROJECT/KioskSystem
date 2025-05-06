import asyncio
import datetime
from typing import List, Dict, Any
from pymongo import MongoClient
from bleak import BleakScanner, BLEDevice

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

    def save_device_info(self, devices: List[BLEDevice]) -> None:
        """
        Save discovered device information to MongoDB.

        Args:
            devices: List of discovered BLE devices
        """
        timestamp = datetime.datetime.now()

        for device in devices:
            device_info = {
                "mac_address": device.address,
                "name": device.name if device.name else "Unknown",
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

        print(f"Saved information for {len(devices)} devices to MongoDB")

    async def monitor_continuously(self, scan_interval: float = 60.0, scan_duration: float = 10.0):
        """
        Continuously monitor for Bluetooth devices at specified intervals.

        Args:
            scan_interval: Time between scans in seconds
            scan_duration: Duration of each scan in seconds
        """
        try:
            while True:
                devices = await self.scan_devices(scan_duration)
                if devices:
                    print(f"Found {len(devices)} Bluetooth devices:")
                    for device in devices:
                        print(f"  - {device.address} ({device.name or 'Unknown'})")
                    self.save_device_info(devices)
                else:
                    print("No Bluetooth devices found")

                print(f"Waiting {scan_interval} seconds until next scan...")
                await asyncio.sleep(scan_interval)
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

    # Start continuous monitoring
    await monitor.monitor_continuously(scan_interval=60, scan_duration=10)


if __name__ == "__main__":
    print("Starting Bluetooth device monitoring...")
    asyncio.run(main())
