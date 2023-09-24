import os
import sqlalchemy as sa
import databases

from .database import Database


# MariaDB 연결 정보
class mysql_db(Database):
    def __init__(self) -> None:
        self.__db_host = os.getenv("DB_HOST")
        self.__db_port = int(os.getenv("DB_PORT", -1))
        self.__db_user = os.getenv("DB_USER")
        self.__db_password = os.getenv("DB_PASSWORD")
        self.__db_name = os.getenv("DB_NAME")
        self.__db_pool_size = int(os.getenv("DB_POOL_SIZE", 10))
        self.__db_url = (
            f"mysql+aiomysql://{self.__db_user}:{self.__db_password}@"
            f"{self.__db_host}:{self.__db_port}/{self.__db_name}"
        )

        if os.getenv("ENV") == "test":
            self.__db_instance = databases.Database(
                self.__db_url,
                min_size=1,
                max_size=self.__db_pool_size,
                force_rollback=True,
            )
        else:
            self.__db_instance = databases.Database(
                self.__db_url, min_size=self.__db_pool_size, max_size=100
            )

        self.__db_engine = sa.create_engine(self.__db_url)
        self.__db_metadata = sa.MetaData()

    def get_connection(self):
        return self.__db_instance

    def get_metadata(self):
        return self.__db_metadata


database = mysql_db()
