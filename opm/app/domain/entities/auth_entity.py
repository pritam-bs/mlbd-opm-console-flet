from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthEntity:
    access_token: str
    refresh_token: str
