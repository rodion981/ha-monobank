"""Tests for the Monobank HTTP client."""

from __future__ import annotations

import unittest

from module_loader import load_monobank_module


api_module = load_monobank_module("api")
MonobankAPI = api_module.MonobankAPI
MonobankAPIError = api_module.MonobankAPIError
MonobankAuthError = api_module.MonobankAuthError
MonobankRateLimitError = api_module.MonobankRateLimitError


class FakeResponse:
    """Small aiohttp response stand-in."""

    def __init__(self, status: int, payload=None, text: str = "") -> None:
        self.status = status
        self._payload = payload
        self._text = text

    async def json(self):
        return self._payload

    async def text(self) -> str:
        return self._text


class TestMonobankAPI(unittest.IsolatedAsyncioTestCase):
    """Verify response and endpoint handling."""

    async def test_success_returns_json(self) -> None:
        api = MonobankAPI("token")
        payload = {"clientId": "client-1"}
        self.assertEqual(
            await api._handle_response(FakeResponse(200, payload)), payload
        )

    async def test_auth_error_is_typed(self) -> None:
        api = MonobankAPI("token")
        with self.assertRaises(MonobankAuthError):
            await api._handle_response(FakeResponse(401))

    async def test_rate_limit_error_is_typed(self) -> None:
        api = MonobankAPI("token")
        with self.assertRaises(MonobankRateLimitError):
            await api._handle_response(FakeResponse(429))

    async def test_other_http_error_contains_status(self) -> None:
        api = MonobankAPI("token")
        with self.assertRaisesRegex(MonobankAPIError, "status 503"):
            await api._handle_response(FakeResponse(503, text="unavailable"))

    async def test_statement_without_end_time_has_no_trailing_slash(self) -> None:
        api = MonobankAPI("token")
        captured = {}

        async def fake_request(endpoint, method="GET", data=None):
            captured["endpoint"] = endpoint
            return []

        api._request = fake_request
        await api.get_statement("account", 123)
        self.assertEqual(captured["endpoint"], "/personal/statement/account/123")
