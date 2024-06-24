# pyOSManager

> Python client for Open Surplus Manager

## Installation

```bash
pip install pyosmanager
```

## Usage

```python
import asyncio

from pyosmanager import OSMClient
from pyosmanager.responses import DeviceResponse


async def main():
    async with OSMClient("http://localhost:8080") as client:
        res = await client.get_devices()
        d: DeviceResponse
        for d in res:
            print(d.name)


if __name__ == "__main__":
    asyncio.run(main())

```

## Methods

- `is_healthy() -> bool`

True if the server is healthy

- `get_devices() -> list[DeviceResponse]`

Retrieve a list of devices

- `get_device(device_name: str) -> DeviceResponse`
  
Retrieve a device data dictionary by name

- `get_device_consumption(device_name: str) -> float`
  
Retrieve the device consumption by name

- `get_surplus() -> float:`

Retrieve the surplus value
