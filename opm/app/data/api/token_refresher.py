
from yarl import URL
import aiohttp
from typing import Dict
from ...settings.settings import settings


async def token_refresh(refresh_token: str) -> Dict:
    base_url = URL(settings.opm_base_url)
    token_path = "auth/client/refresh-token"
    token_end_point = base_url.joinpath(token_path)

    async with aiohttp.ClientSession() as session:
        payload = {
            'refresh_token': refresh_token
        }

        async with session.post(token_end_point, json=payload) as response:
            if response.status != 200:
                raise ValueError(
                    f"Failed to fetch tokens. HTTP status: {response.status}")

            data = await response.json()

            # Ensure the necessary keys are present in the response
            if 'access_token' not in data or 'refresh_token' not in data:
                raise ValueError(
                    "Received invalid response format from token endpoint")

            return {
                'access_token': data['access_token'],
                'refresh_token': data['refresh_token']
            }
