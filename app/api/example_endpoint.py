"""
All routes act in the same way:
1. Receive input data;
2. Optional: Pre-process data before sending to API;
3. Call corresponding Interactor method;
4. Optional: Save received data to the DB;
5. Return requested data.
"""
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Depends

from app.interactors.example import ExampleInteractor
from app.utilities.common import auth
from app.utilities.log_route import LogRoute

router = APIRouter(route_class=LogRoute)


# GET examples
@router.get('/api/simple_get_ep/')
async def simple_get(token: str = Depends(auth)):
    ex_interactor = ExampleInteractor()
    ex_response = await ex_interactor.simple_get()
    if ex_response['status_code'] not in (200, 201, 202):
        raise HTTPException(**ex_response)
    return ex_response


@router.get('/api/auth_get_ep/')
async def auth_get(token: str = Depends(auth)):
    ex_interactor = ExampleInteractor()
    ex_response = await ex_interactor.auth_get(auth_token=token)
    if ex_response['status_code'] not in (200, 201, 202):
        raise HTTPException(**ex_response)
    return ex_response


@router.get('/api/params_get_ep/')
async def params_get(param1: str, param_2_optional: Optional[str]):
    params = {
        "param1": param1
    }
    if param_2_optional:
        params.update({"param_2_optional": param_2_optional})

    ex_interactor = ExampleInteractor()
    ex_response = await ex_interactor.params_get(params=params)
    if ex_response['status_code'] not in (200, 201, 202):
        raise HTTPException(**ex_response)
    return ex_response


@router.get('/api/dynamic_url_get_ep/{uri}')
async def dynamic_url_get(uri: str):
    ex_interactor = ExampleInteractor()
    ex_response = await ex_interactor.dynamic_url_get(uri=uri)
    if ex_response['status_code'] not in (200, 201, 202):
        raise HTTPException(**ex_response)
    return ex_response


@router.get('/api/saved_get_ep/')
async def saved_get():
    ex_interactor = ExampleInteractor()
    ex_response = await ex_interactor.saved_get()
    if ex_response['status_code'] not in (200, 201, 202):
        raise HTTPException(**ex_response)
    return ex_response


@router.get('/api/updated_get_ep/')
async def updated_get():
    ex_interactor = ExampleInteractor()
    ex_response = await ex_interactor.updated_get()
    if ex_response['status_code'] not in (200, 201, 202):
        raise HTTPException(**ex_response)
    return ex_response


# POST examples
@router.post('/api/simple_post_ep')
async def simple_post(body=Body(...)):
    ex_interactor = ExampleInteractor()
    ex_response = await ex_interactor.simple_post(post_data=body)
    if ex_response['status_code'] not in (200, 201, 202):
        raise HTTPException(**ex_response)
    return ex_response


@router.post('/api/auth_post_ep')
async def auth_post(body=Body(...), token: str = Depends(auth)):
    ex_interactor = ExampleInteractor()
    ex_response = await ex_interactor.auth_post(post_data=body, auth_token=token)
    if ex_response['status_code'] not in (200, 201, 202):
        raise HTTPException(**ex_response)
    return ex_response
