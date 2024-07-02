""" A wrapper for the OS Manager API using aiohttp. """

import asyncio
import logging

import aiohttp
import backoff

from pyosmanager.responses import CoreResponse, DeviceResponse

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Base exception for API errors"""


class OSMClient:
    """
    A wrapper for the OS Manager API using aiohttp.

    :param base_url: The base URL of the API
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        """Close the aiohttp session"""
        await self.session.close()

    @backoff.on_exception(
        backoff.expo, (aiohttp.ClientError, asyncio.TimeoutError), max_tries=3
    )
    async def __get_data(self, endpoint, params=None):
        """
        Perform a GET request to the specified endpoint.

        :param endpoint: API endpoint to query
        :param params: Optional query parameters
        :return: JSON response from the API
        """
        try:
            async with self.session.get(
                f"{self.base_url}/api/{endpoint}", params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()
                logger.info(f"Successfully retrieved data from {endpoint}")
                return data
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
            logger.error(f"API request failed: {str(e)}")
            raise APIError(f"API request failed: {str(e)}") from e

    @backoff.on_exception(
        backoff.expo, (aiohttp.ClientError, asyncio.TimeoutError), max_tries=3
    )
    async def __post_data(self, endpoint, data):
        """
        Perform a POST request to the specified endpoint.

        :param endpoint: API endpoint to send data to
        :param data: Data to be sent in the request body
        :return: JSON response from the API
        """
        try:
            async with self.session.post(
                f"{self.base_url}/api/{endpoint}", json=data
            ) as response:
                response.raise_for_status()
                data = await response.json()
                logger.info(f"Successfully posted data to {endpoint}")
                return data
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
            logger.error(f"API request failed: {str(e)}")
            raise APIError(f"API request failed: {str(e)}") from e

    async def is_healthy(self) -> bool:
        """
        Check if the API is healthy.

        :return: True if the API is healthy, False otherwise
        """
        try:
            await self.__get_data("")
            return True
        except APIError:
            return False

    async def get_core_state(self) -> dict:
        """
        Get the core state of the system.

        :return: Core state of the system
        """
        core = await self.__get_data("core")
        return CoreResponse(**core)

    async def get_devices(self) -> list[DeviceResponse]:
        """
        Get a list of all devices.

        :return: List of devices
        """
        devices = await self.__get_data("devices")
        return [DeviceResponse(**device) for device in devices]

    async def get_device(self, device_name) -> DeviceResponse:
        """
        Get information about a specific device.

        :param device_name: Name of the device
        :return: DeviceResponse object with the device information
        """
        device = await self.__get_data(f"device/{device_name}")
        return DeviceResponse(**device)

    async def get_device_consumption(self, device_name) -> float:
        """
        Get the consumption data of a specific device.

        :param device_name: Name of the device
        :return: Consumption data of the device in watts
        """
        res = await self.__get_data(f"device/{device_name}/consumption")

        return res["consumption"]

    async def get_surplus(self) -> float:
        """
        Get the current surplus data.

        :return: Surplus data in watts
        """
        res = await self.__get_data("surplus")

        return res["surplus"]

    async def set_surplus_margin(self, margin: float) -> float:
        """
        Set the surplus margin.

        :param margin: The surplus margin to set
        :return: The new surplus margin
        """
        data = {"surplus_margin": margin}
        res = await self.__post_data("surplus_margin", data)

        return res["surplus_margin"]

    async def set_grid_margin(self, margin: float) -> float:
        """
        Set the grid margin.

        :param margin: The grid margin to set
        :return: The new grid margin
        """
        data = {"grid_margin": margin}
        res = await self.__post_data("grid_margin", data)

        return res["grid_margin"]

    async def set_idle_power(self, idle_power: float) -> float:
        """
        Set the idle power.

        :param idle_power: The idle power to set
        :return: The new idle power
        """
        data = {"idle_power": idle_power}
        res = await self.__post_data("idle_power", data)

        return res["idle_power"]

    async def set_device_max_consumption(
        self, device_name: str, max_consumption: float
    ) -> float:
        """
        Set the maximum consumption of a device.

        :param device_name: Name of the device
        :param max_consumption: The maximum consumption to set
        :return: The new maximum consumption
        """
        data = {"max_consumption": max_consumption}
        res = await self.__post_data(f"device/{device_name}/max_consumption", data)

        return res["max_consumption"]

    async def set_device_expected_consumption(
        self, device_name: str, expected_consumption: float
    ) -> float:
        """
        Set the expected consumption of a device.

        :param device_name: Name of the device
        :param expected_consumption: The expected consumption to set
        :return: The new expected consumption
        """
        data = {"expected_consumption": expected_consumption}
        res = await self.__post_data(f"device/{device_name}/expected_consumption", data)

        return res["expected_consumption"]

    async def set_device_cooldown(self, device_name: str, cooldown: int) -> int:
        """
        Set the cooldown of a device.

        :param device_name: Name of the device
        :param cooldown: The cooldown to set
        :return: The new cooldown
        """
        data = {"cooldown": cooldown}
        res = await self.__post_data(f"device/{device_name}/cooldown", data)

        return res["cooldown"]
