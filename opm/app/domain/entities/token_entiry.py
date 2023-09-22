from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenEntity:
    access_token: str
    refresh_token: str
