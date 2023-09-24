import json
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from starlette.responses import Response

from fast_api_example.account.service.account_service import AccountService, account_service
from fast_api_example.dto.account_dto import AccountDto
from fast_api_example.lib.json import EnhancedJSONEncoder

account_router = APIRouter()


@account_router.get(
    "/api/account",
    responses={
        200: {
            "description": "수행 완료",
            "content": AccountDto,
        },
        422: {
            "description": "error",
            "content": AccountDto,
        },
    },
)
async def search_account(
    __account_service: Annotated[AccountService, Depends(account_service)],
    account_id: str,
):
    """
    # account 조회

    이 API는 account를 조회합니다.

    """
    response_redis = await __account_service.get_account_by_redis(
        account_id
    )
    response_db = await __account_service.get_account_by_db(
        account_id
    )
    response = {
        "redis": response_redis,
        "db": response_db
    }
    return Response(
        content=json.dumps(response, cls=EnhancedJSONEncoder),
        media_type="application/json",
    )
