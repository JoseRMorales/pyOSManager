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

- `get_core_state() -> dict`

Retrieve the core state

- `get_devices() -> list[DeviceResponse]`

Retrieve a list of devices

- `get_device(device_name: str) -> DeviceResponse`
  
Retrieve a device data dictionary by name

- `get_device_consumption(device_name: str) -> float`
  
Retrieve the device consumption by name

- `get_surplus() -> float:`

Retrieve the surplus value

- `set_surplus_margin(margin: float) -> float:`
  
Set the surplus margin

- `set_grid_margin(margin: float) -> float:`

Set the grid margin

- `set_idle_power(idle_power: float) -> float:`

Set the idle power

- `set_device_max_consumption(device_name: str, max_consumption: float) -> float:`

Set the max consumption for a device

- `set_device_expected_consumption(device_name: str, expected_consumption: float) -> float:`

Set the expected consumption for a device

- `set_device_cooldown(device_name: str, cooldown: int) -> int:`

Set the cooldown for a device
