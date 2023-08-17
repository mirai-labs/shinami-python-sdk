from pydantic import BaseModel


class ShinamiWallet(BaseModel):
    id: str
    address: str
