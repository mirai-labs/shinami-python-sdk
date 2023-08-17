import asyncio
import logging
import os
from time import time

from dotenv import load_dotenv

from shinami_python_sdk.iaw import ShinamiIawClient

load_dotenv()

logging.basicConfig(level=logging.INFO)

SHINAMI_IAW_API_KEY = os.environ["SHINAMI_IAW_API_KEY"]


async def test_create_session():
    shinami_iaw_client = ShinamiIawClient(SHINAMI_IAW_API_KEY)
    session = await shinami_iaw_client.create_session("NOT_A_SECURE_SECRET")
    assert isinstance(session, str)
    return session


async def test_create_wallet(
    session_token: str,
    wallet_id: str = f"wallet_test_{int(time())}",
):
    shinami_iaw_client = ShinamiIawClient(SHINAMI_IAW_API_KEY)
    wallet = await shinami_iaw_client.create_wallet(
        wallet_id=wallet_id,
        session_token=session_token,
    )
    assert isinstance(wallet, str)
    return wallet


async def test_get_wallet(
    wallet_id: str,
):
    shinami_iaw_client = ShinamiIawClient(SHINAMI_IAW_API_KEY)
    wallet = await shinami_iaw_client.get_wallet(wallet_id)
    return wallet


wallet = asyncio.run(test_get_wallet("bwhli"))
print(wallet)
