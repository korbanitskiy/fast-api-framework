from fastapi.security import OAuth2PasswordBearer


class APISettings:
    response_messages = {
        200: 'Ok',
        400: 'Bad request',
        401: 'Unauthorized',
        404: 'Not found',
        500: 'Internal Server Error',
    }
    oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
    access_token_lifetime = 2

    base_url = 'http://httpbin.org'

    simple_get_url = '/json'
    auth_get_url = '/json'
    params_get_url = '/json'
    dynamic_url_get_url = '/delay/{uri}'
    saved_get_url = '/json'
    updated_get_url = '/json'

    simple_post = '/post'
    auth_post = '/post'
