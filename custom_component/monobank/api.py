"""Monobank API client."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
from aiohttp import ClientError, ClientSession

from .const import (
    API_BASE_URL,
    API_MAX_RETRIES,
    API_RETRY_DELAY,
    API_TIMEOUT,
    ENDPOINT_CLIENT_INFO,
    ENDPOINT_CURRENCY,
    ENDPOINT_STATEMENT,
    ENDPOINT_WEBHOOK,
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

    async def _request(self, endpoint: str, method: str = "GET", data: dict[str, Any] | None = None) -> dict[str, Any] | list[dict[str, Any]]:
        """Make API request with retry logic.
        
        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, etc.)
            data: Request data for POST requests
            
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

        for attempt in range(API_MAX_RETRIES):
            try:
                async with asyncio.timeout(API_TIMEOUT):
                    if method == "GET":
                        async with session.get(url, headers=headers) as response:
                            return await self._handle_response(response)
                    elif method == "POST":
                        async with session.post(url, headers=headers, json=data) as response:
                            return await self._handle_response(response)
                    else:
                        raise MonobankAPIError(f"Unsupported HTTP method: {method}")

            except MonobankAuthError:
                # Don't retry auth errors
                raise
            except MonobankRateLimitError as err:
                _LOGGER.warning("Rate limit exceeded, attempt %d/%d", attempt + 1, API_MAX_RETRIES)
                if attempt < API_MAX_RETRIES - 1:
                    await asyncio.sleep(API_RETRY_DELAY * (attempt + 1))
                else:
                    raise
            except asyncio.TimeoutError as err:
                _LOGGER.warning("Request timeout, attempt %d/%d", attempt + 1, API_MAX_RETRIES)
                if attempt < API_MAX_RETRIES - 1:
                    await asyncio.sleep(API_RETRY_DELAY)
                else:
                    raise MonobankAPIError("Request timeout after retries") from err
            except ClientError as err:
                _LOGGER.warning("Request failed: %s, attempt %d/%d", err, attempt + 1, API_MAX_RETRIES)
                if attempt < API_MAX_RETRIES - 1:
                    await asyncio.sleep(API_RETRY_DELAY)
                else:
                    raise MonobankAPIError(f"Request failed after retries: {err}") from err

        raise MonobankAPIError("Max retries exceeded")

    async def _handle_response(self, response: aiohttp.ClientResponse) -> dict[str, Any] | list[dict[str, Any]]:
        """Handle API response.
        
        Args:
            response: aiohttp response object
            
        Returns:
            Parsed JSON response
            
        Raises:
            MonobankAuthError: Authentication failed
            MonobankRateLimitError: Rate limit exceeded
            MonobankAPIError: Other API errors
        """
        if response.status == 200:
            return await response.json()
        
        if response.status == 401:
            raise MonobankAuthError("Invalid API token")
        
        if response.status == 429:
            raise MonobankRateLimitError("Rate limit exceeded")
        
        error_text = await response.text()
        _LOGGER.error("API request failed with status %d: %s", response.status, error_text)
        raise MonobankAPIError(
            f"API request failed with status {response.status}: {error_text}"
        )

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

    async def set_webhook(self, webhook_url: str) -> dict[str, Any]:
        """Set webhook URL for receiving transaction notifications.
        
        Args:
            webhook_url: Webhook URL to register
            
        Returns:
            API response
        """
        _LOGGER.debug("Setting webhook URL: %s", webhook_url)
        return await self._request(ENDPOINT_WEBHOOK, method="POST", data={"webHookUrl": webhook_url})

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
