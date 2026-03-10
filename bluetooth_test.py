import asyncio
from bleak import BleakScanner

async def check_bluetooth():
    try:
        devices = await BleakScanner.discover(timeout=2)
        if devices is not None:
            print("(+) Bluetooth включен")
            return True, None
    except Exception as e:
        error = "(Х) Bluetooth выключен"
        print(error)
        return False, error
 
asyncio.run(check_bluetooth())
