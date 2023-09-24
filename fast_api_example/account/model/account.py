from fast_api_example.account.model.base import Base
from sqlalchemy import String, CHAR, TIMESTAMP
from sqlalchemy.orm import mapped_column


class Account(Base):
    __tablename__ = "account"
    id = mapped_column(String(20), nullable=False, primary_key=True)
    bank_id = mapped_column(String(30), nullable=False, primary_key=True)
    is_use = mapped_column(
        CHAR(1),
        nullable=False,
        server_default="T",
    )
    ins_timestamp = mapped_column(
        TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP", comment="등록일시"
    )
    upd_timestamp = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP",
        comment="수정일시",
    )
