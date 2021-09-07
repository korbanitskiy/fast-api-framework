from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from sqlalchemy.exc import NoResultFound

from app.ORM.database import db_manager
from app.ORM.schemas.user_schema import User
from app.api.settings import APISettings
from app.interactors.example import ExampleInteractor


async def auth(token: str = Depends(APISettings.oauth2_schema)):
    with db_manager() as db:
        try:
            user = User.get(db, refresh_token=token)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="User not found")

    token = await _get_access_token(user)
    return token


async def _get_access_token(user: User):
    """
    Helper function that will check User.token lifetime and refresh it if needed.
    :param user: User object
    :return: Access token as str
    """
    if (user.acc_token_ts + timedelta(minutes=APISettings.access_token_lifetime)) < datetime.now():
        params = {'refresh_token': user.refresh_token}
        ex_interactor = ExampleInteractor()
        result = await ex_interactor.refresh_token(params=params)
        return result['data']['token']
    else:
        return user.token
