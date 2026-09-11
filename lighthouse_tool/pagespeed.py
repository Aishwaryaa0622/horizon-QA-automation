"""
pagespeed.py
------------
Responsible for ONE thing only: calling the Google PageSpeed Insights API and
returning the raw JSON response.

Google runs Lighthouse on their own servers, so we do not need Node.js or
Chrome installed locally. This keeps the tool beginner friendly.

API docs: https://developers.google.com/speed/docs/insights/v5/get-started
"""

import os

import requests

# The public endpoint. "v5" is the current version of the API.
API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# A Lighthouse run can take a while, so we allow a generous timeout (seconds).
REQUEST_TIMEOUT = 120


class PageSpeedError(Exception):
    """Raised when the scan could not be completed (bad URL, network, quota)."""


def normalise_url(url: str) -> str:
    """
    Make sure the URL has a scheme.

    Users often type "example.com" instead of "https://example.com".
    Google rejects URLs without a scheme, so we add one.
    """
    url = (url or "").strip()
    if not url:
        raise PageSpeedError("Please enter a website address.")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def run_audit(url: str, strategy: str = "mobile") -> dict:
    """
    Run a Lighthouse audit for `url` and return the raw JSON response.

    Parameters
    ----------
    url : str
        The page to scan, e.g. "https://example.com".
    strategy : str
        "mobile" (default) or "desktop" - which device Lighthouse simulates.

    Returns
    -------
    dict
        The full PageSpeed Insights JSON response.
    """
    url = normalise_url(url)

    # Query string sent to Google. `category` may be repeated, so we use a list
    # of tuples instead of a plain dictionary.
    params = [
        ("url", url),
        ("strategy", strategy),
        ("category", "performance"),
        ("category", "accessibility"),
        ("category", "best-practices"),
        ("category", "seo"),
    ]

    # The API key is optional but raises the daily request quota.
    api_key = os.environ.get("PAGESPEED_API_KEY")
    if api_key:
        params.append(("key", api_key))

    try:
        response = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise PageSpeedError("The scan took too long. Please try again.")
    except requests.exceptions.RequestException as error:
        raise PageSpeedError(f"Could not reach Google PageSpeed: {error}")

    if response.status_code != 200:
        # Google returns a helpful message inside the error body - show it.
        message = _extract_error_message(response)
        raise PageSpeedError(message)

    return response.json()


def _extract_error_message(response: requests.Response) -> str:
    """Pull a readable error message out of a failed API response."""
    try:
        payload = response.json()
        return payload.get("error", {}).get(
            "message", f"Scan failed (status {response.status_code})."
        )
    except ValueError:  # body was not JSON
        return f"Scan failed (status {response.status_code})."
