# REST HTTP calls for the MerchantService

import httpx

class MerchantClient:

    def __init__(self, base_url: str, timeout: float = 5.0):
        self._client = httpx.Client(base_url=base_url, timeout=timeout) # Keeps a pool of connections open to MerchantService

    def get_merchant(self, merchant_id: int) -> dict | None:
        """Returns the merchant or None when MerchantService says 404"""

        response = self._client.get(f"/merchants/{merchant_id}")

        if response.status_code == 404:
            return None

        response.raise_for_status() # A check to ensure that everything other than 2xx becomes an exception
        return response.json()  # Parses the json body into a python dict
