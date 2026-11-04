"""Forwards requests to a downstream service and relays the response."""

import httpx
from fastapi import Response


class ServiceProxy:

    def __init__(self, base_url: str, timeout: float = 10.0):
        self._client = httpx.Client(base_url=base_url, timeout=timeout) # Open a connection pool

    def forward_get(self, path: str) -> Response:
        return self._relay(self._client.get(path))

    def forward_post(self, path: str, body: dict) -> Response:
        return self._relay(self._client.post(path, json=body))

    @staticmethod
    def _relay(upstream: httpx.Response) -> Response:
        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type"),
        )