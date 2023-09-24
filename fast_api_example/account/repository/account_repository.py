from fast_api_example.account.model.account import Account
from fast_api_example.meta_singleton import MetaSingleton
from fast_api_example.persistence.database import Database
from sqlalchemy import and_, select, update, delete

from fast_api_example.persistence.mysql import database


class AccountRepository(metaclass=MetaSingleton):
    def __init__(self, db_instance: Database) -> None:
        self.__db_instance = db_instance

    def get_db_instance(self):
        return self.__db_instance

    async def insert_account(self, id: str, bank_id: str, is_use: str = "T"):
        account = Account(id=id, bank_id=bank_id, is_use=is_use)
        return self.__db_instance.get_connection().add(account)

    async def select_account_by_id(self, id: str):
        query = select(Account).where(Account.id == id)
        result = await self.__db_instance.get_connection().execute(query)
        return result.scalar()

    async def update_account_bank_id_by_id(self, id: str, bank_id: str):
        query = update(Account).where(Account.id == id).values(bank_id=bank_id)
        return await self.__db_instance.get_connection().execute(query)

    async def delete_account_not_equal_id_and_bank_id(self, id: str, bank_id: str):
        query = delete(Account).where(
            and_(
                Account.id != id,
                Account.id == bank_id,
            )
        )
        return await self.__db_instance.get_connection().execute(query)


account_repository: AccountRepository = AccountRepository(database)
