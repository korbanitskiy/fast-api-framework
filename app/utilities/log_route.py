from collections import abc

from app.utilities.custom_logger import YOLogger
from fastapi.routing import APIRoute

logger = YOLogger(__name__)


class LogRoute(APIRoute):

    def get_route_handler(self):
        handler = super().get_route_handler()

        async def log_route_handler(request):
            params = {**request.path_params, **request.query_params}
            self._hide_sensitive_data(params)
            logger.info(f'{self.endpoint.__name__} - '
                        f'start - '
                        f'{params}')
            try:
                response = await handler(request)
            except Exception as e:
                logger.error(f'{self.endpoint.__name__} - '
                             f'failed ({repr(e)}) - '
                             f'{params}')
                raise
            else:
                logger.info(f'{self.endpoint.__name__} - '
                            f'finish - '
                            f'{params}')
                return response

        return log_route_handler

    def _hide_sensitive_data(self, data):
        sensitive_keys = ('username', 'password', 'refresh_token', 'access_token', 'token')
        for key, value in data.items():
            if isinstance(value, abc.Mapping):
                self._hide_sensitive_data(value)
            else:
                if key in sensitive_keys:
                    data[key] = 'obfuscated'
