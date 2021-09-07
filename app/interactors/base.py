"""
Interactor's purpose is to provide level of abstraction over third-party API.
BaseInteractor's functionality includes only data exchange and proper error returning.
All third-party specific functionality should be implemented in a subclass.
"""

import httpx

from app.api.settings import APISettings


class BaseInteractor:
    def __init__(self):
        self.settings = APISettings()

    async def post(self, url_path: str, **kwargs):
        return await self._send_request("POST", url_path, **kwargs)

    async def get(self, url_path: str, **kwargs):
        return await self._send_request("GET", url_path, **kwargs)

    async def _send_request(self, method: str, url_path: str, **kwargs):
        headers = (
            self._get_content_type_header(),
            self._get_auth_header(kwargs.pop('auth', None)),
            self._get_custom_header(kwargs.pop('custom_key', None)),
        )
        headers = dict(h for h in headers if h)

        async with httpx.AsyncClient(base_url=self.settings.base_url) as client:
            response = await client.request(method, url_path, headers=headers, **kwargs)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            return self._create_response(response.status_code, str(e))

        try:
            response_json = response.json()
        except Exception as e:
            return self._create_response(500, f"Response is not JSON convertible: {e}")
        else:
            return self._create_response(200, data=response_json)

    def _get_content_type_header(self):
        return "Content-Type", "application/json"

    def _get_auth_header(self, auth: str):
        if auth:
            return "Authorization", f"Bearer: {auth}"

    def _get_custom_header(self, custom: str):
        if custom:
            return "X-Custom-Key", str(custom)

    def _create_response(self, code: int, message: str = None, data: {} = None):
        return {
            'status_code': code,
            'detail': message or self.settings.response_messages.get(code, 'Something went wrong'),
            'data': data,
        }
