"""Monobank API client."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
from aiohttp import ClientError, ClientSession

from .const import (
    API_BASE_URL,
    API_TIMEOUT,
    ENDPOINT_CLIENT_INFO,
    ENDPOINT_CURRENCY,
    ENDPOINT_STATEMENT,
)

_LOGGER = logging.getLogger(__name__)


class MonobankAPIError(Exception):
    """Base exception for Monobank API errors."""


class MonobankAuthError(MonobankAPIError):
    """Exception for authentication errors."""


class MonobankRateLimitError(MonobankAPIError):
    """Exception for rate limit errors."""


class MonobankAPI:
    """Monobank API client."""

    def __init__(self, token: str, session: ClientSession | None = None) -> None:
        """Initialize the API client.
        
        Args:
            token: Monobank API token
            session: aiohttp ClientSession (optional)
        """
        self._token = token
        self._session = session
        self._close_session = False

    async def _get_session(self) -> ClientSession:
        """Get or create aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True
        return self._session

    async def close(self) -> None:
        """Close the API client session."""
        if self._close_session and self._session:
            await self._session.close()

    async def _request(self, endpoint: str) -> dict[str, Any]:
        """Make API request.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            API response data
            
        Raises:
            MonobankAuthError: Authentication failed
            MonobankRateLimitError: Rate limit exceeded
            MonobankAPIError: Other API errors
        """
        url = f"{API_BASE_URL}{endpoint}"
        headers = {"X-Token": self._token}

        session = await self._get_session()

        try:
            async with asyncio.timeout(API_TIMEOUT):
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    
                    if response.status == 401:
                        raise MonobankAuthError("Invalid API token")
                    
                    if response.status == 429:
                        raise MonobankRateLimitError("Rate limit exceeded")
                    
                    error_text = await response.text()
                    raise MonobankAPIError(
                        f"API request failed with status {response.status}: {error_text}"
                    )

        except asyncio.TimeoutError as err:
            raise MonobankAPIError("Request timeout") from err
        except ClientError as err:
            raise MonobankAPIError(f"Request failed: {err}") from err

    async def get_client_info(self) -> dict[str, Any]:
        """Get client information including accounts and jars.
        
        Returns:
            Client info data with accounts and jars
        """
        _LOGGER.debug("Fetching client info")
        return await self._request(ENDPOINT_CLIENT_INFO)

    async def get_currency_rates(self) -> list[dict[str, Any]]:
        """Get currency exchange rates.
        
        Returns:
            List of currency rates
        """
        _LOGGER.debug("Fetching currency rates")
        return await self._request(ENDPOINT_CURRENCY)

    async def get_statement(
        self, account_id: str, from_time: int, to_time: int | None = None
    ) -> list[dict[str, Any]]:
        """Get account statement (transactions).
        
        Args:
            account_id: Account ID
            from_time: Start timestamp (Unix time in seconds)
            to_time: End timestamp (Unix time in seconds), optional
            
        Returns:
            List of transactions
        """
        if to_time is None:
            endpoint = ENDPOINT_STATEMENT.format(
                account=account_id, from_=from_time, to=""
            ).rstrip("/")
        else:
            endpoint = ENDPOINT_STATEMENT.format(
                account=account_id, from_=from_time, to=to_time
            )
        
        _LOGGER.debug("Fetching statement for account %s", account_id)
        return await self._request(endpoint)

    async def validate_token(self) -> bool:
        """Validate API token.
        
        Returns:
            True if token is valid
            
        Raises:
            MonobankAuthError: If token is invalid
            MonobankAPIError: If validation fails
        """
        try:
            await self.get_client_info()
            return True
        except MonobankAuthError:
            raise
        except MonobankAPIError as err:
            _LOGGER.error("Token validation failed: %s", err)
            raise
