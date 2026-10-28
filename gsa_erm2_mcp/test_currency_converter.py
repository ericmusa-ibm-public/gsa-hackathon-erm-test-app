"""Tests for gsa_erm2_currency_converter."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from server import gsa_erm2_currency_converter as convert


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_response(rates: dict, result: str = "success", error_type: str | None = None):
    """Build a minimal open.er-api.com-shaped response dict."""
    payload = {
        "result": result,
        "time_last_update_utc": "Thu, 01 Jan 2025 00:00:02 +0000",
        "rates": rates,
    }
    if error_type:
        payload["error-type"] = error_type
    return payload


def _mock_client(payload: dict, status_code: int = 200):
    """Return a context-manager mock whose .get() resolves to a mock response."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = payload
    mock_resp.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_resp)
    return mock_client


# ---------------------------------------------------------------------------
# Happy-path tests (mocked network)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_usd_to_eur():
    rates = {"EUR": 0.92, "USD": 1.0}
    with patch("httpx.AsyncClient", return_value=_mock_client(_make_response(rates))):
        result = await convert(100, "USD", "EUR")
    assert result["result"] == pytest.approx(92.0, rel=1e-6)
    assert result["from_currency"] == "USD"
    assert result["to_currency"] == "EUR"
    assert result["rate"] == 0.92
    assert "last_updated" in result


@pytest.mark.asyncio
async def test_amount_and_currency_codes_are_normalised():
    """Lowercase input with whitespace should be normalised to uppercase."""
    rates = {"GBP": 0.79}
    with patch("httpx.AsyncClient", return_value=_mock_client(_make_response(rates))):
        result = await convert(50, " usd ", " gbp ")
    assert result["from_currency"] == "USD"
    assert result["to_currency"] == "GBP"


# ---------------------------------------------------------------------------
# Error-path tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_unknown_target_currency_returns_error():
    rates = {"EUR": 0.92}
    with patch("httpx.AsyncClient", return_value=_mock_client(_make_response(rates))):
        result = await convert(1, "USD", "XYZ")
    assert "error" in result
    assert "XYZ" in result["error"]


@pytest.mark.asyncio
async def test_api_error_result_returns_error():
    payload = _make_response({}, result="error", error_type="unsupported-code")
    with patch("httpx.AsyncClient", return_value=_mock_client(payload)):
        result = await convert(1, "FAKE", "USD")
    assert "error" in result
