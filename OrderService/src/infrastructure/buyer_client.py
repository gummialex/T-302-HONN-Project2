
import httpx

class BuyerClient:

    def __init__(self, base_url: str, timeout: float = 5.0):
        self._client = httpx.Client(base_url=base_url, timeout=timeout) # Keeps a pool of connections open to BuyerService

    def get_buyer(self, buyer_id: int) -> dict | None:
        """Returns the Buyer or None when BuyerService says 404"""

        response = self._client.get(f"/buyers/{buyer_id}")

        if response.status_code == 404:
            return None

        response.raise_for_status() # A check to ensure that everything other than 2xx becomes an exception
        return response.json()  # Parses the json body into a python dict