import uuid

import httpx


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
        result = await self._make_post_request(
            "shinami_key_createSession",
            [secret],
        )
        return result

    async def create_wallet(
        self,
        wallet_id: str,
        session_token: str,
    ):
        """
        Create a Shinami wallet with the given wallet ID and session token.

        Args:
            wallet_id (str): An ID to associate with the wallet.
            session_token (str): The session token to use to create the wallet.
        """
        result = await self._make_post_request(
            "shinami_wal_createWallet",
            [wallet_id, session_token],
        )
        return result

    async def execute_gasless_transaction_block(
        self,
        session_token: str,
        wallet_id: str,
        tx_bytes: str,
        gas_budget: int,
        request_type: str,
    ):
        """
        Execute a gasless transaction block with the given parameters.

        Args:
            session_token (str): The session token to use to execute the transaction block.
            wallet_id (str): The ID of the wallet to use to execute the transaction block.
            tx_bytes (str): The transaction bytes to use to execute the transaction block.
            gas_budget (int): The gas budget to use to execute the transaction block.
            request_type (str): The request type to use to execute the transaction block.
        """
        result = await self._make_post_request(
            "shinami_wal_executeGaslessTransactionBlock",
            [
                wallet_id,
                session_token,
                tx_bytes,
                gas_budget,
                request_type,
            ],
        )
        return result

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
