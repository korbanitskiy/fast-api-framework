from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound

from app.interactors.base import BaseInteractor
from app.ORM.schemas.user_schema import User, UserValidator
from app.ORM.database import db_manager


class ExampleInteractor(BaseInteractor):
    # GET examples
    async def simple_get(self):
        result = await self.get(self.settings.simple_get_url)
        return result

    async def auth_get(self, auth_token: str):
        result = await self.get(self.settings.auth_get_url, auth=auth_token)
        return result

    async def params_get(self, params: dict):
        result = await self.get(self.settings.params_get_url, params=params)
        return result

    async def dynamic_url_get(self, uri: str):
        url_suffix = self.settings.dynamic_url_get_url.format(uri=uri)
        result = await self.get(url_suffix)
        return result

    async def load_user_from_db(self, filter_by: {}):
        with db_manager() as db:
            try:
                user = User.get(db, **filter_by)
            except NoResultFound:
                return self._create_response(404)
            else:
                return user

    async def saved_get(self):
        result = await self.get(self.settings.simple_get_url)
        if result.get('status_code', 500) == 200:
            with db_manager() as db:
                request_user = UserValidator(**result['user_data'])
                user, _ = User.get_or_create(db, _defaults=request_user.dict(), username=request_user.username)
                user.update(db, request_user.dict())

        return result

    async def updated_get(self):
        result = await self.get(self.settings.simple_get_url)
        if result.get('status_code', 500) == 200:
            request_user = UserValidator(**result['user_data'])
            with db_manager() as db:
                try:
                    user = User.get(db, username=request_user.username)
                except NoResultFound:
                    return self._create_response(404)
                else:
                    user.update(db, {'acc_token_ts': datetime.now()})
        return result

    async def simple_post(self, post_data):
        pass

    async def auth_post(self, post_data, auth_token):
        pass
