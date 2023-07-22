import uuid
from dataclasses import dataclass

import httpx


@dataclass
class ShinamiJsonRpcPayload:
    method: str
    params: list[str]
    jsonrpc: str = "2.0"
    id: str = str(uuid.uuid4())


class ShinamiIawClient:
    """
    API wrapper for the Shinami IAW API.
    """

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
        r = await self._make_post_request(
            "shinami_key_createSession",
            [secret],
        )
        return r

    async def _make_post_request(
        self,
        method: str,
        params: list[str],
        id: str | int | None = str(uuid.uuid4()),
    ):
        """
        Make a POST request to the Shinami API.

        Args:
            method (str): The method to call.
            params (list[str]): The parameters to pass to the method.
            id (str | int | None, optional): The ID of the request. Defaults to str(uuid.uuid4()).
        """
        headers = {
            "x-api-key": self.api_token,
            "Content-Type": "application/json",
        }

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": id,
        }

        async with httpx.AsyncClient() as client:
            r = await client.post(
                url=f"{self.api_url}/key/v1",
                json=payload,
                headers=headers,
            )

            if r.status_code == 401:
                raise Exception(
                    "Ser, your Shinami API token is invalid. Please provide a valid API token and try again."
                )

            r.raise_for_status()

        return r.json()
