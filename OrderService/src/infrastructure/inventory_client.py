from fastapi import HTTPException
import httpx

class InventoryClient:

    def __init__(self, base_url: str, timeout: float = 5.0):
        self._client = httpx.Client(base_url=base_url, timeout=timeout) # Keeps a pool of connections open to InventoryService

    def get_product(self, product_id: int) -> dict | None:
        """Returns the product or None when InventoryService says 404"""

        response = self._client.get(f"/products/{product_id}")

        if response.status_code == 404:
            return None

        response.raise_for_status() # A check to ensure that everything other than 2xx becomes an exception
        return response.json()  # Parses the json body into a python dict

    def reserve_product(self, product_id: int, order_id: int) -> None:
        response = self._client.post(
            f"/products/{product_id}/reserve",
            json={"orderId": order_id},
        )

        if response.status_code == 400:
            raise HTTPException(
                status_code=400,
                detail="Product is sold out",
            )

        response.raise_for_status()
