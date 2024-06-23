import asyncio
import logging

import aiohttp
import backoff

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
                f"{self.base_url}/{endpoint}", json=data
            ) as response:
                response.raise_for_status()
                data = await response.json()
                logger.info(f"Successfully posted data to {endpoint}")
                return data
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
            logger.error(f"API request failed: {str(e)}")
            raise APIError(f"API request failed: {str(e)}") from e

    async def get_hello_world(self):
        """
        Get the hello world message from the API to verify connectivity.

        :return: The hello world message
        """
        return await self.__get_data("")

    async def get_devices(self):
        """
        Get a list of all devices.

        :return: List of devices
        """
        return await self.__get_data("devices")

    async def get_device(self, device_name):
        """
        Get information about a specific device.

        :param device_name: Name of the device
        :return: Device information
        """
        return await self.__get_data(f"device/{device_name}")

    async def get_device_consumption(self, device_name):
        """
        Get the consumption data of a specific device.

        :param device_name: Name of the device
        :return: Consumption data
        """
        return await self.__get_data(f"device/{device_name}/consumption")
