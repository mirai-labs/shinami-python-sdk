import uuid

import httpx


class Shinami:
    def __init__(
        self,
        api_token: str,
        api_url: str = "https://api.shinami.com",
    ) -> None:
        self.api_token = api_token
        self.api_url = api_url

    async def create_session(
        self,
        secret: str,
    ):
        """
        Create a Shinami session with the given secret.

        Args:
            secret (str): The secret to use to create the session.
        """
        headers = {
            "x-api-key": self.api_token,
            "Content-Type": "application/json",
        }
        data = {
            "jsonrpc": "2.0",
            "method": "shinami_key_createSession",
            "params": [secret],
            "id": str(uuid.uuid4()),
        }

        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{self.api_url}/key/v1",
                json=data,
                headers=headers,
            )

        return r.json()
