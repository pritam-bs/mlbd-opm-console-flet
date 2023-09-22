from .....api.api_client import APIClient
from .....model.auth.token_dto import TokenDTO
from .....model.request_body.auth.auth_body import AuthBody


class TokenRemoteDatasource:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def login(self, client_name: str, password: str) -> TokenDTO:
        auth_body = AuthBody(client_name=client_name, password=password)
        response = await self.api_client.path(
            '/auth/client/authenticate'
        ).headers(
            should_add_token=False
        ).json(
            auth_body.to_json()
        ).post().request()

        token_dto = TokenDTO.from_dict(response)
        return token_dto
