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


async def main():
    async with OSMClient("http://localhost:8080") as client:
        print(await client.get_devices())


if __name__ == "__main__":
    asyncio.run(main())
```

## Methods

- `get_hello_world(self)`

Retrieve the hello world message from the API to verify connectivity.

- `get_devices(self)`

Retrieve a list of devices

- `get_device(self, device_name: str)`
  
Retrieve a device data dictionary by name

- `get_device_consumption(self, device_name: str)`
  
Retrieve the device consumption by name
