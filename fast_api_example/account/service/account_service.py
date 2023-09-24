from fast_api_example.account.repository.account_repository import AccountRepository, account_repository
from fast_api_example.account.repository.redis_repository import RedisRepository, redis_repository
from fast_api_example.dto.account_dto import AccountDto
from fast_api_example.meta_singleton import MetaSingleton


class AccountService(metaclass=MetaSingleton):

    def __init__(
        self, redis_repository: RedisRepository, account_repository: AccountRepository
    ) -> None:
        self.__redis_repository = redis_repository
        self.__account_repository = account_repository

    def __call__(self):
        return self

    async def get_account_by_redis(self, account_id: str):
        return await self.__redis_repository.get_key(account_id)

    async def get_account_by_db(self, account_id: str) -> AccountDto:
        result = await self.__account_repository.select_account_by_id(account_id)
        return AccountDto(
            id=result.id,
            bank_id=result.bank_id,
            is_use=result.is_use
        )


account_service = AccountService(redis_repository, account_repository)
