import os

from dotenv import load_dotenv

from shinami_python_sdk.shinami import ShinamiIawClient

load_dotenv()

SHINAMI_IAW_API_KEY = os.environ["SHINAMI_IAW_API_KEY"]


def assert_dict_structure(my_dict):
    assert isinstance(my_dict, dict), "Input should be a dictionary."

    required_keys = ["jsonrpc", "result", "id"]

    for key in required_keys:
        assert key in my_dict, f"Missing key: {key}"

    assert isinstance(my_dict["jsonrpc"], str), "'jsonrpc' should be a string."
    assert isinstance(my_dict["result"], str), "'result' should be a string."
    assert isinstance(my_dict["id"], str), "'id' should be a string."


async def test_create_session():
    shinami_iaw_client = ShinamiIawClient(SHINAMI_IAW_API_KEY)
    session = await shinami_iaw_client.create_session("NOT_A_SECURE_SECRET")
    assert_dict_structure(session)
