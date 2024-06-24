""" This module contains the DeviceResponse class. """

from dataclasses import dataclass


@dataclass
class DeviceResponse:
    """
    This class is used to represent the response of the API
    when querying for a device.
    """

    name: str
    device_type: str
    control_integration: str
    expected_consumption: float
    max_consumption: float | None
    consumption: float
    powered: bool
    cooldown: int | None
    enabled: bool
