from dataclasses import dataclass


@dataclass
class AuthEntity:
    access_token: str
    refresh_token: str
